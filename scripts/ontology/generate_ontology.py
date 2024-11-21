#################################################################################
#                                                                               #
#   Script for generating ontology files from atomized names.                   #
#                                                                               #
#   input:  source/raw/svo_atomic_vocabulary.csv,                               #
#           source/csdms_annotated_names.csv                                    #
#           source/variable_name_tags.csv                                       #
#           source/csdms_atomized.csv                                           #
#   output: source/quicklookup/{classname}.txt                                  #
#                                                                               #
#################################################################################

import os
from owlready2 import *
import csv
import pandas as pd
import urllib.parse
from rdflib import Graph

def parse_owl_file(filepath):

    owl_content = {}
    with open(filepath, 'r') as f:
        text = f.readlines()

    header_line = text[0]
    owl_content['header'] = header_line

    line_index = 1
    current_line = text[line_index]
    while '>' not in current_line:
        line_index += 1
        current_line = text[line_index]
    
    line_index += 1
    namespace_lines = ''.join(text[1:line_index])
    owl_content['namespace'] = namespace_lines

    end_tag = text[-1]
    owl_content['end_tag'] = end_tag

    current_line = text[line_index]
    start_section = '<owl:NamedIndividual rdf:about='
    end_section = '</owl:NamedIndividual>'
    while current_line != end_tag:
        while start_section not in current_line:
            line_index += 1
            current_line = text[line_index]
        start_index = line_index
        while end_section not in current_line:
            line_index += 1
            current_line = text[line_index]
        line_index += 1
        current_line = text[line_index]
        end_index = line_index
        entity_name = text[start_index].split('"')[1]
        section_text = ''.join(text[start_index:end_index])
        owl_content[entity_name] = section_text
        while current_line == '\n':
            line_index += 1
            current_line = text[line_index]
    return owl_content

# Set up input files.
script_path               = os.path.dirname(__file__)
raw_path                  = os.path.join(script_path,'../../source/raw/')
atomic_terms_filename     = 'svo_atomic_vocabulary.csv'
terminology_file          = os.path.join(raw_path,atomic_terms_filename)
class_definitions_fname   = 'class_definitions.csv'
class_definitions_fpath   = os.path.join(raw_path, class_definitions_fname)
src_path                  = os.path.join(script_path,'../../source/')
variable_filename         = 'variable_name_tags.csv'
variable_file             = os.path.join(src_path,variable_filename)
annotated_object_filename = 'csdms_annotated_names.csv'
annotated_object_file     = os.path.join(src_path, annotated_object_filename)
object_filename           = 'csdms_atomized.csv'
object_file               = os.path.join(src_path, object_filename)

wikidata_http             = 'https://www.wikidata.org/wiki/{}'

# Set up component ontologies.
onto                   = get_ontology("http://scientificvariablesontology.org/svo#")
phenomenon_individuals = get_ontology("http://scientificvariablesontology.org/svo/phenomenon/")
matter_individuals     = get_ontology("http://scientificvariablesontology.org/svo/matter/")
process_individuals    = get_ontology("http://scientificvariablesontology.org/svo/process/")
property_individuals   = get_ontology("http://scientificvariablesontology.org/svo/property/")
operation_individuals  = get_ontology("http://scientificvariablesontology.org/svo/operation/")
variable_individuals   = get_ontology("http://scientificvariablesontology.org/svo/variable/")
abstraction_individuals = get_ontology("http://scientificvariablesontology.org/svo/abstraction/")
attribute_individuals  = get_ontology("http://scientificvariablesontology.org/svo/attribute/")
direction_individuals  = get_ontology("http://scientificvariablesontology.org/svo/direction/")
form_individuals       = get_ontology("http://scientificvariablesontology.org/svo/form/")
role_individuals       = get_ontology("http://scientificvariablesontology.org/svo/role/")
trajectory_individuals = get_ontology("http://scientificvariablesontology.org/svo/trajectory/")
part_individuals       = get_ontology("http://scientificvariablesontology.org/svo/part/")
propertyrole_individuals = get_ontology("http://scientificvariablesontology.org/svo/propertyrole/")
propertyquantification_individuals = get_ontology("http://scientificvariablesontology.org/svo/propertyquantification/")
propertytype_individuals = get_ontology("http://scientificvariablesontology.org/svo/propertytype/")
domain_individuals     = get_ontology("http://scientificvariablesontology.org/svo/domain/")

# Obtain class definitions for upper ontology.
with open(class_definitions_fpath, mode='r') as cdefs:
    reader = csv.reader(cdefs)
    class_definitions = {rows[0]:rows[1] for rows in reader}

