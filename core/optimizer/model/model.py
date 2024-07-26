from pulp import *
import numpy

class ObjectiveFunction(LpAffineExpression):
	def __init__(self, constant=0):
		super().__init__(constant=constant, name="objective")

	def __iadd__(self, expr: LpAffineExpression):
		if isinstance(expr, LpAffineExpression):
			return super().__iadd__(expr)
		raise TypeError(f"Expected {LpAffineExpression} got {type(expr)}")

class Constraints(LpProblem):
	def __init__(self, name="constraints", sense=const.LpMaximize):
		super().__init__(name, sense)

	def __iadd__(self, constraint: LpConstraint):
		if isinstance(constraint, LpConstraint):
			return super().__iadd__(constraint)
		raise TypeError(f"Expected {LpConstraint} got {type(constraint)}")

class Model:
	def __init__(self):
		self.objective: ObjectiveFunction = ObjectiveFunction(0)
		self.constraints: Constraints = Constraints()

	def addVar(self, name, count = 1, cat=LpBinary):
		vars = LpVariable.dicts(name, indices=range(count), cat=cat)
		vars = numpy.fromiter(vars.values(), dtype=LpVariable)
		return vars[0] if len(vars) == 1 else vars

	def solve(self):
		model = self.constraints.copy()
		model += self.objective

		return dict(
			status=LpStatus[model.solve(PULP_CBC_CMD(msg=False))],
			objective=value(model.objective),
			variables=model.variables(),
		)