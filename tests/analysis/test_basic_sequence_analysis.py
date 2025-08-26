import pytest
from geneanalyzertool.core.sequences import DNA, RNA, Protein
from geneanalyzertool.analysis.basic_analysis import BasicSequenceAnalysis
from geneanalyzertool.core.exceptions import InvalidSequenceTypeError, AnalysisMethodError


@pytest.fixture
def analyzer():
    return BasicSequenceAnalysis()


# ---------- gcPercent ----------
def test_gc_percent_dna(analyzer):
    seq = DNA("ATGCGC")
    result = analyzer._gc_percent(seq)
    expected = f"{round((seq.upper().count("G") + seq.upper().count("C")) / len(seq) * 100, 2)} %"
    assert result == expected


def test_gc_percent_rna(analyzer):
    seq = RNA("AUGCGC")
    result = analyzer._gc_percent(seq)
    expected = f"{round((seq.upper().count("G") + seq.upper().count("C")) / len(seq) * 100, 2)} %"
    assert result == expected


def test_gc_percent_invalid_type(analyzer):
    with pytest.raises(TypeError):
        analyzer._gc_percent(Protein("MKWV"))


# ---------- baseCount ----------
def test_base_count_dna(analyzer):
    seq = DNA("ATGCATGC")
    result = analyzer._base_count(seq)
    assert result == {"A": 2, "T": 2, "G": 2, "C": 2}


def test_base_count_rna(analyzer):
    seq = RNA("AUGCAUGC")
    result = analyzer._base_count(seq)
    # RNA still counts "T" even if absent
    assert result["T"] == 0
    assert result["A"] == 2


# ---------- translate ----------
def test_translate_valid(analyzer):
    seq = RNA("AUGUUUUAA")
    protein = analyzer._translate(seq)
    assert isinstance(protein, Protein)
    assert protein == "MF*"


def test_translate_invalid_type(analyzer):
    with pytest.raises(TypeError):
        analyzer._translate(DNA("ATGTTT"))


# ---------- transcribe ----------
def test_transcribe_dna_to_rna(analyzer):
    seq = DNA("ATGC")
    rna = analyzer._transcribe(seq)
    assert isinstance(rna, RNA)
    assert rna == "AUGC"


def test_transcribe_invalid_type(analyzer):
    with pytest.raises(TypeError):
        analyzer._transcribe(RNA("AUGC"))


# ---------- reverseComplement ----------
def test_reverse_complement_dna(analyzer):
    seq = DNA("ATGC")
    revcomp = analyzer._reverse_complement(seq)
    assert isinstance(revcomp, DNA)
    assert revcomp == "GCAT"


def test_reverse_complement_rna(analyzer):
    seq = RNA("AUGC")
    revcomp = analyzer._reverse_complement(seq)
    assert isinstance(revcomp, RNA)
    assert revcomp == "GCAU"


def test_reverse_complement_invalid_type(analyzer):
    with pytest.raises(TypeError):
        analyzer._reverse_complement(Protein("MKWV"))


# ---------- analyze() dispatcher ----------
def test_analyze_dispatch_calls_gc_percent(analyzer):
    DNA_analysis = ["gc_percent", "base_count", "transcribe", "reverse_complement"]
    RNA_analysis = ["translate", "reverse_complement", "gc_percent", "base_count"]
    protein_analysis = []
    analysis_types = [DNA_analysis, RNA_analysis, protein_analysis]

    for analysis_type in analysis_types:
        try:
            if analysis_type is DNA_analysis:
                sequence_type = DNA
            elif analysis_type is RNA_analysis:
                sequence_type = RNA
            elif analysis_type is protein_analysis:
                sequence_type = Protein
            else:
                raise TypeError("Unrecognized anlysis type")
        except TypeError as e:
            pytest.fail(str(e))

        for analysis in analysis_type:
            seq = sequence_type("ATGC")
            result = analyzer.analyze(seq, analysis)
            expected = getattr(analyzer, f"_{analysis}")(seq)
            assert result == expected


def test_analyze_invalid_method(analyzer):
    seq = DNA("ATGC")
    with pytest.raises(ValueError):
        analyzer.analyze(seq, "nonExistentMethod")


