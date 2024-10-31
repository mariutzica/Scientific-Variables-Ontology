from owlready2 import *

# Load ontology files.
onto_filepath = 'ontology files'
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

# for all property links of variables
search_result = default_world.sparql(
"""                    
    SELECT ?x ?label
    WHERE {{
    ?x a svo:Phenomenon .
    ?x rdfs:label ?label .
    FILTER(CONTAINS(STR(?label), 'water_tide')) .
    }} 
""")
print(list(search_result))

## Variable relationships
# describes_phenomenon
# describes_property

# contains_phenomenon_reference_to
# contains_matter_reference_to
# contains_process_reference_to
# contains_role_reference_to
# contains_abstraction_reference_to
# contains_attribute_reference_to
# contains_property_reference_to
# contains_operation_reference_to
# contains_part_reference_to
# contains_form_reference_to
# contains_trajectory_reference_to

# has_original_label

## Phenomenon relationships

# has_wikipedia_page
# has_wikidata_page
# has_synonym

# has_matter
# has_phenomenon
# has_role
# has_part
# has_form
# has_abstraction
# has_direction
# has_trajectory
# undergoes_process
# has_domain

## DECOMPOSING ATTRIBUTES FROM PHENOMENA
# has_phenomenon_root - the phenomenon that is a root (has_phenomenon?)
# has_attribute - the attribute

## CONTEXT
# is_modeled_by - context linking a phenomenon model to a concrete phenomenon it models
# has_containing_phenomenon - context of containing phenomenon
# is_part_of_containing_phenomenon - context when phen is PART of containing phenomenon
# has_location- context providing location
# has_source_phenomenon - context providing source
# has_observing_phenomenon - has context observer
# orbits - context of what is being orbitted
# has_location_of_origin - context of where the phen originated
# surrounds - context of what phen surrounds

# is_expressed_as
# contains_matter - to express that the current phenomenon contains this matter (has_matter???)
# contains_primary_matter - to express that the current phenomenon is primarily made of this matter (has_primary_matter???)

# has_primary_participant_phenomenon
# has_medium_participant_phenomenon
# has_in_participant_phenomenon
# has_source_participant_phenomenon
# has_participating_primary_phenomenon
# has_sink_participant_phenomenon
# has_numerator_participant_phenomenon
# has_denominator_participant_phenomenon
# has_containing_medium_phenomenon
# has_adjacent_participant_phenomenon
# has_perspective_participant_phenomenon
# has_first_participant_phenomenon
# has_second_participant_phenomenon
# has_minuend_participant_phenomenon
# has_subtrahend_participant_phenomenon

# has_measurement_reference_above
# has_measurement_reference_since
# has_measurement_reference_at
# has_measurement_reference_below
# has_measurement_reference_to
# has_measurement_reference_wrt
# has_measurement_reference_from
# has_measurement_reference_along

# has_reference_for_property
# is_reference_for_property

# has_reference_for_variable
# is_reference_for_variable