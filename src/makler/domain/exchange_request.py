from dataclasses import dataclass

from makler.domain.apartment import Apartment


@dataclass(frozen=True, slots=True)
class ExchangeRequest:
  desired: Apartment
  offered: Apartment