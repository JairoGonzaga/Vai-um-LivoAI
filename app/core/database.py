from app.core.config import get_settings 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=2,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "prepared_statement_cache_size": 0,
        "statement_cache_size": 0,
    }
)

AsyncSessionLocal = async_sessionmaker(
                        bind=engine,
                        expire_on_commit=False,
                        class_=AsyncSession,
                        autoflush=False,
                        autocommit=False
                    )   

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

