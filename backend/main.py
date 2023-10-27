from loadchain import Loadchain
from datetime import datetime

# imports to be removed later
# temp test for adding to db
# only for running main.py
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import re

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
        self.all_chat_histories = []
        self.latest_msg_ls = {}
        self.db = db

    def ask_chatbot(self, session_id: str, provided_question=""):
        if (provided_question == ""):
            return ""

        question_no = 0
        answers = []
        question = ""
        qtime = datetime.strptime(datetime.now().strftime(("%d-%m-%y %H:%M:%S")), "%d-%m-%y %H:%M:%S")
        
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
        atime = datetime.strptime(datetime.now().strftime(("%d-%m-%y %H:%M:%S")), "%d-%m-%y %H:%M:%S")
        answer = result['answer']
        source = [result['source_documents'][0].metadata['source'].split("/")[-1], result['source_documents'][1].metadata['source'].split("/")[-1], result['source_documents'][2].metadata['source'].split("/")[-1]]
        self.save_message(session_id, provided_question, qtime, answer, atime, source)
        answer = Mainbot.embedding_format(answer)
        return answer

    @staticmethod
    def embedding_format(response):
        # Embed images 
        response = re.sub(r'\[(.*?)\]\((.*?)\.(jpg|png|gif)\)\.?', r'<img class="chat-img" src="\2.\3" alt="\1">', response)
        # Embed videos
        response = re.sub(r'\[.*?\]\((.*video.*?)\)\.?', r'<div class="video-container"><iframe class="chat-video" src="\1" allowfullscreen="1" frameborder="0"></iframe></div>', response)
        # Make all other links clickable
        response = re.sub(r'\[(.*?)\]\((?!.*\.(png|jpg|gif))(?!.*video)(.*?)\)|(https:\/\/(?!.*video)(?!.*\.(png|jpg|gif))[^\s]+)', r'<a href="\3\4" target="_blank">\1\4</a>', response)
        return response

    def save_message(self, session_id: str, question: str, qtime: str, answer: str, atime: str, source: str):
        if (question == "" or qtime == "" or atime == ""):
            return False
        dict = {}
        dict['question'] = question
        dict['qtime'] = qtime
        dict['answer'] = answer
        dict['atime'] = atime
        dict['source'] = source

        session_dict = {
            "session_id": session_id,
            "qa": dict
        }
        self.latest_msg_ls[session_id] = len(self.all_chat_histories)
        self.all_chat_histories.append(session_dict)

    def save_feedback(self, session_id: str, feedback_ls: list):
        latest_msg_index = self.latest_msg_ls[session_id]
        latest_session_qa = self.all_chat_histories[latest_msg_index]["qa"]
        latest_session_qa["feedback"] = feedback_ls

    # use langchain load_summarize_chain
    def generate_chat_summary(self, session_id):
        # output questions in chat_history to a json file to use JSONLoader, will delete in the end
        output_file_path = "questions.json"
        questions = []

        # extract history for session_id
        filtered_chat_history = self.get_chat_history_by_session(session_id)

        for item in filtered_chat_history:
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

    def save_to_db(self, session_id: str):
        if (self.db == None):
            return False

        filtered_chat_history = self.get_chat_history_by_session(session_id)

        # nothing to save
        if len(filtered_chat_history) == 0:
            return False

        summary = self.generate_chat_summary(session_id)
        # id is auto generated if not specified e.g. "_id": ObjectID('64ffaf9ddabaaebc7e4cb269'),
        chat = {
            "session_id": session_id,
            "summary": summary,
            "date": datetime.strptime(datetime.now().strftime(("%d-%m-%y")), "%d-%m-%y"),
            "chat_history": filtered_chat_history
        }
        chats = self.db.chats
        chats.insert_one(chat)

        return True

    # because of multiple users, all_chat_histories actually store all chat histories for all users
    def get_chat_history_by_session(self, session_id: str):
        filtered_chat_history = [item['qa'] for item in self.all_chat_histories if item["session_id"] == session_id]
        return filtered_chat_history
