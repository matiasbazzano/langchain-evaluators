def extract_input(example):
    if isinstance(example.get("input"), dict):
        return example["input"].get("input", "")
    return example.get("input", "")
