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
declaration_classname   = '\t\t\trdf:type svu:{} {}\n'

attribute     = '\t\t\tsvu:{} {} {}\n'
synonym       = '\t\t\tskos:altLabel "{}"@en ;\n'
plurality       = '\t\t\tsvu:isPluralityOf :{} ;\n'
preflabel     = '\t\t\tskos:prefLabel "{}"@en .\n'
comment       = '\t\t\trdfs:comment {} {}\n'

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
    operator['root_operator_id'] = operator['operator_id' ].str.split('_of_',1)\
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
                    wikifilename='wikipedia_page', part = False, \
                    process_vocab = None ):
    #Print out comment lable for section, if provided
    if label:
        ttl_file.write( label )
        
    # run through each row of vocabulary
    for index in vocab.index:
        
        #two types of input files, all manually created files have label_id
        # column, while automatically generated files have participant cols
        if collabel+'_id' in vocab.columns.values:
            element = vocab.loc[ index, collabel + '_id' ]
        elif 'participant' in vocab.columns.values:
            
            cat = collabel.replace('participant','role')
            if '_' in vocab.loc[ index, 'participant' ]:
                element = '('+vocab.loc[ index, 'participant' ]+')@'+cat+'~'+\
                    vocab.loc[ index, 'participantrel' ]
            else:
                element = vocab.loc[ index, 'participant' ]+'@'+cat+'~'+\
                    vocab.loc[ index, 'participantrel' ]
        else:
            print ( 'ERROR: No ' + collabel + '_id column found!' )
            sys.exit(0)
            
        #initial declaration    
        element_esc = urllib.quote(element)
        ttl_file.write( '\n' + prefix.format( pref, element_esc ) )
        ttl_file.write( declaration_instance.format( \
                        element_esc, 'svu', classname, ';' ) )
        
        # if it is a part, then declare it a Part class
        if part:
            ttl_file.write( declaration_classname.format( \
                        'Part', ';' ) )
            
        # determine standardized vs quantitative    
        if 'type' in vocab.columns.values:
            cat = vocab.loc[ index, 'type']
            if cat in ['standardized','quantitative']:
                ttl_file.write( declaration_classname.format( \
                        cat.capitalize()+classname, ';' ) )
            elif cat == 'quantification':
                ttl_file.write( declaration_classname.format( \
                        'PropertyQuantification', ';' ) )
                
        # spatial, temporal, etc relationship class        
        if 'relationship_type' in vocab.columns.values:
            types = vocab.loc[ index, 'relationship_type']
            if types != '':
                for t in types.split(', '):
                    ttl_file.write( declaration_classname.format( \
                        t.capitalize()+'Relationship', ';' ) )
                    
        # print wikipedia page, if there is one
        if wikifilename in vocab.columns.values:
            attr = vocab.loc[ index, wikifilename]
            if attr != '':
                ttl_file.write( attribute.format( 'hasAssociatedWikipediaPage', \
                            '\"' + attr + '\"', ';'))
        
        #print synonyms if present
        if 'synonym' in vocab.columns.values:
            synonyms = vocab.loc[ index, 'synonym' ]
            if synonyms != '':
                synonyms = synonyms.split(', ')
                for syn in synonyms:
                    ttl_file.write( synonym.format(h.unescape(syn)))
                    
        # link to singular form, if present
        if 'plural_of' in vocab.columns.values:
            attr = vocab.loc[ index, 'plural_of']
            if attr != '':
                ttl_file.write( plurality.format( urllib.quote(attr)))
                
        # print what element is derived from, if present
        if collabel + '_taxonomic' in vocab.columns.values and \
            vocab.loc[ index, collabel + '_taxonomic' ] != '' :
            for derivation in vocab.loc[ index, collabel + '_taxonomic' ].split(', '):
                ttl_file.write( attribute.format( 'isTypeOf', \
                            ':' + urllib.quote( derivation ), ';' ) )
                
        # compound operatory properties
        if 'root_operator_id' in vocab.columns.values and \
            vocab.loc[ index, 'root_operator_id' ] != '' :
            for derivation in vocab.loc[ index, 'root_operator_id' ].split(', '):
                ttl_file.write( attribute.format( 'hasRootOperator', \
                            ':' + urllib.quote( derivation ), ';' ) )
                
        # for quantities, ... print
        if collabel == 'quantity':
            
            #property from which it is derived
            if vocab.loc[ index, 'property_taxonomic' ] != '' :
                if vocab.loc[ index, 'quantity_taxonomic' ] == '' :
                    derivation = vocab.loc[ index, 'property_taxonomic' ]
                    ttl_file.write( attribute.format( 'isTypeOf', \
                            ':' + urllib.quote( derivation ), ';' ) )
                else:
                    print('WARNING: ' + element + ' has both property and ' + \
                          'quantity derivation. Only quantity derivation ' + \
                          'written to file.' )
            
            # property type, property role, property quantification, units
            if vocab.loc[ index, 'property_type' ] != '' :
                ptype = vocab.loc[ index, 'property_type' ]
                ttl_file.write( attribute.format( 'hasPropertyType', \
                            ':' + urllib.quote( ptype ), ';' ) )
            if vocab.loc[ index, 'property_role' ] != '' :
                prole = vocab.loc[ index, 'property_role' ]
                ttl_file.write( attribute.format( 'hasPropertyRole', \
                            '<role#' + urllib.quote( prole ) +'>', ';' ) )
            if vocab.loc[ index, 'property_quantification' ] != '' :
                pquant = vocab.loc[ index, 'property_quantification' ]
                ttl_file.write( attribute.format( 'hasPropertyQuantification', \
                            ':' + urllib.quote( pquant ), ';' ) )
            if vocab.loc[ index, 'quantity_taxonomic' ] == '' :
                units = vocab.loc[ index, 'units_string' ]
                ttl_file.write( attribute.format( 'hasUnits', \
                            '\"' + (units if units!='' else 'none') + \
                            '\"', ';' ) )
            
            #find relevant processes and write to file
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
                            process_vocab['process_id'] == process, \
                            'process_id'].iloc[0]
                    except:
                        try:
                            process_id = process_vocab.loc[ \
                                process_vocab['process_verb']==process, \
                                'process_id']\
                                .iloc[0]
                        except:
                            print(process)
                            process_id = 'none'
                    ttl_file.write( attribute.format( 'quantifiesProcess', \
                        '<process#' + urllib.quote( process_id ) + '>', \
                        ';' ) )
                    
        # operator information written
        if collabel == 'operator':
            if ('operator_taxonomic' in vocab.columns.values and \
                (vocab.loc[ index, 'operator_taxonomic' ] == '')) or \
                'root_operator_id' in vocab.columns.values:
                units = vocab.loc[ index, 'units' ]
                if units != '':
                    ttl_file.write( attribute.format( 'hasMultiplierUnits', \
                            '\"' + units + '\"', ';' ) )
                else:
                    ttl_file.write( attribute.format( 'hasMultiplierUnits', \
                            '\"none\"', ';' ) )
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
                            '\"' + (units if units!='' else 'none') + \
                            '\"', ';' ) )
                op = vocab.loc[ index, 'operator' ]
                ttl_file.write( attribute.format( 'hasOperator', \
                            '<operator#' + urllib.quote( op )+'>', ';' ) )
                            
        #attribute relationships                    
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
                
        #matter relationships
        if collabel == 'matter':
            if vocab.loc[ index, 'expressed-as' ] != '' :
                mtype = vocab.loc[ index, 'expressed-as' ]
                ttl_file.write( attribute.format( 'isExpressedAs', \
                            ':' + urllib.quote( mtype ), ';' ) )
                
        # phenomenon
        if collabel == 'phenomenon':
            if 'associated_process' in vocab.columns.values and\
                vocab.loc[ index, 'associated_process' ] != '' :
                process = vocab.loc[ index, 'associated_process' ].split(', ')
                for p in process:
                    ttl_file.write( attribute.format( 'hasAssociatedProcess', \
                            '<process#' + urllib.quote( p )+'>', ';' ) )
            if 'process' in vocab.columns.values and \
                vocab.loc[ index, 'process' ] != '' :
                process = vocab.loc[ index, 'process' ].split(', ')
                for p in process:
                    ttl_file.write( attribute.format( 'hasProcess', \
                        '<process#' + urllib.quote( p )+'>', ';' ) )
            if 'body' in vocab.columns.values and \
                vocab.loc[ index, 'body' ] != '' :
                body = vocab.loc[ index, 'body' ]
                ttl_file.write( attribute.format( 'hasBody', \
                        '<body#' + urllib.quote( body )+'>', ';' ) )
            if 'matter' in vocab.columns.values and \
                vocab.loc[ index, 'matter' ] != '' :
                matter = vocab.loc[ index, 'matter' ]
                ttl_file.write( attribute.format( 'hasMatter', \
                        '<matter#' + urllib.quote( matter )+'>', ';' ) )
            if 'part' in vocab.columns.values and \
                vocab.loc[ index, 'part' ] != '' :
                part = vocab.loc[ index, 'part' ]
                ttl_file.write( attribute.format( 'hasPart', \
                        ':' + urllib.quote( part ), ';' ) )
            if 'phenomenon' in vocab.columns.values and \
                vocab.loc[ index, 'phenomenon' ] != '' :
                phen = vocab.loc[ index, 'phenomenon' ]
                ttl_file.write( attribute.format( 'hasPhenomenon', \
                        ':' + urllib.quote( phen ), ';' ) )
            if 'participant1' in vocab.columns.values:
                for i in range(1,5):
                    participant = 'participant'+str(i)
                    if vocab.loc[ index, participant ] != '' :
                        phen = vocab.loc[ index, participant ]
                        category = vocab.loc[ index, participant + 'cat']
                        if category == 'context':
                            if '_' in phen:
                                context = '('+phen+')@context~'+\
                                    vocab.loc[ index, participant + 'cattype']
                            else:
                                context = phen +'@context~'+\
                                    vocab.loc[ index, participant + 'cattype']
                            ttl_file.write( attribute.format( 'hasContext', \
                                '<context#' + urllib.quote( context ) + '>', ';' ) )
                        if category == 'medium':
                            medium = phen
                            pref_opt = vocab.loc[ index, participant+'class' ]\
                                .split(', ')
                            if 'phenomenon' in pref_opt:
                                pref = 'phenomenon'
                            elif 'body' in pref_opt:
                                pref = 'body'
                            elif 'matter' in pref_opt:
                                pref = 'matter'
                            elif 'form' in pref_opt:
                                pref = 'form'
                            elif 'abstraction' in pref_opt:
                                pref = 'abstraction'
                            elif pref_opt == ['']:
                                pref = 'phenomenon'
                            else:
                                pref = 'phenomenon'
                                print('Warning, class not found: '+phen, pref_opt)
                            ttl_file.write( attribute.format( 'hasMediumObject', \
                                '<'+pref+'#' + urllib.quote( medium ) + '>', ';' ) )
                        if category == 'role':
                            if '_' in phen:
                                p = '('+phen+')@role~'+\
                                    vocab.loc[ index, participant + 'cattype']
                            else:
                                p = phen+'@role~'+\
                                    vocab.loc[ index, participant + 'cattype']
                            ttl_file.write( attribute.format( 'hasParticipantObject', \
                                '<participant#' + urllib.quote( p ) + '>', ';' ) )
                        if category == 'reference':
                            if '_' in phen:
                                reference = '('+phen+')@reference~'+\
                                    vocab.loc[ index, participant + 'cattype']
                            else:
                                reference = phen+'@reference~'+\
                                    vocab.loc[ index, participant + 'cattype']
                            ttl_file.write( attribute.format( 'hasReference', \
                                '<reference#' + urllib.quote( reference ) + '>', ';' ) )
                        if category == '':
                            pref_opt = vocab.loc[ index, participant+'class' ]\
                                .split(', ')
                            if 'Context' in classname:
                                if 'phenomenon' in pref_opt:
                                    pref = 'phenomenon'
                                elif 'body' in pref_opt:
                                    pref = 'body'
                                elif 'matter' in pref_opt:
                                    pref = 'matter'
                                elif 'form' in pref_opt:
                                    pref = 'form'
                                elif 'abstraction' in pref_opt:
                                    pref = 'abstraction'
                                elif pref_opt == ['']:
                                    pref = 'phenomenon'
                                else:
                                    pref = 'phenomenon'
                                    print('Warning, class not found: '+phen, pref_opt)
                                ttl_file.write( attribute.format( 'hasObject', \
                                    '<' + pref + '#' + urllib.quote( phen ) + '>', ';' ) )
                            if 'Medium' in classname:
                                rel = 'hasObject'
                                if 'phenomenon' in pref_opt:
                                    pref = 'phenomenon'
                                elif 'body' in pref_opt:
                                    pref = 'body'
                                elif 'matter' in pref_opt:
                                    pref = 'matter'
                                elif 'form' in pref_opt:
                                    pref = 'form'
                                elif 'abstraction' in pref_opt:
                                    pref = 'abstraction'
                                elif pref_opt == ['']:
                                    pref = 'phenomenon'
                                elif 'attribute' in pref_opt:
                                    pref = 'attribute'
                                    rel = 'hasAttribute'
                                elif 'process' in pref_opt:
                                    pref = 'process'
                                    rel = 'hasProcess'    
                                else:
                                    pref = 'phenomenon'
                                    print('Warning, class not found: '+phen, pref_opt)
                                ttl_file.write( attribute.format( rel, \
                                    '<' + pref + '#' + urllib.quote( phen ) + '>', ';' ) )
                            if 'Reference' in classname:
                                if 'phenomenon' in pref_opt:
                                    pref = 'phenomenon'
                                elif 'body' in pref_opt:
                                    pref = 'body'
                                elif 'matter' in pref_opt:
                                    pref = 'matter'
                                elif 'form' in pref_opt:
                                    pref = 'form'
                                elif 'abstraction' in pref_opt:
                                    pref = 'abstraction'
                                elif pref_opt == ['']:
                                    pref = 'phenomenon'
                                else:
                                    pref = 'phenomenon'
                                    print('Warning, class not found: '+phen, pref_opt)
                                ttl_file.write( attribute.format( 'hasObject', \
                                    '<' + pref + '#' + urllib.quote( phen ) + '>', ';' ) )
                            if 'Compound' in classname:
                                rel = 'hasObject'
                                if 'phenomenon' in pref_opt:
                                    pref = 'phenomenon'
                                elif 'body' in pref_opt:
                                    pref = 'body'
                                elif 'matter' in pref_opt:
                                    pref = 'matter'
                                elif 'form' in pref_opt:
                                    pref = 'form'
                                elif 'abstraction' in pref_opt:
                                    pref = 'abstraction'
                                elif pref_opt == ['']:
                                    pref = 'phenomenon'
                                elif 'attribute' in pref_opt:
                                    pref = 'attribute'
                                    rel = 'hasAttribute'
                                elif 'process' in pref_opt:
                                    pref = 'process'
                                    rel = 'hasProcess'    
                                else:
                                    pref = 'phenomenon'
                                    print('Warning, class not found: '+phen, pref_opt)
                                ttl_file.write( attribute.format( rel, \
                                    '<' + pref + '#' + urllib.quote( phen ) + '>', ';' ) )

            if 'trajectory' in vocab.columns.values and \
                vocab.loc[ index, 'trajectory' ] != '' :
                trajectory = vocab.loc[ index, 'trajectory' ]
                ttl_file.write( attribute.format( 'hasTrajectory', \
                        '<trajectory#' + urllib.quote( trajectory )+'>', ';' ) )
            if 'trajectory_direction' in vocab.columns.values and \
                vocab.loc[ index, 'trajectory_direction' ] != '' :
                direction = vocab.loc[ index, 'trajectory_direction' ]
                for d in direction.split(', '):
                    ttl_file.write( attribute.format( 'hasTrajectoryDirection', \
                        '<trajectorydirection#' + urllib.quote( d )+'>', ';' ) )
        if (collabel == 'context') or (collabel == 'reference') or (collabel == 'participant'):
            rel = vocab.loc[ index, 'participantrel' ]
            rel_pref = 'relationship'
            if collabel == 'context':
                rel_label = 'hasContextRelationship'
            elif collabel == 'reference':
                rel_label = 'hasReferenceRelationship'
            elif collabel == 'participant':
                rel_label = 'hasParticipantRole'
                rel_pref = 'role'
            else:
                print('How did I get here?? ' + collabel)
            ttl_file.write( attribute.format( rel_label, \
                '<'+rel_pref+'#' + urllib.quote( rel )+'>', ';' ) )
            phen = vocab.loc[ index, 'participant' ]
            pref_opt = vocab.loc[ index, 'participantclass' ].split(', ')
            if 'phenomenon' in pref_opt:
                pref = 'phenomenon'
            elif 'body' in pref_opt:
                pref = 'body'
            elif 'matter' in pref_opt:
                pref = 'matter'
            elif 'form' in pref_opt:
                pref = 'form'
            elif 'abstraction' in pref_opt:
                pref = 'abstraction'
            elif pref_opt == ['']:
                pref = 'phenomenon'
            else:
                print('Warning, class not found: '+phen, pref_opt)
            count = 0;
            if 'phenomenon' in pref_opt:
                count+=1
            if 'body' in pref_opt:
                count += 1
            if 'matter' in pref_opt:
                count += 1
            if count > 1:
                print('Warning, multiple classed found: '+phen)
            ttl_file.write( attribute.format( 'hasObject', \
                '<'+pref+'#' + urllib.quote( phen )+'>', ';' ) )
        if collabel in ['abstraction']:
            if 'abstraction_applied' in vocab.columns.values and \
                vocab.loc[ index, 'abstraction_applied' ] != '' :
                abst = vocab.loc[ index, 'abstraction_applied' ]
                ttl_file.write( attribute.format( 'abstracts', \
                        ':' + urllib.quote( abst ), ';' ) )
            if 'abstraction' in vocab.columns.values and \
                vocab.loc[ index, 'abstraction' ] != '' :
                abst = vocab.loc[ index, 'abstraction' ]
                ttl_file.write( attribute.format( 'hasAbstraction', \
                        ':' + urllib.quote( abst ), ';' ) )
        if collabel == 'abstraction':
            if 'body' in vocab.columns.values and \
                vocab.loc[ index, 'body' ] != '' :
                body = vocab.loc[ index, 'body' ]
                ttl_file.write( attribute.format( 'abstracts', \
                        '<body#' + urllib.quote( body )+'>', ';' ) )
            if 'process' in vocab.columns.values and \
                vocab.loc[ index, 'process' ] != '' :
                process = vocab.loc[ index, 'process' ].split(', ')
                for p in process:
                    ttl_file.write( attribute.format( 'undergoesProcess', \
                        '<process#' + urllib.quote( p )+'>', ';' ) )
            if 'associated_process' in vocab.columns.values and \
                vocab.loc[ index, 'associated_process' ] != '' :
                process = vocab.loc[ index, 'associated_process' ].split(', ')
                for p in process:
                    ttl_file.write( attribute.format( 'hasAssociatedProcess', \
                        '<process#' + urllib.quote( p )+'>', ';' ) )
        if collabel == 'participant':
            if 'phenomenon' in vocab.columns.values and \
                vocab.loc[ index, 'phenomenon' ] != '' :
                phen = vocab.loc[ index, 'phenomenon' ]
                pref = vocab.loc[ index, 'phenomenon_pref' ]
                ttl_file.write( attribute.format( 'hasPhenomenon', \
                        '<'+pref+'#' + urllib.quote( phen )+'>', ';' ) )
            if 'role' in vocab.columns.values and \
                vocab.loc[ index, 'role' ] != '' :
                role = vocab.loc[ index, 'role' ]
                ttl_file.write( attribute.format( 'hasParticipantRole', \
                        '<role#' + urllib.quote( role )+'>', ';' ) )
        if collabel in ['trajectory','matter','body','abstraction','phenomenon','process'] and \
            'attribute' in vocab.columns.values:
            if vocab.loc[ index, 'attribute' ] != '' :
                attr = vocab.loc[ index, 'attribute' ].split(', ')
                for a in attr:
                    ttl_file.write( attribute.format( 'hasAttribute', \
                            '<attribute#' + urllib.quote( a )+'>', ';' ) )
        if collabel in ['body','phenomenon'] and \
            'role' in vocab.columns.values:
            if vocab.loc[ index, 'role' ] != '' :
                attr = vocab.loc[ index, 'role' ].split(', ')
                for a in attr:
                    ttl_file.write( attribute.format( 'hasRole', \
                            '<role#' + urllib.quote( a )+'>', ';' ) )
        if collabel in ['body','phenomenon'] and \
            'form' in vocab.columns.values:
            if vocab.loc[ index, 'form' ] != '' :
                attr = vocab.loc[ index, 'form' ].split(', ')
                for a in attr:
                    ttl_file.write( attribute.format( 'hasForm', \
                            '<form#' + urllib.quote( a )+'>', ';' ) )
        if collabel in ['body'] and \
            'part' in vocab.columns.values:
            if vocab.loc[ index, 'part' ] != '' :
                attr = vocab.loc[ index, 'part' ].split(', ')
                for a in attr:
                    ttl_file.write( attribute.format( 'hasPart', \
                            '<part#' + urllib.quote( a )+'>', ';' ) )
        if collabel in ['body'] and \
            'body_part' in vocab.columns.values:
            if vocab.loc[ index, 'body_part' ] != '' :
                attr = vocab.loc[ index, 'body_part' ].split(', ')
                for a in attr:
                    ttl_file.write( attribute.format( 'hasPart', \
                            ':' + urllib.quote( a ), ';' ) )
        if collabel in ['body'] and \
            'body' in vocab.columns.values:
            if vocab.loc[ index, 'body' ] != '' :
                attr = vocab.loc[ index, 'body' ].split(', ')
                for a in attr:
                    ttl_file.write( attribute.format( 'hasBody', \
                            ':' + urllib.quote( a ), ';' ) )
        if collabel in ['body'] and \
            'matter' in vocab.columns.values:
            if vocab.loc[ index, 'matter' ] != '' :
                attr = vocab.loc[ index, 'matter' ].split(', ')
                for a in attr:
                    ttl_file.write( attribute.format( 'hasMatter', \
                            '<matter#' + urllib.quote( a )+'>', ';' ) )
        if collabel + '_label' in vocab.columns.values:
            element = vocab.loc[ index, collabel + '_label' ]
        if 'process_verb' in vocab.columns.values:
            attr = vocab.loc[ index, 'process_verb']
            if attr!= '':
                for a in attr.split(', '):
                    ttl_file.write( attribute.format( 'hasPresentTense', \
                                              '\"' + h.unescape(a) + '\"', ';'))
        if 'process_present_participle' in vocab.columns.values:
            attr = vocab.loc[ index, 'process_present_participle']
            if attr!= '':
                for a in attr.split(', '):
                    ttl_file.write( attribute.format( 'hasPresentParticiple', \
                                              '\"' + h.unescape(a) + '\"', ';'))
        if 'process_nominalization' in vocab.columns.values:
            attr = vocab.loc[ index, 'process_nominalization']
            if attr!= '':
                for a in attr.split(', '):
                    ttl_file.write( attribute.format( 'hasNominalization', \
                                              '\"' + h.unescape(a) + '\"', ';'))
        if 'comment' in vocab.columns.values:
            attr = vocab.loc[ index, 'comment']
            if attr!= '':
                ttl_file.write( comment.format(  \
                    '\"' + h.unescape(attr) + '\"', ';'))
        ttl_file.write( preflabel.format( element ) )

