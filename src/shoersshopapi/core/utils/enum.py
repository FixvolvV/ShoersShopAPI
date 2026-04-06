from enum import StrEnum

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
    