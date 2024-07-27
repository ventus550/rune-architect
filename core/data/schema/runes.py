from pandera import DataFrameModel, Field
from pandera.typing import Series, Index
from core.data import mapping
from pandas import BooleanDtype



class FlatRunes(DataFrameModel):
    monster: Series[int] = Field(ge=0)
    slot: Series[int] = Field(isin=range(7))
    set: Series[str] = Field(isin=set(mapping.runes.sets.values()))
    hp: Series[int] = Field(ge=0)
    atk: Series[int] = Field(ge=0)
    deff: Series[int] = Field(ge=0, alias="def")
    spd: Series[int] = Field(ge=0)
    crt: Series[int] = Field(ge=0)
    crd: Series[int] = Field(ge=0)
    res: Series[int] = Field(ge=0)
    acc: Series[int] = Field(ge=0)


class Runes(FlatRunes):
    hpq: Series[int] = Field(ge=0, alias="hp%")
    atkq: Series[int] = Field(ge=0, alias="hp%")
    defq: Series[int] = Field(ge=0, alias="def%")
    spdq: Series[int] = Field(ge=0, alias="spd%")


class SparseRunes(FlatRunes):
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


class NamedMonsterRunes(Runes):
    monster: Series[str] = Field(
        isin=set(mapping.monsters.names.values()), nullable=True
    )

class Synergies(DataFrameModel):
    value: Series[int]
    effect: Series[str] = Field(isin=set(mapping.runes.effects.values()))
    stacked: Series[BooleanDtype]
    id: Index[str] = Field(isin=set(mapping.runes.sets.values()))