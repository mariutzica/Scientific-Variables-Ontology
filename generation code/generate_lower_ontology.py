# -*- coding: utf-8 -*-
"""
Created on Thurs Mar 16 11:25:06 2017
Last Edited on Fri May 25 2018

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

##################################
#   Variable Initialization      #
##################################

ext_vocabulary      = '../foundational vocabulary/'
ext_output          = '../core ontology files/'

qual_property_file  = 'qualitative_property.csv'
property_quantification_file  = 'property_quantification.csv'
property_role_file  = 'property_role.csv'
property_type_file  = 'property_type.csv'
quantitative_property_file  = 'quantitative_property.csv'

operator_file  = 'operator.csv'
operator_quantity_file  = 'quantitative_property_with_operator.csv'

process_file  = 'process.csv'

qualitative_attribute_file  = 'qualitative_attribute.csv'
quantitative_attribute_file  = 'quantitative_attribute.csv'

################################
#   INITIAL DATA LOAD          #
################################

qual_property_vocabulary = utils.load_data( ext_vocabulary, qual_property_file )
property_quantification_vocabulary = \
            utils.load_data( ext_vocabulary, property_quantification_file )
property_role_vocabulary = \
            utils.load_data( ext_vocabulary, property_role_file )
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
qualitative_attribute_vocabulary = \
            utils.load_data( ext_vocabulary, qualitative_attribute_file )   
quantitative_attribute_vocabulary = \
            utils.load_data( ext_vocabulary, quantitative_attribute_file )  
            
######################
#  OUTPUT FILE SETUP #
######################

property_ttl = open( ext_output + 'svo-lower-property.ttl', 'w' )
operator_ttl = open( ext_output + 'svo-lower-operator.ttl', 'w' )
process_ttl = open( ext_output + 'svo-lower-process.ttl', 'w' )
attribute_ttl = open( ext_output + 'svo-lower-attribute.ttl', 'w' )

utils.open_write_file( property_ttl, 'Property' )
utils.open_write_file( operator_ttl, 'Operator' )
utils.open_write_file( process_ttl, 'Process' )
utils.open_write_file( attribute_ttl, 'Attribute' )

################################
#   DATA PREPROCESSING         #
################################

utils.preprocess_quantity( quantitative_property_vocabulary )
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

label = '\n\n###PropertyQuantification\n\n'
utils.create_bb_file( property_quantification_vocabulary, property_ttl, \
                      'PropertyQuantification', 'property_quantification', \
                      'property', label = label )

label = '\n\n###PropertyRole\n\n'
utils.create_bb_file( property_role_vocabulary, property_ttl, \
                      'PropertyRole', 'property_role', \
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
                      'OperatorQuantitativeProperty', 'operator_quantity', \
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

# create Attribute file
label = '\n\n###Attribute\n\n'
utils.create_bb_file( qualitative_attribute_vocabulary, attribute_ttl, \
                      'Attribute', 'attribute', 'attribute', label = label )
utils.create_bb_file( quantitative_attribute_vocabulary, attribute_ttl, \
                      'Attribute', 'attribute', 'attribute', label = label )

######################
#    File Cleanup    #
######################

property_ttl.close()
operator_ttl.close()
process_ttl.close()
attribute_ttl.close()