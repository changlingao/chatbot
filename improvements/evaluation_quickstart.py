# https://docs.smith.langchain.com/evaluation/quickstart
# not that useful some parts confusing......

from langchain.chat_models import ChatOpenAI
from langsmith import Client
from langchain.smith import RunEvalConfig, run_on_dataset


# 1. Create a dataset
example_inputs = [
    "what are some parameters i can use to tune a llm",
    "thank you"
]

client = Client()
dataset_name = "last"
# client.delete_dataset(dataset_name=dataset_name)

# Storing inputs in a dataset lets us
# run chains and LLMs over a shared set of examples.
# dataset = client.create_dataset(
#     dataset_name=dataset_name, description="new example",
# )

for input_prompt in example_inputs:
    # Each example must be unique and have inputs defined.
    # Outputs are optional
    client.create_example(
        inputs={"question": input_prompt},
        outputs=None,
        # dataset_id=dataset.id,
        dataset_name=dataset_name
    )

# 2. define llm
llm = ChatOpenAI(temperature=0)

# 3. evaluate
eval_config = RunEvalConfig(
  evaluators=[
    # You can specify an evaluator by name/enum.
    # In this case, the default criterion is "helpfulness"
    "criteria",
    # Or you can configure the evaluator
    RunEvalConfig.Criteria("harmfulness"),
    RunEvalConfig.Criteria("helpfulness")
  ]
)


run_on_dataset(
    dataset_name=dataset_name,
    llm_or_chain_factory=llm,
    evaluation=eval_config,
    client=client,
    verbose=True,
    project_name="alright", # has to be unique among all projects
)