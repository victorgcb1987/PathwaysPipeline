import argparse
import sys

from pathlib import Path


def parse_arguments():
    desc = "Create a table with gene occurrences"
    parser = argparse.ArgumentParser(description=desc)

    help_input = "(Required) Interpro results for the reference species"
    parser.add_argument("--reference", "-r", type=str,
                        required=True, help=help_input)

    help_interpro = "(Required) directory with InterPro results for species to compare"
    parser.add_argument("--interpro_dir", "-p", type=str,
                        required=True, help=help_interpro)

    help_alignments = "(Required) alignment results directory"
    parser.add_argument("--alignment_dir", "-a", type=str,
                        required=True, help=help_alignments)
    
    help_output = "(Required) Output filepath"
    parser.add_argument("--output", "-o", type=str,
                        required=True, help=help_output)
    
    help_database = "(Optional) Database to do lookup. Default NCBIfam"
    parser.add_argument("--database", "-db", type=str,
                        default="NCBIfam", help=help_database)
    
    
    if len(sys.argv)==1:
        parser.print_help()
        exit()
    return parser.parse_args()


def get_arguments():
    parser = parse_arguments()
    reference = Path(parser.reference)
    interpro_dir = Path(parser.interpro_dir)
    alignments_dir = Path(parser.alignment_dir)
    output = Path(parser.output)
    
    return {"reference": reference, 
            "interpro_dir": interpro_dir,
            "alignments_dir": alignments_dir,
            "output": output}


def main():
    arguments = parse_arguments()
    dict_to_dataframe = {"species": []} | get_sequence_ids(arguments["input_sequences"])







if __name__ == "__main__":
    main()