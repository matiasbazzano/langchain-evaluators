## 1. Setup Instructions

### Step 1: Clone this repo
```bash
git clone https://gitlab.endava.com/testing-accelerators/langchain-evaluators.git
cd langchain-evaluators
```

### Step 2: Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # For Windows
source .venv/bin/activate  # For MacOS / Linux
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create your `.env` file
Create an `.env` file in the project root path with this structure and credentials
```env
OPENAI_API_KEY=<your_openai_api_key>
LANGSMITH_API_KEY=<your_langsmith_api_key>
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

> You can get your **LangSmith API key** from https://smith.langchain.com

---

## 2. Running the Agent

You can run the agent interactively to validate your setup and test basic behavior.

```bash
python -m agents.qa_engineer_agent
```

The agent will prompt you for input until you exit.

---

## 3. Running Evaluations

This repository includes two evaluation flows implemented using LangChain evaluation chains.
When running an evaluation, you can choose how inputs are provided:

- **Single input** (interactive prompt)
- **Dataset file** (`.csv`, `.json`, `.txt`, `.xlsx`)

The evaluator will prompt you to select the input mode and, if applicable, provide the dataset path.

---

### 3.1 QAEval

QAEval compares the agent output against a reference answer (ground truth).

Run the QA evaluation with:

```bash
python -m evaluators.qaeval_chain
```

You will be prompted to provide:
- **Single input mode**
  - Input
  - Ground truth answer
- **Dataset mode**
  - Path to a dataset file

Sample datasets are available under:
- `resources/datasets/qa_engineer_dataset.csv`
- `resources/datasets/qa_engineer_dataset.json`

---

### 3.2 CriteriaEval

CriteriaEval evaluates the agent output without requiring a reference answer.
This is useful for qualitative checks such as relevance, clarity, or completeness.

Run the criteria evaluation with:

```bash
python -m evaluators.criteriaeval_chain
```

You will be prompted to provide:
- **Single input mode**
  - Input
- **Dataset mode**
  - Path to a dataset file

The same dataset formats described above are supported.

---

## 4. Viewing Evaluation Results

If LangSmith tracing is enabled, you can inspect:
- Individual agent executions
- Evaluation scores per input
- Comparison across multiple runs

Results can be viewed at:
https://smith.langchain.com
