from makler.domain import Apartment, ExchangeRequest
from makler.services.matching_service import MatchingService


def apartment(
  rooms: int,
  area: float,
  floor: int,
  district: str = "Центральный",
) -> Apartment:
  return Apartment(
    rooms=rooms,
    area=area,
    floor=floor,
    district=district,
  )


def request(
  desired: Apartment,
  offered: Apartment,
) -> ExchangeRequest:
  return ExchangeRequest(desired=desired, offered=offered)


def test_apartments_match_when_rooms_floor_and_area_are_suitable() -> None:
  assert MatchingService.apartments_match(
    apartment(2, 50, 5),
    apartment(2, 54, 5),
  )


def test_apartments_do_not_match_when_rooms_are_different() -> None:
  assert not MatchingService.apartments_match(
    apartment(2, 50, 5),
    apartment(3, 50, 5),
  )


def test_apartments_do_not_match_when_floor_is_different() -> None:
  assert not MatchingService.apartments_match(
    apartment(2, 50, 5),
    apartment(2, 50, 6),
  )


def test_symmetric_area_rule_accepts_values_within_ten_percent() -> None:
  first = apartment(2, 100, 5)
  second = apartment(2, 110.5, 5)

  assert MatchingService.apartments_match(first, second)
  assert MatchingService.apartments_match(second, first)


def test_symmetric_area_rule_rejects_values_above_ten_percent() -> None:
  first = apartment(2, 100, 5)
  second = apartment(2, 111, 5)

  assert not MatchingService.apartments_match(first, second)
  assert not MatchingService.apartments_match(second, first)


def test_symmetric_area_rule_rejects_twenty_percent_difference() -> None:
  first = apartment(2, 100, 5)
  second = apartment(2, 120, 5)

  assert not MatchingService.apartments_match(first, second)
  assert not MatchingService.apartments_match(second, first)


def test_area_difference_is_symmetric_for_values_near_boundary() -> None:
  first = apartment(2, 50, 5)
  second = apartment(2, 55.3, 5)

  assert MatchingService.apartments_match(first, second) is False
  assert MatchingService.apartments_match(second, first) is False


def test_district_does_not_affect_matching() -> None:
  first = apartment(2, 50, 5, "Центральный")
  second = apartment(2, 50, 5, "Советский")

  assert MatchingService.apartments_match(first, second)


def test_exchange_requests_match_in_both_directions() -> None:
  incoming = request(
    desired=apartment(3, 70, 5),
    offered=apartment(2, 50, 3),
  )
  existing = request(
    desired=apartment(2, 52, 3),
    offered=apartment(3, 65, 5),
  )

  assert MatchingService.requests_match(incoming, existing)


def test_exchange_requests_do_not_match_if_second_direction_fails() -> None:
  incoming = request(
    desired=apartment(3, 70, 5),
    offered=apartment(2, 50, 3),
  )
  existing = request(
    desired=apartment(2, 52, 4),
    offered=apartment(3, 65, 5),
  )

  assert not MatchingService.requests_match(incoming, existing)
