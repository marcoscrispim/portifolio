from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
import uvicorn

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Ajuste o URL conforme necessário
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# URL de conexão com o banco de dados PostgreSQL
DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/postgres"

# Criação do motor assíncrono e da sessão
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)

class UserCreate(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        orm_mode = True

@app.get("/users/", response_model=list[UserCreate])
async def get_users():
    async with SessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users

@app.get("/users/{user_id}", response_model=UserCreate)
async def get_user(user_id: int = Path(..., description="The ID of the user to retrieve")):
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int = Path(..., description="The ID of the user to delete")):
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                text("DELETE FROM users WHERE id = :id").bindparams(id=user_id)
            )
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
            await session.commit()
            return {"detail": "User deleted"}

@app.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate):
    async with SessionLocal() as session:
        async with session.begin():
            db_user = User(email=user.email, name=user.name)
            session.add(db_user)
        await session.commit()
        return db_user

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
