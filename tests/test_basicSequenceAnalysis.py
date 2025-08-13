import pytest
from src.geneanalyzertool.core.sequences import DNA, RNA, Protein
from src.geneanalyzertool.analysis.BasicAnalysis import BasicSequenceAnalysis


@pytest.fixture
def analyzer():
    return BasicSequenceAnalysis()


# ---------- gcPercent ----------
def test_gc_percent_dna(analyzer):
    seq = DNA("ATGCGC")
    result = analyzer.gcPercent(seq)
    expected = (seq.seq.upper().count("G") + seq.seq.upper().count("C")) / len(seq.seq) * 100
    assert result == expected


def test_gc_percent_rna(analyzer):
    seq = RNA("AUGCGC")
    result = analyzer.gcPercent(seq)
    expected = (seq.seq.upper().count("G") + seq.seq.upper().count("C")) / len(seq.seq) * 100
    assert result == expected


def test_gc_percent_invalid_type(analyzer):
    with pytest.raises(TypeError):
        analyzer.gcPercent(Protein("MKWV"))


# ---------- baseCount ----------
def test_base_count_dna(analyzer):
    seq = DNA("ATGCATGC")
    result = analyzer.baseCount(seq)
    assert result == {"A": 2, "T": 2, "G": 2, "C": 2}


def test_base_count_rna(analyzer):
    seq = RNA("AUGCAUGC")
    result = analyzer.baseCount(seq)
    # RNA still counts "T" even if absent
    assert result["T"] == 0
    assert result["A"] == 2


# ---------- translate ----------
def test_translate_valid(analyzer):
    seq = RNA("AUGUUUUAA")  
    protein = analyzer.translate(seq)
    assert isinstance(protein, Protein)
    assert protein.seq == "MF*" 


def test_translate_invalid_type(analyzer):
    with pytest.raises(TypeError):
        analyzer.translate(DNA("ATGTTT"))


# ---------- transcribe ----------
def test_transcribe_dna_to_rna(analyzer):
    seq = DNA("ATGC")
    rna = analyzer.transcribe(seq)
    assert isinstance(rna, RNA)
    assert rna.seq == "AUGC"


def test_transcribe_invalid_type(analyzer):
    with pytest.raises(TypeError):
        analyzer.transcribe(RNA("AUGC"))


# ---------- reverseComplement ----------
def test_reverse_complement_dna(analyzer):
    seq = DNA("ATGC")
    revcomp = analyzer.reverseComplement(seq)
    assert isinstance(revcomp, DNA)
    assert revcomp.seq == "GCAT"


def test_reverse_complement_rna(analyzer):
    seq = RNA("AUGC")
    revcomp = analyzer.reverseComplement(seq)
    assert isinstance(revcomp, RNA)
    assert revcomp.seq == "GCAU"


def test_reverse_complement_invalid_type(analyzer):
    with pytest.raises(TypeError):
        analyzer.reverseComplement(Protein("MKWV"))


# ---------- analyze() dispatcher ----------
def test_analyze_dispatch_calls_gc_percent(analyzer):
    seq = DNA("ATGC")
    result = analyzer.analyze(seq, "gcPercent")
    expected = analyzer.gcPercent(seq)
    assert result == expected


def test_analyze_invalid_method(analyzer):
    seq = DNA("ATGC")
    with pytest.raises(ValueError):
        analyzer.analyze(seq, "nonExistentMethod")
