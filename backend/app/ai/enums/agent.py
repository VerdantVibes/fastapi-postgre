from enum import Enum as PyEnum

class AgentStreamingEventTypeEnum(PyEnum):
    CHAIN_START = "chain_start"
    CAHIN_END = "chain_end"
    MESSAGE = "message"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"