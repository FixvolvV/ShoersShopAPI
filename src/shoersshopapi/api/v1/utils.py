from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
import uuid

from shoersshopapi.core.settings import settings


def gen_uuid() -> str:
    return str(uuid.uuid4())