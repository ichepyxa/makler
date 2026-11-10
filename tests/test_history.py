from pathlib import Path

from makler.database.database import Database
from makler.database.repositories import HistoryRepository, RequestRepository
from makler.domain import Apartment, ExchangeRequest
from makler.services.request_service import RequestService


def make_request(
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


def test_exchange_history_remains_after_requests_are_removed(
    tmp_path: Path,
) -> None:
    database = Database(tmp_path / "history.sqlite3")
    database.create_tables()

    old_request = make_request(2, 52, 3, 3, 65, 5)
    incoming_request = make_request(3, 70, 5, 2, 50, 3)

    with database.session() as session:
        RequestRepository(session).add(old_request)
        session.commit()

    with database.session() as session:
        result = RequestService(session).add_request(incoming_request)
        assert result.exchange is not None

    with database.session() as session:
        assert RequestRepository(session).get_all() == []
        history = HistoryRepository(session).get_all()

    assert len(history) == 1
    assert history[0].exchange.first_request == incoming_request
    assert history[0].exchange.second_request == old_request


def test_history_is_empty_before_first_exchange(tmp_path: Path) -> None:
    database = Database(tmp_path / "history.sqlite3")
    database.create_tables()

    with database.session() as session:
        assert HistoryRepository(session).get_all() == []
