from dataclasses import dataclass

from makler.domain.exchange_request import ExchangeRequest


@dataclass(frozen=True, slots=True)
class Exchange:
  first_request: ExchangeRequest
  second_request: ExchangeRequest