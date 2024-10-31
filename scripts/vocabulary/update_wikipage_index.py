#################################################################################
#                                                                               #
#   Script for looking up Wikipedia pages and checking for missing or updated   #
#   pages. Input file is updated/overwritten.                                    #
#   input:  source/raw/svo_atomic_vocabulary.csv                                #
#   output: source/raw/svo_atomic_vocabulary.csv                                #
#                                                                               #
#################################################################################

import os
import requests
import pandas as pd
import re
import datetime

def cleanhtml(raw_html):
  CLEANR = re.compile('<.*?>')
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

wikipedia_page_query = 'https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch={}'
wikipedia_url = 'https://en.wikipedia.org/wiki/{}'
# Set the filepath for the SVO atomic vocabulary document.
script_path = os.path.dirname(__file__)
src_path = os.path.join(script_path,'../../source/raw/')
vocabulary_file = 'svo_atomic_vocabulary.csv'
vocabulary_filepath = os.path.join(src_path, vocabulary_file)

# Read in SVO vocabulary and definitions.
vocabulary = pd.read_csv(vocabulary_filepath).fillna('')
if 'last_checked' not in vocabulary.columns.tolist():
    vocabulary['last_checked'] = ''

for i, row in vocabulary.iterrows():
    wikipedia_page = row['wikipedia_page']
    entity_label   = row['entity_label']
    last_checked   = str(row['last_checked']).split('.')[0]
    
    # Check the date to see when definition was last checked
    now = datetime.datetime.now()
    if re.search('[0-9]{8}',last_checked):
        last_checked_date = datetime.datetime.strptime(last_checked,'%Y%m%d')
        time_to_check = now - datetime.timedelta(days = 10)
        if time_to_check < last_checked_date:
            continue

    search_page = True
    if row['wikipedia_page']:
        search_page = False
        r = requests.head(wikipedia_page)
        exists = r.ok
        if not exists:
            print(f'Removing url because it no longer exists: {wikipedia_page}')
            vocabulary.at[i,'wikipedia_page'] = ''
            vocabulary.at[i,'definition'] = ''
            search_page = True
        else:
            vocabulary.at[i,'last_checked'] = now.strftime('%Y%m%d')

    if search_page:
        wikiquery = wikipedia_page_query.format(entity_label)
        response = requests.get(wikiquery)
        pages = response.json().get('query').get('search')
        num_pages = len(pages)
        print('===============================================')
        print(f'Search result for {entity_label} yielded {num_pages} results.')
        if num_pages == 0:
            vocabulary.at[i,'last_checked'] = now.strftime('%Y%m%d')
            continue
        print('I will print out the summaries of each entry one at a time.')
        print('To skip an entry press (n)ext.')
        print('To skip adding a page for this term, press (s)kip.')
        for page in pages:
            snippet = page['snippet']
            cleaned_snippet = cleanhtml(snippet)
            print(f'This entry\'s description is: {cleaned_snippet}')
            response = None
            while response not in ['n','y','s','q']:
                response = input('Press (y)es to add this entry to the vocabulary, (n)ext to go to the next entry and (s)kip to go to the next term: ')
            if response == 'n':
                continue
            if response in ['s','q']:
                break
            pagetitle = page['title'].replace(' ','_')
            pagename = wikipedia_url.format(pagetitle)
            print(f'Adding {pagename} to {entity_label}...')
            vocabulary.at[i,'wikipedia_page'] = pagename            
            break
        if response == 'q':
            break
        vocabulary.at[i,'last_checked'] = now.strftime('%Y%m%d')     

# Write file with any new definitions and definition sources.
vocabulary.to_csv(vocabulary_filepath, index=False)

