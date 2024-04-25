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
model_individuals      = get_ontology("http://scientificvariablesontology.org/svo/model/")
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
    class Model(Thing):
        comment = class_definitions['Model']
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

    class describes_phenomenon(Variable >> Phenomenon, FunctionalProperty): pass
    class describes_property(Variable >> Property, FunctionalProperty): pass
    class has_domain(ObjectProperty): pass
    class has_phenomenon(ObjectProperty): pass
    class has_matter(Phenomenon >> Matter): pass
    class contains_matter(Phenomenon >> Matter): pass
    class contains_primary_matter(Phenomenon >> Matter): pass
    class has_medium_matter(Phenomenon >> Matter): pass
    class has_process(Phenomenon >> Process): pass
    class undergoes_process(Phenomenon >> Process): pass
    class has_form(Phenomenon >> Form): pass
    class has_abstraction(Phenomenon >> Abstraction): pass
    class is_modeled_by(ObjectProperty): pass
    class has_part(Phenomenon >> Part): pass
    class has_attribute(Phenomenon >> Attribute): pass
    class has_trajectory(Phenomenon >> Trajectory): pass
    class has_role(Phenomenon >> Role): pass
    class has_source_phenomenon(ObjectProperty): pass
    class has_sink_phenomenon(ObjectProperty): pass
    class has_location(ObjectProperty): pass
    class has_location_within_model(ObjectProperty): pass
    class has_location_of_origin(ObjectProperty): pass
    class has_minuend_participant_phenomenon(ObjectProperty): pass
    class has_subtrahend_participant_phenomenon(ObjectProperty): pass
    class has_primary_participant_phenomenon(ObjectProperty): pass
    class has_adjacent_participant_phenomenon(ObjectProperty): pass
    class has_first_participant_phenomenon(ObjectProperty): pass
    class has_second_participant_phenomenon(ObjectProperty): pass
    class has_in_participant_phenomenon(ObjectProperty): pass
    class has_medium_participant_phenomenon(ObjectProperty): pass
    class has_source_participant_phenomenon(ObjectProperty): pass
    class has_sink_participant_phenomenon(ObjectProperty): pass
    class has_numerator_participant_phenomenon(ObjectProperty): pass
    class has_denominator_participant_phenomenon(ObjectProperty): pass
    class has_participating_primary_phenomenon(ObjectProperty): pass
    class has_participating_medium_phenomenon(ObjectProperty): pass
    class has_observing_phenomenon(ObjectProperty): pass
    class has_modeled_phenomenon(ObjectProperty): pass
    class has_modeling_phenomenon(ObjectProperty): pass
    class has_containing_phenomenon(ObjectProperty): pass
    class has_containing_medium_phenomenon(ObjectProperty): pass
    class is_part_of_containing_phenomenon(ObjectProperty): pass
    class has_perspective_participant_phenomenon(ObjectProperty): pass
    class surrounds(ObjectProperty): pass
    class drives(ObjectProperty): pass
    class has_measurement_reference_at(ObjectProperty): pass
    class has_measurement_reference_above(ObjectProperty): pass
    class has_measurement_reference_since(ObjectProperty): pass
    class has_measurement_reference_along(ObjectProperty): pass
    class has_measurement_reference_from(ObjectProperty): pass
    class has_measurement_reference_to(ObjectProperty): pass
    class has_measurement_reference_below(ObjectProperty): pass
    class has_measurement_reference_wrt(ObjectProperty): pass
    class is_reference_for_property(ObjectProperty): pass
    class has_reference_for_property(ObjectProperty): pass
    class orbits(ObjectProperty): pass
    class contains_phenomenon_reference_to(Variable >> Phenomenon): pass
    class contains_process_reference_to(Variable >> Process): pass
    class contains_matter_reference_to(Variable >> Matter): pass
    class contains_property_reference_to(Variable >> Property): pass
    class contains_form_reference_to(Variable >> Form): pass
    class contains_abstraction_reference_to(Variable >> Abstraction): pass
    class contains_model_reference_to(Variable >> Model): pass
    class contains_operation_reference_to(Variable >> Operation): pass
    class contains_role_reference_to(Variable >> Role): pass
    class contains_part_reference_to(Variable >> Part): pass
    class contains_trajectory_reference_to(Variable >> Trajectory): pass
    class contains_attribute_reference_to(Variable >> Attribute): pass
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

