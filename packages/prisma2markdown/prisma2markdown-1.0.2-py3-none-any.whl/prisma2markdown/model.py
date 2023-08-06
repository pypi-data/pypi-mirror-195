"""Manage data model."""
import structlog


logger = structlog.getLogger(__name__)


class Model:
    """Internal model used to managing prisma model."""

    def __init__(self, model_name):
        logger.info(f"Creating a new model with name {model_name}")
        self.model_name = model_name
        self.optional_attributes = []
        self.attributes = []

    def add_attribute(self, attribute_name, attribute_type, optional: bool = False):
        """Add an attribute to a model."""
        logger.info(f"Adding attribute {attribute_name}")
        self.attributes.append({"name": attribute_name, "type": attribute_type})
        if optional:
            self.optional_attributes.append(attribute_name)

    def to_mermaid(self) -> str:
        """Create mermaid script related to a model."""
        model_attribute_list = [
            f"  {attribute['name']} {attribute['type']}" for attribute in self.attributes
        ]
        model_attribute_string = "\n".join(model_attribute_list)
        mermaid_output = f"{self.model_name}" + "{\n" + model_attribute_string + "\n}"
        return mermaid_output
