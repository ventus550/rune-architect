from pandera.typing import *
from pandera import *
from core.data import mapping


class Monsters(DataFrameModel):
    cls: Series[int] = Field(ge=0, alias="class")
    hp: Series[int] = Field(ge=0)
    atk: Series[int] = Field(ge=0)
    deff: Series[int] = Field(ge=0, alias="def")
    spd: Series[int] = Field(ge=0)
    crt: Series[int] = Field(ge=0)
    crd: Series[int] = Field(ge=0)
    res: Series[int] = Field(ge=0)
    acc: Series[int] = Field(ge=0)
    skills: Series[list]
    attribute: Series[int] = Field(isin=range(6))
    create_time: Series[object]
    source: Series[int]
    name: Series[str] = Field(isin=list(mapping.monsters.names.values()), nullable=True)
