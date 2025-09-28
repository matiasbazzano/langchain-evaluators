def evaluator_needs_reference(evaluator_name: str) -> bool:
    required = [
        "QAEvalChain",
        "ExactMatchStringEvaluator",
        "StringEvaluator",
        "EmbeddingDistanceEvaluator",
        "CosineSimilarityEvaluator",
        "RegexMatchStringEvaluator",
    ]
    optional = ["CriteriaEvalChain", "LabeledCriteriaEvalChain"]

    if evaluator_name in required:
        return True
    elif evaluator_name in optional:
        return "optional"
    else:
        return False
