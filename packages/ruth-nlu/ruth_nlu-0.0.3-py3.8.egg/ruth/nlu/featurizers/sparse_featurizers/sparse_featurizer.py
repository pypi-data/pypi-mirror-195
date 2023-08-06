"""Sparse Featurizer for Feature """
from typing import Any, Dict, List, Text

from ruth.nlu.featurizers.featurizer import Featurizer
from ruth.nlu.featurizers.sparse_featurizers.constants import (
    CLASS_FEATURIZER_UNIQUE_NAME,
)
from ruth.shared.nlu.training_data.collections import TrainData


class SparseFeaturizer(Featurizer):
    """base class Sparse Featurizer for Featurizers"""

    def __init__(self, element_config):
        element_config = element_config or {}
        self.element_config = element_config
        element_config.setdefault(
            CLASS_FEATURIZER_UNIQUE_NAME, self.create_unique_name()
        )
        super().__init__(element_config)

    def _build_vectorizer(self, parameters: Dict[Text, Any]):
        """Builds the vectorizer from the given parameters."""
        raise NotImplementedError

    @staticmethod
    def get_data(training_data: TrainData) -> List[Text]:
        """Get the data from the training data."""
        return training_data.get_text_list(
            training_examples=training_data.training_examples
        )
