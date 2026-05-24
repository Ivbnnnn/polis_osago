from datetime import datetime, timezone, date

from sqlalchemy import Numeric, Integer, String, Boolean, DATE, Float
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class InsuranceCompany(Base):
    __tablename__ = "insurance_companies"
    __table_args__ = {"schema": "info_api"}
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    commission_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    koef: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    # created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)