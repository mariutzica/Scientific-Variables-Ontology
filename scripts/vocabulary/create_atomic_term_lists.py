#################################################################################
#                                                                               #
#   Script for generating quick lookup lists of terms for each top level        #
#   category.                                                                   #
#   input:  source/raw/svo_atomic_vocabulary.csv,                               #
#           source/csdms_standard_names.csv                                     #
#   output: source/quicklookup/{classname}.txt                                  #
#                                                                               #
#################################################################################

import os
import pandas as pd
import numpy as np

# Read in all of the entity labels, entity classes, and entity plurals.
# The labels and plurals form the base vocabulary, while the classes identify
# the category to which each term belongs.
script_path = os.path.dirname(__file__)
src_path = os.path.join(script_path,'../../source/raw/')
atomic_terms_filename = 'svo_atomic_vocabulary.csv'
atomic_terms_filepath = os.path.join(src_path,atomic_terms_filename)
cols_of_interest = ['entity_label','entity_class','plural']
atomic_vocabulary = pd.read_csv(atomic_terms_filepath,usecols = cols_of_interest)

# Generate a list of all of the unique entity classes.
entity_classes = atomic_vocabulary['entity_class'].dropna().tolist()
entity_classes = sorted(np.unique(entity_classes))

# Loop through the entity classes, generate a list of unique terms for that class,
# and write them to a text file named for that class.
# Also tabulate all classes that a term belongs to.
word_classes = {}
dst_path = os.path.join(script_path,'../../source/quicklookup/')
for eclass in entity_classes:
    atomic_vocab = atomic_vocabulary.loc[atomic_vocabulary['entity_class']==eclass,'entity_label'].dropna().tolist()
    plural_vocab = atomic_vocabulary.loc[atomic_vocabulary['entity_class']==eclass,'plural'].dropna().tolist()
    all_vocab = sorted(atomic_vocab + plural_vocab)
    dst_atomic_filepath = os.path.join(dst_path, f'{eclass}.txt')
    with open(dst_atomic_filepath,'w') as f:
        for word in all_vocab:
            f.write(word+'\n')
            if word in word_classes.keys():
                word_classes[word].append(eclass)
            else:
                word_classes[word] = [eclass]

# Loop to print out any label duplicates
print_all_duplicates = False
if print_all_duplicates:
    for word, classes in word_classes.items():
        if len(classes) > 1:
            print(f'{word}: {classes}')

# Loop to print out label duplicates belonging to more than one class
print_multiclass_duplicates = True
if print_multiclass_duplicates:
    for word, classes in word_classes.items():
        unique_classes = np.unique(classes)
        if len(unique_classes) > 1:
            print(f'{word}: {unique_classes}')