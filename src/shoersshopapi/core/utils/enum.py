from enum import Enum

class Role(Enum):
    user = 1
    admin = 2

class Status(Enum):
    confirmation = 1
    transit = 2
    delivered = 3

class Rating(Enum):
    very_bad = 1
    bad = 2
    normal = 3
    good = 4
    very_good = 5