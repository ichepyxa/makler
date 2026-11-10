from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Apartment:
  rooms: int
  area: float
  floor: int
  district: str

  def __post_init__(self) -> None:
    if self.rooms <= 0:
      raise ValueError("Количество комнат должно быть больше нуля.")

    if self.area <= 0:
      raise ValueError("Площадь должна быть больше нуля.")

    if self.floor <= 0:
      raise ValueError("Этаж должен быть больше нуля.")

    if not self.district.strip():
      raise ValueError("Район не может быть пустым.")