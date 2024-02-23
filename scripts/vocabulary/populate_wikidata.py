#################################################################################
#                                                                               #
#   Script for looking up Wikidata pages as linked to Wikipedia.                #
#   Input file is overwritten.
#   input:  source/raw/svo_atomic_vocabulary.csv                                #
#   output: source/raw/svo_atomic_vocabulary.csv                                #
#                                                                               #
#################################################################################

import os
import pandas as pd
import requests

# Set up Wikipedia query string.
wikipedia_definition_query = \
    'https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&format=json&titles={}'

# Set the filepath for the SVO atomic vocabulary document.
script_path = os.path.dirname(__file__)
src_path = os.path.join(script_path,'../../source/raw/')
vocabulary_file = 'svo_atomic_vocabulary.csv'
vocabulary_filepath = os.path.join(src_path, vocabulary_file)

# Read in SVO vocabulary. Set wikidata page to empty if not already present.
vocabulary = pd.read_csv(vocabulary_filepath).fillna('')
vocabulary['wikidata_page'] = vocabulary.get('wikidata_page','')

# Loop through the rows of the vocabulary looking for missing Wikidata pages
# and fill them in if found.
for i, row in vocabulary.iterrows():
    if not row['wikidata_page']:
        wikidata_page = ''

        wikipedia_page = row['wikipedia_page']
        if wikipedia_page:
            print('Wikipedia page:', wikipedia_page)
            title = wikipedia_page.split('wiki/')[-1]
            wikiquery = wikipedia_definition_query.format(title)
            response = requests.get(wikiquery)
            pages = response.json().get('query').get('pages')
            page_indices = list(pages.keys())
            if page_indices:
                pageno = page_indices[0]
                try:
                    wikidata_page = pages.get(pageno).get('pageprops').get('wikibase_item')
                except:
                    print(f'Error in getting Wikidata page.')
        vocabulary.at[i,'wikidata_page'] = wikidata_page

# Write result back to the same file.
vocabulary.to_csv(vocabulary_filepath, index=False)