f = open(terminology_file)
reader = csv.reader(f)
next(reader)

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
                 'attribute'  : {'individuals' : attribute_individuals,  'class': onto.Attribute},
                 'model'      : {'individuals' : model_individuals,      'class': onto.Model},
                 'direction'  : {'individuals' : direction_individuals,  'class': onto.Direction},
                 'form'       : {'individuals' : form_individuals,       'class': onto.Form}, 
                 'role'       : {'individuals' : role_individuals,       'class': onto.Role},
                 'trajectory' : {'individuals' : trajectory_individuals, 'class': onto.Trajectory},
                 'part'       : {'individuals' : part_individuals,       'class': onto.Part},
                 'propertytype': {'individuals' : propertytype_individuals, 'class': onto.PropertyType},
                 'propertyrole': {'individuals' : propertyrole_individuals, 'class': onto.PropertyRole},
                 'propertyquantification': {'individuals' : propertyquantification_individuals, \
                                            'class': onto.PropertyQuantification},
                 'domain'     : {'individuals' : domain_individuals,     'class': onto.Domain} }
# Add atomic SVO vocabulary terms to ontology.
for row in reader:
    try:
        entity_id, entity_label, entity_class, entity_synonym, _, \
            entity_wikipedia_page, entity_definition, entity_definition_source, entity_wikidata = row
    except:
        print('Problem reading line after: ', entity_id)
        continue
    if entity_class in class_mapping.keys():
        individual_mapping = class_mapping[entity_class]
        individuals_ontology = individual_mapping['individuals']
        ontoclass = individual_mapping['class']

        with individuals_ontology:
            individual = ontoclass(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, \
                                        entity_synonym, entity_definition, entity_wikidata)

    else:
        print(entity_class, entity_label)

# Add phenomenon link to the ontology if it is missing
svo_terminology = pd.read_csv(terminology_file)
plural_vocabulary = svo_terminology['plural'].dropna().tolist()
def add_phen_link(phen_link, individuals, object_info, category = 'phenomenon'):
    if (phen_link != '') and individuals[phen_link] not in individuals.individuals():
        #print(f'Adding {phen_link} to {individuals}.')
        attrs = None
        object_root = None
        attr_on = True
        multiphen = None
        if phen_link in object_info['encoded_name'].tolist():
            attr_on = False
        twophen = False
        if attr_on:
            if '-and-' in phen_link and (phen_link.count('~') > 1):
                twophen = True
            elif '-and-soil' in phen_link or 'pool-and-pool' in phen_link:
                twophen = True
            elif '-or-' in phen_link or '-vs-' in phen_link:
                twophen = True
        if '~' in phen_link and attr_on and not twophen:
            attrs = phen_link.split('~',1)[1]
            attrs = re.split('~|-and-', attrs)
            object_root = phen_link.split('~')[0]
        if twophen:
            multiphen = re.split('-and-|-or-|-vs-',phen_link)
            multiphen = [p.strip('()') for p in multiphen]
            for p in multiphen:
                add_phen_link(p, individuals, object_info)
            phen_link = multiphen
        else:
            with individuals:
                if category == 'phenomenon':
                    phen_individual = Phenomenon(phen_link)
                    if object_root:
                        phen_individual.has_phenomenon_root = individuals[object_root]
                elif category == 'abstraction':
                    phen_individual = Abstraction(phen_link)
                    if object_root:
                        phen_individual.has_abstraction_root = individuals[object_root]
                elif category == 'matter':
                    phen_individual = Matter(phen_link)
                    if object_root:
                        phen_individual.has_matter_root = individuals[object_root]
                elif category == 'form':
                    phen_individual = Form(phen_link)
                    if object_root:
                        phen_individual.has_form_root = individuals[object_root]
                elif category == 'property':
                    phen_individual = Property(phen_link)
                elif category == 'part':
                    phen_individual = Part(phen_link)
                    if object_root:
                        phen_individual.has_part_root = individuals[object_root]
                elif category == 'process':
                    phen_individual = Process(phen_link)
                    if object_root:
                        phen_individual.has_process_root = individuals[object_root]
                elif category == 'role':
                    phen_individual = Role(phen_link)
                    if object_root:
                        phen_individual.has_role_root = individuals[object_root]
                elif category == 'domain':
                    phen_individual = Domain(phen_link)
                try:
                    phen_label = object_info.loc[\
                    object_info['encoded_name']==phen_link,\
                                'label_name'].iloc[0]
                except:
                    try:
                        phen_label = svo_terminology.loc[\
                            (svo_terminology['entity_id']==phen_link) & (svo_terminology['entity_class']==category),\
                                'entity_label'].iloc[0]
                    except:
                        #print('Not found:', phen_link, category)
                        phen_label = phen_link
                phen_individual.label = phen_label
                if attrs:
                    not_found = [a for a in attrs if attribute_individuals[a] not in attribute_individuals.individuals()]
                    not_found = [a for a in not_found if direction_individuals[a] not in direction_individuals.individuals()]
                    if not_found:
                        #print(f'Attribute(s) not found: {not_found}, {phen_label}')
                        for a in not_found:
                            with attribute_individuals:
                                attr_individual = Attribute(a)
                                attr_individual.label = a
                    attr_list = [attribute_individuals[a] for a in attrs if attribute_individuals[a] in attribute_individuals.individuals()]
                    if attr_list != []:
                        phen_individual.has_attribute = attr_list
                    attr_list = [direction_individuals[a] for a in attrs if direction_individuals[a] in direction_individuals.individuals()]
                    if attr_list != []:
                        phen_individual.has_direction = attr_list
        if not isinstance(phen_link, list):
            phen_link = [phen_link]
        return phen_link
    return None

