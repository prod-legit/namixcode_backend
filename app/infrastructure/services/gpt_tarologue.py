from abc import ABC, abstractmethod
from dataclasses import dataclass
import httpx


YANDEX_HEADERS = {
    'Authorization': 'Api-Key AQVN2Ji9YSEvsYDh5layWNkg9C51L6j0toJ7RzZN',
    'x-folder-id': 'b1g0jtim007tq3pnsog3',
    'Content-Type': 'application/json'}

#AQVN2Ji9YSEvsYDh5layWNkg9C51L6j0toJ7RzZN
#ajeoj2um289fm60e3pim
@dataclass(eq=False, frozen=True)
class IGPTTarologue(ABC):
    @abstractmethod
    async def hint(self) -> None: ...


@dataclass(eq=False, frozen=True)
class YandexGPTTarologue(IGPTTarologue):
    api_url: str
    api_key: str
    folder_id: str

    async def hint(self, name, date_of_birth, sex, interests, profession) -> None:
        '''Пример запроса:
        Имя: Анастасия 
        Дата рождения: 1990-05-15
        Пол: женский 
        Интересы: психология, искусство, путешествия 
        Профессия: дизайнер'''
        data = {
            "messages": [
                {
                "text": "Ты - эксперт по Таро и астрологии, который помогает определить, подходит ли человек на определенную должность, анализируя его личные данные. На основе предоставленной информации (имя, дата рождения, пол, интересы и профессия) проведи анализ с использованием карт Таро и космограммы. Верни результаты в формате JSON,  включая интерпретации карт Таро и астрологических аспектов.  В ответе нужно упомянуть как минимум два негативных момента исходя из результатов Таро и астрологических аспектов. Нужно 4 карты таро и 5 домов\n\nВходные данные:  \n- Имя: {имя}  \n- Дата рождения: {дата_рождения} (в формате YYYY-MM-DD)  \n- Пол: {пол} (мужской/женский/другой)  \n- Интересы: {интересы} (список через запятую)  \n- Профессия: {профессия}  \n\nВыходные данные в формате JSON должны содержать следующие секции:  \n- `tarot_reading`: информация о картах Таро (название и толкование)  \n- `cosmogram_analysis`: анализ космограммы (знаки Солнца, Луны и асцендента, элементы и дома)  \n- `suitability_analysis`: оценка того, насколько данный человек подходит на указанную должность, с кратким объяснением.  \n\nПример результата:  \n{  \n  \"tarot_reading\": {  \n    \"card_1\": {  \n      \"name\": \"Название карты 1\",  \n      \"meaning\": \"Толкование карты 1\"  \n    },  \n    \"card_2\": {  \n      \"name\": \"Название карты 2\",  \n      \"meaning\": \"Толкование карты 2\"  \n    }  \n    ....\n  },  \n  \"cosmogram_analysis\": {  \n    \"sun_sign\": \"Знак Солнца\",  \n    \"moon_sign\": \"Знак Луны\",  \n    \"rising_sign\": \"Асцендент\",  \n    \"elements\": {  \n      \"fire\": \"Количество планет в огненных знаках\",  \n      \"earth\": \"Количество планет в земных знаках\",  \n      \"air\": \"Количество планет в воздушных знаках\",  \n      \"water\": \"Количество планет в водных знаках\"  \n    },  \n    \"houses\": {  \n      \"house_1\": \"Описание первого дома\",  \n      \"house_2\": \"Описание второго дома\"  \n      ....\n    }  \n  },  \n  \"suitability_analysis\": {  \n    \"is_suitable\": true/false,  \n    \"explanation\": \"Краткое объяснение, почему данный человек подходит/не подходит на указанную должность.\"  \n  }  \n}",
                "role": "system"
                },
                {
                'role': "user",
                'text': f"Имя: {name} Дата рождения: {date_of_birth} Пол: {sex} Интересы: {interests} Профессия: {profession}"
                }
            ],
            "completionOptions": {
                "Stream": False,
                "temperature": 0.5,
                "maxTokens": 1000
            },
            "modelUri": "gpt://b1g0jtim007tq3pnsog3/yandexgpt/rc"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
            url=self.api_url,
            json=data,
            headers=YANDEX_HEADERS
            )
            response = await resp.json()
            msg = response['result']['alternatives'][0]['message']['text']
            return {'text': msg}