# Set up top-level ontology classes.
with onto:
    class Phenomenon(Thing): 
        comment = class_definitions['Phenomenon']
    class Matter(Thing):
        comment = class_definitions['Matter']
    class Process(Thing):
        comment = class_definitions['Process']
    class Property(Thing):
        comment = class_definitions['Property']
    class Operation(Thing):
        comment = class_definitions['Operation']
    class Variable(Thing):
        comment = class_definitions['Variable']
    class Abstraction(Thing):
        comment = class_definitions['Abstraction']
    class Attribute(Thing):
        comment = class_definitions['Attribute']
    class Direction(Thing):
        comment = class_definitions['Direction']
    class Form(Thing):
        comment = class_definitions['Form']
    class Role(Thing):
        comment = class_definitions['Role']
    class Trajectory(Thing):
        comment = class_definitions['Trajectory']
    class Part(Thing):
        comment = class_definitions['Part']
    class PropertyRole(Thing):
        comment = class_definitions['PropertyRole']
    class PropertyType(Thing):
        comment = class_definitions['PropertyType']
    class PropertyQuantification(Thing):
        comment = class_definitions['PropertyQuantification']
    class Domain(Thing):
        comment = class_definitions['Domain']

    # Variable relationships
    class describes_phenomenon(Variable >> Phenomenon, FunctionalProperty): pass
    class describes_property(Variable >> Property, FunctionalProperty): pass

    # Intra-phenomenon relationships
    class has_domain(Phenomenon >> Domain): pass
    class has_phenomenon(Phenomenon >> Phenomenon): pass
    class has_matter(Phenomenon >> Matter): pass
    class contains_matter(Phenomenon >> Matter): pass
    class contains_primary_matter(Phenomenon >> Matter): pass
    class has_medium_matter(Phenomenon >> Matter): pass
    class has_process(Phenomenon >> Process): pass
    class undergoes_process(Phenomenon >> Process): pass
    class has_form(Phenomenon >> Form): pass
    class has_abstraction(Phenomenon >> Abstraction): pass
    class is_modeled_by(ObjectProperty): pass
    class is_expressed_as(ObjectProperty): pass
    class has_part(Phenomenon >> Part): pass
    class has_attribute(Phenomenon >> Attribute): pass
    class has_trajectory(Phenomenon >> Trajectory): pass
    class has_role(Phenomenon >> Role): pass
    class has_source_phenomenon(ObjectProperty): pass
    class has_location(ObjectProperty): pass
    class has_location_of_origin(ObjectProperty): pass
    class has_participant_phenomenon(Phenomenon >> Phenomenon): pass
    class has_minuend_participant_phenomenon(has_participant_phenomenon): pass
    class has_subtrahend_participant_phenomenon(has_participant_phenomenon): pass
    class has_primary_participant_phenomenon(has_participant_phenomenon): pass
    class has_adjacent_participant_phenomenon(has_participant_phenomenon): pass
    class has_first_participant_phenomenon(has_participant_phenomenon): pass
    class has_second_participant_phenomenon(has_participant_phenomenon): pass
    class has_in_participant_phenomenon(has_participant_phenomenon): pass
    class has_medium_participant_phenomenon(has_participant_phenomenon): pass
    class has_source_participant_phenomenon(has_participant_phenomenon): pass
    class has_sink_participant_phenomenon(has_participant_phenomenon): pass
    class has_numerator_participant_phenomenon(has_participant_phenomenon): pass
    class has_denominator_participant_phenomenon(has_participant_phenomenon): pass
    class has_perspective_participant_phenomenon(has_participant_phenomenon): pass
    class has_participating_primary_phenomenon(ObjectProperty): pass
    class has_observing_phenomenon(ObjectProperty): pass
    class has_modeled_phenomenon(ObjectProperty): pass
    class has_modeling_phenomenon(ObjectProperty): pass
    class has_containing_phenomenon(ObjectProperty): pass
    class has_containing_medium_phenomenon(ObjectProperty): pass
    class is_part_of_containing_phenomenon(ObjectProperty): pass
    class surrounds(ObjectProperty): pass
    class has_measurement_reference(ObjectProperty): pass
    class has_measurement_reference_at(has_measurement_reference): pass
    class has_measurement_reference_above(has_measurement_reference): pass
    class has_measurement_reference_since(has_measurement_reference): pass
    class has_measurement_reference_along(has_measurement_reference): pass
    class has_measurement_reference_from(has_measurement_reference): pass
    class has_measurement_reference_to(has_measurement_reference): pass
    class has_measurement_reference_below(has_measurement_reference): pass
    class has_measurement_reference_wrt(has_measurement_reference): pass
    class is_reference_for_property(ObjectProperty): pass
    class has_reference_for_property(ObjectProperty): pass
    class is_reference_for_variable(ObjectProperty): pass
    class has_reference_for_variable(ObjectProperty): pass
    class orbits(ObjectProperty): pass
    class contains_reference_to(ObjectProperty): pass
    class contains_phenomenon_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Phenomenon]
    class contains_process_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Process]
    class contains_matter_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Matter]
    class contains_property_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Property]
    class contains_form_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Form]
    class contains_abstraction_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Abstraction]
    class contains_operation_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Operation]
    class contains_role_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Role]
    class contains_part_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Part]
    class contains_trajectory_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Trajectory]
    class contains_attribute_reference_to(contains_reference_to):
        domain    = [Variable]
        range     = [Attribute]
    class is_transformation_of(Property >> Property): pass
    class is_transformed_by(Property >> Operation): pass
    class has_phenomenon_root(Phenomenon >> Phenomenon, FunctionalProperty): pass
    class has_abstraction_root(Abstraction >> Abstraction, FunctionalProperty): pass
    class has_matter_root(Matter >> Matter, FunctionalProperty): pass
    class has_form_root(Form >> Form, FunctionalProperty): pass
    class has_part_root(Part >> Part, FunctionalProperty): pass
    class has_process_root(Process >> Process, FunctionalProperty): pass
    class has_role_root(Role >> Role, FunctionalProperty): pass
    class has_direction(ObjectProperty): pass
    class has_wikipedia_page(AnnotationProperty): pass
    class has_wikidata_page(AnnotationProperty): pass
    class has_synonym(AnnotationProperty): pass
    class has_original_label(AnnotationProperty): pass

