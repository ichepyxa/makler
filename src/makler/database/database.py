from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from makler.database.models import Base

DEFAULT_DATABASE_PATH = (
  Path.home() / ".makler" / "makler.sqlite3"
)


class Database:
  def __init__(self, database_path: Path | None = None) -> None:
    self.database_path = database_path or DEFAULT_DATABASE_PATH

    self.database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    self.engine = create_engine(
        f"sqlite:///{self.database_path}",
    )

    self.session_factory = sessionmaker(
        bind=self.engine,
        expire_on_commit=False,
    )

  def create_tables(self) -> None:
    Base.metadata.create_all(self.engine)

  def session(self) -> Session:
    return self.session_factory()