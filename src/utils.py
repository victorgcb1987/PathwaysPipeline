from io import StringIO
from pathlib import Path
from re import search
from subprocess import run
from tempfile import NamedTemporaryFile

from Bio import SeqIO


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


def extract_aligned_sequences(dataset, file, out_dir, aligned_sequences_ids):
    species = "_".join(dataset["organism_name"].split())
    accession = dataset["accession"]
    sequence_fpath = out_dir / "{}_{}.AlignedOnly.faa".format(accession, species)
    cmd = "unzip -p {} {}".format(str(file), dataset["file"])
    run(cmd, shell=True, capture_output=True)
    records = SeqIO.index(StringIO(run.stdout))
    with open(sequence_fpath) as sequence_fhand:
        for id in aligned_sequences_ids:
            SeqIO.write(records[id], sequence_fhand, "fasta")
    return sequence_fpath


def get_accesion_code_from_string(string):
    return search("GC[A-Z]{1}_[0-9]+.[0-9]{1}", string).group(0)


def write_matched_sequences(matched_proteins, out_dir, aln_file, dataset, accession):
    temp_file = NamedTemporaryFile()
    filename = aln_file.stem
    out_fpath = out_dir / (filename+".AlignedOnly.faa")
    sequence_filepath = "ncbi_dataset/data/{}/protein.faa".format(accession)
    cmd = "unzip -p {} {} > {}".format(str(dataset), sequence_filepath, temp_file.name)
    run(cmd, shell=True)
    records = SeqIO.index(temp_file.name, "fasta")
    with open(out_fpath, "w") as sequence_fhand:
        for query, matches in matched_proteins.items():
            for match in matches:
                SeqIO.write(records[match], sequence_fhand, "fasta")
    return Path(out_fpath)