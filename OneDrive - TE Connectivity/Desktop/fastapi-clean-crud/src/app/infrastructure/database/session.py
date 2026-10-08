from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = URL.create(
    "mssql+aioodbc",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "server": "MATM1NBO6C9J433",
        "database": "fastapi_crud",
        "trusted_connection": "yes",
        "TrustServerCertificate": "yes",
    },
)

ALEMBIC_DATABASE_URL = URL.create(
"mssql+pyodbc",
query={
"driver": "ODBC Driver 18 for SQL Server",
"server": "MATM1NBO6C9J433",
"database": "fastapi_crud",
"trusted_connection": "yes",
"TrustServerCertificate": "yes",
},
)


engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_reset_on_return=None,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def close_engine() -> None:
    await engine.dispose()