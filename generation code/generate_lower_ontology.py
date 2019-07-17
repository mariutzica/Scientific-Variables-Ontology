# -*- coding: utf-8 -*-
"""
Created on Thurs Mar 16 11:25:06 2017
Last Edited on Fri August 24 2018

@author: Maria Stoica
@decription: Generate the lower ontology version 1.0.0.
    First version of Ontology for Scientific Variables
    Separate RDF files (and namespace) created for: Property
"""

##################################
#   Import required packages     #
##################################

#utils
import utils as utils
import rdflib

##################################
#   Variable Initialization      #
##################################

ext_vocabulary      = '../foundational vocabulary/'
ext_csn_variable    = '../atomize and standardize csn/'
ext_output          = '../core ontology files/svl/'

qual_property_file  = 'qualitative_property.csv'
property_quantification_file  = 'property_quantification.csv'
property_type_file  = 'property_type.csv'
quantitative_property_file  = 'quantitative_property.csv'

operator_file  = 'operator.csv'
operator_quantity_file  = 'quantitative_property_with_operator.csv'

process_file  = 'process.csv'
phenomenon_file  = 'phenomenon.csv'
compound_phenomenon_file  = 'phenomenon_compound.csv'

qualitative_attribute_file  = 'qualitative_attribute.csv'
quantitative_attribute_file  = 'quantitative_attribute.csv'

matter_file  = 'matter.csv'

form_file  = 'form_and_configuration.csv'

inanimate_nat_body_file  = 'inanimate_natural_body.csv'
inanimate_fab_body_file  = 'inanimate_fabricated_body.csv'
animate_body_file  = 'animate_body.csv'

math_abstraction_file  = 'abstraction_mathematical.csv'
phys_abstraction_file  = 'abstraction_physical.csv'
phys_abstraction_part_file  = 'abstraction_physical_part.csv'
math_abstraction_part_file  = 'abstraction_mathematical_part.csv'

part_file  = 'part.csv'

role_file  = 'role.csv'
property_role_file  = 'property_role.csv'
participant_role_file  = 'participant_role.csv'

trajectory_file  = 'trajectory.csv'
trajectory_direction_file  = 'trajectory_direction.csv'

relationship_file  = 'relationship.csv'

context_phen_file  = 'context_phenomena.csv'
role_phen_file  = 'role_phenomena.csv'
medium_phen_file  = 'medium_phenomena.csv'
reference_phen_file  = 'reference_phenomena.csv'

context_file = 'context.csv'
participant_file = 'participant.csv'
reference_file = 'reference.csv'

csn_variables_file  = 'CSDMS_standard_names.csv'

################################
#   INITIAL DATA LOAD          #
################################

qual_property_vocabulary = utils.load_data( ext_vocabulary, qual_property_file )
property_quantification_vocabulary = \
            utils.load_data( ext_vocabulary, property_quantification_file )
property_type_vocabulary = \
            utils.load_data( ext_vocabulary, property_type_file )
quantitative_property_vocabulary = \
            utils.load_data( ext_vocabulary, quantitative_property_file )
operator_vocabulary = \
            utils.load_data( ext_vocabulary, operator_file )
operator_quantity_vocabulary = \
            utils.load_data( ext_vocabulary, operator_quantity_file )
process_vocabulary = \
            utils.load_data( ext_vocabulary, process_file )
phenomenon_vocabulary = \
            utils.load_data( ext_vocabulary, phenomenon_file )
compound_phenomenon_vocabulary = \
            utils.load_data( ext_vocabulary, compound_phenomenon_file )
qualitative_attribute_vocabulary = \
            utils.load_data( ext_vocabulary, qualitative_attribute_file )
quantitative_attribute_vocabulary = \
            utils.load_data( ext_vocabulary, quantitative_attribute_file )
matter_vocabulary = \
            utils.load_data( ext_vocabulary, matter_file )
form_vocabulary = \
            utils.load_data( ext_vocabulary, form_file )
math_abstraction_vocabulary = \
            utils.load_data( ext_vocabulary, math_abstraction_file )
phys_abstraction_vocabulary = \
            utils.load_data( ext_vocabulary, phys_abstraction_file )