# create variable file 
def create_variable_entries( vocab, ttl_file, label=None ):
    if label:
        ttl_file.write( label )
    for index in vocab.index:
        element = vocab.loc[ index, 'variable_label' ]
        element_esc = urllib.quote(element)
        ttl_file.write( '\n' + prefix.format( 'variable', element_esc ) )
        ttl_file.write( declaration_instance.format( \
                        element_esc, 'svu', 'Variable', ';' ) )
        quantity = vocab.loc[ index, 'quantity_id']
        if quantity != '':
            ttl_file.write( attribute.format( 'hasProperty', \
                            '<property#' + urllib.quote(quantity) + '>', ';'))
        obj = vocab.loc[ index, 'object_id']
        pref = vocab.loc[ index, 'object_pref']
        cat = vocab.loc[ index, 'object_cat']
        if obj != '':
            if (cat=='root') and (pref != 'abstraction'):
                ttl_file.write( attribute.format( 'hasRootObject', \
                            '<'+pref+'#' + urllib.quote(obj) + '>', ';'))
            elif pref == 'abstraction':
                ttl_file.write( attribute.format( 'hasAbstractedObject', \
                            '<'+pref+'#' + urllib.quote(obj) + '>', ';'))
            else:
                ttl_file.write( attribute.format( 'hasObject', \
                            '<'+pref+'#' + urllib.quote(obj) + '>', ';'))
        ttl_file.write( preflabel.format( element ) )