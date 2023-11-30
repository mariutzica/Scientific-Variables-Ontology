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
script_path = os.path.dirname(__file__)
raw_path = os.path.join(script_path,'../../source/raw/')
atomic_terms_filename = 'svo_atomic_vocabulary.csv'
terminology_file = os.path.join(raw_path,atomic_terms_filename)
src_path = os.path.join(script_path,'../../source/')
variable_filename = 'variable_name_tags.csv'
variable_file = os.path.join(src_path,variable_filename)
annotated_object_filename = 'csdms_annotated_names.csv'
annotated_object_file = os.path.join(src_path, annotated_object_filename)
object_filename = 'csdms_atomized.csv'
object_file = os.path.join(src_path, object_filename)

wikidata_http = 'https://www.wikidata.org/wiki/{}'

# Set up component ontologies.
onto = get_ontology("http://scientificvariablesontology.org/svo#")
phenomenon_individuals = get_ontology("http://scientificvariablesontology.org/svo/phenomenon/")
matter_individuals = get_ontology("http://scientificvariablesontology.org/svo/matter/")
process_individuals = get_ontology("http://scientificvariablesontology.org/svo/process/")
property_individuals = get_ontology("http://scientificvariablesontology.org/svo/property/")
operation_individuals = get_ontology("http://scientificvariablesontology.org/svo/operation/")
variable_individuals = get_ontology("http://scientificvariablesontology.org/svo/variable/")
abstraction_individuals = get_ontology("http://scientificvariablesontology.org/svo/abstraction/")
attribute_individuals = get_ontology("http://scientificvariablesontology.org/svo/attribute/")
model_individuals = get_ontology("http://scientificvariablesontology.org/svo/model/")
direction_individuals = get_ontology("http://scientificvariablesontology.org/svo/direction/")
form_individuals = get_ontology("http://scientificvariablesontology.org/svo/form/")
role_individuals = get_ontology("http://scientificvariablesontology.org/svo/role/")
trajectory_individuals = get_ontology("http://scientificvariablesontology.org/svo/trajectory/")
part_individuals = get_ontology("http://scientificvariablesontology.org/svo/part/")
propertyrole_individuals = get_ontology("http://scientificvariablesontology.org/svo/propertyrole/")
propertyquantification_individuals = get_ontology("http://scientificvariablesontology.org/svo/propertyquantification/")
propertytype_individuals = get_ontology("http://scientificvariablesontology.org/svo/propertytype/")
domain_individuals = get_ontology("http://scientificvariablesontology.org/svo/domain/")

# Set up top-level ontology classes.
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

