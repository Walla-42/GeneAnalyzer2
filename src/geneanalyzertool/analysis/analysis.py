from abc import ABC, abstractmethod
from typing import Any, List
from geneanalyzertool.core.sequences import Sequence


class Analysis(ABC):
    """
    Abstract base class for analysis modules.
    All analysis classes should inherit from this class.
    """

    @abstractmethod
    def analyze(self, sequence: Sequence, method: str) -> Any:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def process_sequences(self, sequence_input: str, is_file: bool, seq_type: str, analysis_method: str):
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def print_to_terminal(self, results: dict, sequence_keys: List[str]):
        raise NotImplementedError("Subclasses must implement this method.")
