from pathlib import Path

from sqlalchemy import Boolean, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .config import DATABASE_URL

if DATABASE_URL.startswith("sqlite") and "///" in DATABASE_URL:
    Path(DATABASE_URL.split("///", 1)[1]).parent.mkdir(parents=True, exist_ok=True)


class Base(DeclarativeBase):
    pass


class LiveItem(Base):
    __tablename__ = "live_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), index=True)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def list_categories(session: AsyncSession) -> list[str]:
    rows = (await session.execute(
        select(LiveItem.category).distinct().order_by(LiveItem.category)
    )).scalars().all()
    return list(rows)


async def get_items(
    session: AsyncSession,
    category: str | None = None,
    featured: bool | None = None,
) -> list[LiveItem]:
    stmt = select(LiveItem).order_by(LiveItem.name)
    if category:
        stmt = stmt.where(LiveItem.category == category)
    if featured is not None:
        stmt = stmt.where(LiveItem.featured == featured)
    return list((await session.execute(stmt.limit(50))).scalars().all())


async def search_items(session: AsyncSession, query: str) -> list[LiveItem]:
    pattern = f"%{query.lower()}%"
    stmt = (
        select(LiveItem)
        .where(
            LiveItem.name.ilike(pattern)
            | LiveItem.description.ilike(pattern)
            | LiveItem.category.ilike(pattern)
        )
        .order_by(LiveItem.featured.desc(), LiveItem.name)
        .limit(20)
    )
    return list((await session.execute(stmt)).scalars().all())


async def seed_demo_data() -> None:
    async with SessionLocal() as session:
        if (await session.execute(select(LiveItem.id).limit(1))).first():
            return

        session.add_all([
            LiveItem(
                name="Live Updates",
                description="A simple listing for live updates and active Telegram content.",
                category="Live",
                featured=True,
            ),
            LiveItem(
                name="News Live",
                description="Live news updates and current information.",
                category="News",
                featured=True,
            ),
            LiveItem(
                name="Sports Live",
                description="Live sports updates and event information.",
                category="Sports",
                featured=False,
            ),
        ])
        await session.commit()
