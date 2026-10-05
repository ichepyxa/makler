from pathlib import Path

from makler.database import ApartmentModel, Database, DistrictModel


def test_database_creates_tables(tmp_path: Path) -> None:
  database = Database(tmp_path / "test.sqlite3")

  database.create_tables()

  with database.session() as session:
    district = DistrictModel(name="Центральный")

    session.add(district)
    session.commit()

    assert district.id is not None


def test_apartment_can_be_stored(tmp_path: Path) -> None:
  database = Database(tmp_path / "test.sqlite3")

  database.create_tables()

  with database.session() as session:
    district = DistrictModel(name="Центральный")
    session.add(district)
    session.flush()

    apartment = ApartmentModel(
      rooms=2,
      area=50,
      floor=5,
      district_id=district.id,
    )

    session.add(apartment)
    session.commit()

    assert apartment.id is not None