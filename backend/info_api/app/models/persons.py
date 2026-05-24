from datetime import datetime, timezone, date

from sqlalchemy import DateTime, DECIMAL, Integer, String, Date, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Person(Base):
    __tablename__ = "persons"
    __table_args__ = {"schema": "info_api"}
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lastname: Mapped[str] = mapped_column(String(255), nullable=False)
    firstname: Mapped[str] = mapped_column(String(255), nullable=False)
    middlename: Mapped[str] = mapped_column(String(255), nullable=False)
    birthdate: Mapped[date] = mapped_column(Date, nullable=False)
    passport_serial:Mapped[str] = mapped_column(String(255), nullable=False)
    passport_number:Mapped[str] = mapped_column(String(255), nullable=False)
    passport_issue_date:Mapped[date] = mapped_column(Date, nullable=False)
    passport_issuer:Mapped[str] = mapped_column(String(255), nullable=False)
    passport_code:Mapped[str] = mapped_column(String(255), nullable=False)
    passport_foreign:Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    phone:Mapped[str] = mapped_column(String(255), nullable=False)
    email:Mapped[str] = mapped_column(String(255), nullable=False)
    # created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="person",
        cascade="all, delete-orphan",
    )