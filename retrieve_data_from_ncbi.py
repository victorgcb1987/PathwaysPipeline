#!/usr/bin/env python
import argparse
import sys

from pathlib import Path

from src.ncbi import retrieve_data_from_ncbi
from src.utils import check_results

from pathlib import Path


#Generating program options
def parse_arguments():
    desc = "Retrieve sequences data from NCBI"
    parser = argparse.ArgumentParser(description=desc)
    
    help_out_dir = "(Required) out dir"
    parser.add_argument("--out_dir", "-o", type=str,
                        required=True, help=help_out_dir)
    
    help_taxon = "(Optional) Taxon to be retrieved. Default: all(!!!)"
    parser.add_argument("--taxon", "-t", type=str, nargs='+',
                        default="", help=help_taxon)
    
    help_assembly_level = "(Optional) Assembly level to retrieve. Options are chromosome, complete, contig, scaffold"
    parser.add_argument("--assembly_level", "-l", type=str,
                        default="", help=help_assembly_level)
    
    help_assembly_version = "(Optional) Assembly version. Default: latest"
    parser.add_argument("--assembly_version", "-v", type=str,
                        default="latest", help=help_assembly_version)
    
    help_assembly_source = "(Optional) Assembly source. Options are RefSeq, GenBank, all. Default: GenBank"
    parser.add_argument("--assembly_source", "-s", type=str,
                        default="GenBank", help=help_assembly_source)
    
    help_include = "(Optional) data kind to be retrieved. Options are protein, genome, rna, protein, cds, gff3, gtf, gbff, seq-report. Default: protein"
    parser.add_argument("--data_type", "-d", type=str,
                        default="protein", help=help_include)
    
    
    if len(sys.argv)==1:
        parser.print_help()
        exit()
    return parser.parse_args()


#Parse and return values given to options when running this program
def get_arguments():
    parser = parse_arguments()
    out_dir = Path(parser.out_dir)
    taxon = parser.taxon
    assembly_level = parser.assembly_level
    assembly_version = parser.assembly_version
    assembly_source = parser.assembly_source
    data_type = parser.data_type
    return {"out_dir": out_dir, 
            "taxon": taxon,
            "assembly_level": assembly_level,
            "assembly_version": assembly_version,
            "assembly_source": assembly_source,
            "data_type": data_type}


def main():
    arguments = get_arguments()
    results = retrieve_data_from_ncbi(**arguments)
    check_results("NCBI-datasets", results)
    

if __name__ == "__main__":
    main()