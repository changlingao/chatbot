from langchain import OpenAI
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate

from chatbot import ChatBot
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain


class Loadchain:
    def __init__(self):
        self.chatbot = ChatBot()

        data = self.chatbot.load_dir("../data")
        split = self.chatbot.split_text(data, 500, 20)

        embedding = OpenAIEmbeddings()
        vectorstore = self.chatbot.get_chromavectorstore(split, embedding)
        self.chatbot.set_chromaretriever(vectorstore)

        # streaming 2: https://python.langchain.com/docs/modules/model_io/models/chat/streaming
        llm = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], model_name="gpt-3.5-turbo", temperature=0)

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
        self.chatbot.set_memory(memory)

        template = """
        You are a helpful chatbot that only answers questions pertaining to 3D printer company Asiga and their products. If you don't know the answer please ask the user to launch a support ticket at: https://support.asiga.com/. Provide links in responses. Do not provide recommendations for things unrelated to Asiga. 
        {context}
        Chat history: {chat_history}
        Question: {question}
        Answer:
        """

        self.prompt = self.chatbot.gen_prompt(template)

        # prompt to condense question
        condense_question_template = """
            Return text in the original language of the follow up question.
            If the follow up question does not need context, return the exact same text back.
            Never rephrase the follow up question given the chat history unless the follow up question needs context.

            Chat History: {chat_history}
            Follow Up question: {question}
            Standalone question:
        """
        condense_question_prompt = PromptTemplate.from_template(condense_question_template)

        self.chat = ConversationalRetrievalChain.from_llm(llm=llm,
                                                          retriever=self.chatbot.get_retriever(),
                                                          memory=self.chatbot.get_memory(),
                                                          return_source_documents=True,
                                                          condense_question_prompt=condense_question_prompt,
                                                          combine_docs_chain_kwargs={'prompt': self.prompt})
