from openai import OpenAI
from config.settings import settings
from app.tools.weather_tool import get_weather
from app.tools.web_tool import quick_web_search

SYSTEM_PROMPT = (
    "You are FusionBrain, a practical assistant inspired by Jarvis. "
    "Be concise and action oriented."
)


class FusionBrain:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
        )
        self.model = settings.openrouter_model

    async def run(self, user_message: str, memory_context: str = "") -> dict:
        msg_lower = user_message.lower()

        if any(word in msg_lower for word in ["mot", "weather", "temperature"]):
            city = self._extract_city(user_message) or "Tirane"
            weather = await get_weather(city)
            reply = (
                f"Moti ne {weather['city']}: {weather['temp_c']}°C, "
                f"ndjesia {weather['feels_like_c']}°C, {weather['weather_desc']}."
            )
            return {"reply": reply, "tool_used": "weather", "tool_result": weather}

        if any(word in msg_lower for word in ["kerko", "search", "kush eshte", "what is"]):
            result = await quick_web_search(user_message)
            summary = result.get("abstract") or "Nuk gjeta permbledhje te shkurter."
            return {
                "reply": f"Ja cfare gjeta: {summary}",
                "tool_used": "web_search",
                "tool_result": result,
            }

        prompt = f"Memory:\n{memory_context}\n\nUser: {user_message}"
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        reply = completion.choices[0].message.content or "Nuk kam pergjigje per momentin."
        return {"reply": reply, "tool_used": None, "tool_result": None}

    @staticmethod
    def _extract_city(text: str):
        tokens = text.split()
        if "ne" in tokens:
            idx = tokens.index("ne")
            if idx + 1 < len(tokens):
                return tokens[idx + 1].strip(" ,.!?")
        return None
