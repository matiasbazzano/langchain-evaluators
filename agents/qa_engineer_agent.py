from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from utils.settings.models import DEFAULT_MODEL
from utils.settings.prompts import QA_ENGINEER_AGENT_PROMPT


def create_agent(model_name: str = DEFAULT_MODEL):
    llm = ChatOpenAI(model_name=model_name)

    tools = [
        WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
        PythonREPLTool(),
    ]

    react_agent = create_react_agent(
        llm=llm, tools=tools, prompt=QA_ENGINEER_AGENT_PROMPT
    )
    agent_executor = AgentExecutor(
        agent=react_agent, tools=tools, verbose=True, handle_parsing_errors=True
    )
    return agent_executor


def run_agent(input_text: str, model_name: str = DEFAULT_MODEL) -> str:
    agent_executor = create_agent(model_name)
    result = agent_executor.invoke({"input": input_text})
    return result.get("output", str(result))
