class GeneAnalyzerError(Exception):
    """Base exception for GeneAnalyzer2 errors."""
    pass


class UnsupportedFileTypeError(GeneAnalyzerError):
    """Raised when an unsupported file type is provided."""
    pass


class InvalidSequenceTypeError(GeneAnalyzerError):
    """Raised when a sequence is not DNA, RNA, or Protein as expected."""
    pass


class SequenceParsingError(GeneAnalyzerError):
    """Raised when a sequence file cannot be parsed correctly."""
    pass


class AnalysisMethodError(GeneAnalyzerError):
    """Raised when an invalid or unsupported analysis method is requested."""
    pass
