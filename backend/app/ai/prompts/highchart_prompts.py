from typing import Optional
from datetime import datetime
from app.utils.langfuse_client import LangFuseClient
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

class HighChartPrompts:
    
    @classmethod
    def highchart_generation_prompt(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="generate-chart").format(**kwargs)