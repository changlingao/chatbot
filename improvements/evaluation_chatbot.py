# better copy from "add new test run code" from the existing dataset
import langsmith
from langchain import chat_models
from langchain.memory import ConversationBufferMemory
from langchain.smith import RunEvalConfig

from Chatbot import Chatbot

# Define your chain


# Define the evaluators to apply
eval_config = RunEvalConfig(
    evaluators=[
        # "cot_qa",
        # smith.RunEvalConfig.LabeledCriteria("helpfulness")
        RunEvalConfig.Criteria("relevance")
    ],
    custom_evaluators=[],
    eval_llm=chat_models.ChatOpenAI(model="gpt-4", temperature=0)
)


# Since chains and agents can be stateful (they can have memory),
# obviously not helpful as each run has previous run memory....
# TODO: remain unfixed as the tutorial is not mature yet
# TODO: commit to langsmith about the input_mapper bug?
def chain_constructor(inputs):
    new_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    new_memory.clear()
    my_chain = Chatbot(memory=new_memory).get_chain()
    # input_mapper = {'question': inputs['question'], 'chat_history': inputs['chat_history']}
    # my_chain = input_mapper | my_chain
    return my_chain


# deprecated
# def input_mapper(inputs: dict) -> dict:
#     """
#     from doc in client
#     input_mapper: A function to map to the inputs dictionary from an Example
#         to the format expected by the model to be evaluated. This is useful if
#         your model needs to deserialize more complex schema or if your dataset
#         has inputs with keys that differ from what is expected by your chain
#         or agent.
#     """
#     input_keys = {
#         'question': inputs['question'],
#         'chat_history': inputs['chat_history']
#     }
#     return input_keys


client = langsmith.Client()
# change dataset_ name and project_name
chain_results = client.run_on_dataset(
    dataset_name="chatbot-memory",
    llm_or_chain_factory=chain_constructor,
    evaluation=eval_config,
    project_name="test-memeory-7",
    # concurrency_level=5,
    verbose=True,
)

