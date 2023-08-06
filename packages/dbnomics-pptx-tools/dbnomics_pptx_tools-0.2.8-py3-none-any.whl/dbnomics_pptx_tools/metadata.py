from collections import Counter, defaultdict
from enum import Enum
from typing import Callable, Iterator, Literal, TypeAlias

import daiquiri
import isodate
import pandas as pd
from isodate import Duration
from pydantic import BaseModel, Field, StrictStr, validator

from dbnomics_pptx_tools.module_utils import parse_callable

__all__ = ["DataLabelPosition", "PresentationMetadata", "SlideMetadata"]


logger = daiquiri.getLogger(__name__)


class DataLabelPosition(Enum):
    LAST_POINT = "last_point"


ChartName: TypeAlias = str
DataLabelType: TypeAlias = Literal["last_point"]
Frequency: TypeAlias = Literal["annual", "monthly", "quarterly"]
SeriesId: TypeAlias = str
SeriesTransformer: TypeAlias = Callable[["SeriesSpec", pd.Series], pd.Series]
TableLocation: TypeAlias = str


class SeriesSpec(BaseModel):
    id: str
    name: str
    tag: str | None = None
    transformers: list[SeriesTransformer] = Field(default_factory=list)

    @validator("transformers", pre=True, each_item=True)
    def parse_transformers(cls, value: str):
        if not isinstance(value, str):
            raise ValueError(f"str expected, got {type(value)}")
        function = parse_callable(value)
        if function is None:
            raise ValueError(f"The function referenced by {value!r} does not exist")
        return function

    def apply_transformers(self, series: pd.Series, *, series_id: str) -> pd.Series:
        for transformer in self.transformers:
            logger.debug("Applying transformer %r to series %r", transformer.__qualname__, series_id)
            series = transformer(self, series)
        return series

    def has_tag(self, tag: str | None) -> bool:
        return tag == self.tag


class ShapeSpec(BaseModel):
    series: list[SeriesSpec]

    def find_series_id_by_name(self, series_name: str, *, tag: str | None = None) -> str | None:
        """Find series ID by its name.

        When tag is None, return the series without a tag (and not any tag).
        """
        for series_spec in self.series:
            if series_spec.name == series_name and series_spec.has_tag(tag):
                return series_spec.id
        return None

    def find_series_spec(self, series_id: str) -> SeriesSpec | None:
        for series_spec in self.series:
            if series_spec.id == series_id:
                return series_spec
        return None

    def get_series_ids(self) -> list[str]:
        return [series_id_or_spec.id for series_id_or_spec in self.series]

    @validator("series")
    def validate_series_name_is_unique(cls, value: list[SeriesSpec]):
        names_by_tag = defaultdict(list)
        for series_spec in value:
            names_by_tag[series_spec.tag].append(series_spec.name)
        for tag, names in names_by_tag.items():
            counts = Counter(names)
            duplicates = {name for name, count in counts.items() if count > 1}
            if duplicates:
                message = f"Series names must be unique, found those duplicates: {sorted(duplicates)!r}"
                if tag is not None:
                    message += f" (for tag {tag})"
                raise ValueError(message)
        return value


class DataLabelSpec(BaseModel):
    type: DataLabelType
    number_format: StrictStr = "0.0"


class ChartSpec(ShapeSpec):
    data_labels: list[DataLabelType | DataLabelSpec] = Field(default_factory=list)

    def iter_data_label_specs(self) -> Iterator[DataLabelSpec]:
        for data_label in self.data_labels:
            if isinstance(data_label, str):
                yield DataLabelSpec(type=data_label)
            else:
                yield data_label


class ColumnsSpec(BaseModel):
    end_period_offset: Duration | None
    frequency: Frequency
    period_format: str

    class Config:
        arbitrary_types_allowed = True

    @validator("end_period_offset", pre=True)
    def parse_end_period_offset(cls, value: str):
        if not isinstance(value, str):
            raise ValueError(f"str expected, got {type(value)}")
        return isodate.parse_duration(value)


class TableSpec(ShapeSpec):
    columns: ColumnsSpec | None
    header_first_cell: str = "Country"


class SlideMetadata(BaseModel):
    charts: dict[ChartName, ChartSpec] = Field(default_factory=dict)
    tables: dict[TableLocation, TableSpec] = Field(default_factory=dict)

    def get_series_ids(self) -> set[str]:
        series_ids = set()
        for chart_spec in self.charts.values():
            series_ids |= set(chart_spec.get_series_ids())
        for table_spec in self.tables.values():
            series_ids |= set(table_spec.get_series_ids())
        return series_ids


class PresentationMetadata(BaseModel):
    slides: dict[str, SlideMetadata]

    def get_slide_series_ids(self) -> set[str]:
        result = set()
        for slide in self.slides.values():
            result |= slide.get_series_ids()
        return result