# Set the annotation properties for an Individual.
def set_individual_annotation(individual, label, wikipedia_page, synonyms, definition, wikidata_page):
    individual.label = label
    if wikipedia_page:
        individual.has_wikipedia_page = wikipedia_page
    if wikidata_page:
        individual.has_wikidata_page = wikidata_http.format(wikidata_page)
    if synonyms:
        individual.has_synonym = synonyms.split(', ')
    if definition:
        individual.comment = definition

class_mapping = {'phenomenon' : {'individuals' : phenomenon_individuals, 'class': onto.Phenomenon},
                 'matter'     : {'individuals' : matter_individuals,     'class': onto.Matter},
                 'process'    : {'individuals' : process_individuals,    'class': onto.Process},
                 'property'   : {'individuals' : property_individuals,   'class': onto.Property},
                 'operation'  : {'individuals' : operation_individuals,  'class': onto.Operation},
                 'abstraction': {'individuals' : abstraction_individuals,'class': onto.Abstraction},
                 'model'      : {'individuals' : abstraction_individuals,'class': onto.Abstraction},
                 'attribute'  : {'individuals' : attribute_individuals,  'class': onto.Attribute},
                 'direction'  : {'individuals' : direction_individuals,  'class': onto.Direction},
                 'form'       : {'individuals' : form_individuals,       'class': onto.Form}, 
                 'role'       : {'individuals' : role_individuals,       'class': onto.Role},
                 'trajectory' : {'individuals' : trajectory_individuals, 'class': onto.Trajectory},
                 'part'       : {'individuals' : part_individuals,       'class': onto.Part},
                 'propertytype': {'individuals' : propertytype_individuals, 'class': onto.PropertyType},
                 'propertyrole': {'individuals' : propertyrole_individuals, 'class': onto.PropertyRole},
                 'propertyquantification': {'individuals' : propertyquantification_individuals, \
                                            'class': onto.PropertyQuantification},
                 'domain'     : {'individuals' : domain_individuals,     'class': onto.Domain}, \
                 'variable'   : {'individuals' : variable_individuals,   'class': onto.Variable} }

# Add atomic SVO vocabulary terms to ontology.
f = open(terminology_file)
reader = csv.reader(f)
next(reader)
print('Adding atomic vocabulary from vocab file ...')
for row in reader:
    try:
        entity_id, entity_label, entity_class, entity_synonym, _, \
            entity_wikipedia_page, entity_definition, entity_definition_source, entity_wikidata, _ = row
    except:
        print('Problem reading line after: ', entity_id)
        continue
    if entity_class not in class_mapping.keys():
        print('Missing class:', entity_class, entity_label)
        # 'band' does not currently have a class, but not used in CSN
        continue

    individual_mapping = class_mapping[entity_class]
    individuals_ontology = individual_mapping['individuals']
    ontoclass = individual_mapping['class']

    entity_id_enc = urllib.parse.quote(entity_id, safe='/', encoding=None, errors=None)
    #print(f'Adding {entity_id_enc} to {ontoclass}.')
    with individuals_ontology:
        individual = ontoclass(entity_id_enc)
        set_individual_annotation(individual, entity_label, entity_wikipedia_page, \
                                        entity_synonym, entity_definition, entity_wikidata)
        

categories_override = \
{
    'front': 'part',
    'cell':'abstraction',
    'expression':'abstraction',
    'building': 'phenomenon',
    'radiation': 'phenomenon',
    'vegetation': 'phenomenon',
    'link': 'form',
    'skin': 'phenomenon',
    'body': 'phenomenon',
    'neck': 'part',
    'grain': 'phenomenon',
    'mercury': 'matter',
    'square': 'abstraction',
}

# Add phenomenon link to the ontology if it is missing
svo_terminology = pd.read_csv(terminology_file)
plural_vocabulary = svo_terminology['plural'].dropna().tolist()

# Read in the complex phenomena generated and atomized from the object_names of the variables and
# add them to the ontology.
object_info = pd.read_csv(object_file).fillna('')
s = object_info.encoded_name.str.len().sort_values().index
object_info = object_info.reindex(s)
object_info = object_info.reset_index(drop=True)

rel_list = list(object_info.columns)
phenomenon_relationships = {
    'phenomenon': [],
    'process'   : [],
    'matter'   : [],
    'role'   : [],
    'form'   : [],
    'domain'   : [],
    'abstraction': [],
    'part': [],
    'trajectory': [],
    'variable':   [],
    'property': [],
}

for rel in rel_list:
    rel_comp = rel.rstrip('2')
    if rel in ['encoded_name', 'label_name']:
        continue
    if rel_comp.endswith('phenomenon') or 'location' in rel_comp or \
        rel_comp in ['surrounds', 'orbits-around', 'is-observed-by']:
        phenomenon_relationships['phenomenon'].append(rel)
    elif rel_comp.endswith('property'):
        phenomenon_relationships['property'].append(rel)
    elif rel_comp.endswith('matter') or 'expressed-as' in rel_comp:
        phenomenon_relationships['matter'].append(rel)
    elif rel_comp.endswith('role'):
        phenomenon_relationships['role'].append(rel)
    elif rel_comp.endswith('process'):
        phenomenon_relationships['process'].append(rel)
    elif rel_comp.endswith('form'):
        phenomenon_relationships['form'].append(rel)
    elif rel_comp.endswith('domain'):
        phenomenon_relationships['domain'].append(rel)
    elif rel_comp.endswith('abstraction') or rel_comp == 'is-modeled-by-abstraction':
        phenomenon_relationships['abstraction'].append(rel)
    elif rel_comp.endswith('trajectory'):
        phenomenon_relationships['trajectory'].append(rel)
    elif rel_comp.endswith('part'):
        phenomenon_relationships['part'].append(rel)
    elif rel_comp.endswith('variable'):
        phenomenon_relationships['variable'].append(rel)
    else:
        phenomenon_relationships['phenomenon'].append(rel)

