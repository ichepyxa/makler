from dataclasses import dataclass

from sqlalchemy.orm import Session

from makler.database.repositories import RequestRepository, StoredRequest
from makler.domain import (
  CITY_DISTRICTS,
  Apartment,
  CardIndex,
  ExchangeRequest,
)
from makler.services.matching_service import MatchingService


@dataclass(frozen=True, slots=True)
class RequestProcessingResult:
  request: ExchangeRequest
  matched_request: ExchangeRequest | None
  matched_request_id: int | None


class RequestService:
  def __init__(self, session: Session) -> None:
    self.session = session
    self.request_repository = RequestRepository(session)

  def add_request(
    self,
    request: ExchangeRequest,
  ) -> RequestProcessingResult:
    with self.session.begin():
      existing_requests: list[StoredRequest] = (
        self.request_repository.get_all_with_ids()
      )

      for existing in existing_requests:
        if MatchingService.requests_match(
          request,
          existing.request,
        ):
          self.request_repository.delete(existing.id)
          return RequestProcessingResult(
            request=request,
            matched_request=existing.request,
            matched_request_id=existing.id,
          )

      self.request_repository.add(request)
      return RequestProcessingResult(
        request=request,
        matched_request=None,
        matched_request_id=None,
      )

  def update_request(
    self,
    request_id: int,
    request: ExchangeRequest,
  ) -> bool:
    with self.session.begin():
      return self.request_repository.update(request_id, request)

  def delete_request(self, request_id: int) -> bool:
    with self.session.begin():
      return self.request_repository.delete(request_id)

  def get_card_index(self) -> CardIndex:
    requests: list[ExchangeRequest] = self.request_repository.get_all()
    desired_apartments: list[Apartment] = [
      request.desired for request in requests
    ]
    offered_apartments: list[Apartment] = [
      request.offered for request in requests
    ]

    return CardIndex(
      requests=requests,
      desired_apartments=desired_apartments,
      offered_apartments=offered_apartments,
      districts=list(CITY_DISTRICTS),
    )
