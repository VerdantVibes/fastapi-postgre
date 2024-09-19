from enum import Enum as PyEnum

class ToolNameEnum(PyEnum):
    TAVILY_SEARCH = "tavily_search_tool"
    AZUREAI_SEARCH = "azure_ai_search_tool"
    HIGHCHART = "highchart_tool"
    FAISS_SEARCH = "faiss_search_tool"
    EXA_SEARCH = "exa_search_tool"