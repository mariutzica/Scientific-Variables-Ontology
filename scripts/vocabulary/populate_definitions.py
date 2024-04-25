#################################################################################
#                                                                               #
#   Script for looking up Wikipedia or, alternately, Wikidata definitions for   #
#   atomic terms in SVO. Existing definitions are retained, only missing        #
#   definitions are filled in. Input file is updated/overwritten.               #
#   input:  source/raw/svo_atomic_vocabulary.csv                                #
#   output: source/raw/svo_atomic_vocabulary.csv                                #
#                                                                               #
#################################################################################

import os
import pandas as pd
import requests
from wikidata.client import Client

# Initialize Wikipedia query string.
wikipedia_definition_query = \
    'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext=1&titles={}'

# Set the filepath for the SVO atomic vocabulary document.
script_path = os.path.dirname(__file__)
src_path = os.path.join(script_path,'../../source/raw/')
vocabulary_file = 'svo_atomic_vocabulary.csv'
vocabulary_filepath = os.path.join(src_path, vocabulary_file)

# Read in SVO vocabulary and definitions.
vocabulary = pd.read_csv(vocabulary_filepath).fillna('')

# Create an empty definition, definition source columns if they don't already exist
vocabulary['definition']        = vocabulary.get('definition','')
vocabulary['definition_source'] = vocabulary.get('definition_source','')


# Iterate through vocabulary rows to get definitions for each term if they don't
# already exist. Set verbose flag to True to see which defnitions, if any, are updated.
verbose = False
for i, row in vocabulary.iterrows():
    if not row['definition']:
        definition        = ''
        definition_source = ''

        # First, query Wikipedia for first paragraph on page, if it exists.
        # In a few cases, first paragraph is empty so grab the second paragraph.
        wikipedia_page = row['wikipedia_page']
        if wikipedia_page:
            title = wikipedia_page.split('wiki/')[-1]
            wikiquery = wikipedia_definition_query.format(title)
            response = requests.get(wikiquery)
            pages = response.json().get('query').get('pages')
            page_indices = list(pages.keys())
            if page_indices:
                pageno = page_indices[0]
                try:
                    definition = pages.get(pageno).get('extract').split('\n')[0]
                    if definition == '':
                        definition = pages.get(pageno).get('extract').split('\n')[1]
                    definition_source = 'Wikipedia'
                    if verbose:
                        print('Checking Wikipedia.')
                        print(title)
                        print(definition)
                except:
                    print(f'Error in extracting definition for {wikipedia_page}.')

        # If Wikipedia search did not yield results, search Wikidata.
        if not definition:
            wikidata_page = row['wikidata_page']
            if wikidata_page:
                client = Client()
                entity = client.get(wikidata_page, load=True)
                definition = entity.description
                definition_source = 'Wikidata'
                if verbose:
                    print('Checking Wikidata.')
                    print(title)
                    print(definition)

        # Update definition if it was found.
        if definition != '':
            vocabulary.at[i,'definition']        = definition
            vocabulary.at[i,'definition_source'] = definition_source

# Write file with any new definitions and definition sources.
vocabulary.to_csv(vocabulary_filepath, index=False)

