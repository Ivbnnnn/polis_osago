from datetime import datetime, timezone, date

from sqlalchemy import DateTime, DECIMAL, Integer, String, CheckConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Vehicle(Base):
    __tablename__ = "vehicles"
    __table_args__ = (
        
        CheckConstraint(
            """
            NULLIF(vin, '') IS NOT NULL
            OR NULLIF(body_number, '') IS NOT NULL
            OR NULLIF(chassis_number, '') IS NOT NULL
            """,
            name="ck_vehicle_has_identifier",
        ),
        {"schema": "info_api"},
        )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False) # 1=легковое 2 = грузовое
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)  
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    license_plate: Mapped[str] = mapped_column(String, nullable=False)
    vin: Mapped[str] = mapped_column(String, nullable=True)
    body_number: Mapped[str] = mapped_column(String, nullable=True)
    chassis_number: Mapped[str] = mapped_column(String, nullable=True)
    power_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose: Mapped[str] = mapped_column(String(255), nullable=False)
    use_trailer: Mapped[bool] = mapped_column(Boolean, nullable=False)

    sts_documents: Mapped[list["STS"]] = relationship(
        "STS",
        back_populates="vehicle",
        cascade="all, delete-orphan",
    )