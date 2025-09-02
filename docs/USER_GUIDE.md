# User Guide

Welcome to GeneAnalyzer2! This guide will help you install and get started with the command-line bioinformatics tool for analyzing DNA, RNA, and protein sequences.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Basic Usage](#basic-usage)
4. [Documentation Links](#documentation-links)

## Installation

### System Requirements

- **Python**: 3.12 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: At least 512MB RAM (more recommended for large files)

### Simple Installation (Recommended for Users)

Install GeneAnalyzer2 directly from GitHub using pip:

```bash
pip install git+https://github.com/Walla-42/GeneAnalyzer2.git
```

After installation, verify it works:
```bash
geneanalyzer2 --help
```

## Quick Start

### Basic Commands

Once installed, you can use the `geneanalyzer2` command:

```bash
# Calculate GC content of a DNA sequence
geneanalyzer2 --type DNA --analysis gc_percent "ATGCGCGCATGC"

# Find Open Reading Frames
geneanalyzer2 --type DNA --analysis orf "ATGGGGGCGCGCGCGCGCGCGCGCGCGAGTTAG"

# Convert FASTQ to FASTA
geneanalyzer2 --mode file_conv --analysis convert --file sequences.fastq
```

### Getting Help

View all available options:
```bash
geneanalyzer2 --help
```

## Basic Usage

### Command Structure

GeneAnalyzer2 commands follow this general pattern:

```bash
geneanalyzer2 [--mode MODE] --type TYPE --analysis ANALYSIS [sequence/file] [options]
```

### Analysis Modes

GeneAnalyzer2 has two main modes:

1. **Basic Mode** (`--mode basic` or default): Sequence analysis operations
2. **File Conversion Mode** (`--mode file_conv`): File format conversion operations

### Sequence Types

When analyzing sequences, specify the type:
- `DNA`: For DNA sequences (A, T, G, C)
- `RNA`: For RNA sequences (A, U, G, C)  
- `Protein`: For protein sequences (amino acids)

### Input Methods

You can provide sequences in two ways:

1. **Direct sequence input**: Provide the sequence as a command argument
   ```bash
   geneanalyzer2 --type DNA --analysis gc_percent "ATGCATGC"
   ```

2. **FASTA file input**: Use the `--file` option
   ```bash
   geneanalyzer2 --file sequences.fasta --type DNA --analysis gc_percent
   ```

### Output Methods
You can specify an output file using the `--out` option. If not provided, results will be printed to the console.

```bash
geneanalyzer2 --type DNA --analysis gc_percent "ATGCATGC" --out output_file.txt
```

### Available Analyses

#### Basic Mode Analyses
- `gc_percent`: Calculate GC content percentage (DNA/RNA)
- `base_count`: Count nucleotide bases (DNA/RNA)
- `transcribe`: Transcribe DNA to RNA (DNA only)
- `translate`: Translate RNA to protein (RNA only)
- `reverse_complement`: Generate reverse complement (DNA/RNA)
- `orf`: Find Open Reading Frames (DNA/RNA)

#### File Conversion Analyses
- `convert`: Convert FASTQ to FASTA format
- `validate`: Validate FASTQ file format
- `batch_convert`: Convert multiple FASTQ files to FASTA format

### Examples

#### Simple Sequence Analysis
```bash
# GC content
geneanalyzer2 --type DNA --analysis gc_percent "ATGCATGC"

# Base counting  
geneanalyzer2 --type DNA --analysis base_count "ATGCATGC"

# Transcription
geneanalyzer2 --type DNA --analysis transcribe "ATGCATGC"
```

#### File Conversion
```bash
# Convert single file
geneanalyzer2 --mode file_conv --analysis convert --file data.fastq --out data.fasta

# Validate file format
geneanalyzer2 --mode file_conv --analysis validate --file data.fastq

# Batch convert directory
geneanalyzer2 --mode file_conv --analysis batch_convert --file "file1.fastq file2.fastq"
```

## Documentation Links

For more detailed information, see our documentation:

- **[Examples](EXAMPLES.md)** - Practical examples and command references
- **[Documentation](DOCUMENTATION.md)** - Technical documentation of all classes and methods  
- **[Developer Guide](CONTRIBUTING.md)** - How to extend GeneAnalyzer2 and contribute new features
