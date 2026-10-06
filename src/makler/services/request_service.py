from dataclasses import dataclass

from sqlalchemy.orm import Session

from makler.database.repositories import (
  RequestRepository,
)
from makler.domain import Exchange, ExchangeRequest
from makler.services.exchange_service import ExchangeService
from makler.services.matching_service import MatchingService


@dataclass(frozen=True, slots=True)
class RequestProcessingResult:
  request: ExchangeRequest
  exchange: Exchange | None
  matched_request: ExchangeRequest | None


class RequestService:
  def __init__(self, session: Session) -> None:
    self.session = session
    self.request_repository = RequestRepository(session)
    self.exchange_service = ExchangeService(session)

  def add_request(
    self,
    request: ExchangeRequest,
  ) -> RequestProcessingResult:
    with self.session.begin():
      existing_requests = (
        self.request_repository.get_all_with_ids()
      )

      for existing in existing_requests:
        if MatchingService.requests_match(
          request,
          existing.request,
        ):
          exchange = self.exchange_service.complete_exchange(
            request,
            existing,
          )

          return RequestProcessingResult(
            request=request,
            exchange=exchange,
            matched_request=existing.request,
          )

      self.request_repository.add(request)

      return RequestProcessingResult(
        request=request,
        exchange=None,
        matched_request=None,
      )