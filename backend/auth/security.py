import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from config.config import get_settings

settings = get_settings()
SECRET_KEY = settings.JWT_SECRET.get_secret_value()
ALGORITHM = settings.JWT_ALG
ACCESS_TOKEN_EXPIRES_MIN = settings.ACCESS_TOKEN_EXPIRES_MIN

# passwords encode/decode
def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# jwt token encode/decode
def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_minutes is None:
        expires_minutes = ACCESS_TOKEN_EXPIRES_MIN
    expire = now + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire, "iat": now})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload