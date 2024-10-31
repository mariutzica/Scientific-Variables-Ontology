from owlready2 import *
import requests
import os
import pandas as pd
import urllib.parse

template_source = 'source/website_templates'
onto_filepath = 'ontology files'
website_path = 'website'

sitemap_file = 'sitemap.txt'
template_file = 'basic_website_template.html'

# Load sitemap and website templates.
sitemap_path = os.path.join(template_source, sitemap_file)
with open(sitemap_path, 'r') as f:
    sitemap = f.read()

template_path = os.path.join(template_source, template_file)
with open(template_path, 'r') as f:
    template = f.read()

# Set up templates for website components.
definition_paragraph = '<p><emph>Definition:</emph> {}</p>'
varname_paragraph = '<p><emph>Original variable name(s):</emph> {}</p>'
synonyms_paragraph = '<p><emph>Has synonym(s):</emph> {}</p>'
source_paragraph = '<p>Source: {}</p>'
image_paragraph = '<p><img src="{}" alt="picture of term"></p>'
wikipedia_paragraph = '<p><a href="{}" target="_blank">Wikipedia Page</a> (Something wrong with this association? <a href="https://github.com/mariutzica/Scientific-Variables-Ontology/issues/new?assignees=&labels=&template=report-incorrect-resource-link.md&title=%5BBUG+INCORRECT+LINK%5D" target="_blank">Let us know.</a>)</p>'
wikidata_paragraph = '<p><a href="{}" target="_blank">Wikidata Page</a> (Something wrong with this association? <a href="https://github.com/mariutzica/Scientific-Variables-Ontology/issues/new?assignees=&labels=&template=report-incorrect-resource-link.md&title=%5BBUG+INCORRECT+LINK%5D" target="_blank">Let us know.</a>)</p>'
variables_list = '''<p>Occurs in:</p>
    <ul>
        {}
    </ul>'''
variables_element = '<li><a href="{}">{}</a></li>'
create_entry = '''<p>Would you like to link to an existing definition or create a new one? 
You may <a href='{}' target="_blank">check whether a definition exists or add a defintion of this term to Wikipedia</a> or
<a href="https://www.wikidata.org/" target="_blank">check whether the term exists in Wikidata</a> or <a href="https://www.wikidata.org/wiki/Special:NewItem" target="_blank">
create a new term entry in Wikidata</a>
and then <a href='https://github.com/mariutzica/Scientific-Variables-Ontology/issues/new?assignees=&labels=&template=new-documentation-for-existing-entry.md&title=%5BNEW+TERM+DOCUMENTATION+SUBMISSION%5D' target="_blank">
let us know!</a> so we can add it to the ontology.</p>'''
wikipedia_page_base = 'https://en.wikipedia.org/wiki/{}'
property_par = '<p>{}:<ul>{}</ul></p>'
contained_link_element = '<li><a href="{}">{}</a></li>'

wikipedia_image_query = 'http://en.wikipedia.org/w/api.php?action=query&titles={}&prop=pageimages&format=json&pithumbsize=100'
onto = get_ontology(os.path.join(onto_filepath, "svo.owl")).load()
attribute_individuals = get_ontology(os.path.join(onto_filepath, "attribute.owl")).load()
matter_individuals = get_ontology(os.path.join(onto_filepath, "matter.owl")).load()
process_individuals = get_ontology(os.path.join(onto_filepath, "process.owl")).load()
direction_individuals = get_ontology(os.path.join(onto_filepath, "direction.owl")).load()
form_individuals = get_ontology(os.path.join(onto_filepath, "form.owl")).load()
abstraction_individuals = get_ontology(os.path.join(onto_filepath, "abstraction.owl")).load()
trajectory_individuals = get_ontology(os.path.join(onto_filepath, "trajectory.owl")).load()
role_individuals = get_ontology(os.path.join(onto_filepath, "role.owl")).load()
part_individuals = get_ontology(os.path.join(onto_filepath, "part.owl")).load()
domain_individuals = get_ontology(os.path.join(onto_filepath, "domain.owl")).load()
operation_individuals = get_ontology(os.path.join(onto_filepath, "operation.owl")).load()
propertyrole_individuals = get_ontology(os.path.join(onto_filepath, "propertyrole.owl")).load()
propertytype_individuals = get_ontology(os.path.join(onto_filepath, "propertytype.owl")).load()
propertyquantification_individuals = get_ontology(os.path.join(onto_filepath, "propertyquantification.owl")).load()
property_individuals = get_ontology(os.path.join(onto_filepath, "property.owl")).load()
phenomenon_individuals = get_ontology(os.path.join(onto_filepath, "phenomenon.owl")).load()
variable_individuals = get_ontology(os.path.join(onto_filepath, "variable.owl")).load()

