from decimal import Decimal

from makler.domain import Apartment, ExchangeRequest

AREA_TOLERANCE = Decimal("0.10")


class MatchingService:
    @staticmethod
    def apartments_match(first: Apartment, second: Apartment) -> bool:
        if first.rooms != second.rooms:
            return False

        if first.floor != second.floor:
            return False

        first_area = Decimal(str(first.area))
        second_area = Decimal(str(second.area))
        average_area = (first_area + second_area) / Decimal(2)
        area_difference = abs(first_area - second_area)

        return area_difference <= average_area * AREA_TOLERANCE

    @classmethod
    def requests_match(
        cls,
        incoming: ExchangeRequest,
        existing: ExchangeRequest,
    ) -> bool:
        return (
            cls.apartments_match(incoming.desired, existing.offered)
            and cls.apartments_match(incoming.offered, existing.desired)
        )
