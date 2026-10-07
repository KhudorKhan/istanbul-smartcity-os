from typing import Any, Dict, List, Optional, Tuple
import os
import re
from agent.expert_replies import ask_route_destination, ask_route_origin, compose_tool_reply
from providers.gemini_provider import GeminiProvider
from tools.definitions import AGENT_TOOLS_SCHEMA
from tools import implementations

FALLBACK_MESSAGES = {
    "ru": {
        "missing_api_key": "ИИ-ассистент временно недоступен. Оплата городских услуг продолжает работать.",
        "invalid_api_key": "ИИ-ассистент временно недоступен. Оплата городских услуг продолжает работать.",
        "quota_exceeded": "ИИ-ассистент сейчас перегружен. Повторите запрос через несколько минут.",
        "timeout": "ИИ-ассистент не ответил вовремя. Повторите запрос немного позже.",
        "content_blocked": "Запрос не может быть обработан. Пожалуйста, сформулируйте вопрос иначе.",
        "provider_unavailable": "ИИ-ассистент временно недоступен. Повторите запрос немного позже.",
        "generic": "Не удалось получить ответ ИИ-ассистента. Городские сервисы оплаты остаются доступны."
    },
    "tr": {
        "missing_api_key": "Yapay zeka asistanı geçici olarak kullanılamıyor. Şehir ödeme hizmetleri çalışmaya devam ediyor.",
        "invalid_api_key": "Yapay zeka asistanı geçici olarak kullanılamıyor. Şehir ödeme hizmetleri çalışmaya devam ediyor.",
        "quota_exceeded": "Yapay zeka asistanı şu anda yoğun. Lütfen birkaç dakika sonra tekrar deneyin.",
        "timeout": "Yapay zeka asistanı zamanında yanıt vermedi. Lütfen biraz sonra tekrar deneyin.",
        "content_blocked": "İstek işlenemedi. Lütfen sorunuzu farklı şekilde ifade edin.",
        "provider_unavailable": "Yapay zeka asistanı geçici olarak kullanılamıyor. Lütfen biraz sonra tekrar deneyin.",
        "generic": "Yapay zeka asistanından yanıt alınamadı. Şehir ödeme servisleri çalışmaya devam eder."
    }
}

WEATHER_CARD_LABELS = {
    "ru": {"title": "Погода в {district}", "wind": "Ветер", "precipitation": "Осадки",
           "live": "Телеметрия обновлена в реальном времени"},
    "tr": {"title": "{district} hava durumu", "wind": "Rüzgar", "precipitation": "Yağış",
           "live": "Telemetri gerçek zamanlı güncellendi"}
}

MAX_HISTORY_MESSAGES = 6
FOLLOW_UP_MAX_WORDS = 6

# Words that pick which tab the route card opens on
ROUTE_MODE_PATTERNS = [
    ("car", re.compile(r"машин|\bавто(?!бус)|такси(?!м)|araba|taksi(?!m)|otomobil|\bby car\b")),
    ("ferry", re.compile(r"паром|vapur|ferry|şehir hatları")),
    ("transit", re.compile(r"метро|общественн|автобус|трамва|toplu taşıma|metro|otobüs|tramvay")),
]

TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "zh", "з": "z", "и": "i",
    "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "i", "ь": "",
    "э": "e", "ю": "yu", "я": "ya", "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u", "\u0307": ""
}
MAX_HISTORY_CHARS = 2000


