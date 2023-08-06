"""Hugging Face Tokenizer for tokenization of text."""
from pathlib import Path
from typing import Any, Dict, List, Optional, Text

from ruth.constants import TEXT
from ruth.nlu.classifiers.constants import MODEL_NAME
from ruth.nlu.tokenizer.constants import MAX_LENGTH_FOR_PADDING
from ruth.nlu.tokenizer.tokenizer import Tokenizer
from ruth.shared.constants import ATTENTION_MASKS, INPUT_IDS
from ruth.shared.nlu.training_data.collections import TrainData
from ruth.shared.nlu.training_data.ruth_data import RuthData
from tqdm import tqdm
from transformers import AutoTokenizer


class HFTokenizer(Tokenizer):
    """Hugging Face Tokenizer for tokenising text."""

    DO_LOWER_CASE = "do_lower_case"

    defaults = {MODEL_NAME: "bert-base-uncased", DO_LOWER_CASE: True}

    def __init__(self, element_config: Optional[Dict[Text, Any]], tokenizer=None):
        super(HFTokenizer, self).__init__(element_config)
        self.tokenizer = tokenizer or {}

    def _build_tokenizer(self):
        """Builds the tokenizer from the given parameters."""
        return AutoTokenizer.from_pretrained(self.element_config[MODEL_NAME])

    def _create_tokens(self, examples: TrainData):
        """Creates tokens for the given examples."""
        before_padding_text = [message.get(TEXT) for message in examples]

        encoded = self.tokenizer(
            before_padding_text,
            add_special_tokens=True,
            max_length=MAX_LENGTH_FOR_PADDING,
            padding=True,
            truncation=True,
            return_attention_mask=True,
        )

        input_ids = encoded["input_ids"]
        attention_masks = encoded["attention_mask"]
        return input_ids, attention_masks

    def tokenize(self, training_data: TrainData):
        """Tokenizes the given training data."""
        return self._create_tokens(training_data.training_examples)

    @staticmethod
    def _add_tokens_to_data(
        training_examples: List[RuthData],
        input_ids: List[List[int]],
        attention_masks: List[List[int]],
    ):
        """Adds the tokens to the training data."""
        for message, input_id, attention_mask in tqdm(
            zip(training_examples, input_ids, attention_masks),
            desc="tokenization",
            total=len(training_examples),
        ):
            message.set(INPUT_IDS, input_id)
            message.set(ATTENTION_MASKS, attention_mask)

    def train(self, training_data: TrainData):
        """Trains the tokenizer on the given training data."""
        self.tokenizer = self._build_tokenizer()
        input_ids, attention_masks = self.tokenize(training_data)
        self._add_tokens_to_data(
            training_data.training_examples, input_ids, attention_masks
        )

    def persist(self, file_name: Text, model_dir: Path):
        """Persists the tokenizer to the given path."""
        tokenizer_file_name = file_name + "_tokenizer"

        tokenizer_path = str(model_dir) + "/" + tokenizer_file_name

        if self.tokenizer:
            self.tokenizer.save_pretrained(tokenizer_path)

        return {"tokenizer": tokenizer_file_name}

    @classmethod
    def load(cls, meta: Dict[Text, Any], model_dir: Path, **kwargs):
        """Loads the tokenizer from the given path."""
        tokenizer_file_name = model_dir / meta["tokenizer"]

        tokenizer = AutoTokenizer.from_pretrained(tokenizer_file_name)

        return cls(meta, tokenizer=tokenizer)

    def parse(self, message: RuthData):
        """get the tokens for the given message."""
        parser_token = self.tokenizer.encode_plus(
            message.get(TEXT),
            add_special_tokens=True,
            max_length=MAX_LENGTH_FOR_PADDING,
            padding=True,
            truncation=True,
            return_attention_mask=True,
        )
        message.set(INPUT_IDS, parser_token["input_ids"])
        message.set(ATTENTION_MASKS, parser_token["attention_mask"])
