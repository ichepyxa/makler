from pathlib import Path

from makler.database import Database
from makler.database.models import ApartmentModel
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
        RequestRepository(session).add(create_request())
        session.commit()

    with database.session() as session:
        requests = RequestRepository(session).get_all()

    assert requests == [create_request()]


def test_request_can_be_loaded_by_id(tmp_path: Path) -> None:
    database = create_database(tmp_path / "test.sqlite3")

    with database.session() as session:
        repository = RequestRepository(session)
        model = repository.add(create_request())
        session.commit()
        request = repository.get_by_id(model.id)

    assert request == create_request()


def test_request_can_be_updated(tmp_path: Path) -> None:
    database = create_database(tmp_path / "test.sqlite3")
    updated_request = ExchangeRequest(
        desired=Apartment(4, 92.5, 7, "Первомайский"),
        offered=Apartment(2, 48.0, 2, "Фрунзенский"),
    )

    with database.session() as session:
        repository = RequestRepository(session)
        model = repository.add(create_request())
        session.commit()
        assert repository.update(model.id, updated_request)
        session.commit()
        saved = repository.get_by_id(model.id)

    assert saved == updated_request


def test_request_can_be_deleted_with_its_apartments(tmp_path: Path) -> None:
    database = create_database(tmp_path / "test.sqlite3")

    with database.session() as session:
        repository = RequestRepository(session)
        model = repository.add(create_request())
        session.commit()
        assert repository.delete(model.id)
        session.commit()
        assert repository.get_all() == []
        assert session.query(ApartmentModel).count() == 0


def test_delete_returns_false_for_unknown_request(tmp_path: Path) -> None:
    database = create_database(tmp_path / "test.sqlite3")

    with database.session() as session:
        assert not RequestRepository(session).delete(999)


def test_same_district_is_not_duplicated(tmp_path: Path) -> None:
    database = create_database(tmp_path / "test.sqlite3")

    with database.session() as session:
        repository = RequestRepository(session)
        repository.add(create_request())
        repository.add(create_request())
        session.commit()
        requests = repository.get_all()
        districts = {
            requests[0].desired.district,
            requests[0].offered.district,
        }

    assert len(requests) == 2
    assert districts == {"Центральный", "Советский"}
