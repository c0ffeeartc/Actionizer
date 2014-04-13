__author__ = 'cfe'
builtinConditions = [
    {
        "type_name": "condition",
        "uid": "hasActiveDocument",
        "stepA": None,
        "stepB": None,
        "a": [
            1,  # quantity
            ["hasActiveDocument"],  # values
            ["noname"],  # names
            ["step"],  # type_names
        ],
        "op": "eq",
        "b": [
            1,  # quantity
            ["True"],  # values
            ["b"],  # names
            ["bool"],  # type_names
        ],
    },
]
