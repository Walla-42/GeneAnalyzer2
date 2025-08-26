import pytest
import os
import tempfile
from geneanalyzertool.analysis.file_conversion import FileConversion
from geneanalyzertool.core.exceptions import AnalysisMethodError, SequenceParsingError


@pytest.fixture
def converter():
    return FileConversion()


@pytest.fixture
def sample_fastq():
    """Create a temporary FASTQ file for testing."""
    content = """@seq1 sample sequence 1
ATGCGATCGATCGATCG
+
IIIIIIIIIIIIIIIII
@seq2 sample sequence 2
CGATCGATCGATCGATC
+
JJJJJJJJJJJJJJJJJ
@seq3 sample sequence 3
GATCGATCGATCGATCG
+
KKKKKKKKKKKKKKKKK
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fastq', delete=False) as f:
        f.write(content)
        temp_file = f.name
    
    yield temp_file  # This provides the file path to the test
    
    # Cleanup: delete the file after the test
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def invalid_fastq():
    """Create an invalid FASTQ file for testing."""
    content = """seq1 sample sequence 1
ATGCGATCGATCGATCG
+
IIIIIIIIIIIIIIII
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fastq', delete=False) as f:
        f.write(content)
        temp_file = f.name
    
    yield temp_file  # This provides the file path to the test
    
    # Cleanup: delete the file after the test
    if os.path.exists(temp_file):
        os.unlink(temp_file)


def test_process_sequences_requires_file_input(converter):
    """Test that file conversion requires file input."""
    with pytest.raises(AnalysisMethodError, match="File conversion requires a file input"):
        converter.process_sequences("ATGC", is_file=False, seq_type=None, analysis_method="convert")


def test_process_sequences_with_nonexistent_file(converter):
    """Test handling of nonexistent files."""
    with pytest.raises(SequenceParsingError, match="File not found"):
        converter.process_sequences("nonexistent.fastq", is_file=True, seq_type=None, analysis_method="convert")


def test_process_sequences_with_unsupported_format(converter):
    """Test handling of unsupported file formats."""
    with tempfile.NamedTemporaryFile(suffix='.txt') as f:
        with pytest.raises(AnalysisMethodError, match="Unsupported file format"):
            converter.process_sequences(f.name, is_file=True, seq_type=None, analysis_method="convert")


def test_fastq_to_fasta_conversion(converter, sample_fastq):
    """Test FASTQ to FASTA conversion."""
    result = converter._fastq_to_fasta(sample_fastq)
    
    # Check that result indicates success
    assert "Successfully converted 3 sequences" in result
    assert "test_file" in result or sample_fastq in result
    
    # Check output file was created
    fasta_file = sample_fastq.replace('.fastq', '.fasta')
    assert os.path.exists(fasta_file)
    
    # Check contents of output file
    with open(fasta_file, 'r') as f:
        content = f.read()
    
    expected_lines = [
        ">seq1 sample sequence 1",
        "ATGCGATCGATCGATCG",
        ">seq2 sample sequence 2", 
        "CGATCGATCGATCGATC",
        ">seq3 sample sequence 3",
        "GATCGATCGATCGATCG"
    ]
    
    for line in expected_lines:
        assert line in content
    
    # The output file still needs manual cleanup since it's not from a fixture
    os.unlink(fasta_file)


def test_fastq_to_fasta_with_invalid_format(converter, invalid_fastq):
    """Test FASTQ to FASTA conversion with invalid format."""
    with pytest.raises(SequenceParsingError, match="Invalid FASTQ format"):
        converter._fastq_to_fasta(invalid_fastq)


def test_validate_fastq_valid_file(converter, sample_fastq):
    """Test validation of a valid FASTQ file."""
    stats = converter.validate_fastq(sample_fastq)
    
    assert stats["valid"] is True
    assert stats["total_records"] == 3
    assert len(stats["errors"]) == 0


def test_validate_fastq_invalid_file(converter, invalid_fastq):
    """Test validation of an invalid FASTQ file."""
    stats = converter.validate_fastq(invalid_fastq)
    
    assert stats["valid"] is False
    assert len(stats["errors"]) > 0
    assert "Invalid header format" in stats["errors"][0]


def test_process_sequences_full_workflow(converter, sample_fastq):
    """Test the complete process_sequences workflow."""
    results, sequence_keys = converter.process_sequences(
        sample_fastq, is_file=True, seq_type=None, analysis_method="convert"
    )
    
    assert "conversion_result" in results
    assert "Successfully converted 3 sequences" in results["conversion_result"]
    assert sequence_keys == ["conversion_result"]
    
    # Check output file exists and clean it up (output file not from fixture)
    fasta_file = sample_fastq.replace('.fastq', '.fasta')
    assert os.path.exists(fasta_file)
    os.unlink(fasta_file)


def test_analyze_method_not_supported(converter):
    """Test that analyze method raises appropriate error."""
    from geneanalyzertool.core.sequences import DNA
    
    with pytest.raises(AnalysisMethodError, match="File conversion operates on files"):
        converter.analyze(DNA("ATGC"), "convert")


def test_export_to_file(converter):
    """Test export functionality."""
    results = {"conversion_result": "Test conversion successful"}
    sequence_keys = ["conversion_result"]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        output_file = f.name
    
    converter.export_to_file(results, sequence_keys, output_file)
    
    with open(output_file, 'r') as f:
        content = f.read()
    
    assert "Test conversion successful" in content
    
    # Cleanup output file (not from fixture)
    os.unlink(output_file)


def test_unknown_analysis_method(converter, sample_fastq):
    """Test handling of unknown analysis methods."""
    with pytest.raises(AnalysisMethodError, match="Unknown file conversion method"):
        converter.process_sequences(sample_fastq, is_file=True, seq_type=None, analysis_method="unknown")
