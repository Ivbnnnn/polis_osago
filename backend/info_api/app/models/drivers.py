from datetime import datetime, timezone, date

from sqlalchemy import Numeric, ForeignKey, Integer, String, Boolean, Date, false
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Driver(Base):
    __tablename__ = "drivers"
    __table_args__ = {"schema": "info_api"}
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lastname: Mapped[str] = mapped_column(String(255), nullable=False)
    firstname: Mapped[str] = mapped_column(String(255), nullable=False)
    middlename: Mapped[str] = mapped_column(String(255), nullable=True)
    birthdate: Mapped[date] = mapped_column(Date, nullable=False)
    license_serial: Mapped[str] = mapped_column(String(20), nullable=False)
    license_number: Mapped[str] = mapped_column(String(20), nullable=False)
    license_issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    license_exp_date: Mapped[date] = mapped_column(Date, nullable=False)
    licence_foreign: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    kbm: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    # created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)