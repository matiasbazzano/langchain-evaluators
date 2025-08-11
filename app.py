import os
from dotenv import load_dotenv

load_dotenv()

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")

print("Select the evaluation you want to run:")
print("1) QAEval")
print("2) CriteriaEval")

option = input().strip()

match option:
    case "1":
        from evaluators.qaeval_chain import run_qaeval_chain

        run_qaeval_chain()
    case "2":
        from evaluators.criteriaeval_chain import run_criteriaeval_chain

        run_criteriaeval_chain()
    case _:
        print("❌ Invalid option.")
