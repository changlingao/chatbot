from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


llm = OpenAI(model_name="gpt-4-1106-preview")
chat_model = ChatOpenAI()

text = "does the model of open affect the answer speed like gpt-3.5 is slower than gpt-4"
messages = [HumanMessage(content=text)]

print(llm.invoke(text))
