from __future__ import annotations

import sqlite3
from typing import Iterable, Optional

from typeguard import typechecked

import relational_algebra as ra


class Relation(ra.Operator):
    """
    This class represents a relation in relational algebra
    """

    @typechecked
    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the relation
        """
        super().__init__(children=[])
        self.name = name
        self.attributes = list()
        self.rows = set()

    @typechecked
    def __repr__(self) -> str:
        return f"(\\text{{{self.name}}})"

    @typechecked
    def evaluate(self, sql_con: Optional[sqlite3.Connection] = None) -> Relation:
        if sql_con is None:
            return self

        # get the attributes
        cursor = sql_con.cursor()
        cursor.execute(f"PRAGMA table_info({self.name})")
        self.attributes = [row[1] for row in cursor.fetchall()]
        # get the rows
        cursor.execute(f"SELECT * FROM {self.name}")
        self.add_rows(cursor.fetchall())
        return self

    @typechecked
    def add_row(
        self, row: tuple[ra.PRIMITIVE_TYPES] | list[ra.PRIMITIVE_TYPES] | RelationEntry
    ) -> None:
        """
        Adds a row to the relation

        Parameters
        ----------
        row : tuple[ra.PRIMITIVE_TYPES] | list[ra.PRIMITIVE_TYPES] | RelationEntry
            The row to add to the relation
        """
        row = list(row)
        if len(self.attributes) != len(row):
            raise Exception(
                f"Row ({row}) does not have the same number of attributes ({self.attributes}) as the relation {self.name}"
            )
        self.rows.add(RelationEntry(self, row))

    @typechecked
    def add_rows(
        self,
        rows: list[tuple[ra.PRIMITIVE_TYPES] | RelationEntry]
        | set[tuple[ra.PRIMITIVE_TYPES] | RelationEntry]
        | list[list[ra.PRIMITIVE_TYPES] | RelationEntry],
    ) -> None:
        """
        Adds multiple rows to the relation

        Parameters
        ----------
        rows : list[tuple[ra.PRIMITIVE_TYPES] | RelationEntry] | set[tuple[ra.PRIMITIVE_TYPES] | RelationEntry] | list[list[ra.PRIMITIVE_TYPES] | RelationEntry]
            The rows to add to the relation
        """
        for row in rows:
            self.add_row(row)

    @typechecked
    def get_attribute_name(self, attribute: str) -> Optional[str]:
        """
        Returns the name of the attribute

        Parameters
        ----------
        attribute : str
            The attribute

        Returns
        -------
        Optional[str]
            The name of the attribute
        """
        candidates = list()
        for attr in self.attributes:
            if attr.lower() == attribute.lower():
                candidates.append(attr)
            if f"{self.name}.{attr}".lower() == attribute.lower():
                candidates.append(attr)
            if "." in attr:
                if attr.split(".")[-1].lower() == attribute.lower():
                    candidates.append(attr)

        if len(candidates) == 0:
            return None
        if len(candidates) > 1:
            raise Exception(
                f"Multiple candidates for attribute {attribute}: {candidates}"
            )
        return candidates[0]

    @typechecked
    def get_attribute_names(
        self, attributes: list[str] | tuple[str]
    ) -> Optional[list[str]]:
        """
        Returns the names of the attributes

        Parameters
        ----------
        attributes : list[str]
            The attributes

        Returns
        -------
        Optional[list[str]]
            The names of the attributes
        """
        result = [self.get_attribute_name(attribute) for attribute in attributes]
        if None in result:
            return None
        return result

    @typechecked
    def get_minimal_attribute_name(self, attribute: str) -> Optional[str]:
        """
        Returns the minimal attribute name (i.e. the attribute name without the relation name)

        Parameters
        ----------
        attribute : str
            The attribute name

        Returns
        -------
        Optional[str]
            The minimal attribute name
        """
        result = self.get_attribute_name(attribute)
        if result is None:
            return None
        if "." in result:
            return result.split(".")[-1]
        return result

    @typechecked
    def get_minimal_attribute_names(
        self, attributes: list[str] | tuple[str]
    ) -> Optional[list[str]]:
        """
        Returns the minimal attribute names (i.e. the attribute names without the relation names)

        Parameters
        ----------
        attributes : list[str]
            The attribute names

        Returns
        -------
        Optional[list[str]]
            The minimal attribute names
        """
        result = [
            self.get_minimal_attribute_name(attribute) for attribute in attributes
        ]
        if None in result:
            return None
        return result

    @typechecked
    def __getitem__(self, attributes: str | tuple[str]) -> Relation:
        """
        Returns a projection of the relation

        Parameters
        ----------
        attributes : str | tuple[str]
            The attributes to project

        Returns
        -------
        Relation
            The projection of the relation
        """
        if isinstance(attributes, str):
            attr = list()
            attr.append(attributes)
            attributes = attr

        attributes = self.get_attribute_names(attributes)
        if attributes is None:
            raise KeyError(f"Attribute not found in: {attributes}")

        # create new relation using the same name and values of given attributes only
        new_relation = Relation(self.name)
        new_relation.attributes = attributes
        new_relation.rows = set()
        for row in self.rows:
            new_relation.rows.add(
                RelationEntry(
                    new_relation, [row[attribute] for attribute in attributes]
                )
            )
        return new_relation

    @typechecked
    def union_compatibility(self, other: Relation) -> Optional[list[str]]:
        """
        Checks if two relations are compatible for a union operation.
        If so, the names of the attributes are returned.

        Parameters
        ----------
        other : Relation
            The other relation

        Returns
        -------
        Optional[str]
            The names of the attributes
        """
        if len(self.attributes) != len(other.attributes):
            return None
        for attr1, attr2 in zip(self.attributes, other.attributes):
            attr1_minimal = self.get_minimal_attribute_name(attr1)
            attr2_minimal = other.get_minimal_attribute_name(attr2)
            if attr1_minimal != attr2_minimal or attr1 is None or attr2 is None:
                return None
        return self.get_minimal_attribute_names(self.attributes)


class RelationEntry:
    """
    This class represents a entry of a relation
    """

    @typechecked
    def __init__(
        self,
        relation: Relation,
        row: tuple[ra.PRIMITIVE_TYPES] | list[ra.PRIMITIVE_TYPES],
    ) -> None:
        """
        Parameters
        ----------
        relation : Relation
            The relation of the entry
        row : tuple[ra.PRIMITIVE_TYPES] | list[ra.PRIMITIVE_TYPES]
            The row of the entry
        """
        assert len(relation.attributes) == len(row)
        self.relation = relation
        self.row = row

    @typechecked
    def __repr__(self) -> str:
        return f"({','.join([str(value) for value in self.row])})"

    @typechecked
    def __hash__(self) -> int:
        return hash(tuple(self.row))

    @typechecked
    def __eq__(self, other: any) -> bool:
        if isinstance(other, RelationEntry):
            return tuple(self.row) == tuple(other.row)
        if isinstance(other, tuple | list):
            return tuple(self.row) == tuple(other)
        return False

    @typechecked
    def __getitem__(
        self, attributes: str | tuple[str]
    ) -> ra.PRIMITIVE_TYPES | tuple[ra.PRIMITIVE_TYPES] | list[ra.PRIMITIVE_TYPES]:
        """
        Returns the value of the attributes

        Parameters
        ----------
        attributes : str | tuple[str]
            The attributes to get the value of

        Returns
        -------
        ra.PRIMITIVE_TYPES | tuple[ra.PRIMITIVE_TYPES]
            The value of the attributes
        """
        if isinstance(attributes, str):
            attr = list()
            attr.append(attributes)
            attributes = attr

        attribute_names = self.relation.get_attribute_names(attributes)
        if attribute_names is None:
            raise KeyError(f"Attribute not found in: {attributes}")

        result = []
        for attribute_name in attribute_names:
            result.append(self.row[self.relation.attributes.index(attribute_name)])
        if len(result) == 1:
            return result[0]
        return result

    @typechecked
    def __tuple__(self) -> tuple[ra.PRIMITIVE_TYPES]:
        return tuple(self.row)

    @typechecked
    def __iter__(self) -> Iterable[ra.PRIMITIVE_TYPES]:
        return iter(self.row)