# Read in the complex phenomena generated and atomized from the object_names of the variables and
# add them to the ontology.
rel_list = ['has-primary-participant-phenomenon', 
            'has-primary-participant-phenomenon2',
            'participates-in',
            'has-adjacent-participant-phenomenon', 
            'has-first-participant-phenomenon',
            'has-second-participant-phenomenon', 
            'has-medium-participant-phenomenon',
            'has-sink-participant-phenomenon', 
            'has-source-participant-phenomenon',
            'has-in-participant-phenomenon', 
            'has-numerator-participant-phenomenon',
            'has-denominator-participant-phenomenon', 
            'has-minuend-participant-phenomenon',
            'has-subtrahend-participant-phenomenon', 
            'has-perspective-participant-phenomenon',
            'has-source-phenomenon', 'has-sink-phenomenon',
            'has-containing-phenomenon', 'has-containing-medium-phenomenon',
            'is-part-of-containing-phenomenon', 'has-location',
            'has-location-of-origin', 'has-model-location',
            'is-observed-by', 'measured-at', 'measured-above', 'measured-since',
            'measured-along', 'measured-from', 'measured-to', 'measured-below',
            'measured-wrt', 'has-phenomenon', 'surrounds', 'drives', 'orbits-around',
            'has-participating-medium-phenomenon', 'has-participating-primary-phenomenon',
            'undergoes-process', 'undergoes-process2', 'has-part', 'has-part2',
            'has-abstraction','is-modeled-by','has-matter', 'contains-matter',
            'has-primary-matter', 'has-form', 'has-role',
            'has-trajectory', 'has-domain', 'referenced-with-property', 'reference-for-computing']
