from abc import ABC, abstractmethod
from typing import Any, override
from geneanalyzertool.core.sequences import *

class Analysis(ABC):
    """
    Abstract base class for analysis modules.
    All analysis classes should inherit from this class.
    """

    @abstractmethod
    def analyze(self, sequence: Sequence) -> Any:
        raise NotImplementedError("Subclasses must implement this method.")