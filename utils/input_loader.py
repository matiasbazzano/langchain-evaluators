import os
import json
import pandas as pd


def normalize_entry(entry):
    if "answer" not in entry:
        return None

    if isinstance(entry.get("input"), dict):
        return entry
    elif "input" in entry:
        return {"input": {"input": entry["input"]}, "answer": entry["answer"]}
    elif "query" in entry:
        return {"input": {"input": entry["query"]}, "answer": entry["answer"]}
    return None


def load_inputs():
    dataset_examples = []
    print("Select input mode:")
    print("1) Single input")
    print("2) Dataset (.csv, .json, .txt, .xlsx)")
    option = input().strip()

    if option == "1":
        user_input = input("Input: ")
        ground_truth = input("Ground truth: ")
        dataset_examples.append(
            {"input": {"input": user_input}, "answer": ground_truth}
        )

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
                dataset_examples = [
                    {"input": {"input": row["input"]}, "answer": row["answer"]}
                    for _, row in df.iterrows()
                    if pd.notna(row["input"]) and pd.notna(row["answer"])
                ]
            elif extension in [".xls", ".xlsx"]:
                df = pd.read_excel(path)
                dataset_examples = [
                    {"input": {"input": row["input"]}, "answer": row["answer"]}
                    for _, row in df.iterrows()
                    if pd.notna(row["input"]) and pd.notna(row["answer"])
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
                            question = lines[0].replace("Query:", "").strip()
                            answer = lines[1].replace("Answer:", "").strip()
                            dataset_examples.append(
                                {"input": {"input": question}, "answer": answer}
                            )
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
