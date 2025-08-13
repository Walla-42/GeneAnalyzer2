import argparse
from geneanalyzertool.analysis.basic_analysis import BasicSequenceAnalysis
from geneanalyzertool.core.sequences import DNA, RNA, Protein, Sequence
from geneanalyzertool.analysis.analysis import Analysis


parser = argparse.ArgumentParser(
    prog='GeneAnalyzer2',
    description='Command line bioinformatics tool to analyze DNA, RNA, and protein sequences.'
)

# Sequence input (positional argument)
parser.add_argument(
    'sequence',
    help='The sequence to analyze, or the path to a file if --file is specified.'
)

# File flag
parser.add_argument(
    '--file', '-f',
    action='store_true',
    help='Interpret the sequence argument as a file path.'
)

# Sequence type (required)
parser.add_argument(
    '--type', '-t',
    choices=['DNA', 'RNA', 'Protein'],
    required=True,
    help='Specify the type of sequence: DNA, RNA, or Protein.'
)

# Analysis type (required)
parser.add_argument(
    '--analysis', '-a',
    choices=['gc_percent', 'base_count', 'translate', 'transcribe', 'reverse_complement'],
    required=True,
    help='Specify the analysis to perform (e.g., gc_percent, base_count, translate, transcribe, reverse_complement).'
)

args = parser.parse_args()

print(args)

