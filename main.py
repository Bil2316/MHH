from gamspy import Container, Set, Parameter, Variable, Equation, Model, Sum, Sense
import numpy as np
import sys 

n = 8 # Number of product
m = 5 # Number of part of product
s = 2 # Number of scenarios
p = 1/2 # Density

m = Container()

i = Set(container=m, name="i", description="product", records=[1, 2, 3, 4, 5, 6, 7, 8])
j = Set(container=m, name='j', description='part', records=[1, 2, 3, 4, 5])
k = Set(container=m, name='k', description='scenarios', records=[1, 2])

a = Parameter(
    container=m,
    name="unit",
    domain=[i, j],
    records=np.array(
        [
            [12, 4, 1, 18, 12],
            [5, 11, 1, 2, 16],
            [2, 15, 12, 8, 11],
            [16, 6, 19, 3, 19],
            [7, 13, 3, 15, 8],
            [11, 14, 18, 2, 3],
            [15, 2, 16, 16, 16],
            [19, 19, 3, 8, 17],
        ]
    ),
)

c = Parameter(
    container=m,
    name="cost",
    domain=j,
    records=np.array([9, 18, 53, 33, 67]),
)

s = Parameter(
    container=m,
    name="salvage",
    domain=j,
    records=np.array([6, 6, 47, 21, 61]),
)

l = Parameter(
    container=m,
    name="costs_additionally",
    domain=i,
    records=np.array([43, 45, 2, 57, 61, 57, 40, 49]),
)

q = Parameter(
    container=m,
    name="unit_selling_price",
    domain=i,
    records=np.array([2572, 3661, 5606, 8070, 9301, 11568, 13558, 15426]),
)

d = Parameter(
    container=m,
    name="demand",
    domain=[k, i],
    records=np.array(
        [
            [4, 0, 1, 4, 8, 8, 7, 9],
            [2, 0, 5, 0, 6, 8, 3, 8]
        ]),
)

x = Variable(
    container=m,
    name="x",
    domain=j,
    type="Positive",
    description=" the numbers of parts ordered",
)

e1 = Equation(container=m, name='e1', domain=j)
e1[j] = x[j] >= 0

z = Variable(
    container=m,
    name="z",
    domain=[k, i],
    type="Positive",
    description="the numbers of units produced",
)

e2 = Equation(container=m, name='e2', domain=[k, j],)
e2[k, j] = z[k, j] <= d[k, j]

obj = Sum(j, c[j]*x[j]) + Sum(k, (Sum(i, ((l[i] - q[i])*z[k, i]))) - Sum(j, s[i] * (x[j] - Sum(i, a[i, j] * z[k, i]))))

transport = Model(
    m,
    name="transport",
    equations=m.getEquations(),
    problem="LP",
    sense=Sense.MIN,
    objective=obj,
)

transport.solve(output=sys.stdout)