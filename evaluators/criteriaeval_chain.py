from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.evaluation.criteria import CriteriaEvalChain
from utils.input_loader import load_inputs
from utils.report import save_eval_report


def run_criteriaeval_chain():
    llm_pred = ChatOpenAI(model_name="gpt-4o-mini")
    llm_eval = ChatOpenAI(model_name="gpt-4o-mini")

    prompt_template = PromptTemplate.from_template("{input}")
    pred_chain = prompt_template | llm_pred

    criteria = {
        "clarity": "Is the answer clear and easy to understand?",
        "conciseness": "Is the answer brief and avoids unnecessary information?",
        # relevance
    }
    evaluator = CriteriaEvalChain.from_llm(llm=llm_eval, criteria=criteria)

    dataset_examples = load_inputs("CriteriaEvalChain")
    if not dataset_examples:
        print("❌ No data for CriteriaEvalChain.")
        return

    results = []
    for ex in dataset_examples:
        raw = ex.get("input")
        if isinstance(raw, dict) and "input" in raw:
            input_text = raw["input"]
        else:
            input_text = raw

        pred_msg = pred_chain.invoke({"input": input_text})
        prediction = getattr(pred_msg, "content", pred_msg)

        eval_result = evaluator.evaluate_strings(
            input=input_text,
            prediction=prediction,
        )

        results.append(
            {
                "input": input_text,
                "reference": None,
                "prediction": prediction,
                "eval": eval_result,
            }
        )
    save_eval_report(results, evaluator_type="criteria_eval")
