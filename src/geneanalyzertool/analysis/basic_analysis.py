from geneanalyzertool.analysis.analysis import Analysis
from geneanalyzertool.core.sequences import Sequence, DNA, RNA, Protein
from geneanalyzertool.core.file_handler import FileHandler
from typing import Any, override, List
from geneanalyzertool.core.exceptions import InvalidSequenceTypeError, AnalysisMethodError

YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
RESET = "\033[0m"
CYAN = "\033[1;36m"


class BasicSequenceAnalysis(Analysis, FileHandler):
    """
    Class for basic analysis performed on dna, rna or protein sequences. This class holds all the basic mode functionality.
    It extends the Analysis class and implements the FileHandler interface.

    Note: If you are adding a method to the Basic analysis mode, add your method below and add a call to your method in the
    analyze method. Make sure your method is private (pythonic private) by adding an underscore "_" before the method name.
    """

    @override
    def export_to_file(self, results: dict, sequence_keys: List[str], out_file: str):
        def format_orf_result(seq_name, orf_result):
            lines = [f"Sequence Name: {seq_name}"]
            lines.append(f"Number of ORFs: {orf_result['Number of ORFS']}")
            for orf_name, orf_data in orf_result['ORFS'].items():
                lines.append(f"{orf_name}: {orf_data['Sequence']}")
                lines.append(f"  Start: {orf_data['Start']} End: {orf_data['End']} Length: {orf_data['Length']}")
            return "\n".join(lines)

        with open(out_file, 'w') as out:
            for seq in sequence_keys:
                value = results[seq]
                if isinstance(value, dict) and 'ORFS' in value:
                    out.write(format_orf_result(seq, value) + "\n\n")
                else:
                    out.write(f"{seq}: {value}\n")

    @override
    def print_to_terminal(self, results: dict, sequence_keys: List[str]):
        def format_orf_result(seq_name, orf_result):
            lines = [f"{YELLOW}Sequence Name: {RESET}{seq_name}"]
            lines.append(f"{GREEN}Number of ORFs:{RESET} {orf_result['Number of ORFS']}")
            for orf_name, orf_data in orf_result['ORFS'].items():
                lines.append(f"{GREEN}{orf_name}:{RESET} {orf_data['Sequence']}")
                lines.append(f"  {CYAN}Start:{RESET} {orf_data['Start']} {CYAN}End:{RESET} {orf_data['End']}\
                              {CYAN}Length:{RESET} {orf_data['Length']}")
            return "\n".join(lines)

        for seq in sequence_keys:
            value = results[seq]
            if isinstance(value, dict) and 'ORFS' in value:
                print(format_orf_result(seq, value) + "\n")
            else:
                print(f"{YELLOW}{seq}{RESET}: {value}")

    @override
    def analyze(self, sequence: Sequence, method: str) -> Any:
        """
        executes simple analysis of protein, RNA or DNA sequences.
        Args:
            sequence: Sequence object to analyze
            method: Analysis method to perform
        Returns:
            Result of analysis

        Note: If adding a method to the basic analysis options, add it also in the method dispatch below.
        """
        method_dispatch = {
            "gc_percent": self._gc_percent,
            "base_count": self._base_count,
            "translate": self._translate,
            "transcribe": self._transcribe,
            "reverse_complement": self._reverse_complement,
            "orf": self._orf_finder
        }

        if method not in method_dispatch:
            raise ValueError(f"Unknown method {method}")

        return method_dispatch[method](sequence)

    def process_sequences(self, sequence_input: str, is_file: bool, seq_type: str, analysis_method: str):
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
        results = {}
        for key in sequence_keys:
            sequence_obj = seq_type_class(available_sequences[key])
            try:
                result = self.analyze(sequence_obj, analysis_method)
                results[key] = result
            except ValueError as e:
                raise AnalysisMethodError(f"Invalid analysis method provided. {str(e)}")
            except TypeError as e:
                raise InvalidSequenceTypeError(f"Unable to perform this analysis on sequence of type {seq_type.upper()}. {e}")

        return results, sequence_keys

    def _gc_percent(self, sequence: DNA | RNA, ) -> str:
        """
        Calculates the percent Guanine and Cytosine that are present in a DNA or RNA Molecule.
        Sequence must be of type RNA or DNA.
        """
        if not isinstance(sequence, (DNA, RNA)):
            raise TypeError("Error: Sequence must be of type DNA or RNA")

        gc_count = sequence.upper().count("G") + sequence.upper().count("C")
        return f"{round((gc_count / len(sequence)) * 100, 2)} %"

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

    def _orf_finder(self, sequence: DNA):
        if not isinstance(sequence, DNA):
            raise TypeError("Error: Sequence must be of type DNA")

        start_codons = ["ATG"]
        stop_codons = ["TAA", "TAG", "TGA"]
        ORFS = {}
        ORF_count = 0
        for i in range(0, len(sequence)):
            codon = sequence[i:i + 3]
            if codon not in start_codons:
                continue
            for j in range(i, len(sequence), 3):
                codon = sequence[j:j + 3]
                if codon in stop_codons:
                    ORF_count += 1
                    orf_name = f"ORF_{ORF_count}"
                    orf_seq = sequence[i:j+3]
                    ORFS[orf_name] = {
                        "Sequence": orf_seq,
                        "Start": i,
                        "End": j + 2,
                        "Length": (j + 3) - i
                    }
                    break
        if len(ORFS) == 0:
            ORFS = "No Open Reading Frames"
        result = {
            "Number of ORFS": ORF_count,
            "ORFS": ORFS
        }
        return result