def add_phen_link(phen_link, category = 'phenomenon', printit = False):

    # If phen link is empty, return
    if phen_link == '':
        return None
    
    # Set entity id (change to singular if plural).
    phen_link_id = phen_link
    if category == 'variable':
        phen_link_id = '(' + phen_link_id.replace('-has-property-',')-has-property-(') + ')'
    if phen_link_id in plural_vocabulary:
        phen_link_id = svo_terminology.loc[\
                                (svo_terminology['plural']==phen_link),'entity_id'].iloc[0]
        if printit:
            print(f'{phen_link} found in plural. Switching for single term {phen_link_id}.')

    # Check to make sure category provided is valid
    # Determine the class and individuals to use.
    if category not in class_mapping.keys():
        print(f'ERROR in add_phen_link. Category {category} not valid.')
        return None
    
    individual_mapping = class_mapping[category]
    individuals_ontology = individual_mapping['individuals']
    ontoclass = individual_mapping['class']
    
    # If already present, skip.
    if individuals_ontology[phen_link_id] in individuals_ontology.individuals():
        if printit:
            print(f'{phen_link_id} already present in {individuals_ontology}.')
        return (phen_link_id, category)
    
    # Determine label to use.
    try:
        phen_link_label = object_info.loc[object_info['encoded_name']==phen_link_id,\
                                    'label_name'].iloc[0]
    except:
        try:
            phen_link_label = svo_terminology.loc[(svo_terminology['entity_id']==phen_link_id) &\
                                (svo_terminology['entity_class']==category),\
                                    'entity_label'].iloc[0]
        except:
            if printit:
                print(f'Label for {phen_link_id} of type {category} not found. Setting label to link name.')
            phen_link_label = phen_link_id
    if category == 'variable':
        phen_link_label = phen_link_label.replace('-has-property-','__') 

    # Add the phen link id to the desired individuals.
    phen_link_id_enc = urllib.parse.quote(phen_link_id, safe='/', encoding=None, errors=None)
    if printit:
        print(f'Adding {phen_link_id_enc} to {individuals_ontology}.')
    with individuals_ontology:
        individual = ontoclass(phen_link_id_enc)
        individual.label = phen_link_label
    
    if phen_link_id in object_info['encoded_name'].tolist():
        if printit:
            print(f'Successfully added phenomenon subobject {phen_link_id_enc}.')
        return (phen_link_id_enc, 'phenomenon')
    
    # Check to see if the entity is a variable.
    if category == 'variable':
        
        # Determine object and property and add to ontology.
        object_name = phen_link_id.split('-has-property-')[0]
        property_name = phen_link_id.split('-has-property-')[1]
        object_added, _ = add_phen_link(object_name)
        property_added, _ = add_phen_link(property_name, category = 'property')

        # Add variable components.
        with individuals_ontology:
            print(individual, object_added, property_added)
            individual.describes_phenomenon = phenomenon_individuals[object_added]
            individual.describes_property = property_individuals[property_added]
        
        if printit:
            print(f'Successfully added variable {phen_link_id_enc}.')
        return (phen_link_id_enc, 'variable')
    
    # Determine if phen is a compound phenomenon
    if '-and-' in phen_link_id or '-or-' in phen_link_id or '-vs-' in phen_link_id:
        # Split up the phenomenon id and add each component to the ontology.
        # Then add link.
        multiphen = re.split('-and-|-or-|-vs-',phen_link_id)
        multiphen = [p.strip('()') for p in multiphen]
        for p in multiphen:
            phen_added, _ = add_phen_link(p)
            with individuals_ontology:
                individual.has_phenomenon.append(phenomenon_individuals[phen_added])
        if printit:
            print(f'Successfully added compound phenomenon {phen_link_id_enc}.')
        return (phen_link_id_enc, 'phenomenon')

    # Determine the object root if attributes are present.
    attrs = None
    object_root = phen_link_id       
    if '~' in phen_link_id:
        attrs = phen_link_id.split('~',1)[1]
        attrs = re.split('~|-and-', attrs)
        object_root = phen_link_id.split('~')[0]

    # Determine what the phen_link category is in the vocabulary
    try:
        if object_root in categories_override.keys():
            phen_link_category = categories_override[object_root]
        elif category != 'phenomenon':
            phen_link_category = category
        else:
            phen_link_category = svo_terminology.loc[\
                        (svo_terminology['entity_id']==object_root),'entity_class'].tolist()
            if len(phen_link_category) > 1:
                print(f'Warning, more than one category found for {phen_link_id}.')
                print(object_root, phen_link_category)
                input('Press enter to continue ...')
            phen_link_category = phen_link_category[0]
    except:
        phen_link_category = category

    if phen_link_category == 'model':
        phen_link_category = 'abstraction'

    if not attrs and (phen_link_category == category):
        if printit:
            print(f'Successfully added {phen_link_id_enc} to {category}.')
        return (phen_link_id_enc, category)
    
    # Add relationship to atomistic individual if categories are not the same.
    if phen_link_category != category:
        # First add the atomistic term to the ontology
        link_added, _ = add_phen_link(phen_link_id, category = phen_link_category)
        # Then add relationship to it.
        with individuals_ontology:
            if phen_link_category == 'matter':
                matter_link = matter_individuals[link_added]
                individual.has_matter.append(matter_link)
            elif phen_link_category == 'form':
                form_link = form_individuals[link_added]
                individual.has_form.append(form_link)
            elif phen_link_category == 'role':
                role_link = role_individuals[link_added]
                individual.has_role.append(role_link)
            elif phen_link_category == 'abstraction':
                abstraction_link = abstraction_individuals[link_added]
                individual.has_abstraction.append(abstraction_link)
            elif phen_link_category == 'part':
                part_link = part_individuals[link_added]
                individual.has_part.append(part_link)
            elif phen_link_category == 'domain':
                domain_link = domain_individuals[link_added]
                individual.has_domain.append(domain_link)
            elif phen_link_category == 'process':
                process_link = process_individuals[link_added]
                individual.undergoes_process.append(process_link)
            elif phen_link_category == 'attribute':
                attribute_link = attribute_individuals[link_added]
                individual.has_attribute.append(attribute_link)
            else:
                print(f'Relationship not added for category {phen_link_category} ...')
                print(phen_link_id, category, link_added)
    elif attrs:
        # First add the atomistic term to the ontology
        link_added, _ = add_phen_link(object_root, category = phen_link_category)
        # Then add relationship to it.
        with individuals_ontology:
            if phen_link_category == 'matter':
                matter_link = matter_individuals[link_added]
                individual.has_matter_root = matter_link
            elif phen_link_category == 'form':
                form_link = form_individuals[link_added]
                individual.has_form_root = form_link
            elif phen_link_category == 'role':
                role_link = role_individuals[link_added]
                individual.has_role_root = role_link
            elif phen_link_category == 'abstraction':
                abstraction_link = abstraction_individuals[link_added]
                individual.has_abstraction_root = abstraction_link
            elif phen_link_category == 'part':
                part_link = part_individuals[link_added]
                individual.has_part_root = part_link
            elif phen_link_category == 'phenomenon':
                phenomenon_link = phenomenon_individuals[link_added]
                individual.has_phenomenon_root = phenomenon_link
            elif phen_link_category == 'process':
                process_link = process_individuals[link_added]
                individual.has_process_root = process_link
            else:
                print(f'Relationship not added for category {phen_link_category} ...')
                print(phen_link_id_enc, category, link_added)

        # If attributes are present, add relationships.
        attrs = [urllib.parse.quote(a, safe='/', encoding=None, errors=None) for a in attrs]
        attrs_found = [a for a in attrs if attribute_individuals[a] in attribute_individuals.individuals()]
        dirs_found = [a for a in attrs if direction_individuals[a] in direction_individuals.individuals()]
        attrs_not_found = [a for a in attrs if a not in attrs_found and a not in dirs_found]
        with individuals_ontology:
            for a in attrs_not_found:
                link_id, _ = add_phen_link(a, category = 'attribute')
                individual.has_attribute.append(attribute_individuals[link_id])
            for a in attrs_found:
                individual.has_attribute.append(attribute_individuals[a])
            for d in dirs_found:
                individual.has_direction.append(direction_individuals[d])

    if printit:
        print(f'Successfully added {phen_link_id_enc} to {category}.')
    return (phen_link_id_enc, category)