phys_abstraction_part_vocabulary = \
            utils.load_data( ext_vocabulary, phys_abstraction_part_file )
math_abstraction_part_vocabulary = \
            utils.load_data( ext_vocabulary, math_abstraction_part_file )
part_vocabulary = \
            utils.load_data( ext_vocabulary, part_file )
inanimate_nat_body_vocabulary = \
            utils.load_data( ext_vocabulary, inanimate_nat_body_file )
inanimate_fab_body_vocabulary = \
            utils.load_data( ext_vocabulary, inanimate_fab_body_file )
animate_body_vocabulary = \
            utils.load_data( ext_vocabulary, animate_body_file )
role_vocabulary = \
            utils.load_data( ext_vocabulary, role_file )
participant_role_vocabulary = \
            utils.load_data( ext_vocabulary, participant_role_file )
property_role_vocabulary = \
            utils.load_data( ext_vocabulary, property_role_file )
trajectory_vocabulary = \
            utils.load_data( ext_vocabulary, trajectory_file )
trajectory_direction_vocabulary = \
            utils.load_data( ext_vocabulary, trajectory_direction_file )
relationship_vocabulary = \
            utils.load_data( ext_vocabulary, relationship_file )
context_vocabulary = \
            utils.load_data( ext_vocabulary, context_file )
participant_vocabulary = \
            utils.load_data( ext_vocabulary, participant_file )
reference_vocabulary = \
            utils.load_data( ext_vocabulary, reference_file )
phenomenon_context_vocabulary = \
            utils.load_data( ext_vocabulary, context_phen_file )
phenomenon_medium_vocabulary = \
            utils.load_data( ext_vocabulary, medium_phen_file )
phenomenon_reference_vocabulary = \
            utils.load_data( ext_vocabulary, reference_phen_file )
phenomenon_multiple_vocabulary = \
            utils.load_data( ext_vocabulary, role_phen_file )
csn_vocabulary = \
            utils.load_data( ext_csn_variable, csn_variables_file )

######################
#  OUTPUT FILE SETUP #
######################

property_ttl = open( ext_output + 'property/1.0.0/svo-lower-property.ttl', 'w' )
operator_ttl = open( ext_output + 'operator/1.0.0/svo-lower-operator.ttl', 'w' )
process_ttl = open( ext_output + 'process/1.0.0/svo-lower-process.ttl', 'w' )
phenomenon_ttl = open( ext_output + 'phenomenon/1.0.0/svo-lower-phenomenon.ttl', 'w' )
attribute_ttl = open( ext_output + 'attribute/1.0.0/svo-lower-attribute.ttl', 'w' )
matter_ttl = open( ext_output + 'matter/1.0.0/svo-lower-matter.ttl', 'w' )
form_ttl = open( ext_output + 'form/1.0.0/svo-lower-form.ttl', 'w' )
body_ttl = open( ext_output + 'body/1.0.0/svo-lower-body.ttl', 'w' )
abstraction_ttl = open( ext_output + 'abstraction/1.0.0/svo-lower-abstraction.ttl', 'w' )
part_ttl = open( ext_output + 'part/1.0.0/svo-lower-part.ttl', 'w' )
role_ttl = open( ext_output + 'role/1.0.0/svo-lower-role.ttl', 'w' )
rolephen_ttl = open( ext_output + 'rolephenomenon/1.0.0/svo-lower-rolephen.ttl', 'w' )
trajectory_ttl = open( ext_output + 'trajectory/1.0.0/svo-lower-trajectory.ttl', 'w' )
trajectory_direction_ttl = open( ext_output + 'trajectorydirection/1.0.0/svo-lower-trajectorydirection.ttl', 'w' )
relationship_ttl = open( ext_output + 'relationship/1.0.0/svo-lower-relationship.ttl', 'w' )
context_ttl = open( ext_output + 'context/1.0.0/svo-lower-context.ttl', 'w' )
participant_ttl = open( ext_output + 'participant/1.0.0/svo-lower-participant.ttl', 'w' )
reference_ttl = open( ext_output + 'reference/1.0.0/svo-lower-reference.ttl', 'w' )
variable_ttl = open( ext_output + 'variable/1.0.0/svo-lower-variable.ttl', 'w' )

