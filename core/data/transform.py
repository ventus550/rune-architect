import pandas
from .schema import *

@check_types
def sparse_rune_sets(runes: DataFrame[Runes]) -> DataFrame[SparseRunes]:
	return pandas.concat([runes, pandas.get_dummies(runes.set, dtype=bool)], axis=1)