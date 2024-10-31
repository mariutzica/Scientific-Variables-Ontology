#############################################################
#                      STEP 2                               #
#   Parse names as atomic components and generate pattern   #
#   where each atomic element is replaced by its category.  #
#   input: source/csdms_standard_names.csv                  #
#          source/svo_atomic_vocabulary.csv                 #
#   output: source/variable_name_tags.csv                   #
#           source/svo_atomic_vocabulary_meta.csv           #
#                                                           #
#############################################################

import os
import pandas as pd
import numpy as np

# Read in reformatted variable names.
script_path  = os.path.dirname(__file__)
src_path     = os.path.join(script_path,'../../source/')
csn_filename = 'csdms_standard_names.csv'
csn_filepath = os.path.join(src_path,csn_filename)

with open(csn_filepath, 'r') as f:
    names = f.readlines()

# Parse to obtain object and quantity part of name.
original_names = [name.split(', ')[0].strip() for name in names]
names = [name.split(', ')[1].strip() for name in names]
object_names = [name.split('__')[0] for name in names]
quantity_names = [name.split('__')[1] for name in names]

variable_tagging = pd.DataFrame({'original_name':original_names, 
                                 'variable_name':names, 
                                 'object_name': object_names, 
                                 'quantity_name':quantity_names})

# Read in the atomic vocabulary.
raw_path = os.path.join(script_path,'../../source/raw/')
svo_vocab_file = 'svo_atomic_vocabulary.csv'
vocab_filepath = os.path.join(raw_path, svo_vocab_file)
cols_to_read = ['entity_label','entity_class','plural']
atomic_vocabulary = pd.read_csv(vocab_filepath, usecols = cols_to_read)

# Separate out object-related classes from quantity-related classes.
object_classes   = ['phenomenon','process','role','part','domain',
                    'direction','trajectory','matter','form',
                    'attribute','abstraction','model']
quantity_classes = ['property','operation','propertytype',
                    'propertyrole','propertyquantification','model',
                    'direction']
all_classes = object_classes + quantity_classes
atomic_vocabulary_all = sorted(atomic_vocabulary['entity_label'].tolist(), key=len, reverse=True)
atomic_vocabulary_object_index = atomic_vocabulary['entity_class'].isin(object_classes)
atomic_vocabulary_quantity_index = atomic_vocabulary['entity_class'].isin(quantity_classes)

# Gather all object vocabulary, quantity vocabulary, and vocabulary of
# quantities in the object.
atomic_vocabulary_object = sorted(atomic_vocabulary.loc[atomic_vocabulary_object_index,'entity_label']\
                                  .tolist(), key=len, reverse=True)
atomic_vocabulary_objects = sorted(atomic_vocabulary.loc[atomic_vocabulary_object_index,'plural']\
                                   .dropna().tolist(), key=len, reverse=True)
all_object_vocabulary = sorted(atomic_vocabulary_object + atomic_vocabulary_objects, key=len, reverse=True )
all_quantity_vocabulary = sorted(atomic_vocabulary.loc[atomic_vocabulary_quantity_index,'entity_label']\
                                    .tolist(), key=len, reverse=True)
object_quantities = sorted(['pressure_head','speed', 'reference_height',
                            'pressure','reference_depth','temperature','capacity','compressibility'], key=len, reverse=True)

index_map = {'phenomenon':'phenomena', 'process': 'processes',
                 'matter':'matter', 'role':'roles','form':'forms',
                 'property':'properties', 'operation':'operations',
                 'propertytype':'propertytypes','propertyrole':'propertyroles',
                 'propertyquantification':'propertyquantifications',
                 'trajectory':'trajectories','domain':'domains',
                 'attribute':'attributes','abstraction':'abstractions',
                 'model':'models','direction':'directions','part':'parts',
                 'reference':'reference'}

# create a list of terms for each category
atomic_vocab = {}
plural_vocab = {}
for category in all_classes:
    atomic_vocab[category] = atomic_vocabulary.loc[atomic_vocabulary['entity_class']==category,'entity_label'].tolist()
    plural_vocab[category] = atomic_vocabulary.loc[atomic_vocabulary['entity_class']==category,'plural'].dropna().tolist()

atomic_vocabulary['tagged_variables'] = ''

# List of double term to override category
override = {
    'downwelling':'direction',
    'grain':'form',
    'link':'form',
    'front':'part',
    'wave':'form',
    'cell':'abstraction',
    'grazing':'attribute',
    'neck':'part',
    'living':'attribute',
}

special_override = {
    '~interior':'attribute',
    'mercury~':'matter',
}
verbose = False