print('Adding complex objects ...')
for index, row in object_info.iterrows():
    object_name = row['encoded_name']
    object_name_enc = urllib.parse.quote(object_name, safe='/', encoding=None, errors=None)
    object_label = row['label_name']
    #print('Working on', object_name)
    with phenomenon_individuals:
        # Create entity in phenomena if it doesn't already exist.
        if phenomenon_individuals[object_name_enc] not in phenomenon_individuals.individuals():
            phen_individual = Phenomenon(object_name_enc)
            phen_individual.label = object_label
            if 'variable' in object_name:
                print(phen_individual)
        else:
            phen_individual = phenomenon_individuals[object_name_enc]

        # Linked items are phenomena
        for category, relationship_list in phenomenon_relationships.items():
            current_individuals = class_mapping[category]['individuals']
            for relationship in relationship_list:
                if row[relationship] == '':
                    continue

                #print(row[relationship],relationship, category, current_individuals)
                printit = False
                #if 'variable' in row[relationship]:
                #    printit = True
                phen_link, cat_link = add_phen_link(row[relationship], category = category, printit = printit)
                
                if cat_link != category:
                    print('Error, categories don\'t match.')
                    continue
   
                element = current_individuals[phen_link]

                if relationship.startswith('has-primary-participant-phenomenon'):
                    phen_individual.has_primary_participant_phenomenon.append(element)
                elif relationship == 'has-adjacent-participant-phenomenon':
                    phen_individual.has_adjacent_participant_phenomenon.append(element)
                elif relationship == 'has-first-participant-phenomenon':
                    phen_individual.has_first_participant_phenomenon.append(element)
                elif relationship == 'has-second-participant-phenomenon':
                    phen_individual.has_second_participant_phenomenon.append(element)
                elif relationship == 'has-medium-participant-phenomenon':
                    phen_individual.has_medium_participant_phenomenon.append(element)
                elif relationship == 'has-sink-participant-phenomenon':
                    phen_individual.has_sink_participant_phenomenon.append(element)
                elif relationship == 'has-source-participant-phenomenon':
                    phen_individual.has_source_participant_phenomenon.append(element)
                elif relationship == 'has-in-participant-phenomenon':
                    phen_individual.has_in_participant_phenomenon.append(element)
                elif relationship == 'has-numerator-participant-phenomenon':
                    phen_individual.has_numerator_participant_phenomenon.append(element)
                elif relationship == 'has-denominator-participant-phenomenon':
                    phen_individual.has_denominator_participant_phenomenon.append(element)
                elif relationship == 'has-minuend-participant-phenomenon':
                    phen_individual.has_minuend_participant_phenomenon.append(element)
                elif relationship == 'has-subtrahend-participant-phenomenon':
                    phen_individual.has_subtrahend_participant_phenomenon.append(element)
                elif relationship == 'has-perspective-participant-phenomenon':
                    phen_individual.has_perspective_participant_phenomenon.append(element)
                elif relationship == 'has-source-phenomenon':
                    phen_individual.has_source_phenomenon.append(element)
                elif relationship == 'has-containing-phenomenon':
                    phen_individual.has_containing_phenomenon.append(element)
                elif relationship == 'has-containing-medium-phenomenon':
                    phen_individual.has_containing_medium_phenomenon.append(element)
                elif relationship == 'is-part-of-containing-phenomenon':
                    phen_individual.is_part_of_containing_phenomenon.append(element)
                elif relationship == 'has-location':
                    phen_individual.has_location.append(element)
                elif relationship == 'has-location-of-origin':
                    phen_individual.has_location_of_origin.append(element)
                elif relationship == 'is-observed-by':
                    phen_individual.has_observing_phenomenon.append(element)
                elif relationship == 'is-determined-at':
                    phen_individual.has_measurement_reference_at.append(element)
                elif relationship == 'determined-above':
                    phen_individual.has_measurement_reference_above.append(element)
                elif relationship == 'determined-since':
                    phen_individual.has_measurement_reference_since.append(element)
                elif relationship == 'determined-along':
                    phen_individual.has_measurement_reference_along.append(element)
                elif relationship == 'determined-from':
                    phen_individual.has_measurement_reference_from.append(element)
                elif relationship == 'determined-to':
                    phen_individual.has_measurement_reference_to.append(element)
                elif relationship == 'determined-below':
                    phen_individual.has_measurement_reference_below.append(element)
                elif relationship == 'determined-wrt':
                    phen_individual.has_measurement_reference_wrt.append(element)
                elif relationship.startswith('has-phenomenon'):
                    phen_individual.has_phenomenon.append(element)
                elif relationship == 'surrounds':
                    phen_individual.surrounds.append(element)
                elif relationship == 'orbits-around':
                    phen_individual.orbits.append(element)
                elif relationship == 'has-participating-primary-phenomenon':
                    phen_individual.has_participating_primary_phenomenon.append(element)
                elif relationship.startswith('undergoes-process'):
                    phen_individual.undergoes_process.append(element)
                elif relationship == 'has-part':
                    phen_individual.has_part.append(element)
                elif relationship == 'has-abstraction':
                    phen_individual.has_abstraction.append(element)
                elif relationship.startswith('is-modeled-by'):
                    phen_individual.is_modeled_by.append(element)
                elif relationship.startswith('has-matter'):
                    phen_individual.has_matter.append(element)
                elif relationship == 'contains-matter':
                    phen_individual.contains_matter.append(element)
                elif relationship == 'has-primary-matter':
                    phen_individual.contains_primary_matter.append(element)
                elif relationship.startswith('has-form'):
                    phen_individual.has_form.append(element)
                elif relationship.startswith('has-role'):
                    phen_individual.has_role.append(element)
                elif relationship == 'has-trajectory':
                    phen_individual.has_trajectory.append(element)
                elif relationship == 'has-domain':
                    phen_individual.has_domain.append(element)
                elif relationship == 'is-reference-for-determination-of-property':
                    phen_individual.is_reference_for_property.append(element)
                elif relationship == 'is-determined-at-property':
                    phen_individual.has_reference_for_property.append(element)
                elif relationship == 'is-reference-for-determination-of-variable':
                    phen_individual.is_reference_for_variable.append(element)
                elif relationship == 'is-determined-at-variable':
                    phen_individual.has_reference_for_variable.append(element)
                elif relationship == 'expressed-as':
                    phen_individual.is_expressed_as.append(element)
    #input("Press Enter to continue...")

