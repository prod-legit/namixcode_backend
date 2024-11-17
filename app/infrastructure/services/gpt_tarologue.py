import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

import httpx

from app.domain.entities.analyze import (
    SuitabilityEntity,
    CosmogramEntity,
    TaroCardEntity,
    CompareAnalyzeEntity,
    AtmosphereAnalyzeEntity,
    SuitableAnalyzeEntity, UserAnalyzeEntity, CompatibilityEntity, EmployeeAtmosphereAnalyzeEntity
)
from app.domain.entities.user import UserEntity


@dataclass(eq=False, frozen=True)
class IGPTTarologue(ABC):
    @abstractmethod
    async def suitable_analyze(self, user: UserEntity) -> SuitableAnalyzeEntity: ...

    @abstractmethod
    async def compare_analyze(self, user: UserEntity, boss: UserEntity) -> CompareAnalyzeEntity: ...

    @abstractmethod
    async def atmosphere_analyze(self, users: list[UserEntity]) -> AtmosphereAnalyzeEntity: ...

    @staticmethod
    @abstractmethod
    def parse_suitable_analyze(data: str) -> SuitableAnalyzeEntity: ...

    @staticmethod
    @abstractmethod
    def parse_compare_analyze(data: str) -> CompareAnalyzeEntity: ...

    @staticmethod
    @abstractmethod
    def parse_atmosphere_analyze(data: str) -> AtmosphereAnalyzeEntity: ...


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

    async def request(self, data: dict) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                url=self.api_url,
                json=data,
                headers=self.headers
            )
            json_data = response.json()

        llm_response = json_data["result"]["alternatives"][0]["message"]["text"].strip("```")
        return json.loads(llm_response)

    async def suitable_analyze(self, user: UserEntity) -> SuitableAnalyzeEntity:
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
                            "{  "
                            "    \"name\": \"Имя\","
                            "\n  \"cards\": [  \n"
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
                "temperature": 0.4,
                "maxTokens": 1000
            },
            "modelUri": "gpt://b1g0jtim007tq3pnsog3/yandexgpt/rc"
        }
        llm_response = await self.request(data)

        return self.parse_suitable_analyze(llm_response)

    async def compare_analyze(self, user: UserEntity, boss: UserEntity) -> CompareAnalyzeEntity:
        data = {
            "messages": [
                {
                    "text": "Ты – эксперт по Таро и астрологии. "
                            "Твоя задача – определить, насколько сработаются два человека: начальник и потенциальный подчиненный. "
                            "На основе предоставленной информации (имя, дата рождения, пол, интересы и профессия) "
                            "проведи анализ с использованием карт Таро и космограммы для каждого человека. "
                            "Верни результаты в формате JSON.  Иногда будь категоричен. \n\n"
                            "Входные данные:  \n"
                            "1. Начальник:  \n"
                            "   - Имя: {имя_начальника}  \n"
                            "   - Дата рождения: {дата_рождения_начальника} (в формате YYYY-MM-DD)  \n"
                            "   - Пол: {пол_начальника} (мужской/женский/другой)  \n"
                            "   - Интересы: {интересы_начальника} (список через запятую)  \n"
                            "   - Профессия: {профессия_начальника}  \n\n"
                            "2. Подчиненный:  \n"
                            "   - Имя: {имя_подчиненного}  \n"
                            "   - Дата рождения: {дата_рождения_подчиненного} (в формате YYYY-MM-DD)  \n"
                            "   - Пол: {пол_подчиненного} (мужской/женский/другой)  \n"
                            "   - Интересы: {интересы_подчиненного} (список через запятую)  \n"
                            "   - Профессия: {профессия_подчиненного}  \n\n"
                            "Выходные данные в формате JSON должны содержать:  \n"
                            "- `boss`: анализ начальника (карты Таро и космограмма)  \n"
                            "- `employee`: анализ подчиненного (карты Таро и космограмма)  \n"
                            "- `compatibility`: оценка совместимости (степень совместимости и краткое объяснение)  \n\n"
                            "Пример результата:  \n"
                            "{  \n  \"boss\": {  \n"
                            "    \"name\": \"Имя начальника\","
                            "    \"cards\": [  \n"
                            "      {  \n"
                            "        \"name\": \"Название карты\",  \n"
                            "        \"meaning\": \"Толкование карты\"  \n"
                            "      },  \n"
                            "      {  \n"
                            "        \"name\": \"Название карты\",  \n"
                            "        \"meaning\": \"Толкование карты\"  \n"
                            "      }  \n"
                            "    ],  \n"
                            "    \"cosmogram\": {  \n"
                            "      \"sun_sign\": \"Знак Солнца\",  \n"
                            "      \"moon_sign\": \"Знак Луны\",  \n"
                            "      \"rising_sign\": \"Асцендент\",  \n"
                            "      \"elements\": {  \n"
                            "        \"fire\": \"Количество планет в огненных знаках\",  \n"
                            "        \"earth\": \"Количество планет в земных знаках\",  \n"
                            "        \"air\": \"Количество планет в воздушных знаках\",  \n"
                            "        \"water\": \"Количество планет в водных знаках\"  \n"
                            "      }  \n"
                            "     \"houses\": {  \n"
                            "      \"house_1\": \"Описание первого дома\",  \n"
                            "      \"house_2\": \"Описание второго дома\"  \n"
                            "      \"house_3\": \"Описание третьего дома\"  \n"
                            "    }  \n"
                            "  },  \n"
                            "  \"employee\": {  \n"
                            "   \"name\": \"Имя подчиненного\","
                            "    \"cards\": [  \n"
                            "      {  \n"
                            "        \"name\": \"Название карты\",  \n"
                            "        \"meaning\": \"Толкование карты\"  \n"
                            "      },"
                            "       {  \n"
                            "        \"name\": \"Название карты\",  \n"
                            "        \"meaning\": \"Толкование карты\"  \n"
                            "      }  \n"
                            "    ],  \n"
                            "    \"cosmogram\": {  \n"
                            "      \"sun_sign\": \"Знак Солнца\",  \n"
                            "      \"moon_sign\": \"Знак Луны\",  \n"
                            "      \"rising_sign\": \"Асцендент\",  \n"
                            "      \"elements\": {  \n"
                            "        \"fire\": \"Количество планет в огненных знаках\",  \n"
                            "        \"earth\": \"Количество планет в земных знаках\",  \n"
                            "        \"air\": \"Количество планет в воздушных знаках\",  \n"
                            "        \"water\": \"Количество планет в водных знаках\"  \n"
                            "      }  \n"
                            "     \"houses\": {  \n"
                            "      \"house_1\": \"Описание первого дома\",  \n"
                            "      \"house_2\": \"Описание второго дома\"  \n"
                            "      \"house_3\": \"Описание третьего дома\"  \n"
                            "    }  \n"
                            "    }  \n"
                            "  },  \n"
                            "  \"compatibility\": {  \n"
                            "    \"score\": \"Процент совместимости\",  \n"
                            "    \"explanation\": \"Краткое объяснение, почему эти два человека могут хорошо сработаться или наоборот.\"  \n"
                            "  }  "
                            "\n}",
                    "role": "system"
                },
                {
                    "text": f"Начальник:"
                            f"Имя: {boss.name}"
                            f"Дата рождения: {boss.birthdate}"
                            f"Пол: {boss.sex}"
                            f"Интересы: {boss.interests}"
                            f"Профессия: {boss.professions}"
                            f"Подчиненный:"
                            f"Имя: {user.name}"
                            f"Дата рождения: {user.birthdate}"
                            f"Пол: {user.sex}"
                            f"Интересы: {user.interests}"
                            f"Профессия: {user.professions}",
                    "role": "user"
                }
            ],
            "completionOptions": {
                "temperature": 0.4,
                "maxTokens": 1000
            },
            "modelUri": "gpt://b1g0jtim007tq3pnsog3/yandexgpt/rc"
        }
        llm_response = await self.request(data)

        return self.parse_compare_analyze(llm_response)

    async def atmosphere_analyze(self, users: list[UserEntity]) -> AtmosphereAnalyzeEntity:
        text = "".join([
            f"Имя: {user.name} "
            f"Дата рождения: {user.birthdate} "
            f"Пол: {user.sex} "
            f"Интересы: {user.interests} "
            f"Профессия: {user.professions}\n"
            for user in users])

        data = {
        "messages": [
            {
            "text": "Ты - эксперт в области анализа команды, "
                    "использующий карты Таро и астрологические принципы для оценки атмосферы и взаимодействия между сотрудниками."
                    " Пожалуйста, проанализируй информацию о каждом из сотрудников и дай понимание общей атмосферы в коллективе,"
                    " а также воздействие каждого сотрудника.  \n\n"
                    "На вход подаются данные о каждом сотруднике в следующем формате:  \n"
                    "- имя  \n"
                    "- дата рождения (в формате YYYY-MM-DD)  \n"
                    "- пол  \n"
                    "- интересы (через запятую)  \n"
                    "- профессия  \n\n"
                    "На основе этих данных возвращай результат в формате JSON с двумя основными частями:  \n"
                    "1. Общий анализ атмосферы в коллективе.  \n"
                    "2. Список сотрудников с индивидуальным анализом.  \n\n"
                    "Выходные данные должны иметь следующий формат:  \n\n"
                    "{  \n"
                    "  \"overall_analysis\": \"{общий анализ атмосферы в коллективе, основанный на Таро и астрологии. "
                    "Опиши, какие энергии преобладают, какие отношения между сотрудниками являются особенно положительными или негативными, "
                    "и какие проблемы могут возникнуть.}\",  \n"
                    "  \"employees\": [  \n"
                    "    {  \n"
                    "      \"name\": \"{имя_сотрудника}\",  \n"
                    "      \"main_analytics\": \"{подробный текстовый анализ на основе карт Таро и космограммы,"
                    " объясняющий атмосферу, которую создает сотрудник, его сильные и слабые стороны, "
                    "а также воздействие на коллектив}\",  \n"
                    "      \"compatibility_score\": \"{процент_совместимости_сотрудника}\", // Например, \"75%\"  \n"
                    "      \"impact_on_atmosphere\": \"{влияние сотрудника на атмосферу (позитивное/негативное)}\"  \n"
                    "    },  \n"
                    "    ...  \n"
                    "  ]  \n"
                    "}  \n\n"
                    "Пример структуры ответа:  \n\n"
                    "{  \n"
                    "  \"overall_analysis\": \"В коллективе ощущается баланс между творческой энергией и разумной аналитикой. "
                    "Однако есть некоторые напряженные моменты, которые могут вылиться в конфликты, если не решить их вовремя. "
                    "Карты показывают, что некоторые сотрудники, возможно, создают дисгармонию, "
                    "тогда как другие выступают как источники вдохновения и поддержки. ...\",  \n"
                    "  \"employees\": [  \n"
                    "    {  \n"
                    "      \"name\": \"Анна\",  \n"
                    "      \"main_analytics\": \"Анна приносит в команду оптимизм и поддержку. "
                    "Ее энергия, основанная на сочетании карт Таро, таких как 'Солнце' и 'Звезда', "
                    "создает пространство для роста. Однако ей стоит быть на чеку, "
                    "чтобы не перегрузить коллег своим энтузиазмом.\",  \n"
                    "      \"compatibility_score\": \"85%\",  \n"
                    "      \"impact_on_atmosphere\": \"позитивное\"  \n"
                    "    },  \n"
                    "    {  \n"
                    "      \"name\": \"Сергей\",  \n"
                    "      \"main_analytics\": \"Сергей, несмотря на свои сильные стороны как организатора, "
                    "может создавать напряжение из-за своего перфекционизма. "
                    "Карты указывают на то, что его высокие ожидания могут эмоционально подавлять других. "
                    "Необходимо найти баланс.\",  \n"
                    "      \"compatibility_score\": \"60%\",  \n"
                    "      \"impact_on_atmosphere\": \"негативное\"  \n"
                    "    },  \n"
                    "    {  \n"
                    "      \"name\": \"Мария\",  \n"
                    "      \"main_analytics\": \"Мария демонстрирует лидирующие качества благодаря своим астрологическим аспектам, "
                    "что способствует продуктивности. Тем не менее, ей стоит быть осторожной с критикой, чтобы не создавать барьеров в общении.\",  \n"
                    "      \"compatibility_score\": \"75%\",  \n"
                    "      \"impact_on_atmosphere\": \"позитивное\"  \n"
                    "    }  \n"
                    "  ]  \n"
                    "}  \n\n"
                    "Теперь, предоставь данные о сотрудниках, и я проведу анализ атмосферы в коллективе.",
            "role": "system"
            },
            {
            "text": text,
            "role": "user"
            }
        ],
        "completionOptions": {
            "temperature": 0.4,
            "maxTokens": 1000
        },
        "modelUri": "gpt://b1g0jtim007tq3pnsog3/yandexgpt/rc"
        }
        llm_response = await self.request(data)

        return self.parse_atmosphere_analyze(llm_response)

    @staticmethod
    def parse_suitable_analyze(data: dict) -> SuitableAnalyzeEntity:
        cards = data["cards"]
        cosmogram = data["cosmogram"]
        suitability = data["suitability"]

        return SuitableAnalyzeEntity(
            name=data["name"],
            cards=[TaroCardEntity(
                name=card["name"],
                meaning=card["meaning"]
            ) for card in cards],
            cosmogram=CosmogramEntity(
                sun_sign=cosmogram["sun_sign"],
                moon_sign=cosmogram["moon_sign"],
                rising_sign=cosmogram["rising_sign"],
                elements=cosmogram["elements"],
                houses=cosmogram["houses"]
            ),
            suitability=SuitabilityEntity(
                is_suitable=suitability["is_suitable"],
                explanation=suitability["explanation"],
            )
        )

    @staticmethod
    def parse_compare_analyze(data: dict) -> CompareAnalyzeEntity:
        compatibility = data["compatibility"]
        boss_cards = data["boss"]["cards"]
        boss_cosmogram = data["boss"]["cosmogram"]
        employee_cards = data["boss"]["cards"]
        employee_cosmogram = data["boss"]["cosmogram"]

        return CompareAnalyzeEntity(
            boss=UserAnalyzeEntity(
                name=data["boss"]["name"],
                cards=[TaroCardEntity(
                    name=card["name"],
                    meaning=card["meaning"]
                ) for card in boss_cards],
                cosmogram=CosmogramEntity(
                    sun_sign=boss_cosmogram["sun_sign"],
                    moon_sign=boss_cosmogram["moon_sign"],
                    rising_sign=boss_cosmogram["rising_sign"],
                    elements=boss_cosmogram["elements"],
                    houses=boss_cosmogram["houses"]
                ),
            ),
            employee=UserAnalyzeEntity(
                name=data["employee"]["name"],
                cards=[TaroCardEntity(
                    name=card["name"],
                    meaning=card["meaning"]
                ) for card in employee_cards],
                cosmogram=CosmogramEntity(
                    sun_sign=employee_cosmogram["sun_sign"],
                    moon_sign=employee_cosmogram["moon_sign"],
                    rising_sign=employee_cosmogram["rising_sign"],
                    elements=employee_cosmogram["elements"],
                    houses=employee_cosmogram["houses"]
                ),
            ),
            compatibility=CompatibilityEntity(
                score=int(str(compatibility["score"]).strip("%")),
                explanation=compatibility["explanation"]
            )
        )

    @staticmethod
    def parse_atmosphere_analyze(data: dict) -> AtmosphereAnalyzeEntity:
        return AtmosphereAnalyzeEntity(
            overall_analysis=data["overall_analysis"],
            employees=[EmployeeAtmosphereAnalyzeEntity(
                name=employee["name"],
                main_analytics=employee["main_analytics"],
                compatibility_score=int(str(employee["compatibility_score"]).strip("%")),
                impact_on_atmosphere=employee["impact_on_atmosphere"],

            ) for employee in data["employees"]]
        )
