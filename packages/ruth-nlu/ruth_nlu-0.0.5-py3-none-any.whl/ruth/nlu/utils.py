"""
Utils for the NLU pipeline
"""
from typing import List, Text

from ruth.nlu.elements import Element


def module_path_from_object(o: Element) -> Text:
    """Returns the module path of the given object."""
    return o.__class__.__module__ + "." + o.__class__.__name__


def check_required_elements(required_element: Element, pipeline: List[Element]) -> bool:
    """Checks if the required element is present in the pipeline."""
    for element in pipeline:
        if isinstance(element, required_element):
            return True
    return False
