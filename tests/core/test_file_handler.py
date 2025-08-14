import pytest
from unittest.mock import patch
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from geneanalyzertool.core.file_handler import FileHandler


@pytest.fixture
def mock_records():
    return [
        SeqRecord(Seq("ATGC"), id="seq1", description="Sequence 1 description"),
        SeqRecord(Seq("GGGG"), id="seq2", description="Sequence 2 description"),
    ]


def test_file_support_check_valid(capsys):
    fh = FileHandler()
    assert fh.file_support_check("test.fna") is True
    assert fh.file_support_check("test.fasta") is True
    captured = capsys.readouterr()
    assert "Opening and parsing file" in captured.out


def test_file_support_check_invalid(capsys):
    fh = FileHandler()
    assert fh.file_support_check("test.txt") is False
    captured = capsys.readouterr()
    assert "File type not supported" in captured.out


def test_read_sequences(mock_records):
    fh = FileHandler()
    with patch("Bio.SeqIO.parse", return_value=mock_records):
        seq_dict = fh.read_sequences("dummy.fasta")
    assert seq_dict == {"seq1": Seq("ATGC"), "seq2": Seq("GGGG")}


def test_select_sequences_all(mock_records):
    fh = FileHandler()
    with patch("Bio.SeqIO.parse", return_value=mock_records):
        seq_dict, seq_keys = fh.select_sequences("dummy.fasta", selection_func=lambda _: "all")
    assert set(seq_dict.keys()) == {"seq1", "seq2"}
    assert seq_keys == ["seq1", "seq2"]


def test_select_sequences_by_number(mock_records):
    fh = FileHandler()
    with patch("Bio.SeqIO.parse", return_value=mock_records):
        seq_dict, seq_keys = fh.select_sequences("dummy.fasta", selection_func=lambda _: "2")
    assert seq_dict == {"seq2": Seq("GGGG")}
    assert seq_keys == ["seq2"]


def test_select_sequences_invalid_then_valid(mock_records):
    fh = FileHandler()
    inputs = iter(["5", "1"])
    with patch("Bio.SeqIO.parse", return_value=mock_records):
        seq_dict, seq_keys = fh.select_sequences("dummy.fasta", selection_func=lambda _: next(inputs))
    assert seq_dict == {"seq1": Seq("ATGC")}
    assert seq_keys == ["seq1"]


def test_select_sequences_exceed_max_attempts(mock_records):
    fh = FileHandler()
    inputs = iter(["5", "0", "-1"])
    with patch("Bio.SeqIO.parse", return_value=mock_records):
        with pytest.raises(ValueError, match="Maximum attempts exceeded"):
            fh.select_sequences("dummy.fasta", selection_func=lambda _: next(inputs))
