__author__ = 'cfe'
builtinConditions = [
    {
        "type_name": "condition",
        "uid": "hasActiveDocument",
        "step_a": None,
        "step_b": None,
        "a": [
            1,  # quantity
            ["hasActiveDocument"],  # values
            ["step"],  # type_names
            ["noname"],  # names
        ],
        "op": "eq",
        "b": [
            1,  # quantity
            ["True"],  # values
            ["bool"],  # type_names
            ["b"],  # names
        ],
    },
]
