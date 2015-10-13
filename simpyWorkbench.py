from sympy.logic import POSform, And,Or, Xor,  Not
from sympy import to_dnf
from sympy.core.symbol import Symbol
from sympy.simplify.simplify import simplify
from sympy.core.basic import preorder_traversal
from sympy.logic.inference import satisfiable
# minterms = [[0, 0 ], [1, 1] ]
# dontcares = []
# print(sympify(POSform(['a', 'b'], minterms, dontcares)))


#n           0  1  2  3  4  5   6
#n hradel    0  0  1  2  3  4   5
#dept        0  0  1  2  2           ceil(log2(n))
#



# minterms = [[1, 0, 0 ], [1, 1, 1] ]
# print(sympify(POSform(['ready', 'pending', 'done'], minterms, dontcares)))
def findCommonPart(expr1, expr2):
    print(expr1,",", expr2)
    for e1 in preorder_traversal(expr1):
        for e2 in preorder_traversal (expr2):
            s1 = simplify(And( expr1, Not(expr2)))
            s2 = list(satisfiable(e2 , all_models=True))
            if s1 == s2:
                print("Logically equiv subexpr found: ", e1, " and ", e2)


a = Symbol("a")
b = Symbol("b")
c = Symbol("c")
d = Symbol("d")
expr0 = And(a, b, d)
expr1 = Not(And(a, b))
expr2 = And(a, b, c)

expr0 = to_dnf(expr0, simplify=True)
expr1 = to_dnf(expr1, simplify=True)
expr2 = to_dnf(expr2, simplify=True)

#print(to_dnf(expr0, simplify=True))
#print(to_dnf(expr1, simplify=True))
#print(to_dnf(expr2, simplify=True))
#print("----------------")
#print(simplify(And(expr0, Not(expr1))))
#
#print(simplify_logic(expr1))
#print(simplify(And(expr0, Not(expr2))))


findCommonPart(expr0 , expr1)
print(simplify( Or(expr0, expr2)))
