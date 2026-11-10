import pytest

from makler.domain import Apartment, ExchangeRequest


def test_apartment_can_be_created() -> None:
  apartment = Apartment(
    rooms=2,
    area=50,
    floor=5,
    district="Центральный",
  )

  assert apartment.rooms == 2
  assert apartment.area == 50
  assert apartment.floor == 5
  assert apartment.district == "Центральный"


@pytest.mark.parametrize(
  ("field", "value"),
  [
    ("rooms", 0),
    ("area", 0),
    ("floor", 0),
  ],
)
def test_apartment_rejects_invalid_numeric_values(
  field: str,
  value: int,
) -> None:
  values = {
    "rooms": 2,
    "area": 50,
    "floor": 5,
  }
  values[field] = value

  with pytest.raises(ValueError):
    Apartment(**values, district="Центральный")


def test_apartment_rejects_empty_district() -> None:
  with pytest.raises(ValueError):
    Apartment(
      rooms=2,
      area=50,
      floor=5,
      district="   ",
    )


def test_exchange_request_contains_two_apartments() -> None:
  desired = Apartment(
    rooms=3,
    area=70,
    floor=5,
    district="Центральный",
  )

  offered = Apartment(
    rooms=2,
    area=50,
    floor=3,
    district="Советский",
  )

  request = ExchangeRequest(
    desired=desired,
    offered=offered,
  )

  assert request.desired == desired
  assert request.offered == offered