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

# Set up top-level ontology classes and properties.
with onto:
    class Phenomenon(Thing): pass
    class Matter(Thing): pass
    class Process(Thing): pass
    class Property(Thing): pass
    class Operation(Thing): pass
    class Variable(Thing): pass
    class Abstraction(Thing): pass
    class Attribute(Thing): pass
    class Model(Thing): pass
    class Direction(Thing): pass
    class Form(Thing): pass
    class Role(Thing): pass
    class Trajectory(Thing): pass
    class Part(Thing): pass
    class PropertyRole(Thing): pass
    class PropertyType(Thing): pass
    class PropertyQuantification(Thing): pass
    class Domain(Thing): pass

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
    class is_expressed_as(ObjectProperty): pass
    class has_wikipedia_page(AnnotationProperty): pass
    class has_wikidata_page(AnnotationProperty): pass
    class has_synonym(AnnotationProperty): pass
    class has_original_label(AnnotationProperty): pass

### INFORMATION INDEXING ###
    
# For each class, map individuals ontoloogy and individual instantiation method.
class_mapping = {'phenomenon' : {'individuals' : phenomenon_individuals, 'class': onto.Phenomenon, 
                                 'rels'        : ['has-phenomenon', 'has-phenomenon2']},
                 'matter'     : {'individuals' : matter_individuals,     'class': onto.Matter, 
                                 'rels'        : ['has-matter', 'has-matter2', 'contains-matter','has-primary-matter'] },
                 'process'    : {'individuals' : process_individuals,    'class': onto.Process,
                                 'rels'        : ['undergoes-process', 'undergoes-process2', 'has-process', 'has-process2'] },
                 'property'   : {'individuals' : property_individuals,   'class': onto.Property, 
                                 'rels'        : ['referenced-with-property', 'reference-for-computing'] },
                 'operation'  : {'individuals' : operation_individuals,  'class': onto.Operation},
                 'abstraction': {'individuals' : abstraction_individuals,'class': onto.Abstraction, 
                                 'rels'        : ['has-abstraction'] },
                 'attribute'  : {'individuals' : attribute_individuals,  'class': onto.Attribute},
                 'model'      : {'individuals' : model_individuals,      'class': onto.Model},
                 'direction'  : {'individuals' : direction_individuals,  'class': onto.Direction},
                 'form'       : {'individuals' : form_individuals,       'class': onto.Form, 
                                 'rels'        : ['has-form', 'has-form2'] }, 
                 'role'       : {'individuals' : role_individuals,       'class': onto.Role,
                                 'rels'        : ['has-role', 'has-role2'] },
                 'trajectory' : {'individuals' : trajectory_individuals, 'class': onto.Trajectory, 
                                 'rels'        : ['has-trajectory'] },
                 'part'       : {'individuals' : part_individuals,       'class': onto.Part,
                                 'rels'        : ['has-part', 'has-part2'] },
                 'propertytype': {'individuals' : propertytype_individuals, 'class': onto.PropertyType},
                 'propertyrole': {'individuals' : propertyrole_individuals, 'class': onto.PropertyRole},
                 'propertyquantification': {'individuals' : propertyquantification_individuals, \
                                            'class': onto.PropertyQuantification},
                 'domain'     : {'individuals' : domain_individuals,     'class': onto.Domain, 
                                 'rels'        : ['has-domain'] } }

 #'is-modeled-by' ?

# Get a list of all relationships for complex objects.
object_info = pd.read_csv(object_file).fillna('')
rel_list = object_info.columns.to_list()
rel_list.remove('encoded_name')
rel_list.remove('label_name')

# Get the SVO terminology lookup table.
svo_terminology = pd.read_csv(terminology_file)
plural_vocabulary = svo_terminology['plural'].dropna().tolist()

### COMPONENT FUNCTIONS ###
    
def set_individual_annotation(individual, label, wikipedia_page, synonyms, definition, wikidata_page):
    # Set the annotation properties for an Individual with information provided in foundational
    # terminology file.
    individual.label = label
    if wikipedia_page:
        individual.has_wikipedia_page = wikipedia_page
    if wikidata_page:
        individual.has_wikidata_page = wikidata_http.format(wikidata_page)
    if synonyms:
        individual.has_synonym = synonyms.split(', ')
    if definition:
        individual.comment = definition

