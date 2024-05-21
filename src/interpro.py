#interproscan.sh -i e_coli_k12_mep.fasta -cpu 40 -o e_coli_k12_mep.interpro -f TSV --iprlookup

from subprocess import run

def run_interpro(sequences, out_dir, threads=6):
    interpro_fname = sequences.stem
    out_fpath = out_dir / (interpro_fname+".interpro.tsv")
    cmd = "interproscan.sh -i {} -cpu {} -o {} -f TSV --pa".format(str(sequences), str(threads), str(out_fpath))
    run(cmd, shell=True)

