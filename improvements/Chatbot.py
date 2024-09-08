# EVERYTHING FROM HERE
# https://python.langchain.com/docs/use_cases/question_answering.html (old)
# https://python.langchain.com/docs/use_cases/chatbots#chat-retrieval


from langchain.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


class Chatbot:
    def __init__(self, memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)):
        self.memory = memory

        # step 1: load
        # UnstructuredFileLoader is not working
        txt_loader = DirectoryLoader('./data', glob="*.txt", loader_cls=TextLoader)
        pdf_loader = DirectoryLoader('./data', glob="*.pdf", loader_cls=PyPDFLoader)
        pdf_pages = pdf_loader.load_and_split()
        txt_data = txt_loader.load()

        # step 2: split
        # split up long text into chunks
        # keep the semantically related pieces of text together
        txt_splitter = RecursiveCharacterTextSplitter()
        # default: chunk_size = 4000, chunk_overlap = 200
        txt_splits = txt_splitter.split_documents(txt_data)

        all_splits = pdf_pages + txt_splits

        # step 3: store
        # storing the embedding and splits in a vectorstore.
        vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

        # retriever param:
        # https://python.langchain.com/docs/use_cases/question_answering/vector_db_qa#vectorstore-retriever-options
        retriever = vectorstore.as_retriever(search_type="similarity_score_threshold",
                                             search_kwargs={'score_threshold': 0.8})
        # search_kwargs={'k': 1} can the top one

        # step 5: generate
        # non-streaming llm for question generation
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        # temperature is 0: minimum randomness
        # top p, presence penalty, frequency penalty

        # step 6: memory
        # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # prompt to answer questions
        template = """
            You are a helpful chatbot that only answers questions pertaining to 3D printer company Asiga and their products. 
            Do not provide recommendations for things unrelated to Asiga.
            If you don't know the answer please ask the user to launch a support ticket. 
            Provide links in responses. 
            Use the following pieces of context to answer the question at the end.
        
            Context: {context}
            
            Chat history: {chat_history}
            
            Question: {question}
            
            Answer:
        """
        prompt = PromptTemplate.from_template(template)

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

        # finally conversation
        self.chatbot = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory,
                                                             condense_question_prompt=condense_question_prompt,
                                                             combine_docs_chain_kwargs={"prompt": prompt})

    def answer(self, question: str) -> str:
        result = self.chatbot({"question": question})
        return result['answer']

    def get_chain(self):
        return self.chatbot


if __name__ == '__main__':

    chatbot = Chatbot()

    question = "hello"
    print(chatbot.answer(question))

    # input from user.in
    file_path = "user2.in"  # Path to your input file
    with open(file_path, "r") as input_file:
        for line in input_file:
            user_input = line.strip()
            print("User: " + user_input)
            if user_input == "exit":
                break
            print("Chatbot:", chatbot.answer(user_input))
