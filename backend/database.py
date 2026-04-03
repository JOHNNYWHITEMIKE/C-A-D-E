"""
Database engine, session factory, and declarative base for C-A-D-E.
"""
from __future__ import annotations

import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Accept postgresql:// or postgres:// and normalise to postgresql+asyncpg://
_url: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://cade:cade@localhost:5432/cade",
)
if _url.startswith("postgresql://") or _url.startswith("postgres://"):
    _url = _url.replace("://", "+asyncpg://", 1)

DATABASE_URL: str = _url

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:  # type: ignore[misc]
    async with AsyncSessionLocal() as session:
        yield session
