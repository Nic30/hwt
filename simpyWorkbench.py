from sympy.logic import POSform
from sympy import sympify, to_dnf
minterms = [[0, 0 ], [1, 1] ]
dontcares = []
print(sympify(POSform(['a', 'b'], minterms, dontcares)))


minterms = [[1, 0, 0 ], [1, 1, 1] ]
print(sympify(POSform(['ready', 'pending', 'done'], minterms, dontcares)))