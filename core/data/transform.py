import pandas
from .schema import *

@check_types
def sparse_rune_sets(runes: DataFrame[Runes]) -> DataFrame:
	return pandas.concat([runes, pandas.get_dummies(runes.set)], axis=1)