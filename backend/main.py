from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from config.config import get_settings
from config.session import AsyncSessionLocal
from auth.security import hash_password, verify_password, create_access_token, decode_access_token
from models import AppUser, Project, Problem, Solution, Video, Submission

settings = get_settings()
app = FastAPI(title="D33tcode", debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = settings.API_PREFIX

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# simply models for endpoints:

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    role: str


class UserCreate(BaseModel):
    username: str
    email_address: str
    password: str
    role: str = "standard"


class UserRead(BaseModel):
    id: int
    username: str
    email_address: str
    role: str
    update_password: Optional[bool] = None

    class Config:
        from_attributes = True


class UserPasswordUpdate(BaseModel):
    password: str


class ProjectIn(BaseModel):
    title: str
    description: Optional[str] = None
    problem_id: Optional[int] = None
    solution_id: Optional[int] = None
    difficulty: Optional[int] = None


class ProjectOut(ProjectIn):
    id: int

    class Config:
        from_attributes = True


class ProblemOut(BaseModel):
    id: int
    git_link: str
    problem_description: Optional[str] = None

    class Config:
        from_attributes = True


class SolutionOut(BaseModel):
    id: int
    git_link: str
    solution_description: str

    class Config:
        from_attributes = True


class VideoOut(BaseModel):
    id: int
    project_id: int
    yt_code: str
    type: Optional[str] = None
    ordinal: Optional[int] = None

    class Config:
        from_attributes = True


class SubmissionOut(BaseModel):
    app_user_id: int
    project_id: int
    is_complete: bool
    grade: Optional[float] = None

    class Config:
        from_attributes = True


class ProjectsByDifficulty(BaseModel):
    difficulty: Optional[int]
    count: int


# auth

async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
    db: AsyncSession = Depends(get_db),
) -> AppUser:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token missing subject")

    result = await db.execute(select(AppUser).where(AppUser.id == int(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


async def require_admin(user: AppUser = Depends(get_current_user)) -> AppUser:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user

# login endpoint

@app.post(f"{API_PREFIX}/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AppUser).where(AppUser.username == data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Bad username or password")

    token = create_access_token({"sub": str(user.id), "role": user.role})

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        username=user.username,
        role=user.role,
    )



@app.get("/")
def read_root():
    return {"Hey this is the thing!"}

