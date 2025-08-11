from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.evaluation.criteria import CriteriaEvalChain
from utils.input_loader import load_inputs
from utils.report import save_eval_report


def run_criteriaeval_chain():
    llm_pred = ChatOpenAI(model_name="gpt-4o-mini")
    llm_eval = ChatOpenAI(model_name="gpt-4o-mini")

    prompt_template = PromptTemplate.from_template("{input}")
    qa_chain = prompt_template | llm_pred

    dataset_examples = load_inputs("CriteriaEvalChain")
    if not dataset_examples:
        print("❌ No data was loaded for evaluation.")
        return

    criteria = {
        "clarity": "Is the output clear and easy to understand?",
        "conciseness": "Is the output concise without losing meaning?",
    }

    evaluator = CriteriaEvalChain.from_llm(llm=llm_eval, criteria=criteria)
    results = []

    for example in dataset_examples:
        input_ = example["input"]
        response = qa_chain.invoke(input_)
        prediction = response.content

        eval_result = evaluator.evaluate_strings(input=input_, prediction=prediction)

        results.append({"input": input_, "prediction": prediction, "eval": eval_result})

    save_eval_report(results)
