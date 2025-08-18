from geneanalyzertool.analysis.analysis import Analysis
from geneanalyzertool.core.sequences import Sequence, DNA, RNA, Protein
from geneanalyzertool.core.file_handler import FileHandler
from typing import Any, override, List
from geneanalyzertool.core.exceptions import InvalidSequenceTypeError, AnalysisMethodError


class BasicSequenceAnalysis(Analysis, FileHandler):
    """
    Class for basic analysis performed on dna, rna or protein sequences
    """

    @override
    def export_to_file(self, results: List[str], out_file: str):
        with open(out_file, 'w') as out:
            for line in results:
                out.write(line + "\n")

    def process_sequences(self, sequence_input: str, is_file: bool, seq_type: str, analysis_method: str) -> List[str]:
        """
        Process one or more sequences and perform the specified analysis.

        Args:
            sequence_input: Either a sequence string or file path
            is_file: Whether sequence_input is a file path
            seq_type: Type of sequence (DNA, RNA, or Protein)
            analysis_method: Analysis method to perform

        Returns:
            List of result strings
        """

        # Get sequences to analyze
        if is_file:
            available_sequences, sequence_keys = self.select_sequences(sequence_input)
        else:
            # Treat the single sequence as a dict with one entry
            available_sequences = {"input_sequence": sequence_input}
            sequence_keys = ["input_sequence"]

        try:
            # Map sequence type to the appropriate class
            type_map = {"DNA": DNA, "RNA": RNA, "PROTEIN": Protein}
            seq_type_class = type_map[seq_type.upper()]
        
        except KeyError:
            raise InvalidSequenceTypeError("Error: Invalid sequence type provided. Valid types are DNA, RNA, or Protein.")

        # Process each sequence
        results = []
        for key in sequence_keys:
            print(f"Analyzing {key}...")
            sequence_obj = seq_type_class(available_sequences[key])
            try:
                result = self.analyze(sequence_obj, analysis_method)
                results.append(f"{key}: {result}")
            except ValueError as e:
                raise AnalysisMethodError(f"Invalid analysis method provided. {str(e)}")
            except TypeError as e:
                raise InvalidSequenceTypeError(f"Unable to perform this analysis on sequence of type {seq_type.upper()}. {e}")

        return results

    @override
    def analyze(self, sequence: Sequence, method: str) -> Any:
        """
        executes simple analysis of protein, RNA or DNA sequences.
        """
        method_dispatch = {
            "gc_percent": self._gc_percent,
            "base_count": self._base_count,
            "translate": self._translate,
            "transcribe": self._transcribe,
            "reverse_complement": self._reverse_complement
        }

        if method not in method_dispatch:
            raise ValueError(f"Unknown method {method}")

        return method_dispatch[method](sequence)

    def _gc_percent(self, sequence: DNA | RNA) -> float:
        """
        Calculates the percent Guanine and Cytosine that are present in a DNA or RNA Molecule.
        Sequence must be of type RNA or DNA.
        """
        if not isinstance(sequence, (DNA, RNA)):
            raise TypeError("Error: Sequence must be of type DNA or RNA")

        gc_count = sequence.upper().count("G") + sequence.upper().count("C")
        return round((gc_count / len(sequence)) * 100, 2)

    def _base_count(self, sequence) -> dict:
        """
        Counts the number of each base in a DNA sequence.
        Sequence provided must be of type DNA or RNA.
        """
        base_counts = {
            'A': sequence.upper().count('A'),
            'T': sequence.upper().count('T'),
            'G': sequence.upper().count('G'),
            'C': sequence.upper().count('C')
        }

        return base_counts

    def _translate(self, sequence) -> Protein:
        """
        Translates a given RNA sequence into a predicted protein sequence minus
        post translational modifications. Sequence provided must be of type RNA.
        """
        peptide_table = {
            "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
            "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
            "UAU": "Y", "UAC": "Y", "UAA": "STOP", "UAG": "STOP",
            "UGU": "C", "UGC": "C", "UGA": "STOP", "UGG": "W",
            "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
            "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
            "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
            "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
            "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
            "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
            "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
            "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
            "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
            "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
            "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
            "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
        }

        if not isinstance(sequence, RNA):
            raise TypeError("Error: Sequence must be of type RNA.")

        protein_seq = ""

        for i in range(0, len(sequence), 3):
            codon = sequence[i:i + 3]
            if peptide_table.get(codon) == "STOP":
                protein_seq += "*"
                break

            if (peptide := peptide_table.get(codon)) is None:
                protein_seq += "X"
            else:
                protein_seq += peptide

        return Protein(protein_seq)

    def _transcribe(self, sequence: DNA) -> RNA:
        """
        Transcribes a given DNA sequence into an RNA sequence.
        Sequence provided must be of type DNA.
        """
        if not isinstance(sequence, DNA):
            raise TypeError("Error: Sequence must be of type DNA")

        rna_sequence = sequence.replace("T", "U")
        return RNA(rna_sequence)

    def _reverse_complement(self, sequence: DNA | RNA) -> DNA | RNA:
        """
        Returns the reverse complement of a given DNA sequence.
        Sequence provided must be of type DNA.
        """
        if not isinstance(sequence, (DNA, RNA)):
            raise TypeError("Error: Sequence must be of type DNA or RNA")

        if isinstance(sequence, DNA):
            reverse_complement = sequence.translate(str.maketrans("ATGCatgc", "TACGtacg"))[::-1]
            return DNA(reverse_complement)

        if isinstance(sequence, RNA):
            reverse_complement = sequence.translate(str.maketrans("AUGCaugc", "UACGuacg"))[::-1]
            return RNA(reverse_complement)
