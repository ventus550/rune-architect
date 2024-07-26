import pandas
from .schema import *

@check_types
def sparse_rune_sets(runes: DataFrame[Runes]) -> DataFrame[SparseRunes]:
	return pandas.concat([runes, pandas.get_dummies(runes.set, dtype=bool)], axis=1)

@check_types
def filter_equipped(runes: DataFrame[Runes], monsters: DataFrame[Monsters], monster_name: str) -> DataFrame[Runes]:
	selected_monster_id = monsters[monsters.name == monster_name].index
	return runes[runes.monster.isin([0, *selected_monster_id])]

@check_types
def named_monsters_runes_view(runes: DataFrame[Runes], monsters: DataFrame[Monsters]) -> DataFrame[NamedMonsterRunes]:
	view = runes.merge(monsters["name"], left_on="monster", right_index=True, how="left")
	return view.drop(columns=["monster"]).rename(columns={"name": "monster"}).sort_values("slot")
