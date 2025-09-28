def extract_input(example):
    """Devuelve siempre el string del input, normalizado."""
    if isinstance(example.get("input"), dict):
        return example["input"].get("input", "")
    return example.get("input", "")
