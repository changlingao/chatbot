
from langchain.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from operator import itemgetter


def get_rag_chain():
    # step 1: load
    txt_loader = DirectoryLoader('./data', glob="*.txt", loader_cls=TextLoader)
    pdf_loader = DirectoryLoader('./data', glob="*.pdf", loader_cls=PyPDFLoader)
    pdf_pages = pdf_loader.load_and_split()
    txt_data = txt_loader.load()

    # step 2: split
    txt_splitter = RecursiveCharacterTextSplitter()
    txt_splits = txt_splitter.split_documents(txt_data)
    all_splits = pdf_pages + txt_splits

    # step 3: store
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
    # retriever
    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold",
                                         search_kwargs={'score_threshold': 0.8})

    # prompt
    template = """
        You are a helpful chatbot that only answers questions pertaining to 3D printer company Asiga and their products. 
        Do not provide recommendations for things unrelated to Asiga.
        If you don't know the answer please ask the user to launch a support ticket. 
        Provide links in responses. 
        Use the following pieces of context to answer the question at the end.
    
        Context: {context}
    
        Question: {question}
    
        Answer:
    """
    prompt = PromptTemplate.from_template(template)

    # chain
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    # https://python.langchain.com/docs/expression_language/cookbook/retrieval
    # default key is "input", but in prompt is "question"

    # retriever error
    # correct: query: What is LLM?
    # error: query: input: What is LLM?

    rag_chain = (
        {
            "context": itemgetter("input") | retriever,
            "question": itemgetter("input"),
        }
        | prompt | llm | StrOutputParser())

    return rag_chain


if __name__ == '__main__':
    rag_chain = get_rag_chain()
    output = rag_chain.invoke({"input": "where is australia"})
    print(output)

