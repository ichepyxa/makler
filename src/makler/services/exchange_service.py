from sqlalchemy.orm import Session

from makler.database.repositories import (
  ExchangeRepository,
  RequestRepository,
  StoredRequest,
)
from makler.domain import Exchange, ExchangeRequest


class ExchangeService:
  def __init__(self, session: Session) -> None:
    self.request_repository = RequestRepository(session)
    self.exchange_repository = ExchangeRepository(session)

  def complete_exchange(
    self,
    incoming: ExchangeRequest,
    existing: StoredRequest,
  ) -> Exchange:
    exchange = Exchange(
      first_request=incoming,
      second_request=existing.request,
    )

    self.exchange_repository.save(exchange)
    self.request_repository.delete(existing.id)

    return exchange