f = open(variable_file)
reader = csv.reader(f)
next(reader)

# Step through variables in variable_name_tags and link contained atomistic components
# as well as overall described phenomenon and property.
object_annotations = pd.read_csv(annotated_object_file)
print('Adding variables ...')
with variable_individuals:
    for row in reader:
        original_name, variable_name, object_name, quantity_name, phenomena, \
            processes, matter, roles, forms, properties, operations, propertytypes, \
            propertyroles, propertyquantifications, trajectories, domains, attributes, \
            abstractions, models, directions, parts, reference, object_pattern, \
            quantity_pattern = row
        
        object_name = object_annotations.loc[\
                    object_annotations['new_varname']==variable_name,\
                    'annotated_object_name'].iloc[0]
        if not object_name.startswith('('):
            object_name = '(' + object_name + ')'
        variable_iri = object_name + '-has-property-(' + quantity_name + ')'
        variable_name_enc = urllib.parse.quote(variable_iri, safe='/', encoding=None, errors=None)
        if variable_individuals[variable_name_enc] not in list(variable_individuals.individuals()):
            #print(f'Adding variable {variable_name} ...')
            individual = Variable(variable_name_enc)
            individual.label = variable_name
            if original_name != variable_name:
                individual.has_original_label.append(original_name)
                #print(f'Added label {original_name} to {variable_name}.')

            object_label = object_annotations.loc[\
                    object_annotations['new_varname']==variable_name,\
                    'object_name'].iloc[0]
            if object_name.startswith('(') and object_name.endswith(')'):
                object_name = object_name[1:-1]
            printit = False
            #if '-variable-' in object_name:
            #    printit = True
            obj_added, _ = add_phen_link(object_name, printit=printit)
            individual.describes_phenomenon = phenomenon_individuals[obj_added]

            quantity_name_enc = urllib.parse.quote(quantity_name, safe='/', encoding=None, errors=None)
            if '_of_' in quantity_name:
                quantity = quantity_name.split('_of_')[-1]
                quantity_enc = urllib.parse.quote(quantity, safe='/', encoding=None, errors=None)
                operator_list = quantity_name.rsplit('_of_',1)[0].split('_of_')
                if property_individuals[quantity_enc] not in property_individuals.individuals() and \
                    '_and_' not in quantity:
                    print(f'Quantity not present: {quantity_enc}')
                else:
                    for op in reversed(operator_list):
                        op_enc = urllib.parse.quote(op, safe='/', encoding=None, errors=None)
                        if operation_individuals[op_enc] not in operation_individuals.individuals():
                            print(f'Operation missing: {op_enc}.')
                            break
                        else:
                            quantity_temp = op + '_of_' + quantity
                            quantity_temp_enc = urllib.parse.quote(quantity_temp, safe='/', encoding=None, errors=None)
                            with property_individuals:
                                quantity_individual = Property(quantity_temp_enc)
                                quantity_individual.label = quantity_temp
                                quantity_individual.is_transformed_by = [operation_individuals[op_enc]]
                                if '_and_' not in quantity or '_of_' in quantity:
                                    quantity_individual.is_transformation_of = [property_individuals[quantity_enc]]
                                else:
                                    quantities = quantity.split('_and_')
                                    quantities_enc = [urllib.parse.quote(q, safe='/', encoding=None, errors=None) for q in quantities]
                                    quantity_individual.is_transformation_of = [property_individuals[q] for q in quantities_enc]
                            quantity = quantity_temp
                            quantity_enc = quantity_temp_enc
                            #print('Adding property:', quantity_temp)

            if property_individuals[quantity_name_enc] in property_individuals.individuals():
                individual.describes_property = property_individuals[quantity_name_enc]
            else:
                print('Quantity not present:', quantity_name_enc)    

            if phenomena and (phenomena != object_name):
                phen_ind_add = []
                for phen in phenomena.split(', '):
                    if phen in plural_vocabulary:
                        phen = svo_terminology.loc[svo_terminology['plural']==phen,'entity_id'].iloc[0]
                    phen_enc = urllib.parse.quote(phen, safe='/', encoding=None, errors=None)
                    phen_ind_add.append(phenomenon_individuals[phen_enc])
                individual.contains_phenomenon_reference_to = phen_ind_add
            if processes:
                processes_enc = [urllib.parse.quote(p, safe='/', encoding=None, errors=None) for p in processes.split(', ')]
                process_ind_add = [process_individuals[proc] for proc in processes_enc]
                individual.contains_process_reference_to = process_ind_add
            if matter:
                matter_ind_add = []
                for mat in matter.split(', '):
                    if mat in plural_vocabulary:
                        mat = svo_terminology.loc[svo_terminology['plural']==mat,'entity_id'].iloc[0]
                    mat_enc = urllib.parse.quote(mat, safe='/', encoding=None, errors=None)
                    matter_ind_add.append(matter_individuals[mat_enc])
                individual.contains_matter_reference_to = matter_ind_add
            if forms:
                forms_ind_add = []
                for fm in forms.split(', '):
                    if fm in plural_vocabulary:
                        fm = svo_terminology.loc[svo_terminology['plural']==fm,'entity_id'].iloc[0]
                    fm_enc = urllib.parse.quote(fm, safe='/', encoding=None, errors=None)
                    forms_ind_add.append(form_individuals[fm_enc])
                individual.contains_form_reference_to = forms_ind_add
            if attributes:
                attributes_enc = [urllib.parse.quote(a, safe='/', encoding=None, errors=None) for a in attributes.split(', ')]
                attrs_ind_add = [attribute_individuals[attr] for attr in attributes_enc]
                individual.contains_attribute_reference_to = attrs_ind_add
            if abstractions:
                abs_ind_add = []
                for abs in abstractions.split(', '):
                    if abs in plural_vocabulary:
                        abs = svo_terminology.loc[svo_terminology['plural']==abs,'entity_id'].iloc[0]
                    abs_enc = urllib.parse.quote(abs, safe='/', encoding=None, errors=None)
                    abs_ind_add.append(abstraction_individuals[abs_enc])
                individual.contains_abstraction_reference_to = abs_ind_add
            if trajectories:
                traj_enc = [urllib.parse.quote(t, safe='/', encoding=None, errors=None) for t in trajectories.split(', ')]
                traj_ind_add = [trajectory_individuals[traj] for traj in traj_enc]
                individual.contains_trajectory_reference_to = traj_ind_add
            if parts:
                part_ind_add = []
                for prt in parts.split(', '):
                    if prt in plural_vocabulary:
                        prt = svo_terminology.loc[svo_terminology['plural']==prt,'entity_id'].iloc[0]
                    prt_enc = urllib.parse.quote(prt, safe='/', encoding=None, errors=None)
                    part_ind_add.append(part_individuals[prt_enc])
                individual.contains_part_reference_to = part_ind_add
            if roles:
                role_ind_add = []
                for rl in roles.split(', '):
                    if rl in plural_vocabulary:
                        rl = svo_terminology.loc[svo_terminology['plural']==rl,'entity_id'].iloc[0]
                    rl_enc = urllib.parse.quote(rl, safe='/', encoding=None, errors=None)
                    role_ind_add.append(role_individuals[rl_enc])
                individual.contains_role_reference_to = role_ind_add
            if operations:
                new_operations = operations.split(', ')
                if 'cos' in new_operations:
                    index = new_operations.index('cos')
                    new_operations[index] = 'cosine'
                op_enc = [urllib.parse.quote(o, safe='/', encoding=None, errors=None) for o in new_operations]
                op_ind_add = [operation_individuals[op] for op in op_enc]
                individual.contains_operation_reference_to = op_ind_add
            if properties and (properties != quantity_name):
                prop_enc = [urllib.parse.quote(p, safe='/', encoding=None, errors=None) for p in properties.split(', ')]
                property_ind_add = [property_individuals[prop] for prop in prop_enc]
                individual.contains_property_reference_to = property_ind_add
        elif (original_name != variable_name) and \
            original_name not in variable_individuals[variable_name_enc].has_original_label:
            variable_individuals[variable_name_enc].has_original_label.append(original_name)
            #print(f'Added label {original_name} to {variable_name}.')

