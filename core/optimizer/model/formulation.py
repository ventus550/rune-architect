from pulp import *
from ...data.schema import DataFrame, SparseRunes
from .model import Model


class Formulation(Model):
    def __init__(
        self,
        runes: DataFrame[SparseRunes],
        weights,
        min_constraints={},
        max_constraints={},
        sets={},
    ):
        super().__init__()
        self.runes = runes
        self.weights = weights
        self.items = self.addVar("rune", count=len(runes))
        self.items2runes = dict(zip(self.items, self.runes.iterrows()))

        # slot constraints
        for i in (1, 2, 3, 4, 5, 6):
            slot_item_pairs = zip(runes.slot.values, self.items)
            slot_constraint = lpSum(item for slot, item in slot_item_pairs if slot == i)
            self.constraints += slot_constraint <= 1

        # stat constraints
        for stat, count in min_constraints.items():
            self.constraints += runes[stat] @ self.items >= count

        for stat, count in max_constraints.items():
            self.constraints += runes[stat] @ self.items <= count

        # set constraints
        for set, count in sets.items():
            self.constraints += runes[set] @ self.items >= 2*count

        # set synergies
        self.constraints += self.multi_synergy_constraint("Energy", 15, "hp%")
        self.constraints += self.single_synergy_constraint("Fatal", 35, "atk%")
        self.constraints += self.multi_synergy_constraint("Blade", 12, "crt")
        self.constraints += self.single_synergy_constraint("Swift", 25, "spd%")
        self.constraints += self.multi_synergy_constraint("Focus", 20, "acc")
        self.constraints += self.multi_synergy_constraint("Guard", 15, "def%")
        self.constraints += self.multi_synergy_constraint("Endure", 20, "res")
        self.constraints += self.single_synergy_constraint("Rage", 40, "crd")
        self.constraints += self.multi_synergy_constraint("Fight", 8, "atk%")
        self.constraints += self.multi_synergy_constraint("Determination", 8, "def%")
        self.constraints += self.multi_synergy_constraint("Enhance", 8, "hp%")
        self.constraints += self.multi_synergy_constraint("Accuracy", 10, "acc")
        self.constraints += self.multi_synergy_constraint("Tolerance", 10, "res")

        self.objective += sum(
            sum(
                tuple(weights.values()) * props * item
                for props, item in zip(runes[list(weights.keys())].values, self.items)
            )
        )

    def single_synergy_constraint(
        self, set: str, synergy: int, property: str
    ) -> LpConstraint:
        var = self.addVar(set)
        self.objective += var * synergy * self.weights[property]
        return self.runes[set] @ self.items >= 4 * var

    def multi_synergy_constraint(
        self, set: str, synergy: int, property: str
    ) -> LpConstraint:
        vars = self.addVar(set, count=3)
        self.objective += sum(vars) * synergy * self.weights[property]
        return self.runes[set] @ self.items >= 2 * sum(vars)
