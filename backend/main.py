from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from config.config import get_settings
from config.session import AsyncSessionLocal
from auth.security import hash_password, verify_password, create_access_token, decode_access_token
from models import AppUser, Project, Problem, Solution, Video, Submission

settings = get_settings()

API_PREFIX = settings.API_PREFIX
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/login")

app = FastAPI(title="D33tcode", debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> AppUser:

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
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    username = form_data.username
    password = form_data.password

    result = await db.execute(select(AppUser).where(AppUser.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token({"sub": str(user.id), "role": user.role})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        role=user.role,
    )

# get user endpoint

@app.get(f"{API_PREFIX}/users/me", response_model=UserRead)
async def get_me(current_user: AppUser = Depends(get_current_user)):
    return current_user


# admin user actions: list all and create user

@app.get(f"{API_PREFIX}/users", response_model=List[UserRead])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(require_admin),
):
    result = await db.execute(select(AppUser))
    return result.scalars().all()


@app.post(f"{API_PREFIX}/users", response_model=UserRead)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(require_admin),
):
    user = AppUser(
        username=data.username,
        email_address=data.email_address,
        password=hash_password(data.password),
        role=data.role,
        update_password=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# CRUD for PROJECT table. This is our basic crud for the frontend

@app.get(f"{API_PREFIX}/projects", response_model=List[ProjectOut])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    result = await db.execute(select(Project))
    return result.scalars().all()


@app.get(f"{API_PREFIX}/projects/{{project_id}}", response_model=ProjectOut)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    proj = result.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@app.post(f"{API_PREFIX}/projects", response_model=ProjectOut)
async def create_project(
    data: ProjectIn,
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(require_admin),
):
    proj = Project(**data.model_dump())
    db.add(proj)
    await db.commit()
    await db.refresh(proj)
    return proj


@app.put(f"{API_PREFIX}/projects/{{project_id}}", response_model=ProjectOut)
async def update_project(
    project_id: int,
    data: ProjectIn,
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(require_admin),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    proj = result.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(proj, k, v)

    await db.commit()
    await db.refresh(proj)
    return proj


@app.delete(f"{API_PREFIX}/projects/{{project_id}}", status_code=204)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(require_admin),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    proj = result.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(proj)
    await db.commit()
    return

# the rest of these tables are read only for this example app

@app.get(f"{API_PREFIX}/problems", response_model=List[ProblemOut])
async def list_problems(
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    result = await db.execute(select(Problem))
    return result.scalars().all()


@app.get(f"{API_PREFIX}/solutions", response_model=List[SolutionOut])
async def list_solutions(
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    result = await db.execute(select(Solution))
    return result.scalars().all()


@app.get(f"{API_PREFIX}/videos", response_model=List[VideoOut])
async def list_videos(
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    result = await db.execute(select(Video))
    return result.scalars().all()


@app.get(f"{API_PREFIX}/submissions", response_model=List[SubmissionOut])
async def list_submissions(
    db: AsyncSession = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    result = await db.execute(select(Submission))
    return result.scalars().all()

