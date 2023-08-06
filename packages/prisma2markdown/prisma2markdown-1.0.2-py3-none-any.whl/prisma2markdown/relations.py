"""Relation classes and constant"""
from enum import Enum


class RelationTypeLeft(Enum):
    """Cardinality leftside with respect to mermaid."""

    ZERO_OR_ONE = "|o"
    EXACTLY_ONE = "||"
    MANY = "}o"


class RelationTypeRight(Enum):
    """Cardinality rightside with respect to mermaid."""

    ZERO_OR_ONE = "o|"
    EXACTLY_ONE = "||"
    MANY = "o{"


CARDINALITY_DICT = {
    "LEFT": {
        "ZERO_OR_ONE": RelationTypeLeft.ZERO_OR_ONE,
        "EXACTLY_ONE": RelationTypeLeft.EXACTLY_ONE,
        "MANY": RelationTypeLeft.MANY,
    },
    "RIGHT": {
        "ZERO_OR_ONE": RelationTypeRight.ZERO_OR_ONE,
        "EXACTLY_ONE": RelationTypeRight.EXACTLY_ONE,
        "MANY": RelationTypeRight.MANY,
    },
}


class RelationIdentification(Enum):
    """Identifying relationship."""

    FORCED = "--"
    NOT_FORCED = ".."


class Relation:
    """Manages relationship between classes."""
    def __init__(self, left_name, right_name):
        self.left = left_name
        self.right = right_name
        self.cardinality_left = None
        self.cardinality_right = None
        self.existence = None
        self.label = None

    def update_cardinality(self, cardinality_name, reference):
        """Update cardinality in the relationship."""
        if cardinality_name == "LEFT":
            self.cardinality_left = CARDINALITY_DICT[cardinality_name][reference].value
        else:
            self.cardinality_right = CARDINALITY_DICT[cardinality_name][reference].value

    def to_mermaid(self):
        """Convert relationship to mermaid script."""
        mermaid_output = (
            f"{self.left} {self.cardinality_left}{self.existence}"
            f"{self.cardinality_right} {self.right} : {self.label}\n"
        )
        return mermaid_output

    def update_label(self, content: str):
        """Update relationship label."""
        if self.label is None:
            self.label = f'"{content} : '
        else:
            self.label = self.label + f'{content}"'
