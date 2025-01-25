from sqlalchemy.ext.asyncio import (AsyncEngine, 
                                   AsyncSession, 
                                   create_async_engine)
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
)
