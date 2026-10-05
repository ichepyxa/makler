from pathlib import Path

from makler.database import Database
from makler.database.repositories import RequestRepository
from makler.domain import Apartment, ExchangeRequest


def create_request() -> ExchangeRequest:
  return ExchangeRequest(
    desired=Apartment(
      rooms=3,
      area=70,
      floor=5,
      district="Центральный",
    ),
    offered=Apartment(
      rooms=2,
      area=50,
      floor=3,
      district="Советский",
    ),
  )


def create_database(path: Path) -> Database:
  database = Database(path)
  database.create_tables()
  return database


def test_request_can_be_saved_and_loaded(tmp_path: Path) -> None:
  database = create_database(tmp_path / "test.sqlite3")

  with database.session() as session:
    repository = RequestRepository(session)

    repository.add(create_request())
    session.commit()

  with database.session() as session:
    repository = RequestRepository(session)

    requests = repository.get_all()

    assert len(requests) == 1
    assert requests[0] == create_request()


def test_request_can_be_loaded_by_id(tmp_path: Path) -> None:
  database = create_database(tmp_path / "test.sqlite3")

  with database.session() as session:
    repository = RequestRepository(session)

    model = repository.add(create_request())
    session.commit()

    request = repository.get_by_id(model.id)

    assert request == create_request()


def test_request_can_be_deleted(tmp_path: Path) -> None:
  database = create_database(tmp_path / "test.sqlite3")

  with database.session() as session:
    repository = RequestRepository(session)

    model = repository.add(create_request())
    session.commit()

    assert repository.delete(model.id)

    session.commit()

    assert repository.get_by_id(model.id) is None

def test_same_district_is_not_duplicated(
  tmp_path: Path,
) -> None:
  database = create_database(tmp_path / "test.sqlite3")

  with database.session() as session:
    repository = RequestRepository(session)

    repository.add(create_request())
    repository.add(create_request())

    session.commit()

    requests = repository.get_all()

    assert len(requests) == 2

    districts = {
        requests[0].desired.district,
        requests[0].offered.district,
    }

    assert districts == {
        "Центральный",
        "Советский",
    }