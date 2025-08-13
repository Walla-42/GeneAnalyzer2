import pytest
from geneanalyzertool.core.sequences import DNA, RNA, Protein
from geneanalyzertool.analysis.basic_analysis import BasicSequenceAnalysis


@pytest.fixture
def analyzer():
    return BasicSequenceAnalysis()


# ---------- gcPercent ----------
def test_gc_percent_dna(analyzer):
    seq = DNA("ATGCGC")
    result = analyzer._gc_percent(seq)
    expected = (seq.upper().count("G") + seq.upper().count("C")) / len(seq) * 100
    assert result == expected


def test_gc_percent_rna(analyzer):
    seq = RNA("AUGCGC")
    result = analyzer._gc_percent(seq)
    expected = (seq.upper().count("G") + seq.upper().count("C")) / len(seq) * 100
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
            pytest.fail(e)

        for analysis in analysis_type:
            seq = sequence_type("ATGC")
            result = analyzer.analyze(seq, analysis)
            expected = getattr(analyzer, f"_{analysis}")(seq)
            assert result == expected
    


def test_analyze_invalid_method(analyzer):
    seq = DNA("ATGC")
    with pytest.raises(ValueError):
        analyzer.analyze(seq, "nonExistentMethod")
