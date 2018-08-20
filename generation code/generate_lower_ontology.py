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
            
######################
#  OUTPUT FILE SETUP #
######################

property_ttl = open( ext_output + 'svo-lower-property.ttl', 'w' )

utils.open_write_file( property_ttl, 'Property' )

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
######################
#    File Cleanup    #
######################

property_ttl.close()