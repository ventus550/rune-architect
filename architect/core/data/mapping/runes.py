import pandas

sets = {
    1: "Energy",
    2: "Guard",
    3: "Swift",
    4: "Blade",
    5: "Rage",
    6: "Focus",
    7: "Endure",
    8: "Fatal",
    10: "Despair",
    11: "Vampire",
    13: "Violent",
    14: "Nemesis",
    15: "Will",
    16: "Shield",
    17: "Revenge",
    18: "Destroy",
    19: "Fight",
    20: "Determination",
    21: "Enhance",
    22: "Accuracy",
    23: "Tolerance",
    24: "Seal",
    25: "Intangible",
}

effects = {
    1: "hp",
    2: "hp%",
    3: "atk",
    4: "atk%",
    5: "def",
    6: "def%",
    7: "spd%",
    8: "spd",
    9: "crt",
    10: "crd",
    11: "res",
    12: "acc",
}

synergies = pandas.DataFrame(
    {
        "value": [15, 35, 12, 25, 20, 15, 20, 40, 8, 8, 8, 10, 10],
        "effect": ["hp%", "atk%", "crt", "spd%", "acc", "def%", "res", "crd", "atk%", "def%", "hp%", "acc", "res"],
        "stacked": [True, False, True, False, True, True, True, False, True, True, True, True, True]
    },
    index=["Energy", "Fatal", "Blade", "Swift", "Focus", "Guard", "Endure", "Rage", "Fight", "Determination", "Enhance", "Accuracy", "Tolerance"]
).convert_dtypes()
