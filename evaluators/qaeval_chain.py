from langchain_openai import ChatOpenAI
from langchain.evaluation.qa import QAEvalChain
from utils.input.input_loader import load_inputs
from agents.qa_engineer_agent import run_agent
from utils.input.helpers import extract_input
from utils.settings.models import DEFAULT_MODEL


def run_qaeval_chain():
    llm_eval = ChatOpenAI(model_name=DEFAULT_MODEL)
    dataset_examples = load_inputs("QAEvalChain")
    if not dataset_examples:
        return []

    evaluator = QAEvalChain.from_llm(llm=llm_eval)
    results = []

    for example in dataset_examples:
        input_text = extract_input(example)
        if "answer" not in example:
            raise ValueError(f"Missing 'answer' in example: {example}")
        reference = example["answer"]
        prediction = run_agent(input_text)

        eval_result = evaluator.evaluate_strings(
            input=input_text, prediction=prediction, reference=reference
        )

        results.append(
            {
                "input": input_text,
                "reference": reference,
                "prediction": prediction,
                "eval": eval_result,
            }
        )

    return results
