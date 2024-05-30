from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models.models import Base

engine = create_async_engine(
    "sqlite+aiosqlite:///OSport.db", connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(engine)


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

