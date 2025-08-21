from Bio import SeqIO
from typing import List
from geneanalyzertool.core.exceptions import SequenceParsingError

YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
RESET = "\033[0m"
CYAN = "\033[1;36m"


class FileHandler():
    """Handles file operations for GeneAnalyzer2 tool."""

    def __init__(self):
        pass

    def export_to_file(self, results: dict, sequence_keys: List[str], out_file: str):
        raise NotImplementedError("Subclasses must implement this method.")

    def file_support_check(self, file: str) -> bool:
        """Check if the file has a supported extension (.fna or .fasta)."""
        if file.endswith(".fna") or file.endswith(".fasta"):
            print('\033[1;33mOpening and parsing file...\033[0m')
            return True
        else:
            print('\033[1;31mFile type not supported. Please select a .fna or .fasta file.\033[0m')
            return False

    def read_sequences(self, fasta_file: str) -> dict:
        """Parse all sequences from a FASTA file into a dictionary."""
        sequence_dict = {}
        for record in SeqIO.parse(fasta_file, 'fasta'):
            sequence_dict[record.id] = record.seq
        return sequence_dict

    def select_sequences(self, fasta_file: str, selection_func=input, max_attempts: int = 3):
        """User-guided sequence selection with numbered options.

        Args:
            fasta_file: Path to the FASTA file.
            selection_func: Function to get user input (can be mocked in tests).
            max_attempts: Maximum number of invalid attempts before raising an error.

        Returns:
            Tuple[dict, list]: Selected sequences dictionary and ordered list of keys.
        """
        sequences = self.read_sequences(fasta_file)
        keys = list(sequences.keys())

        print(YELLOW + "Available sequences:" + RESET)
        for idx, record_id in enumerate(keys, 1):
            print(f"{CYAN}{idx}.{GREEN} {record_id}{RESET}")

        for _ in range(max_attempts):
            select = selection_func(YELLOW +
                                    'Select a sequence by number, or type "all" for all sequences:\n>>> ' + RESET
                                    ).strip().lower()

            if select == "all":
                return sequences, keys

            if select.isdigit():
                index = int(select) - 1
                if 0 <= index < len(keys):
                    record_id = keys[index]
                    seq = sequences[record_id]

                    print(f"{YELLOW}Name:{GREEN} {record_id}{RESET}")
                    print(f"{YELLOW}Length:{RESET} {len(seq)}")
                    return {record_id: seq}, [record_id]

            print(f'{RED}Invalid selection. Please try again.{RESET}')

        raise SequenceParsingError("Error: Maximum attempts exceeded. No valid sequences selected.")
