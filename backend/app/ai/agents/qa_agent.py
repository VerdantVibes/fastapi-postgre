from typing import AsyncGenerator, Optional
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from app.utils.logging import AppLogger
from app.utils.langchain.tools import AzureAISearchTool, HighChartTool, TavilySearchTool, FaissVectorSearchTool, ExaSearchTool
from app.utils.vector_retriever import AzureAISearchVectorRetriever, FaissVectorRetriever
from app.utils.exa_client import ExaClient
from ..prompts import QAPrompts
from ..schemas import AgentStreamingEvent
from .base import BaseAgent


logger = AppLogger().get_logger()

class QAAgent(BaseAgent):
    """
    Agent for "Ask a Question".

    Tools:
        
        1. Azure AI Search for internal document search
        
        2. Tavily Search Engine for web search
        
    Model: Default
        
    """
    def __init__(self, faiss_vector_store: Optional[FaissVectorRetriever] = None, tool_cfg: dict = {'internal_top': 5, 'web_top': 5, 'file_top': 5,}, **kwargs):
        """
        Initialize tools and agent executors.
        
        Parameters:
        
            faiss_vector_store: faiss vector store
            
            tool_cfg (dict): configuration for agent tools.

                {
                    'internal_top': 1, # number of chunks to use from azure ai search
                    'web_top': 1, # number of chunks to use from tavily search
                }
        """
        self.agent_name = "qa-agent"
        
        super().__init__(**kwargs)
        self.tool_cfg = tool_cfg
        self.azure_ai_search_tool = AzureAISearchTool(
            retriever=AzureAISearchVectorRetriever(
                service_name=self.tenant.ai_search_service_name,
                index_name=self.tenant.ai_search_index_name
            ),
            cfg={
                'top': self.tool_cfg['internal_top']
            }
        )
        
        self.tavily_search_tool = TavilySearchTool(
            cfg = {
                'top': self.tool_cfg['web_top']
            }
        )
        
        self.highchart_tool = HighChartTool()
        
        self.exasearch_tool = ExaSearchTool(
            exa_client=ExaClient()
        )
        
        self.tools = [
            self.azure_ai_search_tool,
            self.tavily_search_tool,
            self.highchart_tool,
            self.exasearch_tool
        ]
        if faiss_vector_store is not None:
            self.faiss_search_tool = FaissVectorSearchTool(
                retriever=faiss_vector_store,
                cfg={
                    'top': self.tool_cfg['file_top']
                }
            )
            self.tools.append(self.faiss_search_tool)
        
        
        self.agent_executor = create_react_agent(self.model, self.tools).with_config({"run_name": self.agent_name})
        self.system_prompt = ""
    
    async def astreaming(self, session_id: str, number_of_messages: int = 10) -> AsyncGenerator[AgentStreamingEvent, None]:
        """
        Invoke the agent and get streaming response.
        
        Parameters:
            
            session_id (str): session id
            
            number_of_messages (int): number of messages to use from the top. Default to 10.
            
        Returns:
        
            same streaming response as BaseAgent.__execute_agent_streaming__().
        """ 
        messages = [self.system_prompt] + await self.__get_messages_from_session__(session_id=session_id, number_of_messages=number_of_messages)
        logger.info(f"QA agent async streaming with {session_id} session")
        async for chunk in self.__execute_agent_streaming__(
            agent_name=self.agent_name,
            agent_executor=self.agent_executor,
            messages=messages
        ):
            yield chunk
            
    async def ainvoke(self, session_id: str, number_of_messages: int = 10) -> str:
        """
        Invoke the agent and get response without streaming.
        
        Parameters:
            
            session_id (str): session id
            
            number_of_messages (int): number of messages to use from the top. Default to 10.
        
        Returns:
        
            str: AI message
        """
        messages = [self.system_prompt] + await self.__get_messages_from_session__(session_id=session_id, number_of_messages=number_of_messages)
        logger.info(f"QA agent async invoking with {session_id}")
        result = await self.__execute_agent__(
            agent_name=self.agent_name,
            agent_executor=self.agent_executor,
            messages=messages
        )
        
        return result
        
        # return  response['messages'][-1]['content']