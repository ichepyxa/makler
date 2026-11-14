from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from makler.database.models import (
    ApartmentModel,
    DistrictModel,
    ExchangeRequestModel,
)
from makler.domain import Apartment, ExchangeRequest


@dataclass(frozen=True, slots=True)
class StoredRequest:
    id: int
    request: ExchangeRequest
    created_at: datetime


class RequestRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, request: ExchangeRequest) -> ExchangeRequestModel:
        desired_district = self.get_or_create_district(
            request.desired.district
        )
        offered_district = self.get_or_create_district(
            request.offered.district
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
        return [item.request for item in self.get_all_with_ids()]

    def get_all_with_ids(self) -> list[StoredRequest]:
        statement = (
            select(ExchangeRequestModel)
            .order_by(
                ExchangeRequestModel.created_at,
                ExchangeRequestModel.id,
            )
        )
        models = list(self.session.scalars(statement))
        return [
            StoredRequest(
                id=model.id,
                request=self.convert_to_request(model),
                created_at=model.created_at,
            )
            for model in models
        ]

    def get_by_id(self, request_id: int) -> ExchangeRequest | None:
        model = self.session.get(ExchangeRequestModel, request_id)
        return self.convert_to_request(model) if model is not None else None

    def update(
        self,
        request_id: int,
        request: ExchangeRequest,
    ) -> bool:
        model = self.session.get(ExchangeRequestModel, request_id)
        if model is None:
            return False

        desired_district = self.get_or_create_district(
            request.desired.district
        )
        offered_district = self.get_or_create_district(
            request.offered.district
        )

        self.update_apartment_data(model.desired_apartment, request.desired)
        self.update_apartment_data(model.offered_apartment, request.offered)
        model.desired_apartment.district = desired_district
        model.offered_apartment.district = offered_district

        self.session.flush()
        return True

    def delete(self, request_id: int) -> bool:
        model = self.session.get(ExchangeRequestModel, request_id)
        if model is None:
            return False

        apartment_ids = {
            model.desired_apartment_id,
            model.offered_apartment_id,
        }
        self.session.delete(model)
        self.session.flush()

        for apartment_id in apartment_ids:
            reference_count = self.session.scalar(
                select(func.count())
                .select_from(ExchangeRequestModel)
                .where(
                    or_(
                        ExchangeRequestModel.desired_apartment_id == apartment_id,
                        ExchangeRequestModel.offered_apartment_id == apartment_id,
                    )
                )
            )
            if reference_count == 0:
                apartment = self.session.get(ApartmentModel, apartment_id)
                if apartment is not None:
                    self.session.delete(apartment)

        self.session.flush()
        return True

    def get_or_create_district(self, name: str) -> DistrictModel:
        normalized_name = name.strip()
        statement = select(DistrictModel).where(
            DistrictModel.name == normalized_name
        )
        district = self.session.scalar(statement)
        if district is not None:
            return district

        district = DistrictModel(name=normalized_name)
        self.session.add(district)
        self.session.flush()
        return district

    @staticmethod
    def update_apartment_data(
        model: ApartmentModel,
        apartment: Apartment,
    ) -> None:
        model.rooms = apartment.rooms
        model.area = apartment.area
        model.floor = apartment.floor

    @staticmethod
    def convert_to_request(model: ExchangeRequestModel) -> ExchangeRequest:
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
