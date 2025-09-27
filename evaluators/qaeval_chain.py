from langchain_openai import ChatOpenAI
from langchain.evaluation.qa import QAEvalChain
from utils.input_loader import load_inputs
from agent.agent import run_agent


def run_qaeval_chain():
    llm_eval = ChatOpenAI(model_name="gpt-4o-mini")

    dataset_examples = load_inputs("QAEvalChain")
    if not dataset_examples:
        return []

    evaluator = QAEvalChain.from_llm(llm=llm_eval)
    results = []
    for example in dataset_examples:
        input_ = example["input"]
        reference = example.get("answer")

        prediction = run_agent(input_text)

        eval_result = evaluator.evaluate_strings(
            input=input_["input"], prediction=prediction, reference=reference
        )

        results.append(
            {
                "input": input_["input"],
                "reference": reference,
                "prediction": prediction,
                "eval": eval_result,
            }
        )

    return results
