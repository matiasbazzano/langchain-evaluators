QA_ENGINEER_AGENT_CRITERIA = {
    "format": """Does the answer follow the requested format?
    - If the input asks for test cases, only test cases are provided.
    - If the input asks for automation scripts, only scripts are provided.
    - If the input asks for both, both are included but clearly separated.
    """,
    "clarity": "Are the proposed test cases or automation scripts clear and easy to understand by other QA engineers?",
    "completeness": "Do the test cases or scripts cover both the main functionality (happy path) and possible edge cases?",
    "automation_ready": "Are the outputs (if test cases) written in a way that makes them suitable for automation scripting?",
    "consistency": "Are the outputs consistent with common QA practices and terminology?",
}
