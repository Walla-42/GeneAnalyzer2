import argparse
from geneanalyzertool.analysis.basic_analysis import BasicSequenceAnalysis
from geneanalyzertool.core.sequences import DNA, RNA, Protein, Sequence
from geneanalyzertool.analysis.analysis import Analysis
from geneanalyzertool.core.file_handler import FileHandler

# if a class is added to this map, --mode in parse_args() must also be updated. 
analysis_map = {
    "basic": BasicSequenceAnalysis
}

analysis_options = {
    "basic": ['gc_percent', 'base_count', 'translate', 'transcribe', 'reverse_complement']
    }

def parse_args():
    parser = argparse.ArgumentParser(
        prog='GeneAnalyzer2',
        description='Command-line bioinformatics tool for analyzing DNA, RNA, and protein sequences.'
    )

    # sequence input args
    parser.add_argument(
        'sequence',
        help='Sequence to analyze, OR a file path if using --file.'
    )
    parser.add_argument(
        '--file', '-f',
        action='store_true',
        help='Treat the "sequence" argument as a file path rather than a raw sequence.'
    )

    # sequence type args
    parser.add_argument(
        '--type', '-t',
        choices=['DNA', 'RNA', 'Protein'],
        required=True,
        help='Specify the sequence type: DNA, RNA, or Protein.'
    )

    # analysis args
    parser.add_argument(
        '--mode', '-m',
        choices=['basic'], 
        default='basic',
        help='Mode of analysis to be performed. Default is basic. Refer to docs for more information.'
    )

    parser.add_argument(
        '--analysis', '-a',
        required=True,
        help='Type of analysis to perform. Based on mode chosen.'
    )
    
    # output file args
    parser.add_argument(
        '--out', '-o',
        metavar='OUTPUT_FILE',
        help='Optional: Path to save analysis results. If omitted, results are printed to stdout.'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    analysis_class = analysis_map[args.mode]
    analyzer = analysis_class()

    if args.analysis not in analysis_options[args.mode]:
        print(f"Error: Analysis '{args.analysis}' is not valid for mode '{args.mode}'.")
        print(f"Valid options: {analysis_options[args.mode]}")
        exit(1)

    if args.file:
        filehandler = FileHandler()
        available_sequences = filehandler.read_in_sequence(args.sequence)
    else:
        available_sequences = args.sequence

    for sequence in available_sequences:
        print(f"Anlyzing {sequence.key}...")
        type_map = {"DNA": DNA, "RNA": RNA, "Protein": Protein}
        seq_type = type_map[args.type]
        sequence_obj = seq_type(sequence.value)
        
        try:
            result = analyzer.analyze(sequence_obj, args.analysis)
            if args.out:
                with open(args.out, 'w') as out_file:
                    out_file.write(f"{sequence.key}: {result}\n")
            else:
                print(result)
        except Exception as e:
            print(f"Error: Analysis interupted - {e}")
            exit(1)

        




if __name__ == "__main__":
    main()