# ---------- process_sequences ----------
def test_process_sequences_single_sequence(analyzer):
    results = analyzer.process_sequences(
        sequence_input="ATGCATGC",
        is_file=False,
        seq_type="DNA",
        analysis_method="gc_percent"
    )
    test_results, sequence_keys = results
    assert len(sequence_keys) == 1
    assert sequence_keys[0] == "input_sequence"
    assert test_results[sequence_keys[0]] == "50.0 %"


def test_process_sequences_invalid_analysis_method(analyzer):
    with pytest.raises(AnalysisMethodError):
        results = analyzer.process_sequences(
            sequence_input="ATGC",
            is_file=False,
            seq_type="DNA",
            analysis_method="invalid_method"
        )

        assert results == []


def test_process_sequences_rna_translation(analyzer):
    results = analyzer.process_sequences(
        sequence_input="AUGUUUUAA",
        is_file=False,
        seq_type="RNA",
        analysis_method="translate"
    )
    test_results, sequence_keys = results
    assert len(sequence_keys) == 1
    assert sequence_keys[0] == "input_sequence"
    assert test_results[sequence_keys[0]] == "MF*"


def test_process_sequences_type_mismatch(analyzer):
    with pytest.raises(InvalidSequenceTypeError):
        analyzer.process_sequences(
            sequence_input="ATGC",
            is_file=False,
            seq_type="DNA",
            analysis_method="translate"
        )


# ---------- ORF Finder ----------

def test_orf_finder_simple_sequence(analyzer):
    results = analyzer.process_sequences(
        sequence_input="ATGGGGGCGCGCGCGCGCGCGCGCGCGAGTTAG",
        is_file=False,
        seq_type="DNA",
        analysis_method="orf"
    )
    result, sequence_keys = results
    expected_result = {
        "Number of ORFS": 1,
        "ORFS": {
            "ORF_1": {
                "Sequence": "ATGGGGGCGCGCGCGCGCGCGCGCGCGAGTTAG",
                "Start": 0,
                "End": 32,
                "Length": 33,
                "Type": "DNA-based ORF"
            }
        },
        "Sequence_Type": "DNA"
    }
    assert result == {"input_sequence": expected_result}


def test_orf_finder_complex_sequence(analyzer):
    results = analyzer.process_sequences(
        sequence_input="ATGAAATGAATGTAGATGCCCTAA",
        is_file=False,
        seq_type="DNA",
        analysis_method="orf"
    )
    result, sequence_keys = results
    expected_result = {
        "Number of ORFS": 3,
        "ORFS": {
            "ORF_1": {
                "Sequence": "ATGAAATGA",
                "Start": 0,
                "End": 8,
                "Length": 9,
                "Type": "DNA-based ORF"
            },
            "ORF_2": {
                "Sequence": "ATGTAG",
                "Start": 9,
                "End": 14,
                "Length": 6,
                "Type": "DNA-based ORF"
            },
            "ORF_3": {
                "Sequence": "ATGCCCTAA",
                "Start": 15,
                "End": 23,
                "Length": 9,
                "Type": "DNA-based ORF"
            }
        },
        "Sequence_Type": "DNA"
    }
    assert result == {"input_sequence": expected_result}


def test_orf_finder_RNA_basic(analyzer):
    """Test ORF finding in RNA sequences (transcript-based) with overlapping ORFs."""
    results = analyzer.process_sequences(
        sequence_input="AUGAAAUGAAUGUCCAUGCCUUAA",
        is_file=False,
        seq_type="RNA",
        analysis_method="orf"
    )
    result, sequence_keys = results
    expected_result = {
        "Number of ORFS": 3,
        "ORFS": {
            "ORF_1": {
                "Sequence": "AUGAAAUGA",
                "Start": 0,
                "End": 8,
                "Length": 9,
                "Type": "RNA-based ORF (transcript)"
            },
            "ORF_2": {
                "Sequence": "AUGUCCAUGCCUUAA", 
                "Start": 9,
                "End": 23,
                "Length": 15,
                "Type": "RNA-based ORF (transcript)"
            },
            "ORF_3": {
                "Sequence": "AUGCCUUAA",
                "Start": 15,
                "End": 23,
                "Length": 9,
                "Type": "RNA-based ORF (transcript)"
            }
        },
        "Sequence_Type": "RNA"
    }
    assert result == {"input_sequence": expected_result}


