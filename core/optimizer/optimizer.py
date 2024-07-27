from PyQt6.QtCore import QThread, pyqtSignal
from pulp import *
from ..data import transform
from ..data.schema import *
from ..data.mapping.runes import synergies
from .model import Model
import time

class Optimizer(QThread):
	finished = pyqtSignal(object)

	@check_types
	def __init__(
		self,
		func: callable,
		runes: DataFrame[Runes],
		monster: DataFrame[Monsters],
		weight_min_max: DataFrame[WeightMinMax],
		sets={},
	):
		super().__init__()
		assert len(monster) == 1, "multiple monsters received"
		self.runes = runes
		self.monster = monster
		self.weight_min_max = weight_min_max
		self.sets = sets

		self.finished.connect(func)
		self.start()

	def run(self):
		sparse_runes = transform.sparse_rune_sets(self.runes)
		sparse_flat_runes = transform.flatten_runes(sparse_runes, self.monster)
		flat_synergies = transform.flatten_synergies(synergies, self.monster)
		model = Model(
			runes=sparse_flat_runes,
			synergies=flat_synergies,
			weights=dict(self.weight_min_max["weight"]),
			min_constraints=dict(self.weight_min_max["min"].dropna()),
			max_constraints=dict(self.weight_min_max["max"].dropna()),
			sets=self.sets,
		)
		solution = model.solve()
		if solution["status"] == LpStatusInfeasible:
			return None
		self.finished.emit(self.runes.loc[
			[
				model.items2runes[var][0]
				for var in solution["variables"]
				if value(var) and var in model.items2runes # value(var) may happen to be none
			]
		])


