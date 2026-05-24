from datetime import datetime, timezone, date

from sqlalchemy import DateTime, Float, Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class STS(Base):
    __tablename__ = "sts"
    __table_args__ = {"schema": "info_api"}
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("info_api.vehicles.id"), nullable=False)
    doc_type: Mapped[int] = mapped_column(Integer, nullable=False) # 0 - ПТС, 1 - СТС, 2 - ЭПТС
    serial: Mapped[str] = mapped_column(String(20), nullable=False)  
    number: Mapped[str] = mapped_column(String(20), nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    # created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="sts_documents",
    )