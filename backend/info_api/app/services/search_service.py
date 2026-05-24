from datetime import date, datetime
from decimal import Decimal
from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import selectinload, InstrumentedAttribute
from app.services.base import BaseService
from app.models import Address, Vehicle, STS, Person, InsuranceCompany, Driver

SearchModel = Address | Vehicle | STS | Person | InsuranceCompany | Driver


class SearchService(BaseService):
    async def query_search(
        self,
        model: type[SearchModel],
        relations: list[InstrumentedAttribute],
        filters: list[Any] | None = None,
    ) -> list[SearchModel]:
        stmt = select(model)

        for relation in relations:
            stmt = stmt.options(selectinload(relation))

        if filters:
            for filter_item in filters:
                column = getattr(model, filter_item.field, None)

                if column is None:
                    raise ValueError(
                        f"Field '{filter_item.field}' not found in model {model.__name__}"
                    )

                converted_value = self._convert_value(
                    column=column,
                    value=filter_item.value,
                )

                stmt = stmt.where(column == converted_value)

        result = await self.uow.session.execute(stmt)
        
        return list(result.scalars().all())
    
    def _convert_value(
        self,
        column: InstrumentedAttribute,
        value: Any,
    ) -> Any:
        python_type = column.property.columns[0].type.python_type

        if value is None:
            return None

        if python_type is str:
            return str(value)

        if python_type is int:
            return int(value)

        if python_type is float:
            return float(value)

        if python_type is bool:
            if isinstance(value, bool):
                return value

            value_str = str(value).strip().lower()

            if value_str in ("true", "1", "yes", "да"):
                return True

            if value_str in ("false", "0", "no", "нет"):
                return False

            raise ValueError(f"Invalid boolean value: {value}")

        if python_type is Decimal:
            return Decimal(str(value))

        if python_type is date:
            if isinstance(value, date):
                return value

            return date.fromisoformat(str(value))

        if python_type is datetime:
            if isinstance(value, datetime):
                return value

            return datetime.fromisoformat(str(value))

        return value