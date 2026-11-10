from makler.domain import Apartment, ExchangeRequest

AREA_TOLERANCE = 0.10


class MatchingService:
  @staticmethod
  def apartments_match(first: Apartment, second: Apartment) -> bool:
    if first.rooms != second.rooms:
      return False

    if first.floor != second.floor:
      return False

    min_area = first.area * (1 - AREA_TOLERANCE)
    max_area = first.area * (1 + AREA_TOLERANCE)

    return min_area <= second.area <= max_area

  @classmethod
  def requests_match(
    cls,
    incoming: ExchangeRequest,
    existing: ExchangeRequest,
  ) -> bool:
    return (
      cls.apartments_match(
        incoming.desired,
        existing.offered,
      )
      and cls.apartments_match(
        incoming.offered,
        existing.desired,
      )
    )