from sqlalchemy.orm import Session

from makler.database.models import (
  ExchangeModel,
  ExchangeSnapshotModel,
)
from makler.domain import Exchange


class ExchangeRepository:
  def __init__(self, session: Session) -> None:
    self.session = session

  def save(self, exchange: Exchange) -> ExchangeModel:
    model = ExchangeModel()

    first_snapshot = self._create_snapshot(
      request_side=1,
      request=exchange.first_request,
    )

    second_snapshot = self._create_snapshot(
      request_side=2,
      request=exchange.second_request,
    )

    model.snapshots.extend(
      [
        first_snapshot,
        second_snapshot,
      ]
    )

    self.session.add(model)
    self.session.flush()

    return model

  @staticmethod
  def _create_snapshot(
    request_side: int,
    request,
  ) -> ExchangeSnapshotModel:
    return ExchangeSnapshotModel(
      request_side=request_side,
      desired_rooms=request.desired.rooms,
      desired_area=request.desired.area,
      desired_floor=request.desired.floor,
      desired_district=request.desired.district,
      offered_rooms=request.offered.rooms,
      offered_area=request.offered.area,
      offered_floor=request.offered.floor,
      offered_district=request.offered.district,
    )