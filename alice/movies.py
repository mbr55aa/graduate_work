import random

fake_films_db = [
    "Зеленая миля",
    "Побег из Шоушенка",
    "Список Шиндлера",
    "Властелин колец: Возвращение короля",
    "Форрест Гамп",
    "Один плюс один",
    "Криминальное чтиво",
    None,
]

fake_persons_db = [
    "Михаил Ефремов",
    "Энсел Элгорт",
    "Элеасар Гомес",
    "Лиа Мишель",
    "Джастин Хартли",
    "Джада Пинкетт Смит",
    "Рики Джервэйс",
    "Амитабх Баччан",
    None,
]


def get_director(form, current_state):
    api_req = {
        "film": form["slots"].get("film", {}).get("value"),
    }
    api_req = {k: v for k, v in api_req.items() if v}
    current_state.update(api_req)

    if "film" not in current_state:
        return "Уточните еще раз фильм", current_state

    response = random.choice(fake_persons_db)  # Fake request to async_api
    if not response:
        return "К сожалению, я не смогла найти режиссера", current_state

    return response, current_state
