from typing import Optional
from datetime import datetime
from app.utils.langfuse_client import LangFuseClient
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

class ReportPrompts:
    
    @classmethod
    def chat_with_report_system_prompts(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="chat-with-report").format(**kwargs)
    
    @classmethod
    def generate_report_prompts(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="generate-report").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)
    
    @classmethod
    def generate_section_content_prompts(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="generate-section-content").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)
    
    @classmethod
    def order_chunks(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="order-chunks").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)

    @classmethod
    def order_section_chunks(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="section-order-chunks").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)
    
    @classmethod
    def check_chunk_relevance(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="check-chunk-relevance").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)
    
    @classmethod
    def get_web_search_queries(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="get-web-search-queries").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)
    
    @classmethod
    def get_web_search_queries_for_section(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="get-web-search-queries-for-section").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)
    
    @classmethod
    def get_rag_queries(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="get-rag-queries").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)
    
    @classmethod
    def get_section_rag_queries(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="get-section-rag-queries").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)

    @classmethod
    def get_template_queries(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="get-template-queries").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)

    @classmethod
    def review_sections(self, **kwargs):
        return LangFuseClient().get_prompt_str(name="review-sections").format(current_date=datetime.now().strftime('%Y-%m-%d'), **kwargs)