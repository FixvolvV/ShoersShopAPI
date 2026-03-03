from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from shoersshopapi.core.settings import settings

class Database:
    def __init__(
        self,
        url,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 50,
        max_overflow: int = 10,
        ):
        
        # Создание движка
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

        # Создание генератора сессий (асинхронного)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
    
    async def GetSession(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def Dispose(self) -> None:
        await self.engine.dispose()


database = Database(
    str(settings.db.url),
    settings.db.echo,
    settings.db.echo_pool,
    settings.db.pool_size,
    settings.db.max_overflow
)
