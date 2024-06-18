from subprocess import run
def make_db(sequences_fpath, blast_dir):
    cmd = "makeblastdb -in {} -dbtype prot -out {}".format(sequences_fpath, str(blast_dir))
    run(cmd, shell=True)


def align_sequences(input_sequences, blast_database, blast_dir, num_threads=6):
    filename = "{}_vs_{}.tab".format(input_sequences.stem, blast_database.stem)
    aln_results_fpath = blast_dir / filename
    cmd = "blastp -query {} -db {} -num_threads {} -outfmt \"6 std qlen slen\" > {}".format(str(input_sequences),
                                                                          str(blast_database),
                                                                          str(num_threads),
                                                                          str(aln_results_fpath))
    run(cmd, shell=True)
    return aln_results_fpath


def select_matches_alignment_results(aln_results):
    results = {}
    with open(aln_results) as aln_fhand:
        for line in aln_fhand:
            if line:
                line = line.rstrip().split()
                e_value = float(line[-10])
                if e_value < 0.00005:
                    query_name = line[0]
                    subject_name = line[1]
                    if query_name not in results:
                        results[query_name] = [subject_name]
                    else:
                        results[query_name].append(subject_name)
    return results

                    
