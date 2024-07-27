from pandera import DataFrameModel, Field
from pandera.typing import Series, Index
from .. import mapping


class WeightMinMax(DataFrameModel):
    weight: Series[int] = Field(ge=0)
    min: Series[int] = Field(ge=0, nullable=True)
    max: Series[int] = Field(ge=0, nullable=True)
    id: Index[str] = Field(isin=mapping.runes.effects.values())