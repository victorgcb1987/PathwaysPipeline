from subprocess import run

def retrieve_data_from_ncbi(out_dir="", taxon="", assembly_level="", 
                            assembly_version="", assembly_source="", 
                            data_type="protein"):
    out_filepath = out_dir / "ncbi_{}.zip".format(taxon)
    if out_filepath.exists():
        results = {"output_file": out_filepath,
                   "return_code": 0,
                   "log_messages": "NCBI data already retrieved"}
        return results
    cmd = ["datasets", "download", "genome"]
    if taxon:
        cmd.append("--taxon {}".format(taxon))
    
    if assembly_level in ["chromosome", "complete", 
                          "complete", "scaffold"]:
        cmd.append("--assembly-level {}".format(assembly_level))
    elif assembly_level:
        raise ValueError("Invalid assembly level value: {}".format(assembly_level))
    
    if assembly_version in ["latest", "all"]:
        cmd.append("--assembly-version {}".format(assembly_version))
    elif assembly_version:  
        raise ValueError("Invalid assembly version value: {}".format(assembly_version))
    
    if assembly_source in ["RefSeq", "GenBank", "all"]:
        cmd.append("--assembly-source {}".format(assembly_source))
    elif assembly_source:
        raise ValueError("Invalid assembly source value: {}".format(assembly_source))
    
    if data_type in ["protein", "genome", "rna", "protein", "cds",
                   "gff3", "gtf", "gbff", "seq-report"]:
        cmd.append("--include {}".format(data_type))
    elif data_type:
        raise ValueError("Invalid assembly source value: {}".format(data_type))
    print("Command running: "+" ".join(cmd))
    retrieve_run = run("\t".join(cmd), capture_output=True, shell=True)
    results = {"output_file": out_filepath,
               "return_code": retrieve_run.returncode,
               "log_messages": retrieve_run.stderr.decode()}
    