def add_phen_link(phen_link, individuals, object_info, category = 'phenomenon'):
    # Add phenomenon link to the ontology if it is missing
    # If not otherwise specified, as a phenomenon and add containing links.

    if (phen_link == ''):
        return None
    if individuals[phen_link] in individuals.individuals():
        return phen_link
    if phen_link.startswith('reference-'):
        phen_link = phen_link.replace('reference-','reference_')
    if phen_link in plural_vocabulary:
        phen_link = svo_terminology.loc[svo_terminology['plural']==phen_link,'entity_id'].iloc[0]
    if individuals[phen_link] not in individuals.individuals():
        # Trackers
        attrs = None # attributes following ~
        object_root = None # root not including attributes

        # Only parse for attributes if term not already present in complex objects.
        attr_on = True
        if phen_link in object_info['encoded_name'].tolist():
            attr_on = False
    
        root_category = category
        native_category = category
        if attr_on:
            if '~' in phen_link:
                object_root = phen_link.split('~')[0]
                if object_root in plural_vocabulary:
                    object_root = svo_terminology.loc[svo_terminology['plural']==object_root,'entity_id'].iloc[0]
                # Check if object_root is in a different class from desired add class
                root_category = svo_terminology.loc[svo_terminology['entity_id']==object_root,'entity_class'].iloc[0]
                if root_category != category:
                    root_individuals = class_mapping[root_category]['individuals']
                    add_phen_link(phen_link, root_individuals, object_info, category = root_category)
                    object_root = None
                else:
                    attrs = phen_link.split('~',1)[1]
                    attrs = re.split('~', attrs)
            else:
                try:
                    native_category = svo_terminology.loc[svo_terminology['entity_id']==phen_link,'entity_class'].iloc[0]
                    if native_category != category:
                        native_individuals = class_mapping[native_category]['individuals']
                        add_phen_link(phen_link, native_individuals, object_info, category = native_category)
                except:
                    pass
                    #print(f'Error, cannot add {phen_link} to native category.')

        base_category = category
        if root_category != category:
            base_category = root_category
        if native_category != category:
            base_category = native_category
        with individuals:
            #print(f'Adding {phen_link} to {category}...')
            if category == 'phenomenon':
                phen_individual = Phenomenon(phen_link)
                if object_root:
                    phen_individual.has_phenomenon_root = individuals[object_root]
                if (base_category != category):
                    if base_category == 'matter':
                        phen_individual.has_matter.append(matter_individuals[phen_link])
                    elif base_category == 'role':
                        phen_individual.has_role.append(role_individuals[phen_link])
                    elif base_category == 'abstraction':
                        phen_individual.has_abstraction.append(abstraction_individuals[phen_link])
                    elif base_category == 'process':
                        phen_individual.undergoes_process.append(process_individuals[phen_link])
                    elif base_category == 'part':
                        phen_individual.has_part.append(part_individuals[phen_link])
                    elif base_category == 'domain':
                        phen_individual.has_domain.append(domain_individuals[phen_link])
                    elif base_category == 'model':
                        phen_individual.has_abstraction.append(model_individuals[phen_link])
                    elif base_category == 'form':
                        phen_individual.has_form.append(form_individuals[phen_link])
                    elif base_category == 'attribute':
                        phen_individual.has_attribute.append(attribute_individuals[phen_link])
                    else:
                        pass
                        #print(phen_link, base_category)
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


            # Determine the label for the new entry.
            try:
                phen_label = object_info.loc[object_info['encoded_name']==phen_link,\
                                'label_name'].iloc[0]
            except:
                try:
                    phen_label = svo_terminology.loc[(svo_terminology['entity_id']==phen_link) & \
                                                     (svo_terminology['entity_class']==category),\
                                                        'entity_label'].iloc[0]
                except:
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
        return phen_link
    return phen_link

# Add atomic SVO vocabulary terms to ontology.
f = open(terminology_file)
reader = csv.reader(f)
next(reader)
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
        print(f'Entity class {entity_class} missing for label {entity_label}. Skipping ...')


# Read in the complex phenomena generated and atomized from the object_names of the variables and
# add them to the ontology.
print('Adding complex objects ...')
object_info = pd.read_csv(object_file).fillna('')

