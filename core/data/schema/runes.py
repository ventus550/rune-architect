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

class SparseRunes(Runes):
    Energy: Series[bool]
    Guard: Series[bool]
    Swift: Series[bool]
    Blade: Series[bool]
    Rage: Series[bool]
    Focus: Series[bool]
    Endure: Series[bool]
    Fatal: Series[bool]
    Despair: Series[bool]
    Vampire: Series[bool]
    Violent: Series[bool]
    Nemesis: Series[bool]
    Will: Series[bool]
    Shield: Series[bool]
    Revenge: Series[bool]
    Destroy: Series[bool]
    Fight: Series[bool]
    Determination: Series[bool]
    Enhance: Series[bool]
    Accuracy: Series[bool]
    Tolerance: Series[bool]
    Seal: Series[bool]
    Intangible: Series[bool]
