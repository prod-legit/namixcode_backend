from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class IGPTTarologue(ABC):
    @abstractmethod
    async def hint(self) -> None: ...


@dataclass(eq=False, frozen=True)
class YandexGPTTarologue(IGPTTarologue):
    api_url: str
    api_key: str
    folder_id: str

    async def hint(self) -> None: ...
# ratings = []
# for group in grouped_answers:
#     if group[1] == 'Range':
#         ratings.append(
#             {
#                 'text': f'вопрос: {group[0]};'
#                         f'оценка: {group[2]} из 10',
#                 'role': 'user'
#             }
#         )
#     else:
#         ratings.append(
#             {
#                 'text': f'вопрос: {group[0]};'
#                         f'оценка: {(group[2] + 1) * 5} из 10',
#                 'role': 'user'
#             }
#         )
#
# data = {
#     'modelUri': 'gpt://b1g2ahktcv1255vqabvd/yandexgpt',
#     'messages': [
#         {
#             'text': 'Ты аналитик, который помогает компании. '
#                     'Дай совет на основе средней оценки в формате вопрос:оценка + твой совет',
#             'role': 'system'
#         },
#         *ratings
#     ],
#     'completionOptions': {
#         'stream': False,
#         'maxTokens': 500,
#         'temperature': 0.4
#     }
# }
# async with httpx.AsyncClient() as client:
#     resp = await client.post(
#         url=self.api_url,
#         json=data,
#         headers=YANDEX_HEADERS
#     )
