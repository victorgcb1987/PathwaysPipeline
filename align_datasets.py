#!/usr/bin/env python
import argparse
import pandas as pd
import sys

from pathlib import Path

from src.aln import make_db, align_sequences, select_matches_alignment_results
from src.ncbi import get_dataset_contents
from src.utils import list_files, extract_sequences_from_zipped_file, remove_database_and_fasta, get_sequence_ids

from pathlib import Path


#Generating program options
def parse_arguments():
    desc = "Blast sequences against NCBI dataset"
    parser = argparse.ArgumentParser(description=desc)
    
    help_input_sequences = "(Required) Input sequences to Blast against datasets"
    parser.add_argument("--input", "-i", type=str, required=True,
                        help=help_input_sequences)
    
    help_datasets = "(Required) Directory with NCBI datasets"
    parser.add_argument("--datasets_dir", "-d", type=str,
                        required=True, help=help_datasets)
    
    help_output = "(Required) Output Directory"
    parser.add_argument("--output_dir", "-o", type=str,
                        required=True, help=help_output)
    
    help_threads = "(Optional) number of threads. Default = 1"
    parser.add_argument("--threads", "-t", default=1,
                        help=help_threads)
    
    if len(sys.argv)==1:
        parser.print_help()
        exit()
    return parser.parse_args()


def get_arguments():
    parser = parse_arguments()
    out_dir = Path(parser.output_dir)
    input_sequences = Path(parser.input)
    datasets_dir = Path(parser.datasets_dir)
    threads = parser.threads
    
    return {"out_dir": out_dir, 
            "input_sequences": input_sequences,
            "datasets_dir": datasets_dir,
            "threads": threads}


def main():
    arguments = get_arguments()
    datasets_listed = list_files(arguments["datasets_dir"])
    if len(datasets_listed) < 1:
        raise RuntimeError("No valid datasets found")
    out_dir = arguments["out_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    blast_dir = out_dir / "alignments"
    blast_dir.mkdir(exist_ok=True, parents=True)
    for dataset in datasets_listed:
        for accession in get_dataset_contents(dataset):
            sequence_file = extract_sequences_from_zipped_file(accession, dataset, blast_dir)
            blastdb_fpath = blast_dir/sequence_file.name
            make_db(sequence_file, blastdb_fpath)
            aln_results = align_sequences(arguments["input_sequences"], sequence_file, blast_dir, num_threads=arguments["threads"])
            remove_database_and_fasta(sequence_file, blastdb_fpath)
      
            # sequences_id = get_sequence_ids(arguments["input_sequences"])
            # matched_proteins = select_matches_alignment_results(sequences_id, aln_results)
            # dict_to_dataframe["species"].append(accession["organism_name"])
            # for key, value in matched_proteins.items():
            #     dict_to_dataframe[key].append(len(value))
    #print(pd.DataFrame.from_dict(dict_to_dataframe))
            

if __name__ == "__main__":
    main()