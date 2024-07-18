import json
import pandas

import numpy as np

def rune2vec(rune):
    try:
        eff_prefix = rune["prefix_eff"]
        eff_primary = rune["pri_eff"]
        eff_secondary = rune["sec_eff"]

        rune_vector = np.zeros(13)

        rune_vector[eff_prefix[0]] += eff_prefix[1]
        rune_vector[eff_primary[0]] += eff_primary[1]

        prop, val, *rest = np.array(eff_secondary).T
        rune_vector[prop] += val
    except:
        return None
    return rune_vector

def rune2series(rune):
    labels = [
        "empty",
        "hp",
        "hp%",
        "atk",
        "atk%",
        "def",
        "def%",
        "empty",
        "spd",
        "crt",
        "crd",
        "res",
        "acc",
    ]
    return pandas.Series(rune2vec(rune), index=labels, dtype=float)

def extract_runes_data(data: pandas.DataFrame):
    runes_series = pandas.DataFrame({col: data.pop(col) for col in ['sec_eff', 'prefix_eff', 'pri_eff']}).apply(rune2series, axis=1)
    dropped_columns = ["empty", "wizard_id", "occupied_type", "rank", "class", "upgrade_limit", "upgrade_curr", "extra", "base_value", "sell_value"]
    return pandas.concat([data, runes_series], axis=1).dropna().drop(columns=dropped_columns).set_index("rune_id", verify_integrity=True)