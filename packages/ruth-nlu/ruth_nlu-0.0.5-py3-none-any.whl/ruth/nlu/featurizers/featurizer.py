"""Featurizer base class."""
from ruth.nlu.elements import Element


class Featurizer(Element):
    """Featurizer class"""

    def __init__(self, element_config):
        super(Featurizer, self).__init__(element_config)
