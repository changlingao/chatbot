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

# step 1: load
# UnstructuredFileLoader is not working
txt_loader = DirectoryLoader('./data', glob="*.txt", loader_cls=TextLoader)
pdf_loader = DirectoryLoader('./data', glob="*.pdf", loader_cls=PyPDFLoader)
pdf_pages = pdf_loader.load_and_split()
txt_data = txt_loader.load()

# TODO: chunk_size, chunk_overlap, temperature
# step 2: split
# split up long text into chunks
# keep the semantically related pieces of text together
txt_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
txt_splits = txt_splitter.split_documents(txt_data)

all_splits = pdf_pages + txt_splits

# step 3: store
# storing the embedding and splits in a vectorstore.
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())


# retriever param:
# https://python.langchain.com/docs/use_cases/question_answering/vector_db_qa#vectorstore-retriever-options

# Only retrieve documents that have a relevance score above a certain threshold
# can be none: No relevant docs were retrieved using the relevance score threshold 0.8
retriever = vectorstore.as_retriever(search_type="similarity_score_threshold",
                                     search_kwargs={'score_threshold': 0.8})


"""
retrieve nonsense
retriever = vectorstore.as_retriever()
[Document(page_content='84', metadata={'page': 84, 'source': 'data/composer-guide.pdf'}), Document(page_content='62', metadata={'page': 62, 'source': 'data/composer-guide.pdf'}), Document(page_content='15', metadata={'page': 15, 'source': 'data/composer-guide.pdf'}), Document(page_content='requiring supports (https://support.asiga.com/wp-content/uploads/2022/08/Support-Dialogue.jpg).', metadata={'source': 'data/delamination-1.txt'})]
"""


retrieved_docs = retriever.invoke("what is delamination")
print(retrieved_docs)