abstraction_individuals.imported_ontologies.append(onto)
abstraction_individuals.imported_ontologies.append(attribute_individuals)
abstraction_individuals.imported_ontologies.append(direction_individuals)
attribute_individuals.imported_ontologies.append(onto)
direction_individuals.imported_ontologies.append(onto)
domain_individuals.imported_ontologies.append(onto)
form_individuals.imported_ontologies.append(onto)
form_individuals.imported_ontologies.append(attribute_individuals)
form_individuals.imported_ontologies.append(direction_individuals)
matter_individuals.imported_ontologies.append(onto)
matter_individuals.imported_ontologies.append(attribute_individuals)
part_individuals.imported_ontologies.append(onto)
part_individuals.imported_ontologies.append(attribute_individuals)
part_individuals.imported_ontologies.append(direction_individuals)
process_individuals.imported_ontologies.append(onto)
process_individuals.imported_ontologies.append(attribute_individuals)
role_individuals.imported_ontologies.append(onto)
role_individuals.imported_ontologies.append(attribute_individuals)
trajectory_individuals.imported_ontologies.append(onto)
operation_individuals.imported_ontologies.append(onto)
propertyrole_individuals.imported_ontologies.append(onto)
propertytype_individuals.imported_ontologies.append(onto)
propertyquantification_individuals.imported_ontologies.append(onto)
property_individuals.imported_ontologies.append(onto)
property_individuals.imported_ontologies.append(operation_individuals)
phenomenon_individuals.imported_ontologies.append(onto)
phenomenon_individuals.imported_ontologies.append(matter_individuals)
phenomenon_individuals.imported_ontologies.append(form_individuals)
phenomenon_individuals.imported_ontologies.append(role_individuals)
phenomenon_individuals.imported_ontologies.append(process_individuals)
phenomenon_individuals.imported_ontologies.append(attribute_individuals)
phenomenon_individuals.imported_ontologies.append(abstraction_individuals)
phenomenon_individuals.imported_ontologies.append(domain_individuals)
phenomenon_individuals.imported_ontologies.append(part_individuals)
phenomenon_individuals.imported_ontologies.append(trajectory_individuals)

