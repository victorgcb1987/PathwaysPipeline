import os
from subprocess import run
def make_db(sequences_fpath):
    cmd = "diamond makedb --in {} --db {}".format(sequences_fpath, sequences_fpath)
    print(cmd)
    run(cmd, shell=True)


def align_sequences(input_sequences, diamond_database, blast_dir, num_threads=6):
    filename = "{}_vs_{}.tab".format(input_sequences.stem, diamond_database.stem)
    aln_results_fpath = blast_dir / filename
    cmd = "diamond blastp -q {} -d {} --threads {} --outfmt 6 qseqid sseqid".format(str(input_sequences),
                                                                          str(diamond_database),
                                                                          str(num_threads))
    cmd += " qstart qend sstart send pident evalue qlen slen qcovhsp > {}".format(str(aln_results_fpath))
    print(cmd)
    run(cmd, shell=True)
    return aln_results_fpath


def select_matches_alignment_results(results, aln_results):
    with open(aln_results) as aln_fhand:
        for line in aln_fhand:
            if line:
                line = line.rstrip().split()
                e_value = float(line[7])
                query_cov = float(line[-1])
                if e_value < 0.00005 and query_cov > 50:
                    query_name = line[0]
                    subject_name = line[1]
                    identity = float(line[6])
                    results[query_name].append(subject_name)
    return results

                    
