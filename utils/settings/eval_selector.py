from evaluators.qaeval_chain import run_qaeval_chain
from evaluators.criteriaeval_chain import run_criteriaeval_chain


def select_and_run_evaluation():
    print("Select the evaluation you want to run:")
    print("1) QAEval")
    print("2) CriteriaEval")

    option = input().strip()

    match option:
        case "1":
            return run_qaeval_chain()
        case "2":
            return run_criteriaeval_chain()
        case _:
            print("❌ Invalid option.")
            return None
