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

    yield temp_file

    # cleanup
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

    yield temp_file

    # cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def multiple_fastq_files():
    """Create multiple temporary FASTQ files for batch testing."""
    files = []

    contents = [
        """@seq1_file1 first file sequence 1
ATGCGATCGATCGATCG
+
IIIIIIIIIIIIIIIII
@seq2_file1 first file sequence 2
CGATCGATCGATCGATC
+
JJJJJJJJJJJJJJJJJ""",

        """@seq1_file2 second file sequence 1
GATCGATCGATCGATCG
+
KKKKKKKKKKKKKKKKK
@seq2_file2 second file sequence 2
TGCGATCGATCGATCGA
+
LLLLLLLLLLLLLLLLL""",

        """@seq1_file3 third file sequence 1
GCGATCGATCGATCGAT
+
MMMMMMMMMMMMMMMMM"""
    ]

    for i, content in enumerate(contents):
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'_batch_test_{i+1}.fastq', delete=False) as f:
            f.write(content)
            files.append(f.name)

    yield files

    # cleanup
    for file_path in files:
        if os.path.exists(file_path):
            os.unlink(file_path)
        fasta_file = file_path.replace('.fastq', '.fasta')
        if os.path.exists(fasta_file):
            os.unlink(fasta_file)


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

    assert "Successfully converted 3 sequences" in result
    assert "test_file" in result or sample_fastq in result

    fasta_file = sample_fastq.replace('.fastq', '.fasta')
    assert os.path.exists(fasta_file)

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

    os.unlink(output_file)


def test_unknown_analysis_method(converter, sample_fastq):
    """Test handling of unknown analysis methods."""
    with pytest.raises(AnalysisMethodError, match="Unknown file conversion method"):
        converter.process_sequences(sample_fastq, is_file=True, seq_type=None, analysis_method="unknown")


def test_batch_convert_multiple_files(converter, multiple_fastq_files):
    """Test batch conversion of multiple valid FASTQ files."""
    results = converter.batch_convert(multiple_fastq_files)

    assert len(results) == 3

    for i, result in enumerate(results):
        assert "Successfully converted" in result
        assert f"_batch_test_{i+1}.fastq" in result
        assert f"_batch_test_{i+1}.fasta" in result

    for file_path in multiple_fastq_files:
        fasta_file = file_path.replace('.fastq', '.fasta')
        assert os.path.exists(fasta_file)


def test_batch_convert_empty_list(converter):
    """Test batch conversion with empty file list."""
    with pytest.raises(SequenceParsingError, match="No file paths provided for batch conversion"):
        converter.batch_convert([])


def test_batch_convert_nonexistent_files(converter):
    """Test batch conversion with nonexistent files."""
    fake_files = ["nonexistent1.fastq", "nonexistent2.fastq"]
    results = converter.batch_convert(fake_files)

    assert len(results) == 2

    for result in results:
        assert "Error: File not found:" in result


def test_batch_convert_mixed_valid_invalid(converter, sample_fastq):
    """Test batch conversion with mix of valid and invalid files."""

    invalid_content = """not a valid fastq
    this will fail
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='_invalid.fastq', delete=False) as f:
        f.write(invalid_content)
        invalid_file = f.name

    try:
        mixed_files = [sample_fastq, invalid_file, "nonexistent.fastq"]
        results = converter.batch_convert(mixed_files)

        assert len(results) == 3
        assert "Successfully converted" in results[0]
        assert "Warning: Failed to convert" in results[1]
        assert "Error: File not found:" in results[2]

    finally:
        if os.path.exists(invalid_file):
            os.unlink(invalid_file)


def test_handle_batch_conversion_via_process_sequences(converter, multiple_fastq_files):
    """Test batch conversion through the main process_sequences interface."""
    file_paths_string = ",".join(multiple_fastq_files)

    results, sequence_keys = converter.process_sequences(
        file_paths_string, is_file=True, seq_type=None, analysis_method="batch_convert"
    )

    assert len(results) == 3
    assert len(sequence_keys) == 3

    expected_keys = ["batch_result_1", "batch_result_2", "batch_result_3"]
    assert sequence_keys == expected_keys

    for key in sequence_keys:
        assert "Successfully converted" in results[key]


def test_handle_batch_conversion_empty_string(converter):
    """Test batch conversion with empty or whitespace-only string."""
    with pytest.raises(SequenceParsingError, match="No file paths provided for batch conversion"):
        converter.process_sequences("", is_file=True, seq_type=None, analysis_method="batch_convert")

    with pytest.raises(SequenceParsingError, match="No file paths provided for batch conversion"):
        converter.process_sequences("   ,  ,  ", is_file=True, seq_type=None, analysis_method="batch_convert")


def test_handle_batch_conversion_single_file(converter, sample_fastq):
    """Test batch conversion with a single file."""
    results, sequence_keys = converter.process_sequences(
        sample_fastq, is_file=True, seq_type=None, analysis_method="batch_convert"
    )

    assert len(results) == 1
    assert sequence_keys == ["batch_result_1"]
    assert "Successfully converted" in results["batch_result_1"]
