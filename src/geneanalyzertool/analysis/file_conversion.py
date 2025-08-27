import os
from typing import Any, override, List
from geneanalyzertool.analysis.analysis import Analysis
from geneanalyzertool.core.file_handler import FileHandler
from geneanalyzertool.core.sequences import Sequence
from geneanalyzertool.core.exceptions import AnalysisMethodError, SequenceParsingError

YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
RESET = "\033[0m"
CYAN = "\033[1;36m"


class FileConversion(Analysis, FileHandler):
    """
    Class for file format conversion operations.
    Supports conversion between common bioinformatics file formats.
    """

    @override
    def analyze(self, sequence: Sequence, method: str) -> Any:
        """
        Not implemented for file conversion as it operates on files rather than sequence objects.
        
        Args:
            sequence (Sequence): Sequence object (not used)
            method (str): Analysis method (not used)
            
        Raises:
            AnalysisMethodError: Always raised as this method is not supported
        """
        raise AnalysisMethodError("File conversion operates on files, not individual sequences. Use process_sequences instead.")

    @override
    def process_sequences(self, sequence_input: str, is_file: bool, seq_type: str, analysis_method: str):
        """
        Process file conversion operations.

        Args:
            sequence_input (str): File path (or pattern for batch operations)
            is_file (bool): Must be True for file conversion
            seq_type (str): Not used in file conversion
            analysis_method (str): Type of conversion (e.g., 'convert', 'validate', 'batch_convert')

        Returns:
            Tuple[dict, List[str]]: Results dictionary and sequence keys
        """
        if not is_file:
            raise AnalysisMethodError("Error: File conversion requires a file input. Use --file flag.")

        # Handle conversion methods
        if analysis_method == "convert":
            return self._handle_conversion(sequence_input)
        elif analysis_method == "validate":
            return self._handle_validation(sequence_input)
        elif analysis_method == "batch_convert":
            return self._handle_batch_conversion(sequence_input)
        else:
            raise AnalysisMethodError(f"Error: Unknown file conversion method: {analysis_method}")

    def _handle_conversion(self, file_path: str):
        """
        Handle file conversion based on input file extension.
        
        Args:
            file_path (str): Path to the file to convert
            
        Returns:
            Tuple[dict, List[str]]: Dictionary with conversion result and list of sequence keys
        """
        if not os.path.exists(file_path):
            raise SequenceParsingError(f"Error: File not found: {file_path}")

        file_ext = file_path.lower().split('.')[-1]

        # If you are adding additional file conversions, add the extension here
        if file_ext in ['fastq', 'fq']:
            result = self._fastq_to_fasta(file_path)
            return {"conversion_result": result}, ["conversion_result"]
        else:
            raise AnalysisMethodError(f"Error: Unsupported file format for conversion: {file_ext}")

    def _handle_validation(self, file_path: str):
        """
        Handle file validation based on input file extension.
        
        Args:
            file_path (str): Path to the file to validate
            
        Returns:
            Tuple[dict, List[str]]: Dictionary with validation result and list of sequence keys
        """
        if not os.path.exists(file_path):
            raise SequenceParsingError(f"Error: File not found: {file_path}")

        file_ext = file_path.lower().split('.')[-1]

        if file_ext in ['fastq', 'fq']:
            stats = self.validate_fastq(file_path)
            if stats["valid"]:
                result = f"Valid FASTQ file: {stats['total_records']} records found"
            else:
                error_summary = "; ".join(stats["errors"][:3])
                if len(stats["errors"]) > 3:
                    error_summary += f" (and {len(stats['errors']) - 3} more errors)"
                result = f"Invalid FASTQ file: {error_summary}"
            return {"validation_result": result}, ["validation_result"]
        else:
            raise AnalysisMethodError(f"Unsupported file format for validation: {file_ext}")

    def _handle_batch_conversion(self, file_paths_string: str):
        """
        Handle batch conversion of multiple files.

        Args:
            file_paths_string (str): Comma-separated string of file paths

        Returns:
            Tuple[dict, List[str]]: Results dictionary and sequence keys
        """
        # Parse comma-separated file paths
        file_paths = [path.strip() for path in file_paths_string.split(',') if path.strip()]

        if not file_paths:
            raise SequenceParsingError("Error: No file paths provided for batch conversion")

        results = self.batch_convert(file_paths)

        # Create a dictionary with numbered results
        result_dict = {}
        sequence_keys = []
        for i, result in enumerate(results, 1):
            key = f"batch_result_{i}"
            result_dict[key] = result
            sequence_keys.append(key)

        return result_dict, sequence_keys

    def _fastq_to_fasta(self, fastq_file: str) -> str:
        """
        Convert FASTQ file to FASTA format.

        Args:
            fastq_file: Path to input FASTQ file

        Returns:
            Path to output FASTA file
        """
        base_name = os.path.splitext(fastq_file)[0]
        fasta_file = f"{base_name}.fasta"

        record_count = 0

        try:
            with open(fastq_file, 'r') as infile, open(fasta_file, 'w') as outfile:
                while True:
                    header = infile.readline().strip()
                    if not header:
                        break

                    sequence = infile.readline().strip()
                    plus_line = infile.readline().strip()

                    # Ignore this line - its here to read past the quality scores
                    infile.readline().strip()

                    # Validate FASTQ format
                    if not header.startswith('@'):
                        raise SequenceParsingError(f"Invalid FASTQ format: Expected '@' at line start, got '{header[:10]}...'")
                    if not plus_line.startswith('+'):
                        raise SequenceParsingError(f"Invalid FASTQ format: Expected '+' at line start, got '{plus_line[:10]}...'")

                    # Write FASTA format (convert @ to >)
                    fasta_header = '>' + header[1:]
                    outfile.write(f"{fasta_header}\n")
                    outfile.write(f"{sequence}\n")

                    record_count += 1

        except Exception as e:
            # Clean up output file if conversion failed
            if os.path.exists(fasta_file):
                os.remove(fasta_file)
            raise SequenceParsingError(f"Error converting FASTQ to FASTA: {str(e)}")

        return f"Successfully converted {record_count} sequences from {fastq_file} to {fasta_file}"

    def batch_convert(self, file_paths: List[str]) -> List[str]:
        """
        Convert multiple files to FASTA format.

        Args:
            file_paths: List of file paths to convert

        Returns:
            List of conversion results for each file
        """
        if not file_paths:
            raise SequenceParsingError("Error: No file paths provided for batch conversion")

        results = []
        for file_path in file_paths:
            try:
                # Check if file exists before attempting conversion
                if not os.path.exists(file_path):
                    results.append(f"Error: File not found: {file_path}")
                    continue

                result = self._fastq_to_fasta(file_path)
                results.append(result)
            except Exception as e:
                results.append(f"Warning: Failed to convert {file_path}: {str(e)}")

        return results

    def validate_fastq(self, fastq_file: str) -> dict:
        """
        Validate FASTQ file format and return statistics.

        Args:
            fastq_file: Path to FASTQ file

        Returns:
            Dictionary with validation results and statistics
        """
        stats = {
            "valid": True,
            "total_records": 0,
            "errors": [],
            "warnings": []
        }

        try:
            with open(fastq_file, 'r') as infile:
                line_num = 0
                record_num = 0

                while True:
                    header = infile.readline()
                    if not header:
                        break

                    line_num += 1
                    record_num += 1

                    sequence = infile.readline()
                    plus_line = infile.readline()
                    quality = infile.readline()

                    line_num += 3

                    if not sequence or not plus_line or not quality:
                        stats["errors"].append(f"Record {record_num}: Incomplete FASTQ record")
                        stats["valid"] = False
                        break

                    # Validate format
                    if not header.strip().startswith('@'):
                        stats["errors"].append(f"Record {record_num}: Invalid header format at line {line_num-3}")
                        stats["valid"] = False

                    if not plus_line.strip().startswith('+'):
                        stats["errors"].append(f"Record {record_num}: Invalid plus line format at line {line_num-1}")
                        stats["valid"] = False

                    if len(sequence.strip()) != len(quality.strip()):
                        stats["errors"].append(f"Record {record_num}: Sequence and quality length mismatch")
                        stats["valid"] = False

                stats["total_records"] = record_num

        except Exception as e:
            stats["valid"] = False
            stats["errors"].append(f"File reading error: {str(e)}")

        return stats

    @override
    def export_to_file(self, results: dict, sequence_keys: List[str], out_file: str):
        """
        Export conversion results to a file.
        
        Args:
            results (dict): Dictionary mapping sequence keys to conversion results
            sequence_keys (List[str]): Ordered list of sequence identifiers
            out_file (str): Path to output file where results will be written
        """
        with open(out_file, 'w') as outfile:
            for key in sequence_keys:
                outfile.write(f"{results[key]}\n")

    @override
    def print_to_terminal(self, results: dict, sequence_keys: List[str]):
        """
        Print conversion results to terminal with colored formatting.
        
        Args:
            results (dict): Dictionary mapping sequence keys to conversion results
            sequence_keys (List[str]): Ordered list of sequence identifiers
        """
        for key in sequence_keys:
            print(f"{GREEN}{results[key]}{RESET}")
