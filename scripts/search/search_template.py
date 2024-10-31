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

# basic search for entry with a certain label
term = 'water'
search_result = default_world.sparql(
"""                    
    SELECT ?x
    WHERE    {{ 
    ?x rdfs:label "{}" .
    }} 
""".format(term))
#print(list(search_result))

# basic search for entry containing a certain string in its label
# return label and SVO class
term = 'water'
search_result = default_world.sparql(
"""                    
    SELECT ?label ?category
    WHERE {{ 
    ?x rdfs:label ?label .
    ?x a ?category .
    FILTER(STRSTARTS(STR(?category), "http://scientificvariablesontology.org/"))
    FILTER regex(str(?label), "{}", "i")
    }} 
""".format(term))
#print(list(search_result))

# search variables to return the ones for which the primary
# phenomenon (target of observation) is water
term = 'water'
search_result = default_world.sparql(
"""                    
    SELECT ?label
    WHERE {{ 
    ?x rdfs:label ?label .
    ?x svo:describes_phenomenon ?phen .
    ?phen svo:has_primary_participant_phenomenon ?pp .
    ?pp rdfs:label "{}".
    }} 
""".format(term))
#print(list(search_result))

# search phenomena to return the ones that contain a simpler phenomenon reference
search_result = default_world.sparql(
"""                    
    SELECT ?label ?category ?pname
    WHERE {{ 
    ?x rdfs:label ?label .
    ?x svo:has_phenomenon ?phen .
    ?phen rdfs:label ?pname .
    ?x a ?category .
    FILTER(STRSTARTS(STR(?category), "http://scientificvariablesontology.org/"))
    }} 
""")
#for item in search_result:
#    print(item)
#    input('Press enter to continue ...')

# for all property links of variables
search_result = default_world.sparql(
"""                    
    SELECT DISTINCT ?relationship
    WHERE {{
    ?x a svo:Phenomenon .
    ?x ?relationship ?pname .
    FILTER(STRSTARTS(STR(?relationship), "http://scientificvariablesontology.org/"))
    }} 
""")
#print(list(search_result[:]))