from pathlib import Path

from makler.database import Database
from makler.database.models import ApartmentModel
from makler.database.repositories import RequestRepository
from makler.domain import Apartment, CITY_DISTRICTS, ExchangeRequest
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
      desired_rooms,
      desired_area,
      desired_floor,
      "Центральный",
    ),
    offered=Apartment(
      offered_rooms,
      offered_area,
      offered_floor,
      "Советский",
    ),
  )


def test_request_is_added_when_no_match_exists(tmp_path: Path) -> None:
  database = create_database(tmp_path / "test.sqlite3")
  request = create_request(3, 70, 5, 2, 50, 3)

  with database.session() as session:
    result = RequestService(session).add_request(request)
    assert result.matched_request_id is None

  with database.session() as session:
    assert RequestRepository(session).get_all() == [request]


def test_matching_request_is_removed_and_reported(tmp_path: Path) -> None:
  database = create_database(tmp_path / "test.sqlite3")
  existing = create_request(2, 52, 3, 3, 65, 5)
  incoming = create_request(3, 70, 5, 2, 50, 3)

  with database.session() as session:
    model = RequestRepository(session).add(existing)
    session.commit()
    existing_id = model.id

  with database.session() as session:
    result = RequestService(session).add_request(incoming)
    assert result.matched_request == existing
    assert result.matched_request_id == existing_id

  with database.session() as session:
    assert RequestRepository(session).get_all() == []
    assert session.query(ApartmentModel).count() == 0


def test_non_matching_request_remains_in_card_index(tmp_path: Path) -> None:
  database = create_database(tmp_path / "test.sqlite3")
  existing = create_request(2, 52, 4, 3, 65, 5)
  incoming = create_request(3, 70, 5, 2, 50, 3)

  with database.session() as session:
    RequestRepository(session).add(existing)
    session.commit()

  with database.session() as session:
    result = RequestService(session).add_request(incoming)
    assert result.matched_request_id is None

  with database.session() as session:
    assert RequestRepository(session).get_all() == [existing, incoming]


def test_service_can_updateselect_pageed_request(tmp_path: Path) -> None:
  database = create_database(tmp_path / "test.sqlite3")
  original = create_request(2, 50, 3, 3, 70, 5)
  updated = create_request(1, 38.5, 2, 4, 105, 8)

  with database.session() as session:
    model = RequestRepository(session).add(original)
    session.commit()
    request_id = model.id

  with database.session() as session:
    assert RequestService(session).update_request(request_id, updated)

  with database.session() as session:
    assert RequestRepository(session).get_by_id(request_id) == updated


def test_service_can_deleteselect_pageed_request(tmp_path: Path) -> None:
  database = create_database(tmp_path / "test.sqlite3")
  original = create_request(2, 50, 3, 3, 70, 5)

  with database.session() as session:
    model = RequestRepository(session).add(original)
    session.commit()
    request_id = model.id

  with database.session() as session:
    assert RequestService(session).delete_request(request_id)

  with database.session() as session:
    assert RequestRepository(session).get_all() == []


def test_service_returns_four_typed_card_index_lists(tmp_path: Path) -> None:
  database = create_database(tmp_path / "test.sqlite3")
  request = create_request(2, 50, 3, 3, 70, 5)

  with database.session() as session:
    RequestRepository(session).add(request)
    session.commit()

  with database.session() as session:
    card_index = RequestService(session).get_card_index()

  assert card_index.requests == [request]
  assert card_index.desired_apartments == [request.desired]
  assert card_index.offered_apartments == [request.offered]
  assert card_index.districts == list(CITY_DISTRICTS)
