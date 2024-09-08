# better copy from "add new test run code" from the existing dataset

import langsmith
from langchain import chat_models
from langchain.smith import RunEvalConfig
from RAG import get_rag_chain

# Define your chain
rag_chain = get_rag_chain()

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


client = langsmith.Client()
# change dataset_name and project_name
chain_results = client.run_on_dataset(
    dataset_name="rag-dataset",
    llm_or_chain_factory=rag_chain,
    evaluation=eval_config,
    project_name="rag-dataset-project-4",
    concurrency_level=5,
    verbose=True,
)

