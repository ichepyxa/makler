from pathlib import Path

from makler.database.database import Database
from makler.database.models import ExchangeModel
from makler.database.repositories import RequestRepository
from makler.domain import Apartment, ExchangeRequest
from makler.services.request_service import RequestService


def create_database(path: Path) -> Database:
  database = Database(path)
  database.create_tables()
  return database


def create_request(
  desired_rooms: int,
  desired_area: float,
  desired_floor: int,
  offered_rooms: int,
  offered_area: float,
  offered_floor: int,
) -> ExchangeRequest:
  return ExchangeRequest(
    desired=Apartment(
      rooms=desired_rooms,
      area=desired_area,
      floor=desired_floor,
      district="Центральный",
    ),
    offered=Apartment(
      rooms=offered_rooms,
      area=offered_area,
      floor=offered_floor,
      district="Советский",
    ),
  )


def test_request_is_added_when_no_match_exists(
  tmp_path: Path,
) -> None:
  database = create_database(tmp_path / "test.sqlite3")

  with database.session() as session:
    service = RequestService(session)

    request = create_request(
      desired_rooms=3,
      desired_area=70,
      desired_floor=5,
      offered_rooms=2,
      offered_area=50,
      offered_floor=3,
    )

    result = service.add_request(request)

    assert result.exchange is None
    assert result.matched_request is None

  with database.session() as session:
    repository = RequestRepository(session)

    requests = repository.get_all()

    assert requests == [request]


def test_matching_requests_create_exchange_and_remove_both(
  tmp_path: Path,
) -> None:
  database = create_database(tmp_path / "test.sqlite3")

  existing_request = create_request(
    desired_rooms=2,
    desired_area=52,
    desired_floor=3,
    offered_rooms=3,
    offered_area=65,
    offered_floor=5,
  )

  incoming_request = create_request(
    desired_rooms=3,
    desired_area=70,
    desired_floor=5,
    offered_rooms=2,
    offered_area=50,
    offered_floor=3,
  )

  with database.session() as session:
    repository = RequestRepository(session)
    repository.add(existing_request)
    session.commit()

  with database.session() as session:
    service = RequestService(session)

    result = service.add_request(incoming_request)

    assert result.exchange is not None
    assert result.matched_request == existing_request

  with database.session() as session:
    repository = RequestRepository(session)

    assert repository.get_all() == []

    exchanges = session.query(ExchangeModel).all()

    assert len(exchanges) == 1
    assert len(exchanges[0].snapshots) == 2


def test_non_matching_request_remains_in_card_index(
  tmp_path: Path,
) -> None:
  database = create_database(tmp_path / "test.sqlite3")

  existing_request = create_request(
    desired_rooms=2,
    desired_area=52,
    desired_floor=4,
    offered_rooms=3,
    offered_area=65,
    offered_floor=5,
  )

  incoming_request = create_request(
    desired_rooms=3,
    desired_area=70,
    desired_floor=5,
    offered_rooms=2,
    offered_area=50,
    offered_floor=3,
  )

  with database.session() as session:
    repository = RequestRepository(session)
    repository.add(existing_request)
    session.commit()

  with database.session() as session:
    service = RequestService(session)

    result = service.add_request(incoming_request)

    assert result.exchange is None

  with database.session() as session:
    repository = RequestRepository(session)

    requests = repository.get_all()

    assert len(requests) == 2