import sys
import os
import time
import numpy as np
import pandas as pd


def main(category, mutation, status, mhc_class):

    mhc_alleles = [x.split(' ')[0] for x in open('/cellar/users/ramarty/programs/netMHCpan-3.0/data/allelenames').readlines() if x[:3] == 'HLA']

    all = get_binders(status, mhc_class, category, mutation, mhc_alleles)

    if not os.path.isdir('/cellar/users/ramarty/Data/hla/residue/mutation_arrays/{0}/{1}/{2}'.format(status, mhc_class, category)):
        os.mkdir('/cellar/users/ramarty/Data/hla/residue/mutation_arrays/{0}/{1}/{2}'.format(status, mhc_class, category))

    all.tofile('/cellar/users/ramarty/Data/hla/residue/mutation_arrays/{0}/{1}/{2}/{3}.txt'.format(status, mhc_class, category, mutation))


def get_binders(status, mhc_class, category, mutation, mhc_alleles):

    gene = mutation.split('_')[0]
    residue = int(mutation.split('_')[1][1:-1]) - 1
    new_aa = mutation.split('_')[1][-1]

    protein = open('/cellar/users/ramarty/Data/hla/whole_gene/fasta_files/{0}.fa'.format(gene)).readlines()[1]

    if status == 'mut':
        protein = protein[:residue] + new_aa + protein[residue+1:]

    peptides = []
    pos = residue
    for kmer in [8,9,10,11]:
        for i in range(len(protein) - (kmer-1)):
            start = i
            end = i + kmer
            if pos >= start and pos < end:
                peptides.append(protein[start:end])

    all = np.zeros(len(mhc_alleles))
    for i, allele in enumerate(mhc_alleles):
        lines = open('/cellar/users/ramarty/Data/hla/residue/affinities/{0}/{1}/{2}/{3}/{4}.txt'.format(status, mhc_class, category, mutation, allele)).readlines()[48:]
        lines = lines[:-5]
        df = pd.DataFrame([line.split()[:14] for line in lines])
        df.columns = ['Pos', 'HLA', 'Peptide', 'Core', 'Of', 'Gp', 'Gl', 'Ip', 'Il', 'Icore', 'Identity', 'Score', 'Aff', 'Rank']
        df.Rank = df.Rank.astype(float)
        df = df[df.Peptide.isin(peptides)]
        all[i] = min(df.Rank)
    return all


###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 5:
        sys.exit()
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print time.time() - start_time
    sys.exit()