# Initialize path for website files.
os.makedirs(website_path, exist_ok=True)

headers = {
    'User-Agent': 'SVOTestScript/2.0 (https://scientificvariablesOntology.org; maria.stoica@colorado.edu) python-requests/2.28'
}

atomic_vocabulary = pd.read_csv('source/svo_atomic_vocabulary_meta.csv').fillna('')

all_properties = []
# Generate webpage for an individual's documentation
def generate_webpage(individual, download_picture = False):

    # Set up the directory for the curent individual.
    directory = individual.iri.split('/')[-2]
    term = individual.iri.split('/')[-1]
    term_url = urllib.parse.unquote(term)
    term_label = individual.label[0]
    term_path = os.path.join('website', directory, term_url)
    os.makedirs(term_path, exist_ok=True)
    
    # Extract first paragraph of definition.
    create_wikipage = False
    definition = individual.comment
    if definition:
        definition = definition_paragraph.format(definition[0])
    else:
        definition = definition_paragraph.format('Not available')
        create_wikipage = True
    
    # Add wikipedia page
    wikipedia_page = individual.has_wikipedia_page
    definition_source = ''
    if wikipedia_page:
        wikipedia_page = wikipedia_page[0]
        wikipedia_page_par = wikipedia_paragraph.format(wikipedia_page)
        definition_source = source_paragraph.format('Wikipedia') #assumption is this is default
    else:
        wikipedia_page_par = ''
    
    # Add wikidata page.
    wikidata_page = individual.has_wikidata_page
    if wikidata_page:
        wikidata_page = wikidata_page[0]
        wikidata_page = wikidata_paragraph.format(wikidata_page)
    else:
        wikidata_page = ''

    # Add original name if different from current.
    original_name = individual.has_original_label
    if original_name:
        original_name = ', '.join(original_name)
        original_varname = varname_paragraph.format(original_name)
    else:
        original_varname = ''

    # Add synonyms if.
    synonyms = individual.has_synonym
    if synonyms:
        synonyms = ', '.join(synonyms)
        synonym_par = synonyms_paragraph.format(synonyms)
    else:
        synonym_par = ''

    # Add text to create a new Wikipedia page
    create_new_entry = ''
    if create_wikipage:
        try:
            label = individual.label[0]
        except:
            label = ''
            print('Label missing:', individual.iri)
        new_wikipedia_page = wikipedia_page_base.format(label)
        create_new_entry = create_entry.format(new_wikipedia_page)

    # Determine if a picture has already been downloaded and if not, 
    # download it (if option enabled)
    files = os.listdir(term_path)
    pic_files = [f for f in files if f.lower().endswith(('png','jpg'))]
    if len(pic_files) >= 1:
        pic_file = pic_files[0]
    else:
        pic_file = None
    if download_picture and not pic_file and wikipedia_page and not '#' in wikipedia_page:            
        page_name = wikipedia_page.split('/')[-1]
        pic_resp = requests.get(wikipedia_image_query.format(page_name), headers=headers)
        pic_link_pages = list(pic_resp.json().get('query').get('pages').keys())
        pageno = pic_link_pages[0]
        try:
            pic_link = pic_resp.json().get('query').get('pages').get(pageno).get('thumbnail').get('source')
            pic_data = requests.get(pic_link, headers=headers)
            #print('Status code:',pic_data.status_code)
            pic_ext = pic_link.split('.')[-1]
            pic_file = f'{term_url}_picture.{pic_ext}'
            with open(os.path.join(term_path,pic_file), 'wb') as handler:
                handler.write(pic_data.content)
            print('Picture found:', term_url)
        except:
            print('No picture found:', term_url)

    if pic_file:
        img_text = image_paragraph.format(pic_file)
    else:
        img_text = ''

    # Determine variables that include this term.
    related_variables = []
    try:
        related_variables = atomic_vocabulary.loc[(atomic_vocabulary['entity_label']==term_url) &\
                         (atomic_vocabulary['entity_class']==directory),'tagged_variables'].tolist()[0]
    except:
        pass

    variables_html = ''
    variable_list_html = ''
    if related_variables:
        related_variables = related_variables.split(', ')
        for variable in related_variables:
            r = list(default_world.sparql("""                    
                    SELECT ?x
                    {{
                    {{ ?x svo:has_original_label "{}" .}}
                    UNION
                    {{ ?x rdfs:label "{}" .}} 
                    }}
                """.format(variable, variable)))
            if r:
                variable_iri = urllib.parse.unquote(r[0][0].iri.split('svo')[1])
                variable_iri = '../..' + variable_iri + '/index.html'
            else:
                variable_iri = ''
                print('Original label not found', variable)
            variable_list_html += variables_element.format(variable_iri, variable)
        variables_html = variables_list.format(variable_list_html)
    
    # Add all of the variable relationships.
    variable_relationships = ''
    for prop in individual.get_properties():
        if prop.python_name in ['label', 'comment', 'has_wikipedia_page', 
                                'has_wikidata_page', 'has_original_label',
                                'has_synonym']:
            continue
        element_list = ''
        ptype = prop.python_name.replace('_',' ').capitalize()
        for value in prop[individual]:
            if isinstance(value, str):
                element_list += value + ', '
            else:
                href = urllib.parse.unquote(value.iri.split('svo')[1])
                href = '../..' + href + '/index.html'
                label = value.label[0]
                element_list += contained_link_element.format(href,label)
        element_list = element_list.rstrip(', ')     
        variable_relationships += property_par.format(ptype, element_list)

    # Write everything to the template string.
    term_template = template.format(term_label, directory, img_text, synonym_par, definition, definition_source, \
                                    wikipedia_page_par, wikidata_page, create_new_entry, \
                                    variable_relationships, original_varname, variables_html)
    index_file = os.path.join(term_path, 'index.html')
    with open(index_file,'w') as f:
        f.write(term_template)

    # Not sure if this is correct, but construct the url and html element to return
    # for the top-level page.
    local_url = term_path.replace('website','https://scientificvariablesontology.org/svo') + 'index.html\n'
    index_ret = contained_link_element.format(term_url + 'index.html', term_label)
    return local_url, index_ret

