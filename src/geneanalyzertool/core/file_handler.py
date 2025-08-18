from Bio import SeqIO
from typing import List


class FileHandler():
    """Handles file operations for GeneAnalyzer2 tool."""

    def __init__(self):
        pass

    def export_to_file(self, results: List[str], out_file: str):
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

        print("Available sequences:")
        for idx, record_id in enumerate(keys, 1):
            print(f"{idx}. {record_id}")

        for _ in range(max_attempts):
            select = selection_func(
                'Select a sequence by number, or type "all" for all sequences:\n>>> '
            ).strip().lower()

            if select == "all":
                return sequences, keys

            if select.isdigit():
                index = int(select) - 1
                if 0 <= index < len(keys):
                    record_id = keys[index]
                    seq = sequences[record_id]

                    print(f"ID: {record_id}")
                    print(f"Length: {len(seq)}")
                    return {record_id: seq}, [record_id]

            print('\033[1;31mInvalid selection. Please try again.\033[0m')

        raise ValueError("Error: Maximum attempts exceeded. No valid sequences selected.")
