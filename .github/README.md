<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/walla-42/GeneAnalyzer2">
    <img src="/docs/images/readme_images/GeneAnalyzer2Logo.png" alt="Logo">
  </a>
</div>

# GeneAnalyzer2

GeneAnalyzer2 is a command-line bioinformatics tool for analyzing DNA, RNA, and protein sequences. It supports a variety of analyses, including GC content, base counting, transcription, translation, reverse complement strand synthesis, and now a new open reading frame finder. The tool can process both raw sequence strings and multi-sequence FASTA files.

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
If you would like to work on this project, view how to contribute <a href="/.github/CONTRIBUTING.md">here</a>.

## Usage

You can run GeneAnalyzer2 using Poetry's script entry point or directly with Python. The CLI supports both raw sequence and FASTA file input.

### Command Line Arguments

- `-f`, `--file` (optional): Treat the sequence argument as a file path (FASTA format).
- `sequence/sequence_file` (positional): The raw sequence string or path to a FASTA file.
- `-t`, `--type` (required): Sequence type (`DNA`, `RNA`, or `Protein`).
- `-m`, `--mode` (optional): Analysis mode/class (default: `basic`).
- `-a`, `--analysis` (required): Analysis type (e.g., `gc_percent`, `base_count`, `transcribe`, `translate`, `reverse_complement`, `orf`).
- `-o`, `--out` (optional): Output file (default: print to terminal).

---

## Examples

### 1. Analyze a Raw DNA Sequence

```sh
geneanalyzer2 --type DNA --analysis gc_percent "ATGCGTACGTAGCTAGCTAGGCTAGCTAGCTGACTGACTGATCGATCGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
```

### 2. Transcribe a Raw DNA Sequence

```sh
geneanalyzer2 --type DNA --analysis transcribe "ATGCGTACGTAGCTAGCTAGGCTAGCTAGCTGACTGACTGATCGATCGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
```

### 3. Analyze All Sequences in a FASTA File

```sh
geneanalyzer2 --file test_sequences.fasta --type DNA --analysis base_count
```

### 4. Output Results to a File

```sh
geneanalyzer2 --file test_sequences.fasta --type DNA --analysis gc_percent --out results.txt
```
## Whats New
- Easier to view terminal output and better file save handling

<div align="center">
  <img src="/docs/images/readme_images/Improved_text_generation_output.png" alt="Improved Terminal Text">
</div>

- New open reading frame finder in basic mode

<div align="center">
  <img src="/docs/images/readme_images/orf_method.png" alt="ORF Method Terminal Output">
</div>

- GC percent calculations now have '%' after the calculated value

<div align="center">  
  <img src="/docs/images/readme_images/updated_gc.png" alt="Updated GC Output">
</div>

- Error handling has been improved with better user end messages

<div align="center">
  <img src="/docs/images/readme_images/error_message.png" alt="Example Error Message">
</div>

## License

MIT License
