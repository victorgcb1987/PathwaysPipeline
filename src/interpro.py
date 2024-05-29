#interproscan.sh -i e_coli_k12_mep.fasta -cpu 40 -o e_coli_k12_mep.interpro -f TSV --iprlookup

from subprocess import run

def run_interpro(sequences, out_dir, threads=6):
    interpro_fname = sequences.stem
    out_fpath = out_dir / (interpro_fname+".interpro.tsv")
    if not out_fpath.exists():
        cmd = "interproscan.sh -i {} -cpu {} -o {} -f TSV --pa".format(str(sequences), str(threads), str(out_fpath))
        run(cmd, shell=True)


def get_interpro_results(fhand, identifier_kind="NCBIfam"):
    results = {}
    for line in fhand:
        line = line.split("\t")
        if line[3] == identifier_kind:
            gene = line[0]
            step = line[5]
            if step not in results:
                results[step] = [gene]
            else:
                results[step].append(gene)
    return results


def add_results(dict_to_dataframe, species_name, results):
    pass