import sys
import os
import time


def main(category, mutation, status, mhc_class):

    mhc_alleles = [x.split(' ')[0] for x in open('/cellar/users/ramarty/programs/netMHCpan-3.0/data/allelenames').readlines() if x[:3] == 'HLA']
    fasta_file = '/cellar/users/ramarty/Data/hla/residue/fasta_files/{0}/{1}/{2}/{3}.fa'.format(status, mhc_class, category, mutation)

    for i, allele in enumerate(mhc_alleles):
        if not os.path.isdir('/cellar/users/ramarty/Data/hla/residue/affinities/{0}/{1}/{2}/{3}'.format(status, mhc_class, category, mutation)):
            os.mkdir('/cellar/users/ramarty/Data/hla/residue/affinities/{0}/{1}/{2}/{3}'.format(status, mhc_class, category, mutation))

        affinities_file = '/cellar/users/ramarty/Data/hla/residue/affinities/{0}/{1}/{2}/{3}/{4}.txt'.format(status, mhc_class, category, mutation, allele)

        # call method
        if mhc_class == 'class_i':
            cmd = '/cellar/users/ramarty/programs/netMHCpan-3.0/netMHCpan -a {0} -f {1} -tdir /cellar/users/ramarty/Data/hla/tmp/{3}.{4}.{5}XXXXXX > {2}'.format(allele, fasta_file, affinities_file, category, status, mutation)
        else:
            cmd = ''
        os.system(cmd)



###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 5:
        sys.exit()
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))