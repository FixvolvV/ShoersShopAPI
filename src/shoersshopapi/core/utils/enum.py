from enum import IntEnum, StrEnum

class Role(StrEnum):
    user = "user"
    admin = "admin"

class Status(StrEnum):
    confirmation = "confirmation"
    transit = "transit"
    delivered = "delivered"
    cancelled = "cancelled"

class Rating(StrEnum):
    very_bad = "very_bad"
    bad = "bad"
    normal = "normal"
    good = "good"
    very_good = "very_good"

class Color(StrEnum):
    black = "чёрный"
    white = "белый"
    red = "красный"
    orange = "оранжевый"
    yellow = "жёлтый"
    green = "зелёный"
    light_blue = "голубой"
    blue = "синий"
    purple = "фиолетовый"

class Category(StrEnum):
    running = "бег"
    everyday = "повседневные"
    basketball = "баскетбол"
    training = "тренинг"

class Sizes(IntEnum):
    size_39 = 39
    size_40 = 40
    size_41 = 41
    size_42 = 42
    size_43 = 43
    size_44 = 44
    size_45 = 45

    