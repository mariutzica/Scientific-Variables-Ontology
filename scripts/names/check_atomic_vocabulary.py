#################################################################################
#                           STEP 1B (optional)                                  #
#   Script for atomizing the reformatted variable names and checking            #
#   whether all of the elements are present in the atomic vocabulary list.      #
#   input:  source/svo_atomic_vocabulary.csv, source/csdms_standard_names.csv   #
#   output: source/dump/extra_items.txt, source/dump/missing_items.txt                    #
#                                                                               #
#################################################################################

import pandas as pd
import re
import os

# Set up input files to read
script_path    = os.path.dirname(__file__)
src_path       = os.path.join(script_path,'../../source')
csn_filename   = 'csdms_standard_names.csv'
csn_filepath   = os.path.join(src_path,csn_filename)
vocab_filename = 'svo_atomic_vocabulary.csv'
src_path       = os.path.join(script_path,'../../source/raw')
vocab_filepath = os.path.join(src_path,vocab_filename)

# Set up output files to read.
dst_path = os.path.join(script_path,'../../source/dump')
missing_items = os.path.join(dst_path,'missing_items.txt')
extra_items = os.path.join(dst_path,'extra_items.txt')

# Gather all SVO vocabulary, including plurals.
svo_vocabulary_df = pd.read_csv(vocab_filepath).fillna('')
svo_vocabulary = svo_vocabulary_df['entity_label'].tolist()
plurals = svo_vocabulary_df.loc[svo_vocabulary_df['plural']!='','plural'].tolist()
svo_vocabulary.extend(plurals)

# Loop through reformatted variables and look up all
# terms in the name to generate the CSN vocabulary.
csdms_vocabulary = []
with open(csn_filepath,'r') as f:
    for variable_line in f:
        variable = variable_line.split(',')[1].strip()
        object, quantity = variable.split('__')
        object_atoms = re.split('~|-and-|-as-|-or-|_|-vs-',object)
        for atom in object_atoms:
            if atom.startswith('at-') or atom.startswith('to-'):
                atom = atom[3:]
            if atom.startswith('from-'):
                atom = atom[5:]
            if atom.startswith('above-') or atom.startswith('below-') or atom.startswith('along-')\
                or atom.startswith('since-'):
                atom = atom[6:]
            if atom.endswith('-below') or atom.endswith('-above'):
                atom = atom[0:-6]
            if atom not in csdms_vocabulary:
                csdms_vocabulary.append(atom)
        quantity_atoms = re.split('_of_|_and_',quantity)
        for atom in quantity_atoms:
            if atom not in csdms_vocabulary:
                csdms_vocabulary.append(atom)

# Look up CSN terms in the SVO vocabulary and if not present, add to 
# missing terms.
missing_vocabulary = []
for atom in csdms_vocabulary:
    if atom not in svo_vocabulary and atom.replace('-','_') not in svo_vocabulary:
        missing_vocabulary.append(atom)

with open(missing_items,'w') as f:
    for atom in missing_vocabulary:
        f.write(atom+'\n')

# Conversely, determine which SVO terms are not part of CSN, add to
# extra terms list.
extra_vocabulary = []
for element in svo_vocabulary:
    if element not in csdms_vocabulary and element.replace('_','-') not in csdms_vocabulary:
        extra_vocabulary.append(element)

with open(extra_items,'w') as f:
    for element in extra_vocabulary:
        f.write(element+'\n')