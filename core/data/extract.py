import pandas
import numpy as np
import json as js
from . import mapping
from .schema import *


def json(filename: str):
    return js.load(open(filename, "r", encoding="utf-8"))


def rune2vec(rune):
    try:
        eff_prefix = rune["prefix_eff"]
        eff_primary = rune["pri_eff"]
        eff_secondary = rune["sec_eff"]

        rune_vector = np.zeros(13)

        rune_vector[eff_prefix[0]] += eff_prefix[1]
        rune_vector[eff_primary[0]] += eff_primary[1]

        prop, val, *_ = np.array(eff_secondary).T
        rune_vector[prop] += val
    except:
        return 0
    return rune_vector


def rune2series(rune):
    labels = [
        mapping.runes.effects.get(i, "empty") for i in range(13)
    ]  # account for 0 and 7 unused indices
    return pandas.Series(rune2vec(rune), index=labels, dtype=int)


def gather_runes_data(data: dict) -> DataFrame:
    return pandas.DataFrame(
        [rune for unit in data["unit_list"] for rune in unit["runes"]] + data["runes"]
    )


def runes(data: dict) -> DataFrame[Runes]:
    renamed_columns = {
        "rune_id": "id",
        "occupied_id": "monster",
        "slot_no": "slot",
        "set_id": "set",
    }
    dropped_columns = [
        "empty",
        "wizard_id",
        "occupied_type",
        "rank",
        "class",
        "upgrade_limit",
        "upgrade_curr",
        "extra",
        "base_value",
        "sell_value",
    ]
    runes = gather_runes_data(data)
    runes["set_id"] = runes.set_id.map(mapping.runes.sets)
    runevec_columns = pandas.DataFrame(
        {col: runes.pop(col) for col in ["sec_eff", "prefix_eff", "pri_eff"]}
    ).apply(rune2series, axis=1)
    return (
        pandas.concat([runes, runevec_columns], axis=1)
        .dropna()
        .drop(columns=dropped_columns)
        .rename(columns=renamed_columns)
        .set_index("id", verify_integrity=True)
    )


def monsters(data: dict) -> DataFrame[Monsters]:
    renamed_columns = {
        "unit_id": "id",
        "resist": "res",
        "accuracy": "acc",
        "critical_rate": "crt",
        "critical_damage": "crd",
        "con": "hp",
    }
    dropped_columns = [
        "wizard_id",
        "island_id",
        "pos_x",
        "pos_y",
        "building_id",
        "unit_master_id",
        "unit_level",
        "experience",
        "exp_gained",
        "exp_gain_rate",
        "costume_master_id",
        "trans_items",
        "runes",
        "unit_index",
        "artifacts",
        "awakening_info",
    ]
    monsters = pandas.DataFrame(data["unit_list"])
    monsters["name"] = monsters.unit_master_id.map(mapping.monsters.names)
    monsters.con *= 15  # change of units!
    return (
        monsters.rename(columns=renamed_columns)
        .drop(columns=dropped_columns)
        .set_index("id", verify_integrity=True)
    )
