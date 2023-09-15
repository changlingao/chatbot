from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma, VectorStore
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.document_loaders import TextLoader
from langchain.prompts.chat import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
import os

class ChatBot:
    def __init__(self):
        self.memory = None
        self.retriever = None

    def load_dir(self, dir: str):

        #use absolute path instead of relative as pytest have trouble reading relative path
        script_dir = os.path.dirname(__file__)  
        full_path = os.path.abspath(os.path.join(script_dir, dir)) 

        txt_loader = DirectoryLoader(full_path, glob="*.txt", loader_cls=TextLoader)
        pdf_loader = DirectoryLoader(full_path, glob="*.pdf", loader_cls=PyPDFLoader)
        data = txt_loader.load() + pdf_loader.load()
        return data
    
    def split_text(self, data: "List[Document]", size: int, overlap: int) -> "List[Document]":
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
        text_split = text_splitter.split_documents(data)
        return text_split
    
    # Future: any retriever
    # Also sets retriever
    def get_chromavectorstore(self, split, embedding: OpenAIEmbeddings) -> Chroma:
        vectorstore = Chroma.from_documents(documents=split, embedding=embedding)

        self.retriever = vectorstore.as_retriever()
        return vectorstore
    
    def set_chromaretriever(self, retriever: VectorStore) -> bool:
        if (retriever == None):
            return False
        self.retriever = retriever.as_retriever()
        return True
    
    def get_retriever(self):
        return self.retriever
    
    def gen_prompt(self, template: str) -> ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_template(template)
        return prompt

    def set_memory(self, memory: ConversationBufferMemory) -> bool:
        if (memory == None):
            return False
        self.memory = memory;
        return True;

    def get_memory(self):
        return self.memory



