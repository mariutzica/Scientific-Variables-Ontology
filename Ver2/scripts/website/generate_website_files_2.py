from owlready2 import *
from pathlib import Path
import requests
import os
import pandas as pd
import urllib.parse


sitemap = \
"""https://scientificvariablesontology.org/index.html
https://scientificvariablesontology.org/documentation.html
https://scientificvariablesontology.org/faq.html
https://scientificvariablesontology.org/tutorial_create_variable_manually.html
https://scientificvariablesontology.org/svo/index.html
https://scientificvariablesontology.org/svo/phenomenon/index.html
https://scientificvariablesontology.org/svo/matter/index.html
https://scientificvariablesontology.org/svo/process/index.html
https://scientificvariablesontology.org/svo/property/index.html
https://scientificvariablesontology.org/svo/variable/index.html
https://scientificvariablesontology.org/svo/role/index.html
https://scientificvariablesontology.org/svo/direction/index.html
https://scientificvariablesontology.org/svo/domain/index.html
https://scientificvariablesontology.org/svo/trajectory/index.html
https://scientificvariablesontology.org/svo/form/index.html
https://scientificvariablesontology.org/svo/propertyrole/index.html
https://scientificvariablesontology.org/svo/propertyquantification/index.html
https://scientificvariablesontology.org/svo/propertytype/index.html
https://scientificvariablesontology.org/svo/abstraction/index.html
https://scientificvariablesontology.org/svo/attribute/index.html
https://scientificvariablesontology.org/svo/model/index.html
https://scientificvariablesontology.org/svo/part/index.html
https://scientificvariablesontology.org/svo/operation/index.html
"""

template = """
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://scientificvariablesontology.org/css/stylesheet.css">
</head>
<body>
  <header id="navigation">
    <a href="https://scientificvariablesontology.org/index.html"><img id="logo" src="https://scientificvariablesontology.org/pics/svo_logo.png" alt="logo"></a>
    <nav>
      <ul id="menu">
        <li class="menu-heading"><a href="https://scientificvariablesontology.org/documentation.html">Documentation</a></li>
        <li class="menu-heading"><a href="https://scientificvariablesontology.org/tutorial_create_variable_manually.html">Tutorial</a></li>
        <hr>
        <li class="menu-heading"><a href="https://scientificvariablesontology.org/svo/index.html">Get Ontology</a></li>
        <hr>
        <li class="menu-heading"><a href="https://scientificvariablesontology.org/faq.html">FAQ</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <h1>{}</h1>
    <h2><a href='../index.html'>{}</a></h2>
    {}
    {}
    {}
    {}
    {}
    {}
    {}
    {}
    {}
  </main>
</body>
"""

definition_paragraph = '<p><emph>Definition:</emph> {}</p>'
varname_paragraph = '<p><emph>Original variable name(s):</emph> {}</p>'
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
contained_element = '<li><a href="{}">{}</a></li>'

wikipedia_image_query = 'http://en.wikipedia.org/w/api.php?action=query&titles={}&prop=pageimages&format=json&pithumbsize=100'
onto = get_ontology("ontology files/svo.owl").load()
phenomenon_individuals = get_ontology("ontology files/phenomenon.owl").load()
matter_individuals = get_ontology("ontology files/matter.owl").load()
process_individuals = get_ontology("ontology files/process.owl").load()
property_individuals = get_ontology("ontology files/property.owl").load()
operation_individuals = get_ontology("ontology files/operation.owl").load()
propertyrole_individuals = get_ontology("ontology files/propertyrole.owl").load()
propertytype_individuals = get_ontology("ontology files/propertytype.owl").load()
propertyquantification_individuals = get_ontology("ontology files/propertyquantification.owl").load()
domain_individuals = get_ontology("ontology files/domain.owl").load()
form_individuals = get_ontology("ontology files/form.owl").load()
abstraction_individuals = get_ontology("ontology files/abstraction.owl").load()
model_individuals = get_ontology("ontology files/model.owl").load()
attribute_individuals = get_ontology("ontology files/attribute.owl").load()
direction_individuals = get_ontology("ontology files/direction.owl").load()
trajectory_individuals = get_ontology("ontology files/trajectory.owl").load()
role_individuals = get_ontology("ontology files/role.owl").load()
part_individuals = get_ontology("ontology files/part.owl").load()
variable_individuals = get_ontology("ontology files/variable.owl").load()

Path('website').mkdir(parents=True, exist_ok=True)

headers = {
    'User-Agent': 'SVOTestScript/2.0 (https://scientificvariablesOntology.org; maria.stoica@colorado.edu) python-requests/2.28'
}

atomic_vocabulary = pd.read_csv('source/svo_atomic_vocabulary_meta.csv').fillna('')

