from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import Row
from sqlmodel import SQLModel
from sqlmodel.main import IncEx


def row_dump(row: Row, convert_datetime=True) -> dict[str, Any]:
    if convert_datetime:
        return {k: v.timestamp() if isinstance(v, datetime) else v for k, v in row._asdict().items()}
    return row._asdict()


def rows_dump(rows: Sequence[Row], convert_datetime=True) -> list[dict[str, Any]]:
    if convert_datetime:
        return [{k: v.timestamp() if isinstance(v, datetime) else v for k, v in row._asdict().items()} for row in rows]
    return [row._asdict() for row in rows]


def model_dump(
    model: SQLModel,
    include: IncEx = None,
    exclude: IncEx = None,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    convert_datetime=True
) -> dict[str, Any]:
    dumped = model.model_dump(include=include, exclude=exclude, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)
    if convert_datetime:
        return {k: v.timestamp() if isinstance(v, datetime) else v for k, v in dumped.items()}
    return dumped


def models_dump(
    models: Sequence[SQLModel],
    include: IncEx = None,
    exclude: IncEx = None,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    convert_datetime=True
) -> list[dict[str, Any]]:
    result = [model.model_dump(include=include, exclude=exclude, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none) for model in models]
    if convert_datetime:
        return [
            {
                k: v.timestamp() if isinstance(v, datetime) else v
                for k, v in model.items()
            }
            for model in result
        ]
    return result
