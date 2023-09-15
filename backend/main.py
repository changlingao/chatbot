from loadchain import Loadchain
from datetime import datetime

# imports to be removed later
# temp test for adding to db
# only for running main.py
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

# imports for generating summary for chat_history
# build chain again... but will not affect chain in loadchain.py
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import JSONLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
import json
import os


class Mainbot:
    def __init__(self, db):
        self.loadchain = Loadchain()
        self.chat_history = []
        self.db = db

    def ask_chatbot(self, provided_question=""): 
        if (provided_question == ""):
            return ""
        
        question_no = 0
        answers = []
        question = ""
        qtime = datetime.now().replace(microsecond=0)
        
        if isinstance(provided_question, list):
            while True:
                if (question_no == len(provided_question)):
                    print("End of provided questions, exiting")
                    return(answers)
                question = provided_question[question_no]
                question_no += 1
                result = self.loadchain.chat({"question": question})
                answers.append(result['answer'])

        result = self.loadchain.chat({"question": provided_question})
        atime = datetime.now().replace(microsecond=0)
        answer = result['answer']
        source = result['source_documents'][0].metadata['source'].split("/")[-1]
        self.save_message(provided_question, qtime, answer, atime, source)
        return answer

    def save_message(self, question: str, qtime: str, answer: str, atime: str, source: str):
        if (question == "" or qtime == "" or atime == ""):
            return False
        dict = {}
        dict['question'] = question
        dict['qtime'] = qtime
        dict['answer'] = answer
        dict['atime'] = atime
        dict['source'] = source
        self.chat_history.append(dict)

    # use langchain load_summarize_chain
    def generate_chat_summary(self):
        # output questions in chat_history to a json file to use JSONLoader, will delete in the end
        output_file_path = "questions.json"
        questions = []
        for item in self.chat_history:
            question = item.get("question", "")  # Extract the "question" field
            questions.append({"question": question})
        # Write the extracted questions to the JSON output file
        with open(output_file_path, "w") as output_file:
            json.dump(questions, output_file, indent=4)

        # summary the question (ignore answers)
        loader = JSONLoader(output_file_path, jq_schema='.[]', content_key='question')
        data = loader.load()

        # Define prompt
        prompt_template = """Write a title of the following:
                            "{text}"
                            CONCISE SUMMARY:"""
        prompt = PromptTemplate.from_template(prompt_template)

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
        chain = load_summarize_chain(llm=llm, chain_type="stuff", prompt=prompt)

        summary = chain.run(data)
        os.remove(output_file_path)
        return summary

    def save_to_db(self):
        if (self.db == None):
            return False

        summary = self.generate_chat_summary()

        # id is auto generated if not specified e.g. "_id": ObjectID('64ffaf9ddabaaebc7e4cb269'),
        chat = {
            "summary": summary,
            "chat_history": self.chat_history
        }
        chats = self.db.chats
        chats.insert_one(chat)

        return True
    
    def get_chat_history(self):
        return self.chat_history


def answer(question, chatbot):

    result = chatbot.ask_chatbot(question)
    return result
