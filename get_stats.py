#!/usr/bin/env python


import argparse
import pandas as pd
import os
import sys


from pathlib import Path

from src.interpro import get_interpro_results, add_results


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
    database = parser.database       
    return {"reference": reference, 
            "interpro_dir": interpro_dir,
            "alignments_dir": alignments_dir,
            "output": output,
            "database": database}


def main():
    arguments = get_arguments()
    dict_to_dataframe = {}
    with open(arguments["reference"]) as reference_fhand:
        reference_results = get_interpro_results(reference_fhand, identifier_kind=arguments["database"])
        dict_to_dataframe["reference"] = ["reference"]
        for step, genes in reference_results.items():
            dict_to_dataframe["reference"].append(len(genes))
    for file in arguments["interpro_dir"].glob("*.interpro.tsv"):
        name = ".".join(file.stem.replace("vs_", "\t").split()[-1].split(".")[0:2])
        accession = "_".join(name.split("_")[0:2])
        species = "_".join(name.split("_")[2:])
        dict_to_dataframe[accession] = [species]
        if os.stat(str(file)) == 0:
            for step in reference_results:
                dict_to_dataframe[accession].append(0)
        else:
            with open(file) as fhand:
                file_results = get_interpro_results(fhand, identifier_kind=arguments["database"])
                for step in reference_results:
                    dict_to_dataframe[accession].append(len(file_results.get(step, [])))
    dataframe = pd.DataFrame.from_dict(dict_to_dataframe, orient="index").reset_index()
    dataframe = dataframe.set_axis(["accession", "species"]+[step for step in reference_results], axis=1)
    dataframe.to_csv(str(arguments["output"]), sep="\t", index=False)


if __name__ == "__main__":
    main()