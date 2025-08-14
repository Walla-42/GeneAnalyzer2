<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/walla-42/GeneAnalyzer2">
    <img src="/docs/images/GeneAnalyzer2Logo.png" alt="Logo">
  </a>
</div>

# GeneAnalyzer2

GeneAnalyzer2 is a command-line bioinformatics tool for analyzing DNA, RNA, and protein sequences. It supports a variety of analyses, including GC content, base counting, transcription, translation, and reverse complement calculation. The tool can process both raw sequence strings and multi-sequence FASTA files.

This program replaces the original GeneAnalyzer interactive command line program which can be found <a href="http://github.com/walla-42/GeneAnalyzer">here</a>.

---

## Features

- Analyze DNA, RNA, or protein sequences
- Supports raw sequence input or FASTA file input
- Multiple analysis modes (easily extensible)
- Output results to terminal or file
- Modular, extensible design for future analyses

---



## Install directly from GitHub
```sh
    pip install git+https://github.com/Walla-42/GeneAnalyzer2.git
```

## Development Setup
If you would like to work on the source code:
```sh
    git clone https://github.com/Walla-42/GeneAnalyzer2.git
    cd GenomeAnalyzer2
    poetry install
    poetry run pytest
```
You can then run the CLI directly from source:

```sh
    poetry run geneanalyzer2 --help
```

## Usage

You can run GeneAnalyzer2 using Poetry's script entry point or directly with Python. The CLI supports both raw sequence and FASTA file input.

### Command Line Arguments

- `-f`, `--file` (optional): Treat the sequence argument as a file path (FASTA format).
- `sequence/sequence_file` (positional): The raw sequence string or path to a FASTA file.
- `-t`, `--type` (required): Sequence type (`DNA`, `RNA`, or `Protein`).
- `-m`, `--mode` (optional): Analysis mode/class (default: `basic`).
- `-a`, `--analysis` (required): Analysis type (e.g., `gc_percent`, `base_count`, `transcribe`, `translate`, `reverse_complement`).
- `-o`, `--out` (optional): Output file (default: print to terminal).

---

## Examples

### 1. Analyze a Raw DNA Sequence (GC Content)

```sh
poetry run geneanalyzer2 --type DNA --analysis gc_percent "ATGCGTACGTAGCTAGCTAGGCTAGCTAGCTGACTGACTGATCGATCGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
```

### 2. Transcribe a Raw DNA Sequence

```sh
poetry run geneanalyzer2 --type DNA --analysis transcribe "ATGCGTACGTAGCTAGCTAGGCTAGCTAGCTGACTGACTGATCGATCGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
```

### 3. Analyze All Sequences in a FASTA File (Base Count)

```sh
poetry run geneanalyzer2 --file test_sequences.fasta --type DNA --analysis base_count
```

### 4. Output Results to a File

```sh
poetry run geneanalyzer2 --file test_sequences.fasta --type DNA --analysis gc_percent --out results.txt
```





## License

MIT License
