"""
AI Agent with MCP Tools
"""
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from app.server.client import MCPClient


class VehicleAgent:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.2")
        self.tools = [MCPClient.list_vehicles, MCPClient.filter_vehicles]
        self.agent = self._create_agent()

    def _create_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a vehicle information assistant. Use tools to answer questions."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        return create_tool_calling_agent(self.llm, self.tools, prompt)

    def query(self, question: str) -> str:
        """Process user query through agent"""
        agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=False
        )
        result = agent_executor.invoke({"input": question})
        return result['output']
