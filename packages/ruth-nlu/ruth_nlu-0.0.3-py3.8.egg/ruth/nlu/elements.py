"""Elements are baseline component structures for ruth, Elements are used to build
the NLU pipeline and these are the components for tokenization, classfication, featurization
and extracting entities. gives the user the ability to build their own NLU pipeline and use the
components in the pipeline to build their own NLU model."""
import logging
from pathlib import Path
from typing import Any, Dict, List, Text

from ruth.shared.constants import ELEMENT_INDEX, KEY_NAME
from ruth.shared.nlu.training_data.collections import TrainData
from ruth.shared.nlu.training_data.ruth_data import RuthData
from ruth.shared.nlu.training_data.utils import override_defaults

logger = logging.getLogger(__name__)


class ElementMetaClass(type):
    """Meta class for all elements."""

    @property
    def name(cls) -> Text:
        """Returns the name of the element."""
        return cls.__name__


class Element(metaclass=ElementMetaClass):
    """Base class for all elements."""

    defaults = {}

    def __init__(self, element_config: Dict[Text, Any]):
        element_config = element_config or {}

        element_config[KEY_NAME] = self.name
        self.element_config = override_defaults(self.defaults, element_config)

    @property
    def name(self):
        """Returns the name of the element."""
        return type(self).name

    def train(self, training_data: TrainData):
        """Trains the element using the given training data."""

    def parse(self, message: RuthData):
        """Parse the message using the element."""

    def create_unique_name(self) -> Text:
        """Creates a unique name for the element."""
        idx = self.element_config.get(ELEMENT_INDEX)
        return self.name if idx is None else f"element_{idx}_{self.name}"

    @classmethod
    def build(cls, element_config: Dict[Text, Any]):
        """Builds the element using the given configuration."""
        return cls(element_config)

    def persist(self, file_name: Text, model_dir: Text):
        """Persists the element to the given path. (Saving the element to disk)"""

    @classmethod
    def load(cls, meta: Dict[Text, Any], model_dir: Path, **kwargs: Any):
        """Loads the element from the given path."""
        return cls(meta)

    @staticmethod
    def required_element() -> List[object]:
        """Returns the required elements for this element."""
        return []