def test_orf_finder_RNA_simple(analyzer):
    """Test simple RNA ORF finding."""
    results = analyzer.process_sequences(
        sequence_input="AUGGGCUUAUAG",
        is_file=False,
        seq_type="RNA",
        analysis_method="orf"
    )
    result, sequence_keys = results
    expected_result = {
        "Number of ORFS": 1,
        "ORFS": {
            "ORF_1": {
                "Sequence": "AUGGGCUUAUAG",
                "Start": 0,
                "End": 11,
                "Length": 12,
                "Type": "RNA-based ORF (transcript)"
            }
        },
        "Sequence_Type": "RNA"
    }
    assert result == {"input_sequence": expected_result}


def test_orf_finder_RNA_no_orfs(analyzer):
    """Test RNA sequence with no ORFs."""
    results = analyzer.process_sequences(
        sequence_input="GGGCCCAAAUUUGGG",
        is_file=False,
        seq_type="RNA",
        analysis_method="orf"
    )
    result, sequence_keys = results
    expected_result = {
        "Number of ORFS": 0,
        "ORFS": {},
        "Sequence_Type": "RNA"
    }
    assert result == {"input_sequence": expected_result}


def test_orf_finder_mixed_case_sequence(analyzer):
    """Test ORF finding with mixed case sequences."""
    results = analyzer.process_sequences(
        sequence_input="atgGGGcgcGCGcgcGCGcgcGCGcgcTAGttag",
        is_file=False,
        seq_type="DNA",
        analysis_method="orf"
    )
    result, sequence_keys = results
    assert result["input_sequence"]["Number of ORFS"] == 1
    assert result["input_sequence"]["ORFS"]["ORF_1"]["Sequence"] == "atgGGGcgcGCGcgcGCGcgcGCGcgcTAG"


def test_orf_finder_overlapping_orfs_DNA(analyzer):
    """Test DNA ORF finding with overlapping ORFs."""
    results = analyzer.process_sequences(
        sequence_input="ATGAAATGGTAAATGCCCTAG",
        is_file=False,
        seq_type="DNA",
        analysis_method="orf"
    )
    result, sequence_keys = results
    assert result["input_sequence"]["Number of ORFS"] >= 2


def test_orf_finder_overlapping_orfs_RNA(analyzer):
    """Test RNA ORF finding with overlapping ORFs."""
    results = analyzer.process_sequences(
        sequence_input="AUGAAAUGGUGAAUGCCGUAG", 
        is_file=False,
        seq_type="RNA",
        analysis_method="orf"
    )
    result, sequence_keys = results
    orfs = result["input_sequence"]["ORFS"]
    for orf_data in orfs.values():
        assert 'U' in orf_data["Sequence"] or 'u' in orf_data["Sequence"]


def test_orf_finder_performance_regex(analyzer):
    """Test that regex-based ORF finding works with larger sequences."""
    long_sequence = "ATGAAATAG" * 100 + "ATGGGGTAG" * 50  
    results = analyzer.process_sequences(
        sequence_input=long_sequence,
        is_file=False,
        seq_type="DNA",
        analysis_method="orf"
    )
    result, sequence_keys = results
    assert result["input_sequence"]["Number of ORFS"] > 0
    
    long_rna_sequence = "AUGAAAUAG" * 100 + "AUGGGGUAG" * 50
    results_rna = analyzer.process_sequences(
        sequence_input=long_rna_sequence,
        is_file=False,
        seq_type="RNA",
        analysis_method="orf"
    )
    result_rna, _ = results_rna
    assert result_rna["input_sequence"]["Number of ORFS"] > 0
    assert result_rna["input_sequence"]["Sequence_Type"] == "RNA"


def test_orf_finder_incomplete_codon_handling(analyzer):
    """Test ORF finder with sequences that don't end on codon boundaries."""
    results = analyzer.process_sequences(
        sequence_input="ATGGGCTAG AA", 
        is_file=False,
        seq_type="DNA",
        analysis_method="orf"
    )
    result, sequence_keys = results
    assert result["input_sequence"]["Number of ORFS"] == 1
    assert result["input_sequence"]["ORFS"]["ORF_1"]["Sequence"] == "ATGGGCTAG"
