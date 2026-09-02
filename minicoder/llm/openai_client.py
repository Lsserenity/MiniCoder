import time

from openai import OpenAI, RateLimitError

from minicoder.config import (
    MODEL_API_KEY,
    MODEL_BASE_URL,
    MODEL_NAME,
    validate_config,
)


class LLMClient:
    """
    对 OpenAI-compatible Chat Completions API 的简单封装。
    """

    def __init__(self) -> None:
        validate_config()

        self.model = MODEL_NAME

        self.client = OpenAI(
            api_key=MODEL_API_KEY,
            base_url=MODEL_BASE_URL,
        )

    def chat(
        self,
        messages,
        tools=None,
        max_attempts: int = 5,
    ):
        """
        调用 OpenAI-compatible Chat Completions API 进行对话。

        param messages: 当前对话历史。
        param tools: 可选工具定义列表。
        param max_attempts: 最大尝试次数。
        return: assistant message。
        """

        request = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            request["tools"] = tools

        for attempt in range(max_attempts):
            try:
                response = (
                    self.client.chat.completions.create(
                        **request
                    )
                )

                return response.choices[0].message

            except RateLimitError:
                if attempt == max_attempts - 1:
                    raise

                wait_seconds = 2 ** attempt

                print(
                    "[LLM] Rate limited. "
                    f"Retrying in {wait_seconds}s..."
                )

                time.sleep(wait_seconds)
