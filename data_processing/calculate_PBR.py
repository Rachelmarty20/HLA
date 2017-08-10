import pandas as pd
import sys
import numpy as np
import cPickle as pickle

category = sys.argv[1]
mhc_class = sys.argv[2]
status = sys.argv[3]

# Create allele-based affinity matrix
mhc_alleles = [x.split(' ')[0] for x in open('/cellar/users/ramarty/programs/netMHCpan-3.0/data/allelenames').readlines() if x[:3] == 'HLA']
mutations = [x.strip() for x in open('/cellar/users/ramarty/Data/hla/residue/mutation_files/{0}.txt'.format(category))]

arrays, mutations_used = [], []
for i, mutation in enumerate(mutations):
    array = np.fromfile('/cellar/users/ramarty/Data/hla/residue/mutation_arrays/{0}/{1}/{2}/{3}.txt'.format(status, mhc_class, category, mutation))
    arrays.append(array)
    mutations_used.append(mutation)


df = pd.DataFrame(arrays)
df.index = mutations_used
df.columns = mhc_alleles

df.to_csv('/cellar/users/ramarty/Data/hla/residue/matrices/{0}/{1}/{2}.txt'.format(status, mhc_class, category))


# Create patient-based affinity matrix
patients = [x.strip() for x in open('/cellar/users/ramarty/Data/hla/patients.txt').readlines()]
sample_and_types = pickle.load(open('/cellar/users/ramarty/Data/hla/hla_typing/sample_and_types.p', 'rb'))

df.columns = [x[:5] + '*' + x[5:] for x in df.columns]

allele_dictionary = {}
patients_included = []
for i, patient in enumerate(patients):
    print i
    hlas = sample_and_types[patient]
    all_affinities_for_patient = []
    for mutation in mutations_used:
        affinity = 100
        for hla in hlas:
            if float(df.loc[mutation, hla]) < affinity:
                affinity = float(df.loc[mutation, hla])
        all_affinities_for_patient.append(affinity)
    allele_dictionary[patient] = all_affinities_for_patient
    patients_included.append(patient)

matrix = pd.DataFrame(allele_dictionary)
matrix.index = mutations_used

matrix.to_csv('/cellar/users/ramarty/Data/hla/patients/affinity_matrices/{0}/{1}/{2}.txt'.format(status, mhc_class, category))
