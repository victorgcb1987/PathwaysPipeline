from Bio import SeqIO
from subprocess import run


def check_results(program, results):
    if results["return_code"] == 0:
        print("{} successfully run".format(program))
    else:
        print("{} failed".format(program))
        raise RuntimeError(results["log_messages"])


def list_files(dir, prefix="ncbi", suffix=".zip"):
    files_listed = []
    lookup_filenames = prefix+"*"+suffix
    for file in dir.glob(lookup_filenames):
        files_listed.append(file.resolve())
    return files_listed

def extract_sequences_from_zipped_file(dataset, file, out_dir):
    species = "_".join(dataset["organism_name"].split())
    accession = dataset["accession"]
    sequence_fpath = out_dir / "{}_{}.faa".format(accession, species)
    cmd = "unzip -p {} {} > {}".format(str(file), dataset["file"], str(sequence_fpath))
    run(cmd, shell=True)
    return sequence_fpath

def remove_database_and_fasta(sequences):
    database_path = sequences.parent / (sequences.name+".dmnd")
    database_path.unlink()
    sequences.unlink()
    
def get_sequence_ids(sequences):
    return {sequence.id: [] for sequence in SeqIO.parse(sequences, "fasta")}