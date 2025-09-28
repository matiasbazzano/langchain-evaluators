from dotenv import load_dotenv
from utils.settings.eval_selector import select_and_run_evaluation
from utils.core.cleaner import clean_pycache

load_dotenv()

results = select_and_run_evaluation()

if results is not None:
    print(results)

clean_pycache()
