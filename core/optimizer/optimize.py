from pulp import *
from ..data import transform
from ..data.schema import *
from .model import Model


@check_types(with_pydantic=True)
def optimize(
    runes: DataFrame[Runes], monster: DataFrame[Monsters], weight_min_max: DataFrame[WeightMinMax], sets={}
) -> DataFrame[Runes]:
    assert len(monster) == 1, "multiple monsters received"
    sparse_runes = transform.sparse_rune_sets(runes)
    sparse_flat_runes = transform.flatten_runes(sparse_runes, monster)
    model = Model(
        sparse_flat_runes,
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
