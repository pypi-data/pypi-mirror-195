import openai

from chatgpt_cli.settings import cli_settings
from pydantic import BaseModel
from typing import List, Optional

openai.api_key = cli_settings.openai_api_key


class ChatGPTMessage(BaseModel):
    role: str
    content: str


class ChatGPTChoices(BaseModel):
    message: ChatGPTMessage
    finish_reason: Optional[str] = None
    index: int


class ChatGPTResponse(BaseModel):
    choices: List[ChatGPTChoices]


def query_chatgpt(prompt: str) -> ChatGPTResponse:
    """
    Query ChatGPT with a prompt.

    Args:
        prompt (str): The prompt to query ChatGPT with.

    Returns:
        ChatGPTResponse: The response from ChatGPT.
    """
    response: dict = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return ChatGPTResponse(**response)
