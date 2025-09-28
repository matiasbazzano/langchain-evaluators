from langchain_openai import ChatOpenAI
from langchain.evaluation.criteria import CriteriaEvalChain
from utils.input.input_loader import load_inputs
from agents.qa_engineer_agent import run_agent
from utils.input.helpers import extract_input
from utils.settings.models import DEFAULT_MODEL
from utils.settings.criteria import QA_ENGINEER_AGENT_CRITERIA


def run_criteriaeval_chain():
    llm_eval = ChatOpenAI(model_name=DEFAULT_MODEL)
    evaluator = CriteriaEvalChain.from_llm(
        llm=llm_eval, criteria=QA_ENGINEER_AGENT_CRITERIA
    )

    dataset_examples = load_inputs("CriteriaEvalChain")
    if not dataset_examples:
        return []

    results = []
    for example in dataset_examples:
        input_text = extract_input(example)
        prediction = run_agent(input_text)

        eval_result = evaluator.evaluate_strings(
            input=input_text, prediction=prediction
        )

        results.append(
            {
                "input": input_text,
                "prediction": prediction,
                "eval": eval_result,
            }
        )

    return results
