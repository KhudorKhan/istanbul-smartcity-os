from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools_schema: List[Dict[str, Any]],
        system_instruction: str
    ) -> Dict[str, Any]:
        """
        Возвращает dict формата:
        {
          "text": str or None,
          "tool_calls": [{"name": str, "arguments": dict}] or []
        }
        """
        pass