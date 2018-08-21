# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:04:45 2017

@author: mast0177
"""

################################
#   LOAD EXTERNAL PACKAGES     #
################################

import sys
# Pandas for data frames and data manipulation
import pandas as pd
# DateTime for getting the timestamp for the file
import datetime
# Create URL friendly string
import urllib.parse as urllib
# import HTMLParser
import html as h

##################################
#   String/constant declarations #
##################################

# header -- top of each file
header = ( '@prefix : <http://www.geoscienceontology.org/svl/{}#> .\n'
           '@prefix svu: <http://www.geoscienceontology.org/svu#> .\n'
           '@prefix owl: <http://www.w3.org/2002/07/owl#> .\n'
           '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
           '@prefix xml: <http://www.w3.org/XML/1998/namespace> .\n'
           '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n'
           '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n'
           '@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n'
           '@base <http://www.geoscienceontology.org/svl/> .\n'
           '\n'
           '<http://www.geoscienceontology.org/svl/{}> rdf:type owl:Ontology ;\n'
           '\t\t\t\trdfs:comment " Scientific Variables Lower Ontology, {} '
           'BETA VERSION." .\n'
           '#\t\t\t\towl:imports <http://www.geoscienceontology.org/svu> .\n'
           '\n\n'
           '#################################################################\n'
           '#    {}   \n'
           '# \n'
           '#################################################################\n' )

# other ttl components
prefix        = '###  http://www.geoscienceontology.org/svl/{}#{}\n'
declaration_class   = ':{} rdf:type owl:Class {}\n'
declaration_subclass = '\t\t\trdfs:subClassOf {} {}\n' 
declaration_instance   = ( ':{} rdf:type owl:NamedIndividual ,\n'
                  '\t\t\t{}:{} {}\n' )

attribute     = '\t\t\tsvu:{} {} {}\n'
synonym       = '\t\t\tskos:altLabel "{}"@en ;\n'
plurality       = '\t\t\tsvu:isPluralityOf :{} ;\n'
preflabel     = '\t\t\tskos:prefLabel "{}"@en .\n'

error_message = ( 'Ooops, the file {} was not found in its expected '
                  'location, {}.\nExiting ...' )

##############################################################################
#                                                                            #
#                       DATA PREPARATION                                     #
#                                                                            #
##############################################################################

# load vocabulary information from files
def load_data( ext, filename, usecols=None ):
    try:
        if not usecols:
            data = pd.read_csv( ext + filename, encoding='utf-8', \
                               index_col=False ).fillna('')
        else:
            data = pd.read_csv( ext + filename, index_col=False, \
                                usecols=usecols ).fillna('')
    except IOError:
        print ( error_message.format( filename, ext) )
        sys.exit(0)
    return data

# Format quantity information for futher processing
def preprocess_quantity( quantity ):    
    # Set non-values to 0 in units columns, reset units for ratios
    col = [ 'L', 'M', 'O', 'T', 'I', 'N', 'radian', 'number', 'currency' ]
    quantity[ col ] = quantity[ col ].replace( '', 0 )
    quantity.loc[ quantity[ 'unitless_ratio' ] == 'yes', col ] = 0

# use root_quantity columne to assign units to modified quantities    
def assign_units( quantity ):
    dim = [ [ 'L', 'M', 'O', 'T', 'I', 'N'] ]
    for i in quantity.index:
        if quantity.loc[i,'root_quantity'] != '':
            quantity.loc[i,dim[0]] = quantity.loc[ \
                        (quantity['quantity_id']==quantity.loc[i,'root_quantity']), \
                        dim[0]].iloc[0]

# create strings to represent units;
# general form, L^# M^# O^# T^# I^# N^#
def create_unit_strings(quantities):
    quantities['units_string'] = ''
    quantities.loc[ quantities['L'] != 0, 'units_string' ] += \
                    'L^' + quantities.loc[quantities['L']!=0,'L']\
                    .map('{:,.2g}'.format) + ' '
    quantities.loc[ quantities['M'] != 0, 'units_string' ] += \
                    'M^' + quantities.loc[quantities['M']!=0,'M']\
                    .map('{:,.2g}'.format)+' '
    quantities.loc[ quantities['O'] != 0, 'units_string' ] += \
                    'O^' + quantities.loc[quantities['O']!=0,'O']\
                    .map('{:,.2g}'.format)+' '
    quantities.loc[ quantities['T'] != 0, 'units_string' ] += \
                    'T^' + quantities.loc[quantities['T']!=0,'T']\
                    .map('{:,.2g}'.format)+' '
    quantities.loc[ quantities['I'] != 0, 'units_string' ] += \
                    'I^' + quantities.loc[quantities['I']!=0,'I']\
                    .map('{:,.2g}'.format)+' '
    quantities.loc[ quantities['N'] != 0, 'units_string' ] += \
                    'N^' + quantities.loc[quantities['N']!=0,'N']\
                    .map('{:,.2g}'.format)+' '
    quantities['units_string'] = quantities['units_string']\
                                .str.replace('\^1 ',' ').str.rstrip(' ')\
                                .str.rstrip('.0')
    quantities.loc[ quantities[ 'unitless_ratio' ] == 'yes', \
                  'units_string' ] = 'dimensionless'
                   
##############################################################################
#                                                                            #
#                       PRINT RELATED FUNCTIONS                              #
#                                                                            #
##############################################################################

# open the different RDF files, output header
def open_write_file(fileptr,rep):
    now = datetime.datetime.now()    
    fileptr.write( header.format(rep.lower(), rep.lower(), rep, rep) )
    fileptr.write( '##Last generated on: ' + now.strftime( "%Y-%m-%d %H:%M" ) )

# create building block (bb) file to output all of the relationships
# for core classes
def create_bb_file( vocab, ttl_file, classname, collabel, pref, label=None, \
                    wikifilename='wikipedia_page' ):
    if label:
        ttl_file.write( label )
    for index in vocab.index:
        if collabel+'_id' in vocab.columns.values:
            element = vocab.loc[ index, collabel + '_id' ]
        else:
            print ( 'ERROR: No ' + collabel + '_id column found!' )
            sys.exit(0)
        element_esc = urllib.quote(element)
        ttl_file.write( '\n' + prefix.format( pref, element_esc ) )
        ttl_file.write( declaration_instance.format( \
                        element_esc, 'svu', classname, ';' ) )
        if wikifilename in vocab.columns.values:
            attr = vocab.loc[ index, wikifilename]
            if attr != '':
                ttl_file.write( attribute.format( 'hasAssociatedWikipediaPage', \
                            '\"' + attr + '\"', ';'))
        if 'synonym' in vocab.columns.values:
            synonyms = vocab.loc[ index, 'synonym' ]
            if synonyms != '':
                synonyms = synonyms.split(', ')
                for syn in synonyms:
                    ttl_file.write( synonym.format(h.unescape(syn)))
        if collabel + '_taxonomic' in vocab.columns.values and \
            vocab.loc[ index, collabel + '_taxonomic' ] != '' :
            derivation = vocab.loc[ index, collabel + '_taxonomic' ]
            ttl_file.write( attribute.format( 'isDerivedFrom', \
                            ':' + urllib.quote( derivation ), ';' ) )
        if collabel == 'quantity':
            if vocab.loc[ index, 'property_taxonomic' ] != '' :
                if vocab.loc[ index, 'quantity_taxonomic' ] == '' :
                    derivation = vocab.loc[ index, 'property_taxonomic' ]
                    ttl_file.write( attribute.format( 'isDerivedFrom', \
                            ':' + urllib.quote( derivation ), ';' ) )
                else:
                    print('WARNING: ' + element + ' has both property and ' + \
                          'quantity derivation. Only quantity derivation ' + \
                          'written to file.' )
            if vocab.loc[ index, 'property_type' ] != '' :
                ptype = vocab.loc[ index, 'property_type' ]
                ttl_file.write( attribute.format( 'hasPropertyType', \
                            ':' + urllib.quote( ptype ), ';' ) )
            if vocab.loc[ index, 'property_role' ] != '' :
                prole = vocab.loc[ index, 'property_role' ]
                ttl_file.write( attribute.format( 'hasPropertyRole', \
                            ':' + urllib.quote( prole ), ';' ) )
            if vocab.loc[ index, 'property_quantification' ] != '' :
                pquant = vocab.loc[ index, 'property_quantification' ]
                ttl_file.write( attribute.format( 'hasPropertyQuantification', \
                            ':' + urllib.quote( pquant ), ';' ) )
            if vocab.loc[ index, 'quantity_taxonomic' ] == '' :
                    units = vocab.loc[ index, 'units_string' ]
                    ttl_file.write( attribute.format( 'hasUnits', \
                            '\"' + (units if units!='' else 'none') + \
                            '\"', ';' ) )
        if collabel + '_label' in vocab.columns.values:
            element = vocab.loc[ index, collabel + '_label' ]
        ttl_file.write( preflabel.format( element ) )
