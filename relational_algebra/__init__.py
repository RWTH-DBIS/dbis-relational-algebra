from relational_algebra.operators.Operator import Operator

from relational_algebra.formulas.Formula import Formula
from relational_algebra.formulas.atoms.Equals import Equals
from relational_algebra.formulas.atoms.GreaterEquals import GreaterEquals
from relational_algebra.formulas.atoms.GreaterThan import GreaterThan
from relational_algebra.formulas.atoms.LessEquals import LessEquals
from relational_algebra.formulas.atoms.LessThan import LessThan
from relational_algebra.formulas.conenctives.And import And
from relational_algebra.formulas.conenctives.Not import Not
from relational_algebra.formulas.conenctives.Or import Or

ATOM_TYPES = Equals | GreaterEquals | GreaterThan | LessEquals | LessThan
PRIMITIVE_TYPES = int | float | str | bool
