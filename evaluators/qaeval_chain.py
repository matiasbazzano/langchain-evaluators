from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.evaluation.qa import QAEvalChain
from utils.input_loader import load_inputs
from utils.report import save_eval_report


def run_qaeval_chain():
    llm_pred = ChatOpenAI(model_name="gpt-4o-mini")
    llm_eval = ChatOpenAI(model_name="gpt-4o-mini")

    prompt_template = PromptTemplate.from_template("{input}")
    qa_chain = prompt_template | llm_pred

    dataset_examples = load_inputs()
    if not dataset_examples:
        print("❌ No data was loaded for evaluation.")
        return

    evaluator = QAEvalChain.from_llm(llm=llm_eval)
    results = []
    for example in dataset_examples:
        input_ = example["input"]
        reference = example["answer"]
        response = qa_chain.invoke(input_)
        prediction = response.content

        eval_result = evaluator.evaluate_strings(
            input=input_, prediction=prediction, reference=reference
        )

        results.append(
            {
                "input": input_,
                "reference": reference,
                "prediction": prediction,
                "eval": eval_result,
            }
        )

    save_eval_report(results)
