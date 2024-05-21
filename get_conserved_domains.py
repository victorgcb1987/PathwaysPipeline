#!/usr/bin/env python

import argparse
import sys

from pathlib import Path

from src.aln import select_matches_alignment_results
from src.interpro import run_interpro
from src.utils import list_files, get_accesion_code_from_string, write_matched_sequences

#Generating program options
def parse_arguments():
    desc = "Get functional domains from aligned sequences"
    parser = argparse.ArgumentParser(description=desc)
    
    help_alns = "(Required) Alignment filedir"
    parser.add_argument("--aln_dir", "-a", type=str, required=True,
                        help=help_alns)
    
    help_sequences = "(Required) zipped file with NCBI dataset with sequences"
    parser.add_argument("--sequences", "-s", type=str,
                        required=True, help=help_sequences)
    
    help_output = "(Required) Output Directory"
    parser.add_argument("--output_dir", "-o", type=str,
                        required=True, help=help_output)
    
    help_threads = "(Optional) number of threads. Default = 1"
    parser.add_argument("--threads", "-t", default=1,
                        help_output=help_threads)
    
    if len(sys.argv)==1:
        parser.print_help()
        exit()
    return parser.parse_args()


def get_arguments():
    parser = parse_arguments()
    out_dir = Path(parser.output_dir)
    input_sequences = Path(parser.sequences)
    alignments_dir = Path(parser.aln_dir)
    threads = parser.threads
    
    return {"out_dir": out_dir, 
            "input_sequences": input_sequences,
            "alignments_dir": alignments_dir,
            "threads": threads}


def main():
    arguments = get_arguments()
    out_dir = arguments["out_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    alignments_files = list_files(arguments["alignments_dir"], prefix="", suffix="tab")
    for aln_file in alignments_files:
        accession = get_accesion_code_from_string(str(aln_file))
        matched_proteins = select_matches_alignment_results(str(aln_file))
        sequences = write_matched_sequences(matched_proteins, out_dir, aln_file, arguments["input_sequences"], accession)
        run_interpro(sequences, out_dir, threads=arguments["threads"])






if __name__ == "__main__":
    main()