utils.open_write_file( property_ttl, 'Property' )
utils.open_write_file( operator_ttl, 'Operator' )
utils.open_write_file( process_ttl, 'Process' )
utils.open_write_file( phenomenon_ttl, 'Phenomenon' )
utils.open_write_file( attribute_ttl, 'Attribute' )
utils.open_write_file( form_ttl, 'Form' )
utils.open_write_file( matter_ttl, 'Matter' )
utils.open_write_file( body_ttl, 'Body' )
utils.open_write_file( abstraction_ttl, 'Abstraction' )
utils.open_write_file( part_ttl, 'Part' )
utils.open_write_file( role_ttl, 'Role' )
utils.open_write_file( rolephen_ttl, 'RolePhenomenon' )
utils.open_write_file( trajectory_ttl, 'Trajectory' )
utils.open_write_file( trajectory_direction_ttl, 'TrajectoryDirection' )
utils.open_write_file( relationship_ttl, 'Relationship' )
utils.open_write_file( context_ttl, 'Context' )
utils.open_write_file( participant_ttl, 'Participant' )
utils.open_write_file( reference_ttl, 'Reference' )
utils.open_write_file( variable_ttl, 'Variable' )

################################
#   DATA PREPROCESSING         #
################################

utils.preprocess_quantity( quantitative_property_vocabulary )
utils.preprocess_quantity( operator_quantity_vocabulary )
compound_operator_vocabulary = utils.preprocess_operator( operator_vocabulary, \
                               operator_quantity_vocabulary )

utils.assign_units( quantitative_property_vocabulary, \
                    operator_quantity_vocabulary, operator_vocabulary )
utils.create_unit_strings( quantitative_property_vocabulary )
utils.create_unit_strings( operator_quantity_vocabulary )

##################################
#    Write Base Individuals      #
##################################

### The following commands create the building blocks for each class

# create Property file
label = '\n\n###Property\n\n'
utils.create_bb_file( qual_property_vocabulary, property_ttl, 'Property', \
                      'property', 'property', label = label )

label = '\n\n###PropertyStandardization\n\n'
utils.create_bb_file( property_quantification_vocabulary, property_ttl, \
                      'PropertyStandardization', 'property_quantification', \
                      'property', label = label )

label = '\n\n###PropertyType\n\n'
utils.create_bb_file( property_type_vocabulary, property_ttl, \
                      'PropertyType', 'property_type', \
                      'property', label = label )

label = '\n\n###QuantitativeProperty (Quantity)\n\n'
utils.create_bb_file( quantitative_property_vocabulary, property_ttl, \
                      'QuantitativeProperty', 'quantity', \
                      'property', label = label, \
                      process_vocab = process_vocabulary )

label = '\n\n###OperatorQuantitativeProperty (OperatorQuantity)\n\n'
utils.create_bb_file( operator_quantity_vocabulary, property_ttl, \
                      'QuantitativeProperty', 'operator_quantity', \
                      'property', label = label )

# create Operator file
label = '\n\n###Operator\n\n'
utils.create_bb_file( operator_vocabulary, operator_ttl, \
                      'Operator', 'operator', 'operator', label = label )

label = '\n\n###(Compound)Operator\n\n'
utils.create_bb_file( compound_operator_vocabulary, operator_ttl, \
                      'Operator', 'operator', 'operator', label = label )

# create Process file
label = '\n\n###Process\n\n'
utils.create_bb_file( process_vocabulary, process_ttl, \
                      'Process', 'process', 'process', label = label )

# create Phenomenon file
label = '\n\n###Phenomenon\n\n'
utils.create_bb_file( phenomenon_vocabulary, phenomenon_ttl, \
                      'SpatiotemporalPhenomenon', 'phenomenon', 'phenomenon', label = label )
label = '\n\n###Compound Phenomenon\n\n'
utils.create_bb_file( compound_phenomenon_vocabulary, phenomenon_ttl, \
                      'SpatiotemporalPhenomenon', 'phenomenon', 'phenomenon', label = label )
