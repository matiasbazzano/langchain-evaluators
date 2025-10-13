import os
import json
import pandas as pd
from utils.input.ground_truth import evaluator_needs_reference


def normalize_entry(entry):
    if "input" in entry and isinstance(entry["input"], dict):
        return entry
    elif "input" in entry:
        out = {"input": {"input": entry["input"]}}
        if "answer" in entry:
            out["answer"] = entry["answer"]
        return out
    elif "query" in entry:
        out = {"input": {"input": entry["query"]}}
        if "answer" in entry:
            out["answer"] = entry["answer"]
        return out
    return None


def load_inputs(evaluator_name: str):
    dataset_examples = []
    print("Select input mode:")
    print("1) Single input")
    print("2) Dataset (.csv, .json, .txt, .xlsx)")
    option = input().strip()

    ref_requirement = evaluator_needs_reference(evaluator_name)

    if option == "1":
        user_input = input("Input: ")
        if ref_requirement is True:
            reference = input("Ground truth: ")
            dataset_examples.append(
                {"input": {"input": user_input}, "answer": reference}
            )
        else:
            dataset_examples.append({"input": {"input": user_input}})

    elif option == "2":
        path = input("Enter the file path: ").strip()
        extension = os.path.splitext(path)[1].lower()
        try:
            if extension == ".json":
                with open(path, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                    for entry in raw_data:
                        normalized = normalize_entry(entry)
                        if normalized:
                            dataset_examples.append(normalized)
            elif extension == ".csv":
                df = pd.read_csv(path)
                df.columns = df.columns.str.strip().str.lower()
                dataset_examples = [
                    {
                        "input": {"input": row["input"]},
                        **(
                            {"answer": row["answer"]}
                            if "answer" in row and pd.notna(row["answer"])
                            else {}
                        ),
                    }
                    for _, row in df.iterrows()
                    if pd.notna(row["input"])
                ]
            elif extension in [".xls", ".xlsx"]:
                df = pd.read_excel(path)
                dataset_examples = [
                    {
                        "input": {"input": row["input"]},
                        **(
                            {"answer": row["answer"]}
                            if "answer" in row and pd.notna(row["answer"])
                            else {}
                        ),
                    }
                    for _, row in df.iterrows()
                    if pd.notna(row["input"])
                ]
            elif extension == ".txt":
                with open(path, "r", encoding="utf-8") as f:
                    blocks = f.read().split("\n\n")
                    for block in blocks:
                        lines = block.strip().split("\n")
                        if (
                            len(lines) == 2
                            and lines[0].startswith("Query:")
                            and lines[1].startswith("Answer:")
                        ):
                            q = lines[0].replace("Query:", "").strip()
                            a = lines[1].replace("Answer:", "").strip()
                            dataset_examples.append(
                                {"input": {"input": q}, "answer": a}
                            )
                        elif len(lines) == 1 and lines[0].startswith("Query:"):
                            q = lines[0].replace("Query:", "").strip()
                            dataset_examples.append({"input": {"input": q}})
            else:
                print("❌ Unsupported file type.")
                return []
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return []
    else:
        print("Invalid option.")
        return []

    if not dataset_examples:
        print("❌ No valid data found in file.")
    return dataset_examples
