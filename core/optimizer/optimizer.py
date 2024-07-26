from pulp import *
from ..data import transform
from ..data.schema import *

class Model(LpProblem):
    ...
        
@check_types
def optimize(runes: DataFrame[Runes], weights, min_constraints={}, max_constraints={}, sets={}):
    runes = transform.sparse_rune_sets(runes)
    model = LpProblem(sense=LpMaximize)
    objective = 0

    def product(A, B):
        return sum(a * b for a, b in zip(A, B))
    
    def single_synergy_constraint(set, synergy, property):
        nonlocal objective
        var = LpVariable(set, cat=LpBinary)
        objective += var * synergy * weights[property]
        return product(runes[set], items) >= 4*var
    
    def multi_synergy_constraint(set, synergy, property):
        nonlocal objective
        vars = LpVariable.dicts(set, indices=range(3), cat=LpBinary)
        objective += sum(vars.values()) * synergy * weights[property]
        return product(runes[set], items) >= 2*sum(vars.values())


    items = LpVariable.dicts("rune", indices=runes.index, cat=LpBinary).values()


    # slot constraints
    for i in range(1, 7):
        model += (
            sum(item for slot, item in zip(runes.slot.values, items) if slot == i)
            <= 1
        )

    # stat constraints
    for stat, count in min_constraints.items():
        model += sum(stat * item for stat, item in zip(runes[stat], items)) >= count

    for stat, count in max_constraints.items():
        model += sum(stat * item for stat, item in zip(runes[stat], items)) <= count

    # set constraints
    for set, count in sets.items():
        model += (
            sum(set_flag * item for set_flag, item in zip(runes[set], items)) >= count
        )

    # set synergies
    model += multi_synergy_constraint("Energy", 15, "hp%")
    model += single_synergy_constraint("Fatal", 35, "atk%")
    model += multi_synergy_constraint("Blade", 12, "crt")
    model += single_synergy_constraint("Swift", 25, "spd%")
    model += multi_synergy_constraint("Focus", 20, "acc")
    model += multi_synergy_constraint("Guard", 15, "def%")
    model += multi_synergy_constraint("Endure", 20, "res")
    model += single_synergy_constraint("Rage", 40, "crd")
    model += multi_synergy_constraint("Fight", 8, "atk%")
    model += multi_synergy_constraint("Determination", 8, "def%")
    model += multi_synergy_constraint("Enhance", 8, "hp%")
    model += multi_synergy_constraint("Accuracy", 10, "acc")
    model += multi_synergy_constraint("Tolerance", 10, "res")

    model += objective + sum(
        sum(
            tuple(weights.values()) * props * item
            for props, item in zip(runes[list(weights.keys())].values, items)
        )
    )

    return dict(
        status=LpStatus[model.solve(PULP_CBC_CMD(msg=False))],
        objective=value(model.objective),
        solution={int(str(item)[5:]): item.value() for item in items if item.value()},
    )