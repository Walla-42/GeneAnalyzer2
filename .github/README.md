<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/walla-42/GeneAnalyzer2">
    <img src="/docs/images/readme_images/GeneAnalyzer2Logo.png" alt="Logo">
  </a>
</div>

# GeneAnalyzer2

GeneAnalyzer2 is a command-line bioinformatics tool for analyzing DNA, RNA, and protein sequences. It supports a variety of analyses, including GC content, base counting, transcription, translation, reverse complement strand synthesis, open reading frame finding, and file format conversion. The tool can process both raw sequence strings and multi-sequence FASTA files, and includes powerful file conversion capabilities.

This program replaces the original GeneAnalyzer interactive command line program which can be found <a href="http://github.com/walla-42/GeneAnalyzer">here</a>.

---

## Features

### Sequence Analysis
- Analyze DNA, RNA, or protein sequences
- GC content calculation with percentage formatting
- Nucleotide base counting
- DNA transcription to RNA
- RNA translation to protein
- Reverse complement generation
- Open Reading Frame (ORF) detection for both DNA and RNA
- Support for both raw sequence input and FASTA file input

### File Operations
- **File Format Conversion**: Convert FASTQ files to FASTA format
- **Batch Processing**: Convert multiple files simultaneously
- **File Validation**: Validate FASTQ file format and integrity
- **Multi-sequence Support**: Process multiple sequences from FASTA files

### Output & Usability
- Colored terminal output for better readability
- Save results to files
- Improved error handling with informative messages
- Modular, extensible design for future analyses

---

## Documentation

📚 **Comprehensive Documentation Available:**

- **[User Guide](docs/USER_GUIDE.md)** - Installation and getting started  
- **[Examples](docs/EXAMPLES.md)** - Command reference and practical examples
- **[Documentation](docs/DOCUMENTATION.md)** - Technical documentation of classes and methods
- **[Developer Guide](docs/DEVELOPER.md)** - How to extend and contribute to the project

---



## Quick Start

### Basic Installation
```sh
pip install git+https://github.com/Walla-42/GeneAnalyzer2.git
```

### Simple Usage Examples

```bash
# Calculate GC content
geneanalyzer2 --type DNA --analysis gc_percent "ATGCATGC"

# Find Open Reading Frames
geneanalyzer2 --type DNA --analysis orf "ATGGGGGCGCGCGCGCGCGCGCGCGCGAGTTAG"

# Convert FASTQ to FASTA
geneanalyzer2 --mode file_conv --analysis convert --file sequences.fastq

# Analyze sequences from FASTA file
geneanalyzer2 --file sequences.fasta --type DNA --analysis gc_percent --out results.txt
```

For detailed instructions, see the [User Guide](docs/USER_GUIDE.md).

---

## Analysis Modes

### Basic Mode (`--mode basic`)
Sequence analysis operations:

| Analysis | Description | Input Types |
|----------|-------------|-------------|
| `gc_percent` | Calculate GC content percentage | DNA, RNA |
| `base_count` | Count nucleotide bases | DNA, RNA |  
| `transcribe` | Transcribe DNA to RNA | DNA |
| `translate` | Translate RNA to protein | RNA |
| `reverse_complement` | Generate reverse complement | DNA, RNA |
| `orf` | Find Open Reading Frames | DNA, RNA |

### File Conversion Mode (`--mode file_conv`)
File format operations:

| Analysis | Description | Input | Output |
|----------|-------------|-------|--------|
| `convert` | Convert file format | FASTQ | FASTA |
| `validate` | Validate file format | FASTQ | Validation report |
| `batch_convert` | Convert multiple files | Multiple FASTQ | Multiple FASTA |

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
  <img src="/docs/images/readme_images/option_handling.png" alt="Improved option handling">
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
