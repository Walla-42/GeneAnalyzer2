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
        """
        Perform analysis on a single sequence using the specified method.
        
        Args:
            sequence (Sequence): Sequence object to analyze
            method (str): Analysis method to perform
            
        Returns:
            Any: Result of the analysis (type depends on method)
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def process_sequences(self, sequence_input: str, is_file: bool, seq_type: str, analysis_method: str):
        """
        Process one or more sequences and perform the specified analysis.
        
        Args:
            sequence_input (str): Either a sequence string or file path
            is_file (bool): Whether sequence_input is a file path
            seq_type (str): Type of sequence (DNA, RNA, or Protein)
            analysis_method (str): Analysis method to perform
            
        Returns:
            Tuple[dict, List[str]]: Analysis results and list of sequence keys
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def print_to_terminal(self, results: dict, sequence_keys: List[str]):
        """
        Print analysis results to terminal.
        
        Args:
            results (dict): Dictionary mapping sequence keys to analysis results
            sequence_keys (List[str]): Ordered list of sequence identifiers
        """
        raise NotImplementedError("Subclasses must implement this method.")
