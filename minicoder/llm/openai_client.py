from openai import OpenAI
from minicoder.config import (
    MODEL_API_KEY,
    MODEL_BASE_URL,
    MODEL_NAME,
    validate_config,
)

class LLMClient:
    '''
    对 OpenAI-compatible Chat Completions API 简单封装。
    '''

    def __init__(self) -> None:
        validate_config()
        self.model = MODEL_NAME
        self.client = OpenAI(
            api_key=MODEL_API_KEY,
            base_url=MODEL_BASE_URL,
        )

    def chat(self, messages, tools=None):
        """
        调用 OpenAI-compatible Chat Completions API 进行对话。

        :param messages: 消息列表，当前对话历史。
        :param tools: 可选的工具列表。
        :return: 模型返回的一条 assistant message。
        """

        request = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            request["tools"] = tools

        response = self.client.chat.completions.create(**request)
        return response.choices[0].message