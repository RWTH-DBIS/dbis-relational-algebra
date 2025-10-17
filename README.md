# DBIS Relational Algebra

[![pypi](https://img.shields.io/pypi/pyversions/dbis-relational-algebra)](https://pypi.org/project/dbis-relational-algebra/)
[![PyPI Status](https://img.shields.io/pypi/v/dbis-relational-algebra)](https://pypi.org/project/dbis-relational-algebra/)

This library provides a Python implementation of the [relational algebra](https://en.wikipedia.org/wiki/Relational_algebra).

# Features
 - Create relational algebra expressions in Python.
 - Load data from SQLite or directly in memory.
 - Evaluate expressions an get results as relations.
 - Convert expressions to LaTeX math mode.
 - Render relations as Markdown tables.

# Installation
Install via pip:
```bash
pip install dbis-relational-algebra
```

# Loading Data
## From SQLite (recommended)
To load data, an [SQLite connection](https://docs.python.org/3/library/sqlite3.html) can be used. This connection must be passed to the relational algebra expression for the evaluation.
```python
import sqlite3
from relational_algebra import *

connection = sqlite3.connect("example.db")
relation = Relation("R") # uses table R from the database
```

## Manually
It is also possible to load a relation with data by hand
```python
relation = Relation("R")
relation.add_attributes(["a", "b", "c"])
relation.add_rows([
	[1, 2, 3],
	[4, 5, 6],
	[7, 8, 9],
])
```
Manual data loading is useful for quick examples but suffers from missings SQLite's optimization which results in higher memory usage and slower performance.

# Building and Evaluating Expressions
## Operators
- [x] Cross Product / Cartesian Product (`*`)
- [x] Difference (`-`)
- [x] Division (`/`)
- [x] Intersection (`&`)
- [x] Left/Right Semijoin
- [x] Natural Join
- [x] Projection
- [x] Rename
- [x] Selection
- [x] Theta Join
- [x] Union (`|`)

The set operators Union, Intersection, and Difference require the relations to be [union-compatible](https://en.wikipedia.org/wiki/Relational_algebra#Union-compatible_relations).

## Formulas
For the Theta Join and Selection, a formula is used to specify the join or selection condition. These formulas can be created using the following operators:
- [x] And
- [x] Or
- [x] Not
- [x] Equals
- [x] GreaterEquals
- [x] GreaterThan
- [x] LessEquals
- [x] LessThan

In the comparators, two values have to be specified. At least one of these values must be a Python `str`, which references a column of the relation.

## Examples
Example using SQLite to load data
```python
import sqlite3
from relational_algebra import *

connection = sqlite3.connect("example.db")

expr = Projection(
	Selection(
		Relation("R") * Relation("S"),
		Equals("R.b", "S.d")
	),
	["R.a", "S.c"]
)

result = expr.evaluate(sql_con=connection)

print(result.attributes)  # column names
print(result.rows)        # data rows

"""
Alternative for displaying if using jupyter notebooks:
display(Markdown(result.tabulate()))
"""
```

Example that manually loads data
```python
from relational_algebra import *

relation = Relation("R")
relation.add_attributes(["a", "b"])
relation.add_rows([
	[1, 2],
	[4, 5],
])
relation_2 = Relation("S")
relation_2.add_attributes(["c", "d"])
relation_2.add_rows([
	[6, 3],
	[4, 2],
])

expr = Projection(
	Selection(
		Relation("R") * Relation("S"),
		Equals("R.b", "S.d")
	),
	["R.a", "S.c"]
)

result = expr.evaluate(sql_con=connection)

print(result.attributes)  # column names
print(result.rows)        # data rows

"""
Alternative for displaying if using jupyter notebooks:
display(Markdown(result.tabulate()))
"""
```

# Best Practice
 - Before joining two relations or the cross product of two relations, you should always give column names that appear in both relations a new distinct name.
 - After joining two relations, the cross product of two relations, or some set operation on two relations, you should always give the resulting relation a new distinct name.
 - When referencing a column in a comparator, it is recommended that this column should be referred to using a detailed description, i.e. refer to column `a` of relation `R` as `"R.a"` instead of `"a"`.

# Developer Notes
 - Internally, the data is stored in a [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html). This accelerates the relational algebra operators greatly.
 - In relational algebra, a column `a` from a relation `R` can be referred to as `a` and `R.a`. Internally, the column name is always stored using the full name, i.e. `R.a`. This is done to avoid ambiguities when a column `a` is present in multiple relations.
 - When joining two relations (or also cross product), the relational algebra provides no guidelines on how the resulting relation should be named. Thus, if `a` is a column of relation `R`, joining relations `R` and `S` results in a relation, where `R.a` and `S.a` might refer to this column `a` (depending on if `a` also references a column in `S`). Thus, generally speaking, joining two relations `R` and `S` will internally result in a relation named `RS`, and the column `R.a` will now be named `R+S.a` (if there is no column `S.a`).
