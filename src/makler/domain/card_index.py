from dataclasses import dataclass

from makler.domain.apartment import Apartment
from makler.domain.exchange_request import ExchangeRequest


@dataclass(frozen=True, slots=True)
class CardIndex:
  requests: list[ExchangeRequest]
  desired_apartments: list[Apartment]
  offered_apartments: list[Apartment]
  districts: list[str]
