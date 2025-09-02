# Documentation

This document provides detailed technical documentation for GeneAnalyzer2's classes, methods, and internal structure.

## Table of Contents

1. [Usage](#usage)
2. [Core Classes](#core-classes)
3. [Analysis Classes](#analysis-classes)
4. [File Handler](#file-handler)
5. [Exception Classes](#exception-classes)

## Usage
- [Basic Mode](#basic-mode)
- [File Conversion Mode](#file-conversion-mode)

### Basic Mode
Basic mode (`--mode basic`) is the default mode for the GeneAnalyzer2 CLI tool. It proivdes basic sequence analysis on files and strings containing DNA, RNA or protein sequences.  Below is a list of available analysis.
- [base count](#base-count)
- [translation](#translation)
- [transcription](#transcription)
- [gc percent](#gc-percent)
- [ORF finder](#orf-finder)
- [reverse complement](#reverse-complement)

#### Base Count
`base_count` is a method that counts the occurrences of each nucleotide base in a DNA or RNA sequence. 

**Inputs:** DNA or RNA string containing any of the standard sequence letter notations from the following:

| Description | Symbol |
|-------------|--------|
| Adenine     | A      |
| Cytosine    | C      |
| Guanine     | G      |
| Thymine     | T      |
| Uracil      | U      |


These common sequence letter notations are ignored in this analysis:

| Description | Symbol |
|-------------|--------|
| Not A       | B      |
| Not C       | D      |
| Not G       | H      |
| Not T       | V      |
| Any Base    | N      |
| Gap         | -      |

**Output**: A dictionary of key value pairs of A, T, G, C, or U with the respecive count for each nucleotide found in the provided sequence. 

```sh
# Input
geneanalyzer2 --mode basic --type DNA --analysis base_count

# Output
input_sequence: {'A': 3, 'T': 3, 'G': 5, 'C': 3}
```

This analysis works with both string input and file input. 

#### Translation
Translate an RNA sequence to a protein sequence using the genetic code.
```sh

```
#### Transcription
Transcribe a DNA sequence to RNA by replacing T with U.
```sh

```
#### GC Percent
Calculate the GC content percentage of a DNA or RNA sequence.
```sh

```
#### ORF Finder
Find all open reading frames (ORFs) in a DNA or RNA sequence.
```sh

```
#### Reverse Complement
Generate the reverse complement of a DNA or RNA sequence.
```sh

```


### File Conversion Mode
File conversion mode (`--mode file_conv`) provides file format conversion operations. Below is a list of methods that can be done in this mode.
- [convert](#convert)
- [validate](#validate)
- [batch convert](#batch-convert)

## Core Classes

### Sequence Classes

#### `geneanalyzertool.core.sequences.Sequence`

Base class for all sequence types.

```python
class Sequence(str):
    """
    Abstract base class for all sequence type data.
    
    Args:
        sequence (str): The sequence string data
        
    Returns:
        Sequence: A new sequence instance
    """
```

#### `geneanalyzertool.core.sequences.DNA`

```python
class DNA(Sequence):
    """
    DNA sequence class for representing deoxyribonucleic acid sequences.
    Expected to contain nucleotides A, T, G, C.
    """
```

#### `geneanalyzertool.core.sequences.RNA`

```python
class RNA(Sequence):
    """
    RNA sequence class for representing ribonucleic acid sequences.
    Expected to contain nucleotides A, U, G, C.
    """
```

#### `geneanalyzertool.core.sequences.Protein`

```python
class Protein(Sequence):
    """
    Protein sequence class for representing amino acid sequences.
    Expected to contain standard amino acid letters.
    """
```

## Analysis Classes

### Basic Analysis

#### `geneanalyzertool.analysis.basic_analysis.BasicSequenceAnalysis`

Primary analysis class providing fundamental sequence analysis methods.

##### Methods:

**`gc_percent(sequence: Sequence) -> float`**
```python
def gc_percent(self, sequence: Sequence) -> float:
    """
    Calculate the GC content percentage of a DNA or RNA sequence.
    
    Args:
        sequence (Sequence): DNA or RNA sequence to analyze
        
    Returns:
        float: GC content as a percentage (0-100)
        
    Raises:
        InvalidSequenceTypeError: If sequence is not DNA or RNA
    """
```

**`base_count(sequence: Sequence) -> dict`**
```python
def base_count(self, sequence: Sequence) -> dict:
    """
    Count the occurrences of each nucleotide base in a DNA or RNA sequence.
    
    Args:
        sequence (Sequence): DNA or RNA sequence to analyze
        
    Returns:
        dict: Dictionary with base counts {'A': count, 'T/U': count, 'G': count, 'C': count}
        
    Raises:
        InvalidSequenceTypeError: If sequence is not DNA or RNA
    """
```

**`transcribe(sequence: DNA) -> RNA`**
```python
def transcribe(self, sequence: DNA) -> RNA:
    """
    Transcribe a DNA sequence to RNA by replacing T with U.
    
    Args:
        sequence (DNA): DNA sequence to transcribe
        
    Returns:
        RNA: Transcribed RNA sequence
        
    Raises:
        InvalidSequenceTypeError: If sequence is not DNA
    """
```

**`translate(sequence: RNA) -> Protein`**
```python
def translate(self, sequence: RNA) -> Protein:
    """
    Translate an RNA sequence to a protein sequence using the genetic code.
    
    Args:
        sequence (RNA): RNA sequence to translate
        
    Returns:
        Protein: Translated protein sequence
        
    Raises:
        InvalidSequenceTypeError: If sequence is not RNA
    """
```

**`reverse_complement(sequence: Sequence) -> Sequence`**
```python
def reverse_complement(self, sequence: Sequence) -> Sequence:
    """
    Generate the reverse complement of a DNA or RNA sequence.
    
    Args:
        sequence (Sequence): DNA or RNA sequence to reverse complement
        
    Returns:
        Sequence: Reverse complement sequence of the same type
        
    Raises:
        InvalidSequenceTypeError: If sequence is not DNA or RNA
    """
```

**`orf(sequence: Sequence) -> list`**
```python
def orf(self, sequence: Sequence) -> list:
    """
    Find all open reading frames (ORFs) in a DNA or RNA sequence.
    
    Args:
        sequence (Sequence): DNA or RNA sequence to analyze
        
    Returns:
        list: List of ORF dictionaries containing position, length, and sequence information
        
    Raises:
        InvalidSequenceTypeError: If sequence is not DNA or RNA
    """
```

### File Conversion

#### `geneanalyzertool.analysis.file_conversion.FileConversion`

Handles file format conversion operations.

##### Methods:

**`convert(file_path: str, out_dir: str = None) -> str`**
```python
def convert(self, file_path: str, out_dir: str = None) -> str:
    """
    Convert a FASTQ file to FASTA format.
    
    Args:
        file_path (str): Path to the input FASTQ file
        out_dir (str, optional): Output directory for converted file
        
    Returns:
        str: Path to the converted FASTA file
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        InvalidFileFormatError: If input file is not valid FASTQ
    """
```

**`validate(file_path: str) -> bool`**
```python
def validate(self, file_path: str) -> bool:
    """
    Validate that a file is in proper FASTQ format.
    
    Args:
        file_path (str): Path to the file to validate
        
    Returns:
        bool: True if file is valid FASTQ, False otherwise
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
```

**`batch_convert(input_dir: str, out_dir: str = None) -> list`**
```python
def batch_convert(self, input_dir: str, out_dir: str = None) -> list:
    """
    Convert multiple FASTQ files to FASTA format in batch.
    
    Args:
        input_dir (str): Directory containing FASTQ files
        out_dir (str, optional): Output directory for converted files
        
    Returns:
        list: List of paths to converted FASTA files
        
    Raises:
        FileNotFoundError: If input directory doesn't exist
    """
```

## File Handler

### `geneanalyzertool.core.file_handler.FileHandler`

Handles file operations for sequence analysis.

#### Methods:

**`select_files(start_dir: str) -> list`**
```python
def select_files(self, start_dir: str) -> list:
    """
    Interactive file selection from a directory.
    
    Args:
        start_dir (str): Starting directory for file selection
        
    Returns:
        list: List of selected file paths
        
    Raises:
        FileNotFoundError: If directory doesn't exist
    """
```

**`read_sequences_from_fasta(file_path: str) -> list`**
```python
def read_sequences_from_fasta(self, file_path: str) -> list:
    """
    Read sequences from a FASTA file.
    
    Args:
        file_path (str): Path to the FASTA file
        
    Returns:
        list: List of Bio.SeqRecord objects
        
    Raises:
        FileNotFoundError: If file doesn't exist
        InvalidFileFormatError: If file is not valid FASTA
    """
```

**`write_results_to_file(results: str, output_path: str) -> None`**
```python
def write_results_to_file(self, results: str, output_path: str) -> None:
    """
    Write analysis results to a file.
    
    Args:
        results (str): Results to write
        output_path (str): Path for the output file
        
    Raises:
        PermissionError: If unable to write to the specified path
    """
```

## Exception Classes

### `geneanalyzertool.core.exceptions.InvalidSequenceTypeError`

```python
class InvalidSequenceTypeError(Exception):
    """
    Raised when an analysis method receives an incompatible sequence type.
    
    Args:
        message (str): Error description
        sequence_type (str): The invalid sequence type that was provided
        expected_types (list): List of expected sequence types
    """
```

### `geneanalyzertool.core.exceptions.InvalidFileFormatError`

```python
class InvalidFileFormatError(Exception):
    """
    Raised when a file is not in the expected format.
    
    Args:
        message (str): Error description
        file_path (str): Path to the invalid file
        expected_format (str): The expected file format
    """
```

### `geneanalyzertool.core.exceptions.SequenceError`

```python
class SequenceError(Exception):
    """
    Raised when there's an issue with sequence data or processing.
    
    Args:
        message (str): Error description
        sequence (str, optional): The problematic sequence
    """
```
