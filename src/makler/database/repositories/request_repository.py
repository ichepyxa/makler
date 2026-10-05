from sqlalchemy import select
from sqlalchemy.orm import Session

from makler.database.models import (
  ApartmentModel,
  DistrictModel,
  ExchangeRequestModel,
)
from makler.domain import Apartment, ExchangeRequest


class RequestRepository:
  def __init__(self, session: Session) -> None:
    self.session = session

  def add(self, request: ExchangeRequest) -> ExchangeRequestModel:
    desired_district = self._get_or_create_district(
      request.desired.district,
    )
    offered_district = self._get_or_create_district(
      request.offered.district,
    )

    desired_apartment = ApartmentModel(
      rooms=request.desired.rooms,
      area=request.desired.area,
      floor=request.desired.floor,
      district=desired_district,
    )

    offered_apartment = ApartmentModel(
      rooms=request.offered.rooms,
      area=request.offered.area,
      floor=request.offered.floor,
      district=offered_district,
    )

    model = ExchangeRequestModel(
      desired_apartment=desired_apartment,
      offered_apartment=offered_apartment,
    )

    self.session.add(model)
    self.session.flush()

    return model

  def get_all(self) -> list[ExchangeRequest]:
    statement = select(ExchangeRequestModel).order_by(
      ExchangeRequestModel.created_at,
      ExchangeRequestModel.id,
    )

    models = list(self.session.scalars(statement))

    return [
      self._to_domain(model)
      for model in models
    ]

  def get_by_id(self, request_id: int) -> ExchangeRequest | None:
    model = self.session.get(
      ExchangeRequestModel,
      request_id,
    )

    if model is None:
      return None

    return self._to_domain(model)

  def delete(self, request_id: int) -> bool:
    model = self.session.get(
      ExchangeRequestModel,
      request_id,
    )

    if model is None:
      return False

    self.session.delete(model)
    self.session.flush()

    return True

  def _get_or_create_district(self, name: str) -> DistrictModel:
    normalized_name = name.strip()

    statement = select(DistrictModel).where(
      DistrictModel.name == normalized_name,
    )
    district = self.session.scalar(statement)

    if district is not None:
      return district

    district = DistrictModel(name=normalized_name)
    self.session.add(district)
    self.session.flush()

    return district

  @staticmethod
  def _to_domain(
      model: ExchangeRequestModel,
  ) -> ExchangeRequest:
    return ExchangeRequest(
      desired=Apartment(
        rooms=model.desired_apartment.rooms,
        area=model.desired_apartment.area,
        floor=model.desired_apartment.floor,
        district=model.desired_apartment.district.name,
      ),
      offered=Apartment(
        rooms=model.offered_apartment.rooms,
        area=model.offered_apartment.area,
        floor=model.offered_apartment.floor,
        district=model.offered_apartment.district.name,
      ),
    )