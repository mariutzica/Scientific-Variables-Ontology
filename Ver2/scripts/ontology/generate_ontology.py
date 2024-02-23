from owlready2 import *
import csv

terminology_file = 'source/svo_atomic_vocabulary.csv'
variable_file = 'source/variable_name_tags.csv'

wikidata_http = 'https://www.wikidata.org/wiki/{}'

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
    class has_matter(Phenomenon >> Matter): pass
    class has_process(Phenomenon >> Process): pass
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

with variable_individuals:
    for row in reader:
        original_name, variable_name, object_name, quantity_name, \
            object_pattern, quantity_pattern, phenomena, processes, matter, forms, roles, \
            properties, operations, propertytypes, propertyroles, \
            propertyquantifications, trajectories, domains, attributes, \
            abstractions, models, directions, parts = row
        if variable_individuals[variable_name] not in list(variable_individuals.individuals()):
            individual = Variable(variable_name)
            individual.label = variable_name
            individual.has_original_label = original_name
            if phenomenon_individuals[object_name] not in phenomenon_individuals.individuals():
                with phenomenon_individuals:
                    phen_individual = Phenomenon(object_name)
                    phen_individual.label = object_name
                    if matter_individuals[object_name] in matter_individuals.individuals():
                        phen_individual.has_matter = [matter_individuals[object_name]]
                    elif process_individuals[object_name] in process_individuals.individuals():
                        phen_individual.has_process = [process_individuals[object_name]]
            individual.describes_phenomenon = phenomenon_individuals[object_name]
            individual.describes_property = property_individuals[quantity_name]
            if phenomena:
                if phenomena != object_name:
                    phen_ind_add = [phenomenon_individuals[phen] for phen in phenomena.split(', ')]
                    individual.contains_phenomenon_reference_to = phen_ind_add
            if processes:
                process_ind_add = [process_individuals[proc] for proc in processes.split(', ')]
                individual.contains_process_reference_to = process_ind_add
            if matter:
                matter_ind_add = [matter_individuals[mat] for mat in matter.split(', ')]
                individual.contains_matter_reference_to = matter_ind_add
            if forms:
                forms_ind_add = [form_individuals[f] for f in forms.split(', ')]
                individual.contains_form_reference_to = forms_ind_add
            if attributes:
                attrs_ind_add = [attribute_individuals[attr] for attr in attributes.split(', ')]
                individual.contains_attribute_reference_to = attrs_ind_add
            if abstractions:
                abs_ind_add = [abstraction_individuals[abs] for abs in abstractions.split(', ')]
                individual.contains_abstraction_reference_to = abs_ind_add
            if models:
                model_ind_add = [model_individuals[mod] for mod in models.split(', ')]
                individual.contains_model_reference_to = model_ind_add
            if trajectories:
                traj_ind_add = [trajectory_individuals[traj] for traj in trajectories.split(', ')]
                individual.contains_trajectory_reference_to = traj_ind_add
            if parts:
                part_ind_add = [part_individuals[part] for part in parts.split(', ')]
                individual.contains_part_reference_to = part_ind_add
            if roles:
                role_ind_add = [role_individuals[role] for role in roles.split(', ')]
                individual.contains_role_reference_to = role_ind_add
            if operations:
                op_ind_add = [operation_individuals[op] for op in operations.split(', ')]
                individual.contains_operation_reference_to = op_ind_add
            if properties:
                if properties != quantity_name:
                    property_ind_add = [property_individuals[prop] for prop in properties.split(', ')]
                    individual.contains_property_reference_to = property_ind_add
        else:
            #print('Duplicate variable:', variable_name)
            variable_individuals[variable_name].has_original_label.append(original_name)

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