# loop through all of the variable names and replace terms with their categories
for index, row in variable_tagging.iterrows():
    object_name = row['object_name']
    quantity_name = row['quantity_name']
    original_name = row['original_name']
    variable_name = row['variable_name']

    contained_elements = {}

    # If the object name has not underscore or ~, it is a phenomenon.
    #if '_' not in object_name and '~' not in object_name:
    #    if 'phenomenon' in contained_elements.keys():
    #        contained_elements['phenomenon'].append(object_name)
    #    else:
    #        contained_elements['phenomenon'] = [object_name]
    #    if atomic_vocabulary.query('@object_name == entity_label and \'phenomenon\' == entity_class').empty:
    #        atomic_vocabulary.loc[len(atomic_vocabulary.index)] = [object_name, 'phenomenon', np.nan, variable_name]
    #    else:
    #        atomic_vocabulary.loc[(atomic_vocabulary['entity_label']==object_name) & \
    #                                (atomic_vocabulary['entity_class']=='phenomenon'), 'tagged_variables'] += ', ' + variable_name
    #    object_name = 'PHENOMENON'
    #else:
    
    # If the term ends in at- followed by a quantity, this is a reference to a property
    if '_at-' in object_name:
        ending = object_name.split('_at-')[1]
        for atomic_term in object_quantities:
            hyphenated_term = atomic_term.replace('_','-')
            if hyphenated_term in ending or ending.endswith('_'+hyphenated_term):
                if 'reference' in contained_elements.keys():
                    contained_elements['reference'].append(atomic_term)
                else:
                    contained_elements['reference'] = [atomic_term]
                object_name = object_name.replace(hyphenated_term,'PROPERTY')
                atomic_vocabulary.loc[(atomic_vocabulary['entity_label']==atomic_term) & \
                                    (atomic_vocabulary['entity_class']=='property'), 'tagged_variables'] += ', ' + variable_name

    if ('sediment' in object_name or 'sand' in object_name) and ('grain' in object_name):
        object_name = object_name.replace('grain', 'PHENOMENON')
        if 'phenomenon' in contained_elements.keys():
            contained_elements['phenomenon'].append('grain')
        else:
            contained_elements['phenomenon'] = ['grain']
        atomic_vocabulary.loc[(atomic_vocabulary['entity_label']=='grain') & \
                    (atomic_vocabulary['entity_class']=='phenomenon'), 'tagged_variables'] += ', ' + variable_name
    
    for key, val in special_override.items():
        if key not in object_name:
            continue
            
        term = key.strip('~')
        object_name = object_name.replace(term, val.upper())
        if val in contained_elements.keys():
            contained_elements[val].append(term)
        else:
            contained_elements[val] = [term]
        atomic_vocabulary.loc[(atomic_vocabulary['entity_label']==term) & \
                            (atomic_vocabulary['entity_class']==val), 'tagged_variables'] += ', ' + variable_name
              
    # Loop through object vocabulary to label all terms in object_name
    for atomic_term in all_object_vocabulary:
        if atomic_term in object_name:
            category = None
            col_label = None
            if atomic_term in override.keys():
                category = override[atomic_term]
                col_label = 'entity_label'
            else:
                for key, val in atomic_vocab.items():
                    if key not in object_classes:
                        continue
                    if atomic_term in val:
                        if category is None:
                            category = key
                            col_label = 'entity_label'
                        else:
                            print(f'Warning, multiple category: {atomic_term}.')
                            print(f'The default is set to {category}.')
                if category is None:
                    for key, val in plural_vocab.items():
                        if key not in object_classes:
                            continue
                        if atomic_term in val:
                            if category is None:
                                category = key
                                col_label = 'plural'
                            else:
                                print(f'Error, multiple category: {atomic_term}.')

            if category is None:
                print(f'Error, no category found: {atomic_term}')
                continue

            if category in contained_elements.keys():
                contained_elements[category].append(atomic_term)
            else:
                contained_elements[category] = [atomic_term]
            object_name = object_name.replace(atomic_term,category.upper())
            atomic_vocabulary.loc[(atomic_vocabulary[col_label]==atomic_term) & \
                        (atomic_vocabulary['entity_class']==category), 'tagged_variables'] += ', ' + variable_name

        
    # Loop through quantity vocabulary to label all terms quantity_name
    for atomic_term in all_quantity_vocabulary:
        if atomic_term in quantity_name:
            for key, val in atomic_vocab.items():
                if key in quantity_classes:
                    if atomic_term in atomic_vocab[key]:
                        if key in contained_elements.keys():
                            contained_elements[key].append(atomic_term)
                        else:
                            contained_elements[key] = [atomic_term]
                        quantity_name = quantity_name.replace(atomic_term,key.upper())
                        atomic_vocabulary.loc[(atomic_vocabulary['entity_label']==atomic_term) & \
                                    (atomic_vocabulary['entity_class']==key), 'tagged_variables'] += ', ' + variable_name
                    elif atomic_term in plural_vocab[key]:
                        if key in contained_elements.keys():
                            contained_elements[key].append(atomic_term)
                        else:
                            contained_elements[key] = [atomic_term]
                        quantity_name = quantity_name.replace(atomic_term,key.upper())
                        atomic_vocabulary.loc[(atomic_vocabulary['plural']==atomic_term) & \
                                    (atomic_vocabulary['entity_class']==key), 'tagged_variables'] += ', ' + variable_name

    # Add all contained terms to corresponding category columns.                    
    for key, val in index_map.items():
        if key in contained_elements.keys():
            variable_tagging.at[index,val] = ', '.join(contained_elements[key])
        else:
            variable_tagging.at[index,val] = ''
    variable_tagging.at[index,'object_pattern'] = object_name
    variable_tagging.at[index,'quantity_pattern'] = quantity_name

    if verbose:
        print(variable_name, object_name, quantity_name)
        input('Press enter to continue ...')

# Write file with object and quantity category pattern,
# as well as terms belonging to each category.
variable_tagging.to_csv(os.path.join(src_path,'variable_name_tags.csv'), index=False)

# Write 'meta' atomic vocabulary file that contains variables that contain each term.
atomic_vocabulary['tagged_variables'] = atomic_vocabulary['tagged_variables'].str.strip(', ')
atomic_vocabulary.to_csv(os.path.join(src_path,'svo_atomic_vocabulary_meta.csv'), index=False)