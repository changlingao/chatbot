# https://python.langchain.com/docs/expression_language/cookbook/retrieval

from operator import itemgetter
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap, RunnablePassthrough, RunnableLambda
from langchain.schema import format_document, StrOutputParser
from langchain.prompts.prompt import PromptTemplate
from typing import Tuple, List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.vectorstores.chroma import Chroma

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

# step 1: load
# txt_loader = DirectoryLoader('./data', glob="*.txt", loader_cls=TextLoader)
# pdf_loader = DirectoryLoader('./data', glob="*.pdf", loader_cls=PyPDFLoader)
# pdf_pages = pdf_loader.load_and_split()
# txt_data = txt_loader.load()
#
# # step 2: split
# txt_splitter = RecursiveCharacterTextSplitter()
# txt_splits = txt_splitter.split_documents(txt_data)
# all_splits = pdf_pages + txt_splits
#
# # step 3: store
# vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
# # retriever
# retriever = vectorstore.as_retriever(search_type="similarity_score_threshold",
#                                      search_kwargs={'score_threshold': 0.8})



# Conversational Retrieval Chain
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

# Answer the question based on the following context:
template = """
you are a helpful chatbot that can answer questions.
The following context if for your reference
{context}

Question: {question}
"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(template)


DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


def _format_chat_history(chat_history: List[Tuple]) -> str:
    buffer = ""
    for dialogue_turn in chat_history:
        human = "Human: " + dialogue_turn[0]
        ai = "Assistant: " + dialogue_turn[1]
        buffer += "\n" + "\n".join([human, ai])
    return buffer


# _inputs = RunnableMap(
#     standalone_question=RunnablePassthrough.assign(
#         chat_history=lambda x: _format_chat_history(x["chat_history"])
#     )
#     | CONDENSE_QUESTION_PROMPT
#     | ChatOpenAI(temperature=0)
#     | StrOutputParser(),
# )
# _context = {
#     "context": itemgetter("standalone_question") | retriever | _combine_documents,
#     "question": lambda x: x["standalone_question"],
# }
# conversational_qa_chain = _inputs | _context | ANSWER_PROMPT | ChatOpenAI()

# result = conversational_qa_chain.invoke(
#     {
#         "question": "where did he work?",
#         "chat_history": [("Who wrote this notebook?", "Harrison")],
#     }
# )
# print(result)

# Memory and returning source documents
memory = ConversationBufferMemory(
    return_messages=True, output_key="answer", input_key="question"
)

# First we add a step to load memory
# This adds a "memory" key to the input object
loaded_memory = RunnablePassthrough.assign(
    chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("history"),
)
# Now we calculate the standalone question
standalone_question = {
    "standalone_question": {
        "question": lambda x: x["question"],
        "chat_history": lambda x: _format_chat_history(x["chat_history"]),
    }
    | CONDENSE_QUESTION_PROMPT
    | ChatOpenAI(temperature=0)
    | StrOutputParser(),
}
# Now we retrieve the documents
retrieved_documents = {
    "docs": itemgetter("standalone_question") | retriever,
    "question": lambda x: x["standalone_question"],
}
# Now we construct the inputs for the final prompt
final_inputs = {
    "context": lambda x: _combine_documents(x["docs"]),
    "question": itemgetter("question"),
}
# And finally, we do the part that returns the answers
answer = {
    "answer": final_inputs | ANSWER_PROMPT | ChatOpenAI(),
    "docs": itemgetter("docs"),
}
# And now we put it all together!
final_chain = loaded_memory | standalone_question | retrieved_documents | answer

# inputs = {"question": "where did harrison work?"}
# result = final_chain.invoke(inputs)
# print(result)
# print(memory.load_memory_variables({}))


# input from console
question = input("User: ")
while question != "exit":
    inputs = {"question": question}
    result = final_chain.invoke(inputs)
    print(result['answer'])
    memory.save_context(inputs, {"answer": result["answer"].content})
    question = input("User: ")
