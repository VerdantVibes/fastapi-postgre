from typing import Optional, Any, List
from pydantic import BaseModel
from ..enums import AgentStreamingEventTypeEnum

class AgentStreamingEvent(BaseModel):
    """
    Agent Streaming Event.
    
    Parameters:

        type (AgentStreamingEventTypeEnum): type of the event.
        
        name (Optional[str]): agent name or tool name.
        
        content (Optional[str]): llm response message chunk. type is "message"
        
        input (Optional[Any]): input of tool or agent
        
        output (Optional[Any]): output of tool or agent
    """
    type: AgentStreamingEventTypeEnum
    name: Optional[str] = None
    content: Optional[str] = None
    input: Optional[Any] = None
    output: Optional[Any] = None

class QAAgentStreamingEvent(AgentStreamingEvent):
    web_chunks: Optional[List] = []
    internal_chunks: Optional[List] = []
    chart_link: Optional[Any] = None