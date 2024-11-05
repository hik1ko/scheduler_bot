from sqlalchemy import Column, DateTime, BigInteger, VARCHAR, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr, sessionmaker
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Db:
    DB_USER = getenv('DB_USER')
    DB_PORT = getenv('DB_PORT')
    DB_HOST = getenv('DB_HOST')
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_NAME = getenv('DB_NAME')
    URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


TASHKENT_TZ = timezone(timedelta(hours=5))

class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'


class CreatedModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(TASHKENT_TZ))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(TASHKENT_TZ),
                        onupdate=lambda: datetime.now(TASHKENT_TZ))


class User(CreatedModel):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    full_name: Mapped[str] = mapped_column(VARCHAR(500))

    def __repr__(self):
        return self.full_name

class Voice(CreatedModel):
    file_id: Mapped[str] = mapped_column(VARCHAR(255))
    name: Mapped[str] = mapped_column(VARCHAR(255))
    times_used: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return self.name


engine = create_async_engine(Db.URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)