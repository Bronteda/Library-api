from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

#Engine is the connection pool. Created once at startup.
engine = create_engine(
    settings.database_url,
    echo=settings.sql_echo,# allows for every sql statement used to be printed
    connect_args=connect_args,
)

def create_db_and_tables() -> None:
    """Create any tables that don't exist yet."""
    SQLModel.metadata.create_all(engine)

#Session is a connection that you can start , read and write and close at the end.
def get_session() -> Generator[Session, None, None]:
    """Yield a database session, guaranteed to close afterwards."""
    with Session(engine) as session:
        yield session

# A reusable type alias so endpoints stay readable.
SessionDep = Annotated[Session, Depends(get_session)]

