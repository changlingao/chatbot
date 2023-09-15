# EVERYTHING FROM HERE
# https://python.langchain.com/docs/use_cases/question_answering.html
from langchain import OpenAI, LLMChain
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# step 1: load
# UnstructuredFileLoader is not working
text_loader = DirectoryLoader('../data', glob="*.txt", loader_cls=TextLoader)
# TODO: manually add all pdf
# pdf_loader = PyPDFLoader("../Brian/small_data/PRO 4K User Guide 20210712.pdf")
# data = text_loader.load() + pdf_loader.load()
data = text_loader.load()

# TODO: chunk_size, chunk_overlap, temperature
# step 2: split
# split up long text into chunks
# keep the semantically related pieces of text together
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# step 3: store
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# step 5: generate
# non-streaming llm for question generation
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# streaming to stdout
streaming_llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)

# step 6: memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


# finally conversation
retriever = vectorstore.as_retriever()
# ConversationalRetrievalChain( retriever=vectorstore.as_retriever(), combine_docs_chain=doc_chain, question_generator=question_generator)
chat = ConversationalRetrievalChain.from_llm( llm=streaming_llm, retriever=retriever, memory=memory, condense_question_llm = llm)

query = "say something that haas 100 words"
chat({"question": query})





# input from console
# user = input("User: ")
# while user != "exit":
#     result = chat({"question": user})
#     print("Chatbot: " + result['answer'])
#     user = input("User: ")


# input from user.in
# file_path = "../user.in"  # Path to your input file
# with open(file_path, "r") as input_file:
#     for line in input_file:
#         user_input = line.strip()
#         print("User: " + user_input)
#         if user_input == "exit":
#             break
#         reply = chat({"question": user_input})
#         print("Chatbot:", reply['answer'])