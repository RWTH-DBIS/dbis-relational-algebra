from __future__ import annotations
from typeguard import typechecked

from typing import Optional
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
    def evaluate(self) -> Relation:
        return self

    @typechecked
    def add_row(
        self, row: tuple[ra.PRIMITIVE_TYPES] | list[ra.PRIMITIVE_TYPES]
    ) -> None:
        """
        Adds a row to the relation

        Parameters
        ----------
        row : tuple[ra.PRIMITIVE_TYPES]
            The row to add to the relation
        """
        if len(self.attributes) != len(row):
            raise Exception(
                f"Row ({row}) does not have the same number of attributes ({self.attributes}) as the relation {self.name}"
            )
        self.rows.add(RelationEntry(self, row))

    @typechecked
    def add_rows(
        self,
        rows: list[tuple[ra.PRIMITIVE_TYPES]]
        | set[tuple[ra.PRIMITIVE_TYPES]]
        | list[list[ra.PRIMITIVE_TYPES]],
    ) -> None:
        """
        Adds multiple rows to the relation

        Parameters
        ----------
        rows : list[tuple[ra.PRIMITIVE_TYPES]] | set[tuple[ra.PRIMITIVE_TYPES]] | list[list[ra.PRIMITIVE_TYPES]]
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
        for attr in self.attributes:
            if attr.lower() == attribute.lower():
                return attr
            if f"{self.name}.{attr}".lower() == attribute.lower():
                return attr
        return None

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
            attributes = [attributes]

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
            return self.relation == other.relation and self.row == other.row
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
            attributes = [attributes]

        attribute_names = self.relation.get_attribute_names(attributes)
        if attribute_names is None:
            raise KeyError(f"Attribute not found in: {attributes}")

        result = []
        for attribute_name in attribute_names:
            result.append(self.row[self.relation.attributes.index(attribute_name)])
        if len(result) == 1:
            return result[0]
        return result
