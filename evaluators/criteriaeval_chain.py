from langchain_openai import ChatOpenAI
from langchain.evaluation.criteria import CriteriaEvalChain
from utils.input_loader import load_inputs
from agent.agent import run_agent


def run_criteriaeval_chain():
    llm_eval = ChatOpenAI(model_name="gpt-4o-mini")

    criteria = {
        "clarity": "Are the proposed test cases clear and easy to understand by other QA engineers?",
        "completeness": "Do the test cases cover both the main functionality (happy path) and possible edge cases?",
        "automation_ready": "Are the test cases written in a way that makes them suitable for automation scripting?",
        "consistency": "Are the test cases consistent with common QA practices and terminology?",
    }

    evaluator = CriteriaEvalChain.from_llm(llm=llm_eval, criteria=criteria)

    dataset_examples = load_inputs("CriteriaEvalChain")
    if not dataset_examples:
        return []

    results = []
    for ex in dataset_examples:
        raw = ex.get("input")
        input_text = raw["input"] if isinstance(raw, dict) else raw

        prediction = run_agent(input_text)

        eval_result = evaluator.evaluate_strings(
            input=input_text,
            prediction=prediction,
        )

        results.append(
            {
                "input": input_text,
                "prediction": prediction,
                "eval": eval_result,
            }
        )

    return results
