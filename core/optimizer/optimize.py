from pulp import *
from ..data import transform
from ..data.schema import *
from .model import Formulation


@check_types(with_pydantic=True)
def optimize(
    runes: DataFrame[Runes], weight_min_max: DataFrame[WeightMinMax], sets={}
) -> DataFrame[Runes]:
    sparse_runes = transform.sparse_rune_sets(runes)
    model = Formulation(
        sparse_runes,
        weights=dict(weight_min_max["weight"]),
        min_constraints=dict(weight_min_max["min"].dropna()),
        max_constraints=dict(weight_min_max["max"].dropna()),
        sets=sets,
    )
    solution = model.solve()
    if solution["status"] == LpStatusInfeasible:
        return None
    return runes.loc[
        [
            model.items2runes[var][0]
            for var in solution["variables"]
            if value(var) and var in model.items2runes # value(var) may happen to be none
        ]
    ]
