import asyncio
import google.generativeai as genai
from google.api_core import exceptions as core_exceptions
from google.api_core.retry_async import AsyncRetry, if_exception_type
from typing import List, Dict, Any
from .base import BaseLLMProvider
from config import settings


def _classify_error(exc: Exception) -> str:
    message = f"{type(exc).__name__} {exc}".lower()
    if any(marker in message for marker in ("401", "403", "api key", "api_key", "permission", "unauthenticated")):
        return "invalid_api_key"
    if any(marker in message for marker in ("429", "resource exhausted", "resourceexhausted", "quota")):
        return "quota_exceeded"
    if any(marker in message for marker in ("timeout", "timed out", "deadline")):
        return "timeout"
    if "blocked" in message or "safety" in message:
        return "content_blocked"
    return "provider_unavailable"


def _error_result(exc: Exception) -> Dict[str, Any]:
    return {
        "text": "",
        "tool_calls": [],
        "error_code": _classify_error(exc),
        "error": str(exc)[:300]
    }


class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL
        self.timeout = settings.GEMINI_TIMEOUT_SECONDS
        # The SDK default retries 503 for up to 600s; keep retries short and inside the total budget.
        self.retry = AsyncRetry(
            predicate=if_exception_type(core_exceptions.ServiceUnavailable),
            initial=0.5,
            maximum=2.0,
            multiplier=2.0,
            timeout=self.timeout
        )

    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools_schema: List[Dict[str, Any]],
        system_instruction: str
    ) -> Dict[str, Any]:
        if not settings.GEMINI_API_KEY:
            return {
                "text": "",
                "tool_calls": [],
                "error_code": "missing_api_key"
            }

        tools = None
        if tools_schema:
            function_declarations = [
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
                for tool in tools_schema
            ]
            tools = [{"function_declarations": function_declarations}]

        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [msg["content"]]})

        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction,
                tools=tools,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=1024
                )
            )
            response = await asyncio.wait_for(
                model.generate_content_async(
                    contents,
                    request_options={"timeout": self.timeout, "retry": self.retry}
                ),
                timeout=self.timeout
            )
        except Exception as exc:
            return _error_result(exc)

        tool_calls = []
        text_response = ""

        try:
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if fn := part.function_call:
                        args = {key: val for key, val in fn.args.items()}
                        tool_calls.append({"name": fn.name, "arguments": args})
                    elif part.text:
                        text_response += part.text
        except Exception as exc:
            return _error_result(exc)

        return {
            "text": text_response.strip(),
            "tool_calls": tool_calls
        }
