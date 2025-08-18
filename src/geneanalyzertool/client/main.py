import argparse
from geneanalyzertool.analysis.basic_analysis import BasicSequenceAnalysis
from geneanalyzertool.core.exceptions import InvalidSequenceTypeError, AnalysisMethodError

# if a class is added to this map, --mode in parse_args() must also be updated.
analysis_map = {
    "basic": BasicSequenceAnalysis
}

analysis_options = {
    "basic": ['gc_percent', 'base_count', 'translate', 'transcribe', 'reverse_complement']
}


# if a new analysis is added to analysis_options, it must also be added to the map above.
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

    # Validate analysis option for the selected mode
    if args.analysis not in analysis_options[args.mode]:
        print(f"Error: Analysis '{args.analysis}' is not valid for mode '{args.mode}'.")
        print(f"Valid options: {analysis_options[args.mode]}")
        exit(1)

    # Get the appropriate analysis class based on mode
    analysis_class = analysis_map[args.mode]
    analyzer = analysis_class()

    try:
        # Delegate sequence processing to the analysis class
        results = analyzer.process_sequences(
            sequence_input=args.sequence,
            is_file=args.file,
            seq_type=args.type,
            analysis_method=args.analysis
        )

        # Output results
        if args.out:
            analyzer.export_to_file(results, args.out)
        else:
            for line in results:
                print(line)

    except InvalidSequenceTypeError as e:
        print(str(e))
        exit(1)
    except AnalysisMethodError as e:
        print(str(e))
        exit(1)


if __name__ == "__main__":
    main()
