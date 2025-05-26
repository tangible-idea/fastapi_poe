# utils.py

import asyncio
from typing import AsyncGenerator, Optional
from fastapi_poe.types import ProtocolMessage, ToolDefinition
from fastapi_poe.client import get_bot_response
from fastapi import HTTPException
import os
from openai import OpenAI

async def concat_message(partial_gen: AsyncGenerator[str, None]) -> str:
    concated = ""  # Each function call gets a separate `concated`
    async for partial in partial_gen:
        concated += partial  # No shared state
    return concated

async def openai_full_message(request: str) -> str:
    """
    Asynchronously fetch a full response from OpenAI's ChatCompletion API.

    Args:
        request (str): User's request message.

    Returns:
        str: Full response from the bot.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    )
    try:
        # Run the blocking OpenAI API call in a separate thread to avoid blocking the event loop
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": request,
                    }
                ],
                model="gpt-4",  # Use the desired model, e.g., "gpt-3.5-turbo" or "gpt-4"
            )
        )
    except Exception as e:
        print(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to OpenAI API.")

    try:
        # Extract the content of the assistant's reply from the response
        if 'choices' in response:
            return response['choices'][0]['message']['content']
        else:
            raise HTTPException(status_code=500, detail="Unexpected response format from OpenAI API.")
    except Exception as e:
        print(f"Error processing OpenAI response: {e}")
        raise HTTPException(status_code=500, detail="Error processing the OpenAI response.")
    


# 가짜 실행 함수 (실제로는 사용 안 함)
def fake_tool(**kwargs):
    return kwargs  # 아무거나 반환 (실행되지 않음)

async def get_poe_partial_messages(messages, bot_name: str, api_key: str, tools: Optional[list[ToolDefinition]] = None) -> AsyncGenerator[str, None]:
    """
    Fetch partial messages from fastapi_poe's get_bot_response.

    Args:
        messages (list): List of ProtocolMessage objects.
        bot_name (str): Name of the bot to interact with.
        api_key (str): API key for authentication.
        tools (Optional[list[ToolDefinition]]): List of tools to be used by the bot.

    Yields:
        str: Partial message content.
    """
    async for partial in get_bot_response(messages=messages, bot_name=bot_name, api_key=api_key, tools=tools, tool_executables=[fake_tool]):
        yield partial.text
            
    