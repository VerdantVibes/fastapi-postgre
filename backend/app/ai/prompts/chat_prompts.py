from typing import Optional
from datetime import datetime
from app.utils.langfuse_client import LangFuseClient
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

class QAPrompts:
    
    @classmethod
    def chat_agent_prompt(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="chat-agent-prompt").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)
    
    @classmethod
    def qa_system_prompt(self, **kwargs):
        chat_agent_prompt = self.chat_agent_prompt(**kwargs)
        return LangFuseClient().get_prompt_str(name="qa-agent-prompt").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs) + "\n\n" + chat_agent_prompt

    @classmethod
    def report_chat_system_prompt(self, **kwargs):
        chat_agent_prompt = self.chat_agent_prompt(**kwargs)
        return LangFuseClient().get_prompt_str(name="report-agent-prompt").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs) + "\n\n" + chat_agent_prompt