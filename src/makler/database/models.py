from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
  pass


class DistrictModel(Base):
  __tablename__ = "districts"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

  apartments: Mapped[list["ApartmentModel"]] = relationship(
    back_populates="district",
  )


class ApartmentModel(Base):
  __tablename__ = "apartments"

  id: Mapped[int] = mapped_column(primary_key=True)
  rooms: Mapped[int] = mapped_column(Integer, nullable=False)
  area: Mapped[float] = mapped_column(Float, nullable=False)
  floor: Mapped[int] = mapped_column(Integer, nullable=False)

  district_id: Mapped[int] = mapped_column(
    ForeignKey("districts.id"),
    nullable=False,
  )

  district: Mapped[DistrictModel] = relationship(
    back_populates="apartments",
  )

  desired_requests: Mapped[list["ExchangeRequestModel"]] = relationship(
    foreign_keys="ExchangeRequestModel.desired_apartment_id",
    back_populates="desired_apartment",
  )

  offered_requests: Mapped[list["ExchangeRequestModel"]] = relationship(
    foreign_keys="ExchangeRequestModel.offered_apartment_id",
    back_populates="offered_apartment",
  )


class ExchangeRequestModel(Base):
  __tablename__ = "exchange_requests"

  id: Mapped[int] = mapped_column(primary_key=True)

  desired_apartment_id: Mapped[int] = mapped_column(
    ForeignKey("apartments.id"),
    nullable=False,
  )

  offered_apartment_id: Mapped[int] = mapped_column(
    ForeignKey("apartments.id"),
    nullable=False,
  )

  created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=lambda: datetime.now(UTC),
    nullable=False,
  )

  desired_apartment: Mapped[ApartmentModel] = relationship(
    foreign_keys=[desired_apartment_id],
    back_populates="desired_requests",
  )

  offered_apartment: Mapped[ApartmentModel] = relationship(
    foreign_keys=[offered_apartment_id],
    back_populates="offered_requests",
  )

class ExchangeModel(Base):
  __tablename__ = "exchanges"

  id: Mapped[int] = mapped_column(primary_key=True)

  created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=lambda: datetime.now(UTC),
    nullable=False,
  )

  snapshots: Mapped[list["ExchangeSnapshotModel"]] = relationship(
    back_populates="exchange",
    cascade="all, delete-orphan",
  )


class ExchangeSnapshotModel(Base):
  __tablename__ = "exchange_snapshots"

  id: Mapped[int] = mapped_column(primary_key=True)

  exchange_id: Mapped[int] = mapped_column(
    ForeignKey("exchanges.id"),
    nullable=False,
  )

  request_side: Mapped[int] = mapped_column(
    Integer,
    nullable=False,
  )

  desired_rooms: Mapped[int] = mapped_column(
    Integer,
    nullable=False,
  )
  desired_area: Mapped[float] = mapped_column(
    Float,
    nullable=False,
  )
  desired_floor: Mapped[int] = mapped_column(
    Integer,
    nullable=False,
  )
  desired_district: Mapped[str] = mapped_column(
    String(100),
    nullable=False,
  )

  offered_rooms: Mapped[int] = mapped_column(
    Integer,
    nullable=False,
  )
  offered_area: Mapped[float] = mapped_column(
    Float,
    nullable=False,
  )
  offered_floor: Mapped[int] = mapped_column(
    Integer,
    nullable=False,
  )
  offered_district: Mapped[str] = mapped_column(
    String(100),
    nullable=False,
  )

  exchange: Mapped[ExchangeModel] = relationship(
    back_populates="snapshots",
  )