class AgentOrchestrator:
    def __init__(self):
        self.provider = GeminiProvider()
        self.tariffs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "istanbul_tariffs.txt")

    def _get_tariffs_context(self) -> str:
        if os.path.exists(self.tariffs_path):
            with open(self.tariffs_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return ""

    def _fallback(self, language: str, code: str = "generic") -> Dict[str, Any]:
        pack = FALLBACK_MESSAGES["tr"] if language == "tr" else FALLBACK_MESSAGES["ru"]
        return {
            "message": pack.get(code, pack["generic"]),
            "intent": "FALLBACK",
            "grounded_source": "Istanbul SmartCity OS local fallback",
            "action": None
        }

    @staticmethod
    def _build_messages(history: Optional[List[Dict[str, str]]], user_message: str) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        for item in (history or [])[-MAX_HISTORY_MESSAGES:]:
            role = "user" if item.get("role") == "user" else "model"
            content = (item.get("content") or "").strip()[:MAX_HISTORY_CHARS]
            if not content:
                continue
            if not messages and role != "user":
                continue
            if messages and messages[-1]["role"] == role:
                messages[-1]["content"] += "\n" + content
            else:
                messages.append({"role": role, "content": content})
        user_message = AgentOrchestrator._link_follow_up(messages, user_message)
        if messages and messages[-1]["role"] == "user":
            messages[-1]["content"] += "\n" + user_message
        else:
            messages.append({"role": "user", "content": user_message})
        return messages

    @staticmethod
    def _normalize_place(text: str) -> str:
        return "".join(TRANSLIT.get(ch, ch) for ch in text.lower())

    @staticmethod
    def _is_mentioned(place: str, user_message: str) -> bool:
        """True when the user named the place in the current message (Cyrillic, Latin or Turkish spelling)."""
        message = AgentOrchestrator._normalize_place(user_message)
        words = [w for w in re.findall(r"[a-z]+", AgentOrchestrator._normalize_place(place)) if len(w) >= 3]
        return bool(words) and any(word[:3] in message for word in words)

    @staticmethod
    def _link_follow_up(messages: List[Dict[str, str]], user_message: str) -> str:
        """Ties a short reply to the clarifying question the assistant asked last."""
        if not messages or messages[-1]["role"] != "model":
            return user_message
        if len(user_message.split()) > FOLLOW_UP_MAX_WORDS:
            return user_message
        questions = re.findall(r"[^.!?\n]*\?", messages[-1]["content"])
        if not questions:
            return user_message
        last_question = questions[-1].replace("*", "").strip()
        return f'[Reply to your last question: "{last_question}"] {user_message}'

    async def run(
        self,
        user_message: str,
        language: str = "ru",
        history: Optional[List[Dict[str, str]]] = None,
        current_location: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            return await self._run_internal(user_message, language, history, (current_location or "").strip())
        except Exception:
            return self._fallback(language, "generic")

    async def _run_internal(
        self,
        user_message: str,
        language: str,
        history: Optional[List[Dict[str, str]]],
        current_location: str = ""
    ) -> Dict[str, Any]:
        tariffs_context = self._get_tariffs_context()
        target_lang = "Turkish" if language == "tr" else "Russian"

        system_instruction = (
            "You are the official Intelligent AI Agent of Istanbul Smart City (2026). "
            f"You help citizens and visitors. Respond accurately in {target_lang}, concise but complete. "
            "Use the official verified tariffs below for any price, transport, or utility policy questions:\n"
            f"--- OFFICIAL TARIFFS REGULATION ---\n{tariffs_context}\n-----------------------------------\n"
            "Call a tool only when the user requests new data or an action (weather, transport route, "
            "utility bill, official guidelines, housing search). "
            "For follow-up or clarifying questions about information already present in the conversation "
            "(for example, a detail of a route or bill that was already shown), answer directly in text "
            "using the conversation history and the regulation above; do not call the same tool again. "
            "If neither the history nor the regulation covers the detail, say so briefly and point the user "
            "to the official portal mentioned earlier in the conversation.\n"
            "--- DIALOGUE RULES (HIGHEST PRIORITY) ---\n"
            "Strict follow-up resolution: if your last reply asked the user a clarifying question (for example, "
            "the origin of a route, the legal basis for a residence permit, or a housing budget), the user's next "
            "short message is a DIRECT answer to that exact question. Switching back to older topics from earlier "
            "in the conversation is FORBIDDEN. Example: if you asked 'Where are you departing from to Karaköy?' "
            "and the user answered 'Haramidere', you MUST immediately call search_transport_route with "
            "origin 'Haramidere' and destination 'Karaköy', and must not discuss renting a flat in Haramidere.\n"
            "Topic shift: when the user changes the topic (for example, from housing to transport or utilities), "
            "the context of the previous topic is fully discarded and must not influence the new task.\n"
            "--- RESIDENCE PERMIT (İKAMET) CONSULTATIONS ---\n"
            "For questions about obtaining or extending a residence permit, act as an experienced Istanbul "
            "migration lawyer. You MUST:\n"
            "1. Not call search_official_guidelines while the permit type or legal basis is unknown.\n"
            "2. Show expertise: explain that in 2026 extending a short-term tourist permit based on a rental "
            "contract is very limited and requires strong grounds, while extensions based on property ownership "
            "(Tapu), student status or family ties follow the standard procedure.\n"
            "3. Ask the user: what is the legal basis (rental, Tapu ownership, study, marriage, work), and how "
            "much time is left on the current permit (an extension can be filed via e-ikamet no earlier than "
            "60 days before expiry and strictly before the expiry date).\n"
            "4. Remind the user that address registration in the Nüfus system and an active UETS electronic "
            "address are mandatory.\n"
            "Once the procedure and basis are known and the user wants the final checklist, call "
            "search_official_guidelines with topic 'extension <basis>' or 'initial <basis>'.\n"
            "--- HOUSING (EMLAK) CONSULTATIONS ---\n"
            "Act as an experienced Istanbul real estate consultant. For a general request (for example, "
            "'I want to rent a flat in Beylikdüzü') do not call search_real_estate yet; first clarify: "
            "the budget in TRY, whether a gated complex with security (Site/Rezidans) matters or a regular "
            "building is fine, whether walking distance to a Metrobüs station (3-5 min) is critical, and whether "
            "the neighbourhood must be open to foreigners' residence registration (for an İkamet). "
            "Give a short expert note about the district while asking, but never name specific parks, residential "
            "complexes, streets or landmarks unless you are certain they exist. Call search_real_estate only when the "
            "district and approximate parameters are known, or the user explicitly asks to show available options.\n"
            "--- MOBILITY (ULAŞIM) CONSULTATIONS ---\n"
            "Act as an Istanbul urban mobility expert. When origin and destination are known, call "
            "search_transport_route; the response will explain the transfer logic (Metrobüs dedicated lane on E-5, "
            "Istanbulkart aktarma discount, ferry or Marmaray alternatives). If the origin or destination is "
            "not stated in the current transport request, ask for it instead of guessing; never take it from "
            "an earlier topic such as a housing search.\n"
            "--- UTILITIES (İSKİ, İGDAŞ, İSPARK) CONSULTATIONS ---\n"
            "When answering in text about utilities, remind the user of the regulation: İSKİ water up to 15 m³ is "
            "billed at the base tariff, İSKİ water bills are due by the 20th and İGDAŞ gas bills by the 25th of "
            "each month, and a 2.5% penalty applies after 30 days of delay. İSPARK parking in Zone A costs 40.00 TRY "
            "for the first hour and 20.00 TRY for each additional hour, paid cashless by Istanbulkart or bank card. "
            "Payments through the city gateway are instant and free of bank commission."
        )
        if current_location:
            system_instruction += (
                "\n--- USER LOCATION ---\n"
                f"The user's current start point is '{current_location}'. When the user asks for a route without naming "
                "the origin, says 'from home', 'let's go' or 'by car', use it as the origin and call "
                "search_transport_route immediately without asking where they depart from."
            )

        messages = self._build_messages(history, user_message)

        decision = await self.provider.generate_with_tools(
            messages=messages,
            tools_schema=AGENT_TOOLS_SCHEMA,
            system_instruction=system_instruction
        )

        if decision.get("error_code"):
            return self._fallback(language, decision.get("error_code", "generic"))

        if not decision.get("tool_calls"):
            empty_msg = (
                "Resmi veritabanında bu soruya ait kayıt bulunamadı."
                if language == "tr"
                else "Информация по вашему запросу не найдена в официальной базе данных."
            )
            return {
                "message": decision.get("text") or empty_msg,
                "intent": "GROUNDED_ANSWER",
                "grounded_source": "İstanbul Büyükşehir Belediyesi Resmi Bilgi Bankası (2026)",
                "action": None
            }

        tool_call = decision["tool_calls"][0]
        tool_name = tool_call["name"]
        args = tool_call.get("arguments", {})

        if tool_name == "search_transport_route":
            clarification = self._resolve_route_endpoints(args, user_message, history, current_location, language)
            if clarification:
                return clarification

        try:
            action_payload, source_name, tool_data = await self._execute_tool(tool_name, args, language)
        except Exception:
            return self._fallback(language, "generic")

        if action_payload is None:
            return self._fallback(language, "generic")

        if tool_name == "search_transport_route":
            last_user_turn = next((item.get("content") or "" for item in reversed(history or []) if item.get("role") == "user"), "")
            tool_data["activeMode"] = self._requested_route_mode(user_message) or self._requested_route_mode(last_user_turn)

        return {
            "message": compose_tool_reply(tool_name, tool_data, language),
            "intent": tool_name.upper(),
            "grounded_source": source_name,
            "action": action_payload
        }

    def _resolve_route_endpoints(
        self,
        args: Dict[str, Any],
        user_message: str,
        history: Optional[List[Dict[str, str]]],
        current_location: str,
        language: str
    ) -> Optional[Dict[str, Any]]:
        """Fills the route origin from the user's location instead of re-asking; returns a clarification if needed."""
        origin = str(args.get("origin") or "").strip()
        answers_question = bool(history) and history[-1].get("role") != "user" and "?" in (history[-1].get("content") or "")
        trusted = bool(origin) and (
            answers_question
            or self._is_mentioned(origin, user_message)
            or (current_location and self._is_mentioned(origin, current_location))
        )
        if not trusted and current_location:
            args["origin"] = origin = current_location
            trusted = True

        destination = str(args.get("destination") or "").strip()
        conversation = [user_message] + [item.get("content") or "" for item in history or []]
        destination_known = bool(destination) and any(self._is_mentioned(destination, text) for text in conversation)

        question = None
        if not trusted:
            question = ask_route_origin(destination if destination_known else "", language)
        elif not destination_known:
            question = ask_route_destination(origin, language)
        if not question:
            return None
        return {
            "message": question,
            "intent": "CLARIFICATION",
            "grounded_source": "İBB TUHİM Toplu Ulaşım Ağı (2026)",
            "action": None
        }

    @staticmethod
    def _requested_route_mode(user_message: str) -> Optional[str]:
        text = user_message.lower()
        for mode, pattern in ROUTE_MODE_PATTERNS:
            if pattern.search(text):
                return mode
        return None

    async def _execute_tool(
        self,
        tool_name: str,
        args: Dict[str, Any],
        language: str
    ) -> Tuple[Optional[Dict[str, Any]], str, Dict[str, Any]]:
        action_payload = None
        data: Dict[str, Any] = {}
        source_name = "İstanbul Büyükşehir Belediyesi"

        if tool_name == "get_current_weather":
            district = args.get("district", "Beylikdüzü")
            data = await implementations.execute_get_current_weather(district, language)
            source_name = data.get("source", source_name)
            labels = WEATHER_CARD_LABELS["tr" if language == "tr" else "ru"]
            action_payload = {
                "type": "ROUTE_CARD",
                "data": {
                    "origin": labels["title"].format(district=data.get("district", district)),
                    "destination": data.get("temperature", "—"),
                    "fare": f"{labels['wind']}: {data.get('wind', '—')}",
                    "duration": f"{labels['precipitation']}: {data.get('precipitation', '—')}",
                    "steps": [labels["live"]]
                }
            }

        elif tool_name == "search_transport_route":
            origin = args.get("origin", "Beylikdüzü")
            destination = args.get("destination", "Taksim")
            data = await implementations.execute_search_transport_route(origin, destination, language)
            source_name = data.get("source", source_name)
            action_payload = {"type": "ROUTE_CARD", "data": data}

        elif tool_name == "get_utility_bill":
            service_type = args.get("service_type", "WATER")
            data = await implementations.execute_get_utility_bill(service_type, language)
            source_name = data.get("source", source_name)
            action_payload = {"type": "PAYMENT_CARD", "data": data}

        elif tool_name == "search_official_guidelines":
            topic = args.get("topic", "ikamet")
            data = await implementations.execute_search_official_guidelines(topic, language)
            source_name = data.get("source", source_name)
            action_payload = {"type": "INFO_GUIDE", "data": data}

        elif tool_name == "search_real_estate":
            data = await implementations.execute_search_real_estate(
                location=args.get("location", "Beylikdüzü"),
                max_budget_try=float(args.get("max_budget_try", 35000)),
                rooms=args.get("rooms", "2+1"),
                language=language
            )
            source_name = data.get("source", source_name)
            action_payload = {"type": "ESTATE_CARD", "data": data}

        return action_payload, source_name, data