# Write ontology relationships to owl/rdf and ttl
ontology_dir = 'ontology files'
svo_filename = 'svo.owl'
svo_filepath = os.path.join(ontology_dir, svo_filename)
onto.save(svo_filepath)
for category, items in class_mapping.items():
    category_dir = os.path.join(ontology_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    category_individuals = items['individuals']
    category_filename = f'{category}.owl'
    category_filepath = os.path.join(category_dir, category_filename)
    category_individuals.save(category_filepath)

    # convert to ttl
    g = Graph()
    g.parse(category_filepath)
    ttl_filepath = category_filepath.replace('.owl','.ttl')
    g.serialize(ttl_filepath)

    parsed_owl = parse_owl_file(category_filepath)

    for cat_individual in category_individuals.individuals():
        ind_extension = cat_individual.iri.split('/')[-1]
        ind_label = cat_individual.label[0]
        ind_dir = os.path.join(category_dir,ind_extension)
        os.makedirs(ind_dir, exist_ok=True)
        ind_filename = f'{ind_label}.owl'
        ind_filepath = os.path.join(ind_dir,ind_filename)
        ind_file_text = ''.join([
            parsed_owl['header'], parsed_owl['namespace'], parsed_owl[ind_extension], parsed_owl['end_tag']
        ])
        with open(ind_filepath, 'w') as f:
            f.write(ind_file_text)

        # convert to ttl
        g = Graph()
        g.parse(ind_filepath)
        ttl_filepath = ind_filepath.replace('.owl','.ttl')
        g.serialize(ttl_filepath)