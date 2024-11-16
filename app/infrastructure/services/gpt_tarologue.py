import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

import httpx

from app.domain.entities.analyze import AnalyzeEntity, SuitabilityEntity, CosmogramEntity, TaroCardEntity
from app.domain.entities.user import UserEntity


@dataclass(eq=False, frozen=True)
class IGPTTarologue(ABC):
    @abstractmethod
    async def analyze(self, user: UserEntity) -> AnalyzeEntity: ...


@dataclass(eq=False, frozen=True)
class YandexGPTTarologue(IGPTTarologue):
    api_url: str
    api_key: str
    folder_id: str

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Api-Key {self.api_key}",
            "x-folder-id": self.folder_id,
            "Content-Type": "application/json"
        }

    async def analyze(self, user: UserEntity) -> AnalyzeEntity:
        data = {
            "messages": [
                {
                    "text": "Ты - эксперт по Таро и астрологии, который помогает определить, "
                            "подходит ли человек на определенную должность, анализируя его личные данные. "
                            "На основе предоставленной информации (имя, дата рождения, пол, интересы и профессия) "
                            "проведи анализ с использованием карт Таро и космограммы. "
                            "Верни результаты в формате JSON,  "
                            "включая интерпретации карт Таро и астрологических аспектов.  "
                            "В ответе нужно упомянуть как минимум два негативных момента исходя из результатов Таро "
                            "и астрологических аспектов. Нужно 4 карты таро и 5 домов"
                            "\n\nВходные данные:  \n"
                            "- Имя: {имя}  \n"
                            "- Дата рождения: {дата_рождения} (в формате YYYY-MM-DD)  \n"
                            "- Пол: {пол} (мужской/женский/другой)  \n"
                            "- Интересы: {интересы} (список через запятую)  \n"
                            "- Профессия: {профессия}  \n\n"
                            "Выходные данные в формате JSON должны содержать следующие секции:  \n"
                            "- `cards`: информация о картах Таро (название и толкование)  \n"
                            "- `cosmogram`: анализ космограммы (знаки Солнца, Луны и асцендента, элементы и дома)  \n"
                            "- `suitability`: оценка того, насколько данный "
                            "человек подходит на указанную должность, с кратким объяснением.  "
                            "\n\nПример результата:  \n"
                            "{  \n  \"cards\": [  \n"
                            "    {  \n"
                            "      \"name\": \"Название карты 1\",  \n"
                            "      \"meaning\": \"Толкование карты 1\"  \n"
                            "    },  \n"
                            "    {  \n"
                            "      \"name\": \"Название карты 2\",  \n "
                            "     \"meaning\": \"Толкование карты 2\"  \n"
                            "    }  \n    ....\n  ],  \n"
                            "  \"cosmogram\": {  \n"
                            "    \"sun_sign\": \"Знак Солнца\",  \n"
                            "    \"moon_sign\": \"Знак Луны\",  \n"
                            "    \"rising_sign\": \"Асцендент\",  \n"
                            "    \"elements\": {  \n "
                            "     \"fire\": \"Количество планет в огненных знаках\",  \n"
                            "      \"earth\": \"Количество планет в земных знаках\",  \n"
                            "      \"air\": \"Количество планет в воздушных знаках\",  \n"
                            "      \"water\": \"Количество планет в водных знаках\"  \n "
                            "   },  \n"
                            "    \"houses\": {  \n "
                            "     \"house_1\": \"Описание первого дома\",  \n"
                            "      \"house_2\": \"Описание второго дома\"  \n "
                            "     ....\n"
                            "    }  \n"
                            "  },  \n "
                            " \"suitability\": {  \n "
                            "   \"is_suitable\": true/false,  \n"
                            "    \"explanation\": \"Краткое объяснение, почему данный человек "
                            "подходит/не подходит на указанную должность.\"  \n"
                            "  }  "
                            "\n}",
                    "role": "system"
                },
                {
                    "role": "user",
                    "text": f"Имя: {user.name} "
                            f"Дата рождения: {user.birthdate} "
                            f"Пол: {user.sex} "
                            f"Интересы: {user.interests}"
                            f" Профессия: {user.professions}"
                }
            ],
            "completionOptions": {
                "Stream": False,
                "temperature": 0.5,
                "maxTokens": 1000
            },
            "modelUri": "gpt://b1g0jtim007tq3pnsog3/yandexgpt/rc"
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                url=self.api_url,
                json=data,
                headers=self.headers
            )
            json_data = response.json()

        llm_response = json_data["result"]["alternatives"][0]["message"]["text"]
        return self.parse_response(llm_response)

    @staticmethod
    def parse_response(response: str) -> AnalyzeEntity:
        response = response.strip("```")
        data = json.loads(response)

        return AnalyzeEntity(
            cards=[TaroCardEntity(
                name=card["name"],
                meaning=card["meaning"]
            ) for card in data["cards"]],
            cosmogram=CosmogramEntity(
                sun_sign=data["cosmogram"]["sun_sign"],
                moon_sign=data["cosmogram"]["moon_sign"],
                rising_sign=data["cosmogram"]["rising_sign"],
                elements=data["cosmogram"]["elements"],
                houses=data["cosmogram"]["houses"]
            ),
            suitability=SuitabilityEntity(
                is_suitable=data["suitability"]["is_suitable"],
                explanation=data["suitability"]["explanation"],
            )
        )
