from pulp import *
from ...data.schema import DataFrame, SparseRunes, Synergies
from .formulation import Formulation
from collections import defaultdict


class Model(Formulation):
    def __init__(
        self,
        runes: DataFrame[SparseRunes],
        synergies: DataFrame[Synergies],
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
        self.synergy_accumulator = defaultdict(int)

        # set synergies
        for set, properties in synergies.iterrows():
            if properties.stacked:
                self.constraints += self.multi_synergy_constraint(set, properties.value, properties.effect)
            else:
                self.constraints += self.single_synergy_constraint(set, properties.value, properties.effect)
        
        # slot constraints
        for i in (1, 2, 3, 4, 5, 6):
            slot_item_pairs = zip(runes.slot.values, self.items)
            slot_constraint = lpSum(item for slot, item in slot_item_pairs if slot == i)
            self.constraints += slot_constraint <= 1

        # stat constraints
        for stat, count in min_constraints.items():
            self.constraints += runes[stat] @ self.items + self.synergy_accumulator[stat] >= count

        for stat, count in max_constraints.items():
            self.constraints += runes[stat] @ self.items + self.synergy_accumulator[stat] <= count

        # set constraints
        for set, count in sets.items():
            self.constraints += runes[set] @ self.items >= 2*count

        self.objective += sum(
            sum(
                tuple(weights.values()) * props * item
                for props, item in zip(runes[list(weights.keys())].values, self.items)
            )
        )

    def single_synergy_constraint(
        self, set: str, value: int, property: str
    ) -> LpConstraint:
        var = self.addVar(set)
        synergy = var * value
        self.synergy_accumulator[property] += synergy
        self.objective += synergy * self.weights[property]
        return self.runes[set] @ self.items >= 4 * var

    def multi_synergy_constraint(
        self, set: str, value: int, property: str
    ) -> LpConstraint:
        vars = self.addVar(set, count=3)
        synergy = sum(vars) * value
        self.synergy_accumulator[property] += synergy
        self.objective += synergy * self.weights[property]
        return self.runes[set] @ self.items >= 2 * sum(vars)
