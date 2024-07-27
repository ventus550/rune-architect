import pandas
from .schema import *

@check_types
def get_monsters_by_name(monsters: DataFrame[Monsters], monster_name: str) -> DataFrame[Monsters]:
	return monsters[monsters.name == monster_name]

@check_types
def sparse_rune_sets(runes: DataFrame[Runes]) -> DataFrame[SparseRunes]:
	return pandas.concat([runes, pandas.get_dummies(runes.set, dtype=bool)], axis=1)

@check_types
def filter_equipped(runes: DataFrame[Runes], allowed_monsters: DataFrame[Monsters]) -> DataFrame[Runes]:
	selected_monster_ids = allowed_monsters.index
	return runes[runes.monster.isin([0, *selected_monster_ids])]

@check_types
def named_monster_runes_view(runes: DataFrame[Runes], monsters: DataFrame[Monsters]) -> DataFrame[NamedMonsterRunes]:
	view = runes.merge(monsters["name"], left_on="monster", right_index=True, how="left")
	return view.drop(columns=["monster"]).rename(columns={"name": "monster"}).sort_values("slot")

@check_types
def flatten_runes(runes: DataFrame[Runes], selected_monsters: DataFrame[Monsters]) -> DataFrame[FlatRunes]:
	monster = selected_monsters.iloc[0]
	runes["hp"] += runes["hp%"] * monster["hp"]
	runes["spd"] += runes["spd%"] * monster["spd"]
	runes["def"] += runes["def%"] * monster["def"]
	runes["atk"] += runes["atk%"] * monster["atk"]
	return runes.drop(columns=runes.filter(regex='%$').columns)