object_info = pd.read_csv(object_file).fillna('')
print('Adding complex objects ...')
for index, row in object_info.iterrows():
    object_name = row['encoded_name']
    object_label = row['label_name']
    with phenomenon_individuals:
        # Create entity in phenomena if it doesn't already exist.
        if phenomenon_individuals[object_name] not in phenomenon_individuals.individuals():
            phen_individual = Phenomenon(object_name)
            phen_individual.label = object_label
        else:
            phen_individual = phenomenon_individuals[object_name]
            #print(f'{object_name} already exists.')

        # Linked items are phenomena
        for idx, relationship in enumerate(rel_list):
            category = 'phenomenon'
            current_individuals = phenomenon_individuals
            if idx in [38, 39]:
                category = 'process'
                current_individuals = process_individuals
            elif idx in [40, 41]:
                category = 'part'
                current_individuals = part_individuals
            elif idx == 42: # is 43 - is-modeled-by also an abstraction?
                category = 'abstraction'
                current_individuals = abstraction_individuals
            elif idx in [44, 45, 46]:
                category = 'matter'
                current_individuals = matter_individuals
            elif idx == 47:
                category = 'form'
                current_individuals = form_individuals
            elif idx == 48:
                category = 'role'
                current_individuals = role_individuals
            elif idx == 49:
                category = 'trajectory'
                current_individuals = trajectory_individuals
            elif idx in [51,52]:
                category = 'property'
                current_individuals = property_individuals

            phen_link = add_phen_link(row[relationship], current_individuals, object_info, category = category)

            if phen_link:
                
                for pl in phen_link:
                    element = current_individuals[pl]

                    if idx in [0,1,2]:
                        phen_individual.has_primary_participant_phenomenon.append(element)
                    elif idx == 3:
                        phen_individual.has_adjacent_participant_phenomenon.append(element)
                    elif idx == 4:
                        phen_individual.has_first_participant_phenomenon.append(element)
                    elif idx == 5:
                        phen_individual.has_second_participant_phenomenon.append(element)
                    elif idx == 6:
                        phen_individual.has_medium_participant_phenomenon.append(element)
                    elif idx == 7:
                        phen_individual.has_sink_participant_phenomenon.append(element)
                    elif idx == 8:
                        phen_individual.has_source_participant_phenomenon.append(element)
                    elif idx == 9:
                        phen_individual.has_in_participant_phenomenon.append(element)
                    elif idx == 10:
                        phen_individual.has_numerator_participant_phenomenon.append(element)
                    elif idx == 11:
                        phen_individual.has_denominator_participant_phenomenon.append(element)
                    elif idx == 12:
                        phen_individual.has_minuend_participant_phenomenon.append(element)
                    elif idx == 13:
                        phen_individual.has_subtrahend_participant_phenomenon.append(element)
                    elif idx == 14:
                        phen_individual.has_perspective_participant_phenomenon.append(element)
                    elif idx == 15:
                        phen_individual.has_source_phenomenon.append(element)
                    elif idx == 16:
                        phen_individual.has_sink_phenomenon.append(element)
                    elif idx == 17:
                        phen_individual.has_containing_phenomenon.append(element)
                    elif idx == 18:
                        phen_individual.has_containing_medium_phenomenon.append(element)
                    elif idx == 19:
                        phen_individual.is_part_of_containing_phenomenon.append(element)
                    elif idx == 20:
                        phen_individual.has_location.append(element)
                    elif idx == 21:
                        phen_individual.has_location_of_origin.append(element)
                    elif idx == 22:
                        phen_individual.has_location_within_model.append(element)
                    elif idx == 23:
                        phen_individual.has_observing_phenomenon.append(element)
                    elif idx == 24:
                        phen_individual.has_measurement_reference_at.append(element)
                    elif idx == 25:
                        phen_individual.has_measurement_reference_above.append(element)
                    elif idx == 26:
                        phen_individual.has_measurement_reference_since.append(element)
                    elif idx == 27:
                        phen_individual.has_measurement_reference_along.append(element)
                    elif idx == 28:
                        phen_individual.has_measurement_reference_from.append(element)
                    elif idx == 29:
                        phen_individual.has_measurement_reference_to.append(element)
                    elif idx == 30:
                        phen_individual.has_measurement_reference_below.append(element)
                    elif idx == 31:
                        phen_individual.has_measurement_reference_wrt.append(element)
                    elif idx == 32:
                        phen_individual.has_phenomenon.append(element)
                    elif idx == 33:
                        phen_individual.surrounds.append(element) 
                    elif idx == 34:
                        phen_individual.drives.append(element)
                    elif idx == 35:
                        phen_individual.orbits.append(element)
                    elif idx == 36:
                        phen_individual.has_participating_medium_phenomenon.append(element)
                    elif idx == 37:
                        phen_individual.has_participating_primary_phenomenon.append(element)
                    elif idx in [38,39]:
                        phen_individual.undergoes_process.append(element)
                    elif idx in [40,41]:
                        phen_individual.has_part.append(element)
                    elif idx == 42:
                        phen_individual.has_abstraction.append(element)
                    elif idx == 43:
                        phen_individual.is_modeled_by.append(element)
                    elif idx == 44:
                        phen_individual.has_matter.append(element)
                    elif idx == 45:
                        phen_individual.contains_matter.append(element)
                    elif idx == 46:
                        phen_individual.contains_primary_matter.append(element)
                    elif idx == 47:
                        phen_individual.has_form.append(element)
                    elif idx == 48:
                        phen_individual.has_role.append(element)
                    elif idx == 49:
                        phen_individual.has_trajectory.append(element)
                    elif idx == 50:
                        phen_individual.has_domain.append(element)
                    elif idx == 51:
                        phen_individual.is_reference_for_property.append(element)
                    elif idx == 52:
                        phen_individual.has_reference_for_property.append(element)


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
        
        if variable_individuals[variable_name] not in list(variable_individuals.individuals()):
            individual = Variable(variable_name)
            individual.label = variable_name
            individual.has_original_label = original_name

            object_label = object_name
            object_name = object_annotations.loc[\
                    object_annotations['new_varname']==variable_name,\
                    'annotated_object_name'].iloc[0]
            object_label = object_annotations.loc[\
                    object_annotations['new_varname']==variable_name,\
                    'object_name'].iloc[0]
            if object_name.startswith('(') and object_name.endswith(')'):
                object_name = object_name[1:-1]
            if phenomenon_individuals[object_name] not in phenomenon_individuals.individuals():
                #print(f'Phenomenon missing: {object_name}')
                with phenomenon_individuals:
                    object_root = object_name.split('~')[0]
                    phen_individual = Phenomenon(object_name)
                    phen_individual.label = object_label
                    items_to_add = []
                    if matter_individuals[object_root] in matter_individuals.individuals():        
                        if matter_individuals[object_name] not in matter_individuals.individuals():
                            pl = add_phen_link(object_name, matter_individuals, object_info, category = 'matter')
                            if pl:
                                items_to_add = [matter_individuals[p] for p in pl]
                        else:
                            items_to_add = [matter_individuals[object_name]]
                        phen_individual.has_matter.extend(items_to_add)
                    elif process_individuals[object_root] in process_individuals.individuals():
                        if process_individuals[object_name] not in process_individuals.individuals():
                            pl = add_phen_link(object_name, process_individuals, object_info, category = 'process')
                            if pl:
                                items_to_add = [process_individuals[p] for p in pl]
                        else:
                            items_to_add = [process_individuals[object_name]]
                        phen_individual.has_process.extend(items_to_add)
                    elif abstraction_individuals[object_root] in abstraction_individuals.individuals():
                        if abstraction_individuals[object_name] not in abstraction_individuals.individuals():
                            pl = add_phen_link(object_name, abstraction_individuals, object_info, category = 'abstraction')
                            if pl:
                                items_to_add = [abstraction_individuals[p] for p in pl]
                        else:
                            items_to_add = [abstraction_individuals[object_name]]
                        phen_individual.has_abstraction.extend(items_to_add)
                    elif role_individuals[object_root] in role_individuals.individuals():
                        if role_individuals[object_name] not in role_individuals.individuals():
                            pl = add_phen_link(object_name, role_individuals, object_info, category = 'role')
                            if pl:
                                items_to_add = [role_individuals[p] for p in pl]
                        else:
                            items_to_add = [role_individuals[object_name]]
                        phen_individual.has_role.extend(items_to_add)
                    elif phenomenon_individuals[object_root] in phenomenon_individuals.individuals():
                        if phenomenon_individuals[object_name] not in phenomenon_individuals.individuals():
                            pl = add_phen_link(object_name, phenomenon_individuals, object_info, category = 'phenomenon')
                            if pl:
                                items_to_add = [phenomenon_individuals[p] for p in pl]
                        else:
                            items_to_add = [phenomenon_individuals[object_name]]
                        phen_individual.has_phenomenon.extend(items_to_add)
                    elif domain_individuals[object_name] in domain_individuals.individuals():
                        phen_individual.has_domain = [domain_individuals[object_name]]

            individual.describes_phenomenon = phenomenon_individuals[object_name]

            if '_of_' in quantity_name:
                quantity = quantity_name.split('_of_')[-1]
                operator_list = quantity_name.rsplit('_of_',1)[0].split('_of_')
                if property_individuals[quantity] not in property_individuals.individuals() and \
                    '_and_' not in quantity:
                    print(f'Quantity not present: {quantity}')
                else:
                    for op in reversed(operator_list):
                        if operation_individuals[op] not in operation_individuals.individuals():
                            print(f'Operation missing: {op}.')
                            break
                        else:
                            quantity_temp = op + '_of_' + quantity
                            with property_individuals:
                                quantity_individual = Property(quantity_temp)
                                quantity_individual.label = quantity_temp
                                quantity_individual.is_transformed_by = [operation_individuals[op]]
                                if '_and_' not in quantity or '_of_' in quantity:
                                    quantity_individual.is_transformation_of = [property_individuals[quantity]]
                                else:
                                    quantities = quantity.split('_and_')
                                    quantity_individual.is_transformation_of = [property_individuals[q] for q in quantities]
                            quantity = quantity_temp
                            #print('Adding property:', quantity_temp)

            if property_individuals[quantity_name] in property_individuals.individuals():
                individual.describes_property = property_individuals[quantity_name]
            else:
                print('Quantity not present:', quantity_name)    

            if phenomena:
                if phenomena != object_name:
                    phen_ind_add = []
                    for phen in phenomena.split(', '):
                        if phen in plural_vocabulary:
                            phen = svo_terminology.loc[svo_terminology['plural']==phen,'entity_id'].iloc[0]
                        phen_ind_add.append(phenomenon_individuals[phen])
                    individual.contains_phenomenon_reference_to = phen_ind_add
            if processes:
                process_ind_add = [process_individuals[proc] for proc in processes.split(', ')]
                individual.contains_process_reference_to = process_ind_add
            if matter:
                matter_ind_add = []
                for mat in matter.split(', '):
                    if mat in plural_vocabulary:
                        mat = svo_terminology.loc[svo_terminology['plural']==mat,'entity_id'].iloc[0]
                    matter_ind_add.append(matter_individuals[mat])
                individual.contains_matter_reference_to = matter_ind_add
            if forms:
                forms_ind_add = []
                for fm in forms.split(', '):
                    if fm in plural_vocabulary:
                        fm = svo_terminology.loc[svo_terminology['plural']==fm,'entity_id'].iloc[0]
                    forms_ind_add.append(form_individuals[fm])
                individual.contains_form_reference_to = forms_ind_add
            if attributes:
                attrs_ind_add = [attribute_individuals[attr] for attr in attributes.split(', ')]
                individual.contains_attribute_reference_to = attrs_ind_add
            if abstractions:
                abs_ind_add = []
                for abs in abstractions.split(', '):
                    if abs in plural_vocabulary:
                        abs = svo_terminology.loc[svo_terminology['plural']==abs,'entity_id'].iloc[0]
                    abs_ind_add.append(abstraction_individuals[abs])
                individual.contains_abstraction_reference_to = abs_ind_add
            if models:
                model_ind_add = [model_individuals[mod] for mod in models.split(', ')]
                individual.contains_model_reference_to = model_ind_add
            if trajectories:
                traj_ind_add = [trajectory_individuals[traj] for traj in trajectories.split(', ')]
                individual.contains_trajectory_reference_to = traj_ind_add
            if parts:
                part_ind_add = []
                for prt in parts.split(', '):
                    if prt in plural_vocabulary:
                        prt = svo_terminology.loc[svo_terminology['plural']==prt,'entity_id'].iloc[0]
                    part_ind_add.append(part_individuals[prt])
                individual.contains_part_reference_to = part_ind_add
            if roles:
                role_ind_add = []
                for rl in roles.split(', '):
                    if rl in plural_vocabulary:
                        rl = svo_terminology.loc[svo_terminology['plural']==rl,'entity_id'].iloc[0]
                    role_ind_add.append(role_individuals[rl])
                individual.contains_role_reference_to = role_ind_add
            if operations:
                op_ind_add = [operation_individuals[op.replace('cos','cosine')] for op in operations.split(', ')]
                individual.contains_operation_reference_to = op_ind_add
            if properties:
                if properties != quantity_name:
                    property_ind_add = [property_individuals[prop] for prop in properties.split(', ')]
                    individual.contains_property_reference_to = property_ind_add
        else:
            #print('Duplicate variable:', variable_name)
            variable_individuals[variable_name].has_original_label.append(original_name)

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
model_individuals.imported_ontologies.append(onto)
process_individuals.imported_ontologies.append(onto)
process_individuals.imported_ontologies.append(attribute_individuals)

# Write ontology relationships to owl/rdf.        
onto.save('ontology files/svo.owl')
phenomenon_individuals.save('ontology files/phenomenon.owl')
matter_individuals.save('ontology files/matter.owl')
abstraction_individuals.save('ontology files/abstraction.owl')
process_individuals.save('ontology files/process.owl')
property_individuals.save('ontology files/property.owl')
operation_individuals.save('ontology files/operation.owl')
variable_individuals.save('ontology files/variable.owl')
attribute_individuals.save('ontology files/attribute.owl')
model_individuals.save('ontology files/model.owl')
direction_individuals.save('ontology files/direction.owl')
form_individuals.save('ontology files/form.owl')
role_individuals.save('ontology files/role.owl')
trajectory_individuals.save('ontology files/trajectory.owl')
part_individuals.save('ontology files/part.owl')
propertyrole_individuals.save('ontology files/propertyrole.owl')
propertytype_individuals.save('ontology files/propertytype.owl')
propertyquantification_individuals.save('ontology files/propertyquantification.owl')
domain_individuals.save('ontology files/domain.owl')
