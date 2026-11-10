from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from makler.database.models import ExchangeModel, ExchangeSnapshotModel
from makler.domain import Apartment, Exchange, ExchangeRequest


@dataclass(frozen=True, slots=True)
class StoredExchange:
    id: int
    created_at: datetime
    exchange: Exchange


class HistoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[StoredExchange]:
        statement = (
            select(ExchangeModel)
            .options(selectinload(ExchangeModel.snapshots))
            .order_by(ExchangeModel.created_at.desc(), ExchangeModel.id.desc())
        )
        exchanges = self.session.scalars(statement).all()
        return [self._to_stored_exchange(model) for model in exchanges]

    @classmethod
    def _to_stored_exchange(cls, model: ExchangeModel) -> StoredExchange:
        snapshots = sorted(model.snapshots, key=lambda item: item.request_side)
        if len(snapshots) != 2:
            raise ValueError(
                f"У обмена № {model.id} должно быть две записи истории."
            )

        return StoredExchange(
            id=model.id,
            created_at=model.created_at,
            exchange=Exchange(
                first_request=cls._to_request(snapshots[0]),
                second_request=cls._to_request(snapshots[1]),
            ),
        )

    @staticmethod
    def _to_request(snapshot: ExchangeSnapshotModel) -> ExchangeRequest:
        return ExchangeRequest(
            desired=Apartment(
                rooms=snapshot.desired_rooms,
                area=snapshot.desired_area,
                floor=snapshot.desired_floor,
                district=snapshot.desired_district,
            ),
            offered=Apartment(
                rooms=snapshot.offered_rooms,
                area=snapshot.offered_area,
                floor=snapshot.offered_floor,
                district=snapshot.offered_district,
            ),
        )