label = '\n\n###ContextPhenomenon\n\n'
utils.create_bb_file( phenomenon_context_vocabulary, phenomenon_ttl, \
                      'ContextPhenomenon', 'phenomenon', 'phenomenon', label = label )
label = '\n\n###MediumPhenomenon\n\n'
utils.create_bb_file( phenomenon_medium_vocabulary, phenomenon_ttl, \
                      'MediumPhenomenon', 'phenomenon', 'phenomenon', label = label )
label = '\n\n###ReferencePhenomenon\n\n'
utils.create_bb_file( phenomenon_reference_vocabulary, phenomenon_ttl, \
                      'ReferencePhenomenon', 'phenomenon', 'phenomenon', label = label )
label = '\n\n###CompoundPhenomenon\n\n'
utils.create_bb_file( phenomenon_multiple_vocabulary, phenomenon_ttl, \
                      'CompoundPhenomenon', 'phenomenon', 'phenomenon', label = label )

# create Attribute file
label = '\n\n###(Qualitative)Attribute\n\n'
utils.create_bb_file( qualitative_attribute_vocabulary, attribute_ttl, \
                      'Attribute', 'attribute', 'attribute', label = label )
label = '\n\n###(Quantitative)Attribute\n\n'
utils.create_bb_file( quantitative_attribute_vocabulary, attribute_ttl, \
                      'Attribute', 'attribute', 'attribute', label = label )

# create Matter file
label = '\n\n###Matter\n\n'
utils.create_bb_file( matter_vocabulary, matter_ttl, \
                      'Matter', 'matter', 'matter', label = label )

# create Form file
label = '\n\n###Form\n\n'
utils.create_bb_file( form_vocabulary, form_ttl, \
                      'Form', 'form', 'form', label = label )

# create Body file
label = '\n\n###Inanimate Natural Body\n\n'
utils.create_bb_file( inanimate_nat_body_vocabulary, body_ttl, \
                      'Body', 'body', 'body', label = label )
label = '\n\n###Inanimate Fabricated Body\n\n'
utils.create_bb_file( inanimate_fab_body_vocabulary, body_ttl, \
                      'Body', 'body', 'body', label = label )
label = '\n\n###Animate Body\n\n'
utils.create_bb_file( animate_body_vocabulary, body_ttl, \
                      'Body', 'body', 'body', label = label )

# create Abstraction file
label = '\n\n###Mathematical Abstraction\n\n'
utils.create_bb_file( math_abstraction_vocabulary, abstraction_ttl, \
                      'MathematicalAbstraction', 'abstraction', 'abstraction', label = label )
label = '\n\n###Physical Abstraction\n\n'
utils.create_bb_file( phys_abstraction_vocabulary, abstraction_ttl, \
                      'PhysicalAbstraction', 'abstraction', 'abstraction', label = label )
label = '\n\n###Physical Abstraction Part\n\n'
utils.create_bb_file( phys_abstraction_part_vocabulary, abstraction_ttl, \
                      'PhysicalAbstraction', 'abstraction', 'abstraction', label = label, part = True )
label = '\n\n###Mathematical Abstraction Part\n\n'
utils.create_bb_file( math_abstraction_part_vocabulary, abstraction_ttl, \
                      'MathematicalAbstraction', 'abstraction', 'abstraction', label = label, part = True )


# create Part file
label = '\n\n###Part\n\n'
utils.create_bb_file( part_vocabulary, part_ttl, \
                      'Part', 'part', 'part', label = label )

# create Role file
label = '\n\n###Role\n\n'
utils.create_bb_file( role_vocabulary, rolephen_ttl, \
                      'RolePhenomenon', 'role', 'rolephenomenon', label = label )
label = '\n\n###ParticipantRole\n\n'
utils.create_bb_file( participant_role_vocabulary, role_ttl, \
                      'ParticipantRole', 'participant_role', 'role', label = label )
label = '\n\n###PropertyRole\n\n'
utils.create_bb_file( property_role_vocabulary, role_ttl, \
                      'PropertyRole', 'property_role', \
                      'role', label = label )

