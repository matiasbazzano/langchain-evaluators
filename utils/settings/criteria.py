QA_ENGINEER_AGENT_CRITERIA = {
    "format": """Does the answer strictly follow the requested format?
    - If the input asks for test cases, only test cases are provided.
    - If the input asks for automation scripts, only automation scripts are provided.
    - If the input asks for both, both are included in clearly separated sections.
    - The output must never mix test cases and scripts unless explicitly requested by the user.
    """,
    "clarity": """Are the proposed test cases or automation scripts clear, well-structured,
    and understandable by other QA engineers without additional context?
    Do they use meaningful names, comments (if scripts), and structured steps (if test cases)?
    """,
    "completeness": """Do the test cases or automation scripts cover both:
    - The main functionality (happy path).
    - Relevant edge cases (e.g., invalid inputs, empty fields, timeouts, session issues, error handling)?
    """,
    "automation_ready": """Are the outputs ready for automation?
    - For scripts: are they syntactically correct, executable, and written using standard automation practices?
    - For test cases: are they detailed enough (preconditions, steps, expected results) to be automated in a tool/framework?
    """,
    "consistency": """Are the outputs consistent with common QA practices,
    standard terminology, and conventions for test case and automation script design?
    Do they align with the instructions given in the agent's role?
    """,
}