# Add atomic SVO vocabulary terms to ontology.
for row in reader:
    try:
        entity_id, entity_label, entity_class, entity_synonym, _, \
            entity_wikipedia_page, entity_definition, entity_definition_source, entity_wikidata = row
    except:
        print('Problem reading line after: ', entity_id)
        continue
    if entity_class == 'phenomenon':
        with phenomenon_individuals:
            individual = onto.Phenomenon(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'matter':
        with matter_individuals:
            individual = onto.Matter(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'process':
        with process_individuals:
            individual = onto.Process(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'property':
        with property_individuals:
            individual = onto.Property(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'operation':
        with operation_individuals:
            individual = onto.Operation(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'abstraction':
        with abstraction_individuals:
            individual = onto.Abstraction(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'attribute':
        with attribute_individuals:
            individual = onto.Attribute(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'model':
        with model_individuals:
            individual = onto.Model(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'direction':
        with direction_individuals:
            individual = onto.Direction(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'form':
        with form_individuals:
            individual = onto.Form(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'role':
        with role_individuals:
            individual = onto.Role(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'trajectory':
        with trajectory_individuals:
            individual = onto.Trajectory(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'part':
        with part_individuals:
            individual = onto.Part(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'propertytype':
        with propertytype_individuals:
            individual = onto.PropertyType(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'propertyrole':
        with propertyrole_individuals:
            individual = onto.PropertyRole(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'propertyquantification':
        with propertyquantification_individuals:
            individual = onto.PropertyQuantification(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    elif entity_class == 'domain':
        with domain_individuals:
            individual = onto.Domain(entity_id)
            set_individual_annotation(individual, entity_label, entity_wikipedia_page, entity_synonym, entity_definition, entity_wikidata)
    else:
        print(entity_class, entity_label)

f = open(variable_file)
reader = csv.reader(f)
next(reader)

# Step through variables in variable_name_tags and link contained atomistic components
# as well as overall described phenomenon and property.
object_annotations = pd.read_csv(annotated_object_file)
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
                    phen_individual = Phenomenon(object_name)
                    phen_individual.label = object_label
                    if matter_individuals[object_name] in matter_individuals.individuals():
                        phen_individual.has_matter = [matter_individuals[object_name]]
                    elif process_individuals[object_name] in process_individuals.individuals():
                        phen_individual.has_process = [process_individuals[object_name]]
            individual.describes_phenomenon = phenomenon_individuals[object_name]
            individual.describes_property = property_individuals[quantity_name]
            if phenomena:
                if phenomena != object_name:
                    phen_ind_add = [phenomenon_individuals[phen.replace('buildings','building')\
                                                           .replace('clouds','cloud')\
                                                            .replace('foreset-beds','foreset-bed')\
                                                            .replace('topset-beds','topset-bed')\
                                                            .replace('diatoms','diatom')\
                                                            .replace('rhizodeposits','rhizodeposit')\
                                                            .replace('roots','root')\
                                                            .replace('plants','plant')] for phen in phenomena.split(', ')]
                    individual.contains_phenomenon_reference_to = phen_ind_add
            if processes:
                process_ind_add = [process_individuals[proc] for proc in processes.split(', ')]
                individual.contains_process_reference_to = process_ind_add
            if matter:
                matter_ind_add = [matter_individuals[mat.replace('alkanes','alkane')\
                                                     .replace('alkenes','alkene')] for mat in matter.split(', ')]
                individual.contains_matter_reference_to = matter_ind_add
            if forms:
                forms_ind_add = [form_individuals[f.replace('macropores','macropore')\
                                                  .replace('grains','grain')] for f in forms.split(', ')]
                individual.contains_form_reference_to = forms_ind_add
            if attributes:
                attrs_ind_add = [attribute_individuals[attr] for attr in attributes.split(', ')]
                individual.contains_attribute_reference_to = attrs_ind_add
            if abstractions:
                abs_ind_add = [abstraction_individuals[abs.replace('endpoints','endpoint')\
                                                       .replace('foci','focus')] for abs in abstractions.split(', ')]
                individual.contains_abstraction_reference_to = abs_ind_add
            if models:
                model_ind_add = [model_individuals[mod] for mod in models.split(', ')]
                individual.contains_model_reference_to = model_ind_add
            if trajectories:
                traj_ind_add = [trajectory_individuals[traj] for traj in trajectories.split(', ')]
                individual.contains_trajectory_reference_to = traj_ind_add
            if parts:
                part_ind_add = [part_individuals[part.replace('constituents','constituent')\
                                                 .replace('tops','top')] for part in parts.split(', ')]
                individual.contains_part_reference_to = part_ind_add
            if roles:
                role_ind_add = [role_individuals[role.replace('sources','source')\
                                                 .replace('crops','crop')\
                                                 .replace('substrates','substrate')] for role in roles.split(', ')]
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

# Add phenomenon link to the ontology if it is missing
def add_phen_link(row, column, individuals, object_info, category = 'phenomenon'):
    if row[column] != '':
        phen_link = row[column]
        if individuals[phen_link] not in individuals.individuals():
            print(f'Adding {phen_link} to {individuals}.')
            with individuals:
                if category == 'phenomenon':
                    phen_individual = Phenomenon(phen_link)
                elif category == 'abstraction':
                    phen_individual = Abstraction(phen_link)
                elif category == 'matter':
                    phen_individual = Matter(phen_link)
                elif category == 'form':
                    phen_individual = Form(phen_link)
                elif category == 'property':
                    phen_individual = Property(phen_link)
                elif category == 'part':
                    phen_individual = Part(phen_link)
                elif category == 'process':
                    phen_individual = Process(phen_link)
                elif category == 'role':
                    phen_individual = Role(phen_link)
                elif category == 'domain':
                    phen_individual = Domain(phen_link)
                try:
                    phen_label = object_info.loc[\
                    object_info['encoded_name']==phen_link,\
                        'label_name'].iloc[0]
                except:
                    phen_label = phen_link
                phen_individual.label = phen_label
        return phen_link
    return None

# Read in the complex phenomena generated and atomized from the object_names of the variables and
# add them to the ontology.
object_info = pd.read_csv(object_file).fillna('')
for index, row in object_info.iterrows():
    object_name = row['encoded_name']
    object_label = row['label_name']
    with phenomenon_individuals:
        if phenomenon_individuals[object_name] not in phenomenon_individuals.individuals():
            phen_individual = Phenomenon(object_name)
            phen_individual.label = object_label
        else:
            phen_individual = phenomenon_individuals[object_name]

        # Linked items are phenomena
        phen_link = add_phen_link(row, 'has-primary-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_primary_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-adjacent-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_adjacent_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'participates-in', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_primary_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-primary-participant-phenomenon2', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_primary_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-first-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_first_participant_phenomenon.append(phenomenon_individuals[phen_link])
        phen_link = add_phen_link(row, 'has-second-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_second_participant_phenomenon.append(phenomenon_individuals[phen_link])
        phen_link = add_phen_link(row, 'has-medium-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_medium_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-sink-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_sink_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-source-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_source_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-in-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_in_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-numerator-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_numerator_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-denominator-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_denominator_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-minuend-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_minuend_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-subtrahend-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_subtrahend_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-perspective-participant-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_perspective_participant_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-source-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_source_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-sink-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_sink_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-containing-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_containing_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-containing-medium-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_containing_medium_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'is-part-of-containing-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.is_part_of_containing_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-location', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_location = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-location-of-origin', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_location_of_origin = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-model-location', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_location_within_model = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'is-observed-by', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_observing_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'measured-at', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_measurement_reference_at = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'measured-above', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_measurement_reference_above = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'measured-since', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_measurement_reference_since = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'measured-along', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_measurement_reference_along = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'measured-from', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_measurement_reference_from = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'measured-to', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_measurement_reference_to = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'measured-below', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_measurement_reference_below = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'measured-wrt', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_measurement_reference_below = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_phenomenon.append(phenomenon_individuals[phen_link])
        phen_link = add_phen_link(row, 'surrounds', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.surrounds = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'drives', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.drives = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'orbits-around', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.orbits = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-participating-medium-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_participating_medium_phenomenon = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-participating-primary-phenomenon', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.has_participating_primary_phenomenon = [phenomenon_individuals[phen_link]]

        # Linked items are processes.
        phen_link = add_phen_link(row, 'undergoes-process', process_individuals, object_info, category = 'process')
        if phen_link:
            phen_individual.undergoes_process = [process_individuals[phen_link]]
        phen_link = add_phen_link(row, 'undergoes-process2', process_individuals, object_info, category = 'process')
        if phen_link:
            phen_individual.undergoes_process.append(process_individuals[phen_link])

        # Linked items are parts.
        phen_link = add_phen_link(row, 'has-part', part_individuals, object_info, category = 'part')
        if phen_link:
            phen_individual.has_part = [part_individuals[phen_link]]
        phen_link = add_phen_link(row, 'has-part2', part_individuals, object_info, category = 'part')
        if phen_link:
            phen_individual.has_part.append(part_individuals[phen_link])

        # Linked items are abstractions.
        phen_link = add_phen_link(row, 'has-abstraction', abstraction_individuals, object_info, category = 'abstraction')
        if phen_link:
            print(phen_link)
            phen_individual.has_abstraction = [abstraction_individuals[phen_link]]
        phen_link = add_phen_link(row, 'is-modeled-by', phenomenon_individuals, object_info)
        if phen_link:
            phen_individual.is_modeled_by.append(phenomenon_individuals[phen_link])

        # Linked terms are matter.
        phen_link = add_phen_link(row, 'has-matter', matter_individuals, object_info, category = 'matter')
        if phen_link:
            phen_individual.has_matter.append(matter_individuals[phen_link])
        phen_link = add_phen_link(row, 'contains-matter', matter_individuals, object_info, category = 'matter')
        if phen_link:
            phen_individual.contains_matter.append(matter_individuals[phen_link])
        phen_link = add_phen_link(row, 'has-primary-matter', matter_individuals, object_info, category = 'matter')
        if phen_link:
            phen_individual.contains_primary_matter.append(matter_individuals[phen_link]) 

        # Linked terms are forms.
        phen_link = add_phen_link(row, 'has-form', form_individuals, object_info, category = 'form')
        if phen_link:
            phen_individual.has_form = [form_individuals[phen_link]]

        # Linked terms are roles.
        phen_link = add_phen_link(row, 'has-role', role_individuals, object_info, category = 'role')
        if phen_link:
            phen_individual.has_role = [role_individuals[phen_link]]


        # Linked terms are trajectories.
        phen_link = add_phen_link(row, 'has-trajectory', trajectory_individuals, object_info, category = 'trajectory')
        if phen_link:
            phen_individual.has_trajectory = [trajectory_individuals[phen_link]]   
        
        # Linked terms are domain.
        phen_link = add_phen_link(row, 'has-domain', phenomenon_individuals, object_info, category = 'domain')
        if phen_link:
            phen_individual.has_domain = [phenomenon_individuals[phen_link]]
        
        # Linked terms are property.
        phen_link = add_phen_link(row, 'referenced-with-property', phenomenon_individuals, object_info, category = 'property')
        if phen_link:
            phen_individual.is_reference_for_property = [phenomenon_individuals[phen_link]]
        phen_link = add_phen_link(row, 'reference-for-computing', phenomenon_individuals, object_info, category = 'property')
        if phen_link:
            phen_individual.has_reference_for_property = [phenomenon_individuals[phen_link]]

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