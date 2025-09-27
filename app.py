import os
from dotenv import load_dotenv

load_dotenv()

print("Select the evaluation you want to run:")
print("1) QAEval")
print("2) CriteriaEval")

option = input().strip()

match option:
    case "1":
        from evaluators.qaeval_chain import run_qaeval_chain

        results = run_qaeval_chain()
        print(results)
    case "2":
        from evaluators.criteriaeval_chain import run_criteriaeval_chain

        results = run_criteriaeval_chain()
        print(results)
    case _:
        print("❌ Invalid option.")