def generate_individuals_documentation(individuals_onto, ontoclass):
    
    index_template = os.path.join(template_source, f'{ontoclass}_index_template.html')
    index_dest = os.path.join(website_path, ontoclass,'index.html')
    index_str = ''
    sitemap_str = ''
    num_sites = 0
    for individual in individuals_onto.individuals():
        sitemap_add, index_add = generate_webpage(individual)
        sitemap_str += sitemap_add
        index_str += index_add
        num_sites += 1

    index_site_text = f'<ul>{index_str}</ul>'
    with open(index_template,'r') as f:
        site_text = f.read()

    site_text = site_text.replace('Placeholder page',index_site_text)
    with open(index_dest,'w') as f:
        f.write(site_text)

    return sitemap_str, num_sites

subontologies = {phenomenon_individuals: 'phenomenon', 
                 property_individuals: 'property', 
                 part_individuals: 'part',
                 process_individuals: 'process', 
                 variable_individuals: 'variable', 
                 role_individuals: 'role',
                 propertyrole_individuals: 'propertyrole', 
                 propertytype_individuals: 'propertytype', 
                 propertyquantification_individuals: 'propertyquantification',
                 form_individuals: 'form', 
                 abstraction_individuals: 'abstraction', 
                 attribute_individuals: 'attribute',
                 direction_individuals: 'direction', 
                 domain_individuals: 'domain', 
                 trajectory_individuals : 'trajectory',
                 operation_individuals: 'operation', 
                 matter_individuals: 'matter'}

sitemap_str = ''
num_sites = 0
for individuals_ontology, ontoclass in subontologies.items():
    sitemap_add, num_subonto_sites = generate_individuals_documentation(individuals_ontology, ontoclass)
    sitemap_str += sitemap_add
    num_sites += num_subonto_sites

# Sitemaps cannot list more than 50,000 URLs or be more than 50MB in size
sitemap = sitemap + sitemap_str
with open('website/sitemap.txt','w') as f:
    f.write(sitemap)
print('Number sites:', num_sites)
