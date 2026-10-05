from sqlalchemy import select
from sqlalchemy.orm import Session

from makler.database.models import DistrictModel


class DistrictRepository:
  def __init__(self, session: Session) -> None:
    self.session = session

  def get_all(self) -> list[DistrictModel]:
    statement = select(DistrictModel).order_by(DistrictModel.name)
    return list(self.session.scalars(statement))

  def get_or_create(self, name: str) -> DistrictModel:
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