# First loop instantiaties all complex objects as individuals if not already present.
for index, row in object_info.iterrows():
    
    object_name = row['encoded_name']
    # Create entity in phenomena if it doesn't already exist.
    if phenomenon_individuals[object_name] not in phenomenon_individuals.individuals():
        object_label = row['label_name']
        with phenomenon_individuals:
            phen_individual = Phenomenon(object_name)
            phen_individual.label = object_label

# Second loop creates links to subobject terms.
for index, row in object_info.iterrows():
    object_name = row['encoded_name']
    if phenomenon_individuals[object_name] not in phenomenon_individuals.individuals():
        print(f'Error, term missing: {object_name}')
        continue
    phen_individual = phenomenon_individuals[object_name]

    for relationship in rel_list:
        if row[relationship] == '':
            continue

        category = 'phenomenon'
        current_individuals = phenomenon_individuals
        if relationship in class_mapping['process']['rels']:
            category = 'process'
            current_individuals = process_individuals
        elif relationship in class_mapping['part']['rels']:
            category = 'part'
            current_individuals = part_individuals
        elif relationship in class_mapping['abstraction']['rels']:
            category = 'abstraction'
            current_individuals = abstraction_individuals
        elif relationship in class_mapping['matter']['rels']:
            category = 'matter'
            current_individuals = matter_individuals
        elif relationship in class_mapping['form']['rels']:
            category = 'form'
            current_individuals = form_individuals
        elif relationship in class_mapping['role']['rels']:
            category = 'role'
            current_individuals = role_individuals
        elif relationship in class_mapping['trajectory']['rels']:
            category = 'trajectory'
            current_individuals = trajectory_individuals
        elif relationship in class_mapping['property']['rels']:
            category = 'property'
            current_individuals = property_individuals

        phen_link = ''
        rel_value = row[relationship]
        if rel_value != '':
            phen_link = add_phen_link(rel_value, current_individuals, object_info, category = category)

        if phen_link:
            element = current_individuals[phen_link]
            if relationship.startswith('has-primary-participant') or \
                (relationship == 'participates-in'):
                phen_individual.has_primary_participant_phenomenon.append(element)
            elif relationship == 'has-adjacent-participant-phenomenon':
                phen_individual.has_adjacent_participant_phenomenon.append(element)
            elif relationship == 'has-first-participant-phenomenon':
                phen_individual.has_first_participant_phenomenon.append(element)
            elif relationship == 'has-second-participant-phenomenon':
                phen_individual.has_second_participant_phenomenon.append(element)
            elif relationship.startswith('has-medium-participant-phenomenon'):
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
            elif relationship == 'has-sink-phenomenon':
                phen_individual.has_sink_phenomenon.append(element)
            elif relationship.startswith('has-containing-phenomenon'):
                phen_individual.has_containing_phenomenon.append(element)
            elif relationship == 'has-containing-medium-phenomenon':
                phen_individual.has_containing_medium_phenomenon.append(element)
            elif relationship == 'is-part-of-containing-phenomenon':
                phen_individual.is_part_of_containing_phenomenon.append(element)
            elif relationship == 'has-location':
                phen_individual.has_location.append(element)
            elif relationship == 'has-location-of-origin':
                phen_individual.has_location_of_origin.append(element)
            elif relationship == 'has-model-location':
                phen_individual.has_location_within_model.append(element)
            elif relationship == 'is-observed-by':
                phen_individual.has_observing_phenomenon.append(element)
            elif relationship == 'measured-at':
                phen_individual.has_measurement_reference_at.append(element)
            elif relationship == 'measured-above':
                phen_individual.has_measurement_reference_above.append(element)
            elif relationship == 'measured-since':
                phen_individual.has_measurement_reference_since.append(element)
            elif relationship == 'measured-along':
                phen_individual.has_measurement_reference_along.append(element)
            elif relationship == 'measured-from':
                phen_individual.has_measurement_reference_from.append(element)
            elif relationship == 'measured-to':
                phen_individual.has_measurement_reference_to.append(element)
            elif relationship == 'measured-below':
                phen_individual.has_measurement_reference_below.append(element)
            elif relationship == 'measured-wrt':
                phen_individual.has_measurement_reference_wrt.append(element)
            elif relationship in [ 'has-phenomenon',  'has-phenomenon2']:
                phen_individual.has_phenomenon.append(element)
            elif relationship == 'surrounds':
                phen_individual.surrounds.append(element)  
            elif relationship == 'drives':
                phen_individual.drives.append(element)
            elif relationship == 'orbits-around':
                phen_individual.orbits.append(element)
            elif relationship == 'has-participating-medium-phenomenon':
                phen_individual.has_participating_medium_phenomenon.append(element)
            elif relationship == 'has-participating-primary-phenomenon': 
                phen_individual.has_participating_primary_phenomenon.append(element)
            elif relationship.startswith('undergoes-process') or relationship.startswith('has-process'):
                phen_individual.undergoes_process.append(element)
            elif relationship in ['has-part', 'has-part2']:
                phen_individual.has_part.append(element)
            elif relationship == 'has-abstraction':
                phen_individual.has_abstraction.append(element)
            elif relationship == 'is-modeled-by':
                phen_individual.is_modeled_by.append(element)
            elif relationship in ['has-matter', 'has-matter2']:
                phen_individual.has_matter.append(element)
            elif relationship == 'contains-matter':
                phen_individual.contains_matter.append(element)
            elif relationship == 'has-primary-matter':
                phen_individual.contains_primary_matter.append(element)
            elif relationship in ['has-form', 'has-form2']:
                phen_individual.has_form.append(element)
            elif relationship in ['has-role', 'has-role2']:
                phen_individual.has_role.append(element)
            elif relationship == 'has-trajectory':
                phen_individual.has_trajectory.append(element)
            elif relationship == 'has-domain':
                phen_individual.has_domain.append(element)
            elif relationship == 'reference-for-computing':
                phen_individual.is_reference_for_property.append(element)
            elif relationship == 'referenced-with-property':
                phen_individual.has_reference_for_property.append(element)
            elif relationship == 'is-expressed-as':
                phen_individual.is_expressed_as.append(element)
            else:
                print(f'Unknown relationship: {relationship}')
        else:
            print(f'Error adding {phen_link}.')