def generate_webpage(individual):

    create_option = False
    directory = individual.iri.split('/')[-2]
    term = individual.iri.split('/')[-1]
    term_url = urllib.parse.quote(term, safe='/', encoding=None, errors=None)
    term_label = individual.label[0]
    term_path = 'website/' + directory + '/' + term + '/'
    Path(term_path).mkdir(parents=True, exist_ok=True)
    
    definition = individual.comment
    if definition:
        definition = definition_paragraph.format(definition[0])
    else:
        definition = definition_paragraph.format('Not available')
        create_option = True
    
    wikipedia_page = individual.has_wikipedia_page
    definition_source = ''
    if wikipedia_page:
        wikipedia_page = wikipedia_page[0]
        wikipedia_page = wikipedia_paragraph.format(wikipedia_page)
        definition_source = source_paragraph.format('Wikipedia') #assumption is this is default
    else:
        wikipedia_page = ''
    
    wikidata_page = individual.has_wikidata_page
    if wikidata_page:
        wikidata_page = wikidata_page[0]
        wikidata_page = wikidata_paragraph.format(wikidata_page)
    else:
        wikidata_page = ''

    original_name = individual.has_original_label
    if original_name:
        original_name = ', '.join(original_name)
        original_varname = varname_paragraph.format(original_name)
    else:
        original_varname = ''

    create_new_entry = ''
    if create_option:
        try:
            label = individual.label[0]
        except:
            label = ''
            print('Label missing:', individual.iri)
        new_wikipedia_page = wikipedia_page_base.format(label)
        create_new_entry = create_entry.format(new_wikipedia_page)

    # download and save thumbnail picture to directory
    files = os.listdir(term_path)
    pic_file = ''
    for f in files:
        f_endswith = f.split('.')[-1].lower()
        if f_endswith in ['png','jpg']:
            pic_file = f
            break
            #os.remove(os.path.join(term_path,f))
    if False and not pic_file and wikipedia_page:
        pic_resp = requests.get(wikipedia_image_query.format(term), headers=headers)
        pic_link_pages = list(pic_resp.json().get('query').get('pages').keys())
        pageno = pic_link_pages[0]
        try:
            pic_link = pic_resp.json().get('query').get('pages').get(pageno).get('thumbnail').get('source')
            pic_data = requests.get(pic_link, headers=headers)
            #print('Status code:',pic_data.status_code)
            pic_ext = pic_link.split('.')[-1]
            pic_file = f'{term}_picture.{pic_ext}'
            with open(os.path.join(term_path,pic_file), 'wb') as handler:
                handler.write(pic_data.content)
        except:
            print('No picture found:', term)

    if pic_file:
        img_text = image_paragraph.format(pic_file)
    else:
        img_text = ''

    # variables with this term
    related_variables = []
    try:
        related_variables = atomic_vocabulary.loc[(atomic_vocabulary['entity_id']==term) & \
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
                    {{ ?x svo:has_original_label "{}" .}}
                """.format(variable)))
            
            if r:
                variable_iri = '../..' + r[0][0].iri.split('svo')[1] + '/index.html'
            else:
                variable_iri = ''
                print('Original label not found', variable)
            variable_iri = urllib.parse.quote(variable_iri, safe='/', encoding=None, errors=None)
            variable_list_html += variables_element.format(variable_iri, variable)
        variables_html = variables_list.format(variable_list_html)
    
    relationships = ''
    for prop in individual.get_properties():
        if prop.python_name in ['describes_phenomenon', 'describes_property',
                                    'contains_phenomenon_reference_to', 'contains_process_reference_to',
                                    'contains_matter_reference_to', 'contains_property_reference_to',
                                    'contains_operation_reference_to','contains_role_reference_to',
                                    'contains_abstraction_reference_to','contains_model_reference_to',
                                    'contains_attribute_reference_to', 'contains_part_reference_to',
                                    'contains_trajectory_reference_to','contains_form_reference_to', 
                                    'has_matter', 'has_process', 'has_source',
                                    'has_location', 'has_location_of_origin',
                                    'undergoes_process', 'has_form',
                                    'has_abstraction', 'has_part', 'has_main_participant',
                                    'has_in_participant', 'has_medium_participant',
                                    'has_source_participant', 'has_sink_participant',
                                    'has_numerator_participant', 'has_attribute',
                                    'has_role', 'has_trajectory', 'has_observed_element',
                                    'has_observing_element', 'contains', 'contains_part',
                                    'has_container', 'has_medium_container', 'has_perspective']:
            element_list = ''
            ptype = prop.python_name.replace('_',' ').capitalize()
            for value in prop[individual]:
                href = '../..' + value.iri.split('svo')[1] + '/index.html'
                href =  urllib.parse.quote(href, safe='/', encoding=None, errors=None)
                label = value.label[0]
                element_list += contained_element.format(href,label)
                
            relationships += property_par.format(ptype, element_list)

    term_template = template.format(term_label, directory, img_text, definition, definition_source, \
                                    relationships, wikipedia_page, \
                                    wikidata_page, original_varname, create_new_entry, variables_html)
    with open(term_path+'index.html','w') as f:
        f.write(term_template)

    local_url = term_path.replace('website','https://scientificvariablesontology.org/svo') + 'index.html\n'
    index_ret = contained_element.format(term_url+'/index.html',term_label)
    return local_url, index_ret


def generate_individuals_documentation(individuals_onto, ontoclass):
    
    index_str = ''
    sitemap_str = ''
    num_sites = 0
    for individual in individuals_onto.individuals():
        sitemap_add, index_add = generate_webpage(individual)
        sitemap_str += sitemap_add
        index_str += index_add
        num_sites += 1

    index_site_text = f'<ul>{index_str}</ul>'
    with open(f'website/{ontoclass}/index_template.html','r') as f:
        site_text = f.read()

    site_text = site_text.replace('Placeholder page',index_site_text)
    with open(f'website/{ontoclass}/index.html','w') as f:
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
                 model_individuals: 'model', 
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
