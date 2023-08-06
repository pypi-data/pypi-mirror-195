"""Module that store classes related to mermaid."""
from typing import List, Optional, Dict

import re
import structlog

from .model import Model
from .relations import Relation, RelationIdentification


logger = structlog.getLogger()


class MermaidBuilder:
    """A builder or a mermaid schema."""

    def __init__(self):
        self.named_class_list: List[str] = []
        self.model_list: List[Model] = []
        self.current_model: Optional[Model] = None
        self.relation_dict: Dict[str, Relation] = {}

    def parse_named_classes(self, lines: List[str]):
        """Fill an internal attribute that list named classes in the schema."""
        for line in lines:
            tokens = line.split()
            if "model" in tokens:
                model_index = tokens.index("model")
                model_name = tokens[model_index + 1]
                self.named_class_list.append(model_name)

    def store_model(self):
        """Add current model to the list."""
        self.model_list.append(self.current_model)
        self.current_model = None

    def parse_attribute_or_relation(self, tokens: List[str]):
        """Parse the line that should be analysed in a model."""
        attribute_type = re.sub("[^0-9a-zA-Z]+", "", tokens[1])
        if attribute_type in self.named_class_list:
            self.parse_relation(tokens, attribute_type)
        else:
            self.parse_attribute(tokens)

    def parse_relation(self, tokens: List[str], other_model_name: str):
        """Create the necessary connections in the internal model."""
        if "?" in tokens[1]:
            relation_right = "ZERO_OR_ONE"
        elif "[]" in tokens[1]:
            relation_right = "MANY"
        else:
            relation_right = "EXACTLY_ONE"
        self.create_or_update_relation(
            self.current_model.model_name, other_model_name, relation_right
        )

    def create_or_update_relation(
        self,
        left_entity: str,
        right_entity: str,
        relation_right: str,
    ):
        """Create a relation between two models."""
        if right_entity + left_entity in self.relation_dict.keys():
            self.relation_dict[right_entity + left_entity].update_cardinality(
                "LEFT", relation_right
            )
            self.relation_dict[right_entity + left_entity].update_label(left_entity)
        else:
            relation = Relation(left_entity, right_entity)
            relation.update_cardinality("RIGHT", relation_right)
            relation.update_label(left_entity)
            self.relation_dict[left_entity + right_entity] = relation

    def parse_attribute(self, tokens: List[str]):
        """Parse a string row as model attribute."""
        optional = False
        if tokens[1].endswith("[]"):
            attribute_type = f"ListOf{tokens[1][:-2]}"
        elif tokens[1].endswith("?"):
            attribute_type = tokens[1][:-1]
            optional = True
        elif tokens[1].startswith("@@"):
            return
        else:
            attribute_type = tokens[1]
        self.current_model.add_attribute(tokens[0], attribute_type, optional)

    def update_relations(self):
        """Update all generated relations with required meta."""
        for relation in self.relation_dict.values():
            relation.existence = (
                RelationIdentification.NOT_FORCED.value
                if ("o" not in relation.cardinality_right) or ("o" not in relation.cardinality_left)
                else RelationIdentification.FORCED.value
            )

    def parse_lines(self, lines: List[str]) -> str:
        """Build the mermaid output."""
        self.parse_named_classes(lines)
        for line in lines:
            tokens = line.split()
            if ("model" in tokens) & ("{" in tokens):
                model_index = tokens.index("model")
                model_name = tokens[model_index + 1]
                self.current_model = Model(model_name)
            elif (self.current_model is not None) & ("}" in tokens):
                self.store_model()
            elif (self.current_model is not None) & (len(tokens) > 1):
                self.parse_attribute_or_relation(tokens)
        self.update_relations()
        return "\n\n".join(
            [model.to_mermaid() for model in self.model_list]
            + [relation.to_mermaid() for relation in self.relation_dict.values()]
        )