# Step through variables in variable_name_tags and link contained atomistic components
# as well as overall described phenomenon and property.
f = open(variable_file)
reader = csv.reader(f)
next(reader)
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
                
                with phenomenon_individuals:
                    #print(f'General phenomenon missing: {object_name}')
                    add_phen_link(object_name, phenomenon_individuals, object_info)
                    if '-or-' in object_name:
                        object_subnames = object_name.split('-or-')
                        phen_individual = phenomenon_individuals[object_name]
                        for subobject in object_subnames:
                            if matter_individuals[subobject] in matter_individuals.individuals():
                                phen_individual.has_matter.append(matter_individuals[subobject])
                            elif role_individuals[subobject] in role_individuals.individuals():
                                phen_individual.has_role.append(role_individuals[subobject])
                            else:
                                print(f'{subobject} not found')

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

# Write ontology relationships to owl/rdf. 
ontology_dst_path = os.path.join(script_path, '../../ontology files/')      
onto.save(os.path.join(ontology_dst_path, 'svo.owl'))
phenomenon_individuals.save(os.path.join(ontology_dst_path, 'phenomenon.owl'))
matter_individuals.save(os.path.join(ontology_dst_path, 'matter.owl'))
abstraction_individuals.save(os.path.join(ontology_dst_path, 'abstraction.owl'))
process_individuals.save(os.path.join(ontology_dst_path, 'process.owl'))
property_individuals.save(os.path.join(ontology_dst_path, 'property.owl'))
operation_individuals.save(os.path.join(ontology_dst_path, 'operation.owl'))
variable_individuals.save(os.path.join(ontology_dst_path, 'variable.owl'))
attribute_individuals.save(os.path.join(ontology_dst_path, 'attribute.owl'))
model_individuals.save(os.path.join(ontology_dst_path, 'model.owl'))
direction_individuals.save(os.path.join(ontology_dst_path, 'direction.owl'))
form_individuals.save(os.path.join(ontology_dst_path, 'form.owl'))
role_individuals.save(os.path.join(ontology_dst_path, 'role.owl'))
trajectory_individuals.save(os.path.join(ontology_dst_path, 'trajectory.owl'))
part_individuals.save(os.path.join(ontology_dst_path, 'part.owl'))
propertyrole_individuals.save(os.path.join(ontology_dst_path, 'propertyrole.owl'))
propertytype_individuals.save(os.path.join(ontology_dst_path, 'propertytype.owl'))
propertyquantification_individuals.save(os.path.join(ontology_dst_path, 'propertyquantification.owl'))
domain_individuals.save(os.path.join(ontology_dst_path, 'domain.owl'))
