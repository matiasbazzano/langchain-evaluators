QA_ENGINEER_AGENT_CRITERIA = {
    "domain_relevance": """Does the agent correctly identify whether the user’s request is QA-related?
    - If the request is unrelated to QA, the agent must politely and explicitly state: "I'm sorry, but I can only assist with QA-related tasks."
    - The agent may also include placeholder reasoning such as "Thought: This question is unrelated to QA." followed by "Action: None" — this is acceptable.
    - If the request is QA-related, the agent should proceed normally without unnecessary refusals.
    - If the agent returns no answer (None) or fails to provide this refusal when appropriate, it should be considered incorrect.
    """,
    "format": """Does the answer strictly follow the requested format?
    - If the input asks for test cases, only test cases are provided.
    - If the input asks for automation scripts, only automation scripts are provided.
    - If the input asks for both, both are included in clearly separated sections.
    - The output must never mix test cases and scripts unless explicitly requested by the user.
    - If the input is unrelated to QA, this criterion is considered **not applicable** and should automatically be treated as passed.
    """,
    "clarity": """Are the proposed test cases or automation scripts clear, well-structured,
    and understandable by other QA engineers without additional context?
    Do they use meaningful names, comments (if scripts), and structured steps (if test cases)?
    - If the input is unrelated to QA, this criterion is **not applicable** and should automatically be treated as passed.
    """,
    "completeness": """Do the test cases or automation scripts cover both:
    - The main functionality (happy path).
    - Relevant edge cases (e.g., invalid inputs, empty fields, timeouts, session issues, error handling)?
    - If the input is unrelated to QA, this criterion is **not applicable** and should automatically be treated as passed.
    """,
    "automation_ready": """Are the outputs ready for automation?
    - For scripts: are they syntactically correct, executable, and written using standard automation practices?
    - For test cases: are they detailed enough (preconditions, steps, expected results) to be automated in a tool/framework?
    - If the input is unrelated to QA, this criterion is **not applicable** and should automatically be treated as passed.
    """,
    "consistency": """Are the outputs consistent with common QA practices,
    standard terminology, and conventions for test case and automation script design?
    Do they align with the instructions given in the agent's role?
    - If the input is unrelated to QA, this criterion is **not applicable** and should automatically be treated as passed.
    """,
}
