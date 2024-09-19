from datetime import datetime
from typing import AsyncGenerator, List, Optional, Dict
from sqlmodel.ext.asyncio.session import AsyncSession
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.graph import CompiledGraph
from app.database.main import TenantModel
from app.database.agent import MessageModel, MessageService
from app.utils.logging import AppLogger
from app.utils.langfuse_client import StatefulTraceClient, StatefulSpanClient
from app.enums import MessageRoleEnum
from app.config import get_settings
from ..schemas import AgentStreamingEvent
from ..enums import AgentStreamingEventTypeEnum

logger = AppLogger().get_logger()

class BaseAgent:

    def __init__(
        self,
        tenant: TenantModel,
        db_session: AsyncSession,
        langfuse_trace: Optional[StatefulTraceClient] = None,
        **kwargs
    ):
        self.settings = get_settings()
        self.tenant = tenant
        self.db_session = db_session
        self.message_service = MessageService(db_session=db_session)
        
        self.langfuse_trace = langfuse_trace
        # if self.langfuse_trace:
        #     self.langfuse_event = self.langfuse_trace.event(name=self.agent_name) # agent_name must be set on a main agent class
            
        if self.langfuse_trace:
            self.model_callbacks = [self.langfuse_trace.get_langchain_handler(update_parent=True)]
        else:
            self.model_callbacks = []
            
        self.model = AzureChatOpenAI(
            name=self.agent_name,
            model=self.settings.SMART_LLM_MODEL,
            azure_endpoint=self.settings.AZURE_OPENAI_ENDPOINT,
            azure_deployment=self.settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            openai_api_version=self.settings.AZURE_OPENAI_API_VERSION,
            callbacks=self.model_callbacks
        )
        
    
    def __get_agent_message_content__(self, message: MessageModel):
        return message.content + (
            "Files Attached:" + ",".join(message.files) if message.files is not None and len(message.files) > 0 else
            ""
        )
    
    def __get_agent_messages__(self, messages: List[MessageModel]):
        """
        Convert db messages to langchain messages
        """
        return [
            HumanMessage(content=self.__get_agent_message_content__(message)) if message.role == MessageRoleEnum.USER.value  
            else AIMessage(content=message.content) if message.role == MessageRoleEnum.ASSISTANT.value  
            else None
            for message in messages
        ]
        
    async def __get_messages_from_session__(self, session_id: str, number_of_messages: int = -1):
        """
        Get messages for langchain agent from db by session_id
        """
        messages = await self.message_service.find_by_session_id(
            session_id=session_id
        )
        
        if number_of_messages == -1:
            return self.__get_agent_messages__(messages=messages)
        else:
            return self.__get_agent_messages__(messages=messages[-number_of_messages:])
    
    async def __execute_agent_streaming__(self, agent_name: str, agent_executor: CompiledGraph, messages: List) -> AsyncGenerator[AgentStreamingEvent, None]:
        """  
        Execute agent streaming.  
        
        This method streams events associated with the execution of an agent. The events provide detailed information  
        about the agent's state, such as starting, ending, and intermediate processing.  

        Parameters:
         
            agent_name (str): The name of the agent being executed.  
            
            agent_executor (CompiledGraph): The executor handling the agent's compiled graph.  
            
            messages (List): A list of messages to be processed by the agent.  

        Yields:
            
            AgentStreamingEvent: Contains the type of the event, the name of the agent/tool, and relevant data such as content, inputs, and outputs.

        Event Types and Data:  

            1. `on_chain_start`:  
                - Indicates the start of the agent's chain.  
                - Data:   
                    - `type`: CHAIN_START  
                    - `name`: The name of the agent.  

            2. `on_chain_end`:  
                - Indicates the end of the agent's chain.  
                - Data:  
                    - `type`: CHAIN_END  
                    - `name`: The name of the agent.  
                    - `output`: The output message content from the agent.  

            3. `on_chat_model_stream`:  
                - Represents the streaming of messages from the chat model.  
                - Data:  
                    - `type`: MESSAGE  
                    - `content`: The content of the streamed message.  

            4. `on_tool_start`:  
                - Indicates the start of a tool associated with the agent.  
                - Data:  
                    - `type`: TOOL_START  
                    - `name`: The name of the tool.  
                    - `input`: The input data for the tool.  

            5. `on_tool_end`:  
                - Indicates the end of a tool's execution.  
                - Data:  
                    - `type`: TOOL_END  
                    - `name`: The name of the tool.  
                    - `output`: The output data from the tool.    
        """
        agent_span = None
        events: Dict[str, StatefulSpanClient] = {}
        final_response = ""
        
        async for event in agent_executor.astream_events(
            {"messages": messages}, version="v1"
        ):
            kind = event["event"]
            if kind == "on_chain_start":
                if (
                    event["name"] == agent_name
                ):
                    logger.info(f"Starting agent: {event['name']} ")
                        
                    # logger.info(event)
                    yield AgentStreamingEvent(
                        type=AgentStreamingEventTypeEnum.CHAIN_START,
                        name=event['name']
                    )
                    
            elif kind == "on_chain_end":
                if (
                    event["name"] == agent_name
                ):
                    
                    logger.info(f"Done agent: {event['name']} with output: {event['data'].get('output')}")

                    yield AgentStreamingEvent(
                        type=AgentStreamingEventTypeEnum.CAHIN_END,
                        name=event['name'],
                        output=final_response
                        # output=event['data'].get('output').get('agent').get('messages')[0].content
                    )
                    
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    final_response = final_response + content
                    yield AgentStreamingEvent(
                        type=AgentStreamingEventTypeEnum.MESSAGE,
                        content=content
                    )
                    
            elif kind == "on_tool_start":
                logger.info(f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}")

                if self.langfuse_trace:
                    events[event['run_id']] = self.langfuse_trace.span(
                        name=event['name'],
                        input=event['data'].get('input'),
                        start_time=datetime.now()
                    )
                    
                yield AgentStreamingEvent(
                    type=AgentStreamingEventTypeEnum.TOOL_START,
                    name=event['name'],
                    input=event['data'].get('input')
                )
                
            elif kind == "on_tool_end":
                logger.info(f"Done tool: {event['name']}")
                logger.info(f"Tool output was: {event['data'].get('output')}")
                
                if event['run_id'] in events:
                    events[event['run_id']].update(
                        end_time=datetime.now(),
                        output=event['data'].get('output')
                    )
                    
                yield AgentStreamingEvent(
                    type=AgentStreamingEventTypeEnum.TOOL_END,
                    name=event['name'],
                    output=event['data'].get('output')
                )
    
    async def __execute_agent__(self, agent_name: str, agent_executor: CompiledGraph, messages: List):
        """
        Execute agent.
        """
        async for event in agent_executor.astream_events(
            {"messages": messages}, version="v1"
        ):
            kind = event["event"]
            if kind == "on_chain_start":
                if (
                    event["name"] == agent_name
                ):
                    logger.info(f"Starting agent: {event['name']}.")
                    
            elif kind == "on_chain_end":
                if (
                    event["name"] == agent_name
                ):
                    logger.info(f"Done agent: {event['name']} with output: {event['data'].get('output')}")
                    return event['data'].get('output').get('agent').get('messages')[0].content
                    
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    pass
                    # print(content, end="|")
            elif kind == "on_tool_start":
                logger.info(f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}")
                
            elif kind == "on_tool_end":
                logger.info(f"Done tool: {event['name']}")
                logger.info(f"Tool output was: {event['data'].get('output')}")
                