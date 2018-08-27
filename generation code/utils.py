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
# Numpy for 'unique'
import numpy as np
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
            data = pd.read_csv( open(ext + filename,'rU'), encoding='utf-8', \
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

# Format operator information for futher processing
def preprocess_operator( operator, quantity ):    
    # Set non-values to 0 in units columns, reset units for ratios
    col = [ 'units', 'f_units' ]
    for i in operator.index:
        base_op = operator.loc[ i, 'operator_taxonomic' ]
        if base_op != '' :
            operator.loc[i, col] = operator.loc[ \
                        operator['operator_id'] == base_op, col].iloc[0]

    compound_operator_vocabulary = \
        extract_compound_operator_vocabulary( quantity['operator'] )
    compound_operator_vocabulary = set(np.unique(compound_operator_vocabulary))
    compound_operators = pd.DataFrame( \
                         { 'operator_id' : list(compound_operator_vocabulary) } )

    col = [ 'L', 'M', 'O', 'T', 'I', 'N', 'radian', 'number', 'currency' ]
    for c in col:
        compound_operators[c] = 0
    compound_operators['f_units'] = 0
    compound_operators['operator_label'] = compound_operators['operator_id'].copy()
    
    for i in compound_operators.index:
        op = compound_operators.loc[i,'operator_id']
        factor, L, T, O = calc_operator_units(op,operator)
        compound_operators.loc[i,'f_units'] = factor
        compound_operators.loc[i,'L']      = L
        compound_operators.loc[i,'O']      = O
        compound_operators.loc[i,'T']      = T
    create_unit_strings(compound_operators,label='units')
    determine_head_and_root(compound_operators)
    return compound_operators

def determine_head_and_root(operator):
    operator['head_operator_id'] = operator['operator_id' ].str.split('_of_',1)\
                                    .str[0]
    operator['operator_taxonomic'] = operator['operator_id' ].str.split('_of_',1)\
                                    .str[1]

# generate numeric unit exponents for operators
def calc_operator_units( operator, metadata ):
    ops = operator.split( '_of_' )
    factor = 1
    L = 0
    T = 0
    O = 0
    for op in ops[::-1]:
        if op == '':
            continue
        fact = metadata.loc[metadata['operator_label']==op,'f_units'].iloc[0]
        factor *= fact
        L *= fact
        T *= fact
        O *= fact
        units = metadata.loc[metadata['operator_label']==op,'units'].iloc[0]
        if units=='L':
            L += 1
        elif 'L^-1' in units:
            L += -1
        elif 'L^-2' in units:
            L += -2
        elif units=='T':
            T += 1
        elif 'T^-1' in units:
            T += -1
        elif units=='O':
            O += 1
        elif units=='O^-1':
            O += -1
    return factor, L, T, O   

# calculate unit exponents of a quantity with an operator applied
def calc_full_quantity_units( quantity ):
    L = quantity['L']*quantity['op factor']+quantity['op L']
    M = quantity['M']*quantity['op factor']
    O = quantity['O']*quantity['op factor']+quantity['op O']
    T = quantity['T']*quantity['op factor']+quantity['op T']
    I = quantity['I']*quantity['op factor']
    N = quantity['N']*quantity['op factor']
    return [L,M,O,T,I,N]
            
# use root_quantity columne to assign units to modified quantities    
def assign_units( quantity, operator_quantity, operator ):
    dim = [ 'L', 'M', 'O', 'T', 'I', 'N']
    for i in quantity.index:
        if quantity.loc[i,'root_quantity'] != '':
            quantity.loc[i,dim[0]] = quantity.loc[ \
                        (quantity['quantity_id']==quantity.loc[i,'root_quantity']), \
                        dim[0]].iloc[0]

    for i in dim:
        operator_quantity[i]=0
    operator_quantity['op factor']=1
    for i in operator_quantity.index:
        if operator_quantity.loc[i,'operator'] != '':
            operator_quantity.loc[ i, dim ] = quantity.loc[ \
                        ( quantity['quantity_id'] == \
                          operator_quantity.loc[i,'quantity_taxonomic'] ), dim ]\
                         .iloc[0]
            factor, L, T, O = calc_operator_units( operator_quantity.loc[i,'operator'], \
                                                   operator )
            operator_quantity.loc[ i, 'op factor' ] = factor
            operator_quantity.loc[ i, 'op L' ]      = L
            operator_quantity.loc[ i, 'op O' ]      = O
            operator_quantity.loc[ i, 'op T' ]      = T
            operator_quantity.loc[ i, dim ] = calc_full_quantity_units( \
                                              operator_quantity.loc[[i]].iloc[0] )
                        
# create strings to represent units;
# general form, L^# M^# O^# T^# I^# N^#
def create_unit_strings(quantities,label='units_string'):
    quantities[label] = ''
    quantities.loc[ quantities['L'] != 0, label ] += \
                    'L^' + quantities.loc[quantities['L']!=0,'L']\
                    .map('{:,.2g}'.format) + ' '
    quantities.loc[ quantities['M'] != 0, label ] += \
                    'M^' + quantities.loc[quantities['M']!=0,'M']\
                    .map('{:,.2g}'.format)+' '
    quantities.loc[ quantities['O'] != 0, label ] += \
                    'O^' + quantities.loc[quantities['O']!=0,'O']\
                    .map('{:,.2g}'.format)+' '
    quantities.loc[ quantities['T'] != 0, label ] += \
                    'T^' + quantities.loc[quantities['T']!=0,'T']\
                    .map('{:,.2g}'.format)+' '
    quantities.loc[ quantities['I'] != 0, label ] += \
                    'I^' + quantities.loc[quantities['I']!=0,'I']\
                    .map('{:,.2g}'.format)+' '
    quantities.loc[ quantities['N'] != 0, label ] += \
                    'N^' + quantities.loc[quantities['N']!=0,'N']\
                    .map('{:,.2g}'.format)+' '
    quantities[label] = quantities[label]\
                                .str.replace('\^1 ',' ').str.rstrip(' ')\
                                .str.rstrip('.0')
    if 'unitless_ratio' in quantities.columns.values:
        quantities.loc[ quantities[ 'unitless_ratio' ] == 'yes', \
                  label ] = 'dimensionless'

# get all combinations of compound operators (recursive function)
def extract_compound_operator_vocabulary(data):
    if data.empty:
        return pd.Series()
    vocabulary = data[data.str.contains('_of_')]
    return vocabulary.append( extract_compound_operator_vocabulary( \
                      data[ data.str.contains('_of_') ].str.split('_of_',1)\
                      .str[1] ) )
                   
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
                    wikifilename='wikipedia_page', process_vocab = None ):
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
        if 'plural_of' in vocab.columns.values:
            attr = vocab.loc[ index, 'plural_of']
            if attr != '':
                ttl_file.write( plurality.format( urllib.quote(attr)))
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
            if 'process_quantity' in vocab.columns.values:
                pquant = vocab.loc[ index, 'process_quantity' ]
                if pquant != '':
                    process2 = ''
                    if 'process2' in pquant:
                        process2 = vocab.loc[ index, 'quantity_id' ]\
                            .replace(pquant.split('process2')[0],'')\
                            .replace(pquant.split('process2')[1],'')\
                            .split('_')[1]
                        try:
                            process_id = process_vocab.loc[ \
                                process_vocab['process_nominalization']\
                                == process2, 'process_id'].iloc[0]
                        except:
                            try:
                                process_id = process_vocab.loc[ \
                                    process_vocab['process_nominalization']\
                                    .str.contains(process2+','), 'process_id'].iloc[0]
                            except:
                                process_id = process_vocab.loc[ \
                                    process_vocab['process_nominalization']\
                                    .str.contains(' '+process2), 'process_id'].iloc[0]
                        ttl_file.write( attribute.format( 'quantifiesProcess', \
                            '<process#' + urllib.quote( process_id ) + '>', \
                            ';' ) )
                        pquant = pquant.replace('process2','').replace('__','_')
                    process = vocab.loc[ index, 'quantity_id' ]\
                        .replace(pquant.split('process')[0],'')\
                        .replace(pquant.split('process')[1],'')\
                        .split('_')[0]
                    try:
                        process_id = process_vocab.loc[ \
                            process_vocab['process_nominalization'] == process, \
                            'process_id'].iloc[0]
                    except:
                        try:
                            process_id = process_vocab.loc[ \
                                process_vocab['process_nominalization']\
                                .str.contains(process+','), 'process_id']\
                                .iloc[0]
                        except:
                            process_id = process_vocab.loc[ \
                                process_vocab['process_nominalization']\
                                .str.contains(' '+process), 'process_id']\
                                .iloc[0]
                    ttl_file.write( attribute.format( 'quantifiesProcess', \
                        '<process#' + urllib.quote( process_id ) + '>', \
                        ';' ) )
        if collabel == 'operator':
            if vocab.loc[ index, 'operator_taxonomic' ] == '' :
                units = vocab.loc[ index, 'units' ]
                ttl_file.write( attribute.format( 'hasMultiplierUnits', \
                            '\"' + units + '\"', ';' ) )
                units = vocab.loc[ index, 'f_units' ]
                ttl_file.write( attribute.format( 'hasPowerUnits', \
                            str(units), ';' ) )
            if 'head_operator_id' in vocab.columns.values:
                hop = vocab.loc[ index, 'head_operator_id' ]
                ttl_file.write( attribute.format( 'hasHeadOperator', ':' + hop, ';' ))
        if collabel == 'operator_quantity':
            if vocab.loc[ index, 'operator' ] != '' :
                derivation = vocab.loc[ index, 'quantity_taxonomic' ]
                ttl_file.write( attribute.format( 'isDerivedFrom', \
                            ':' + urllib.quote( derivation ), ';' ) )
                units = vocab.loc[ index, 'units_string' ]
                ttl_file.write( attribute.format( 'hasUnits', \
                            '\"' + units + '\"', ';' ) )
                op = vocab.loc[ index, 'operator' ]
                ttl_file.write( attribute.format( 'hasOperator', \
                            '<operator#' + urllib.quote( op )+'>', ';' ) )
        if collabel == 'attribute':
            if vocab.loc[ index, 'property_id' ] != '' :
                prop = vocab.loc[ index, 'property_id' ]
                ttl_file.write( attribute.format( 'hasProperty', \
                            '<property#' + urllib.quote( prop )+'>', ';' ) )
            if vocab.loc[ index, 'value' ] != '' :
                value = vocab.loc[ index, 'value' ]
                ttl_file.write( attribute.format( 'hasValue', \
                            '\"' + value + '\"', ';' ) )
            if 'canonical_unit' in vocab.columns.values and \
                ( vocab.loc[ index, 'canonical_unit' ] != '' ):
                unit = vocab.loc[ index, 'canonical_unit' ]
                ttl_file.write( attribute.format( 'hasUnits', \
                            '\"' + unit + '\"', ';' ) )
            if 'unit' in vocab.columns.values and \
                vocab.loc[ index, 'unit' ] != '' :
                unit = vocab.loc[ index, 'unit' ]
                ttl_file.write( attribute.format( 'hasAsignedUnits', \
                            '\"' + unit + '\"', ';' ) )
            if 'noun' in vocab.columns.values and \
                ( vocab.loc[ index, 'noun' ] == 'noun' ):
                ttl_file.write( attribute.format( 'isNoun', \
                            'true', ';' ) )
            else:
                ttl_file.write( attribute.format( 'isNoun', \
                            'false', ';' ) )
        if collabel == 'matter':
            if vocab.loc[ index, 'matter_type' ] != '' :
                mtype = vocab.loc[ index, 'matter_type' ]
                ttl_file.write( attribute.format( 'hasType', \
                            ':' + urllib.quote( mtype ), ';' ) )
        if collabel in ['trajectory','matter','body'] and \
            'attribute' in vocab.columns.values:
            if vocab.loc[ index, 'attribute' ] != '' :
                attr = vocab.loc[ index, 'attribute' ]
                ttl_file.write( attribute.format( 'hasAttribute', \
                            '<attribute#' + urllib.quote( attr )+'>', ';' ) )
        if collabel + '_label' in vocab.columns.values:
            element = vocab.loc[ index, collabel + '_label' ]
        if 'process_present_participle' in vocab.columns.values:
            attr = vocab.loc[ index, 'process_present_participle']
            if attr != '':
                ttl_file.write( attribute.format( 'hasPresentParticiple', \
                                              '\"' + h.unescape(attr) + '\"', ';'))
        if 'process_nominalization' in vocab.columns.values:
            attr = vocab.loc[ index, 'process_nominalization']
            if attr != '':
                ttl_file.write( attribute.format( 'hasNominalization', \
                                              '\"' + h.unescape(attr) + '\"', ';'))
        ttl_file.write( preflabel.format( element ) )
