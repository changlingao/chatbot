import pytest
from backend import chatbot
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

@pytest.fixture
def sut():
	bot = chatbot.ChatBot()
	return bot

def test_getrectriever_none(sut):
    retriever = sut.get_retriever()
    assert retriever == None

def test_setchroma_none(sut):
    actual = sut.set_chromaretriever(None)
    expected = False
    assert actual == expected
    assert sut.get_retriever() == None

# def test_setchroma(sut):
#     docs = TextLoader("/tests/resources/1.txt").load()
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
#     split = splitter.split_documents(docs)
#     db = Chroma.from_documents(split, OpenAIEmbeddings())

#     actual = sut.set_chromaretriever(db)
#     assert actual == True
#     assert sut.get_retriever == db.as_retriever()

def test_setmemory_none(sut):
    bool = sut.set_memory(None)
    assert bool == False
    assert sut.get_memory() == None

# Stuff
# def test_genprompt(sut):
#     template2 = """
#     You are a chatbot.
#     """
#     result = sut.gen_prompt(template2)
#     assert (result) is ChatPromptTemplate
#     assert (result.format()) == "string"

def test_setmemory_memory(sut):
    mem = ConversationBufferMemory()

    bool = sut.set_memory(mem)
    assert bool == True
    assert sut.get_memory() != None

    mem.save_context({"input": "human message"}, {"output": "generated message"})

    bool = sut.set_memory(mem)
    assert bool == True

    curr_mem = sut.get_memory() 
    assert curr_mem != None
    
    actual = curr_mem.load_memory_variables({})
    expected = """{'history': [HumanMessage(content='human message', additional_kwargs={}),
      AIMessage(content='generated message', additional_kwargs={})]}"""

def test_getmemory_none(sut):
    mem = sut.get_memory()
    assert mem == None