# create Trajectory file
label = '\n\n###Trajectory\n\n'
utils.create_bb_file( trajectory_vocabulary, trajectory_ttl, \
                      'Trajectory', 'trajectory', 'trajectory', label = label )

# create TrajectoryDirection file
label = '\n\n###TrajectoryDirection\n\n'
utils.create_bb_file( trajectory_direction_vocabulary, trajectory_direction_ttl, \
                      'TrajectoryDirection', 'trajectory_direction', 'trajectorydirection', label = label )

# create Relationship file
label = '\n\n###Relationship\n\n'
utils.create_bb_file( relationship_vocabulary, relationship_ttl, \
                      'Relationship', 'relationship', 'relationship', label = label )

# create Context file
label = '\n\n###Context\n\n'
utils.create_bb_file( context_vocabulary, context_ttl, \
                      'Context', 'context', 'context', label = label )
# create Participant file
label = '\n\n###Participant\n\n'
utils.create_bb_file( participant_vocabulary, participant_ttl, \
                      'Participant', 'participant', 'participant', label = label )
# create Reference file
label = '\n\n###Reference\n\n'
utils.create_bb_file( reference_vocabulary, reference_ttl, \
                      'Reference', 'reference', 'reference', label = label )


# create Variable file
label = '\n\n###CSN Variables\n\n'
utils.create_variable_entries( csn_vocabulary, variable_ttl, label = label )

######################
#    File Cleanup    #
######################

property_ttl.close()
operator_ttl.close()
process_ttl.close()
phenomenon_ttl.close()
attribute_ttl.close()
matter_ttl.close()
form_ttl.close()
part_ttl.close()
body_ttl.close()
abstraction_ttl.close()
role_ttl.close()
rolephen_ttl.close()
trajectory_ttl.close()
trajectory_direction_ttl.close()
relationship_ttl.close()
context_ttl.close()
participant_ttl.close()
reference_ttl.close()
variable_ttl.close()

######################
#    File Conversion #
######################

def convert_graph(input_file, format_in='n3', format_out='xml'):
    g=rdflib.Graph()
    g.parse(input_file, format=format_in)
    g.serialize(destination=input_file.rsplit('.',1)[0]+'.rdf', format='xml')

convert_graph(ext_output+'property/1.0.0/svo-lower-property.ttl')
convert_graph(ext_output+'operator/1.0.0/svo-lower-operator.ttl')
convert_graph(ext_output+'process/1.0.0/svo-lower-process.ttl')
convert_graph(ext_output+'phenomenon/1.0.0/svo-lower-phenomenon.ttl')
convert_graph(ext_output+'attribute/1.0.0/svo-lower-attribute.ttl')
convert_graph(ext_output+'matter/1.0.0/svo-lower-matter.ttl')
convert_graph(ext_output+'form/1.0.0/svo-lower-form.ttl')
convert_graph(ext_output+'body/1.0.0/svo-lower-body.ttl')
convert_graph(ext_output+'abstraction/1.0.0/svo-lower-abstraction.ttl')
convert_graph(ext_output+'role/1.0.0/svo-lower-role.ttl')
convert_graph(ext_output+'rolephenomenon/1.0.0/svo-lower-rolephen.ttl')
convert_graph(ext_output+'trajectory/1.0.0/svo-lower-trajectory.ttl')
convert_graph(ext_output+'trajectorydirection/1.0.0/svo-lower-trajectorydirection.ttl')
convert_graph(ext_output+'relationship/1.0.0/svo-lower-relationship.ttl')
convert_graph(ext_output+'context/1.0.0/svo-lower-context.ttl')
convert_graph(ext_output+'part/1.0.0/svo-lower-part.ttl')
convert_graph(ext_output+'participant/1.0.0/svo-lower-participant.ttl')
convert_graph(ext_output+'reference/1.0.0/svo-lower-reference.ttl')
convert_graph(ext_output+'variable/1.0.0/svo-lower-variable.ttl')
convert_graph(ext_output+'../svu/1.0.0/svo-upper.ttl')
convert_graph(ext_output+'1.0.0/svo-lower.ttl')
convert_graph(ext_output+'../1.0.0/svo.ttl')

