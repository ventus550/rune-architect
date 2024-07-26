from pandera.typing import *
from pandera import *
from core.data import mapping

class Runes(DataFrameModel):
    monster: Series[int] = Field(ge=0)
    slot: Series[int] = Field(isin=range(7))
    set: Series[str] = Field(isin=set(mapping.runes.sets.values()))
    hp: Series[int] = Field(ge=0)
    hpq: Series[int] = Field(ge=0, alias="hp%")
    atk: Series[int] = Field(ge=0)
    atkq: Series[int] = Field(ge=0, alias="hp%")
    deff: Series[int] = Field(ge=0, alias="def")
    defq: Series[int] = Field(ge=0, alias="def%")
    spdq: Series[int] = Field(ge=0, alias="spd%")
    spd: Series[int] = Field(ge=0)
    crt: Series[int] = Field(ge=0)
    crd: Series[int] = Field(ge=0)
    res: Series[int] = Field(ge=0)
    acc: Series[int] = Field(ge=0)