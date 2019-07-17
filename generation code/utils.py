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
header = ( '@prefix : <http://www.geoscienceontology.org/svo/svl/{}#> .\n'
           '@prefix svu: <http://www.geoscienceontology.org/svo/svu#> .\n'
           '@prefix owl: <http://www.w3.org/2002/07/owl#> .\n'
           '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
           '@prefix xml: <http://www.w3.org/XML/1998/namespace> .\n'
           '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n'
           '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n'
           '@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n'
           '@base <http://www.geoscienceontology.org/svo/svl/> .\n'
           '\n'
           '<http://www.geoscienceontology.org/svo/svl/{}> rdf:type owl:Ontology ;\n'
           '\t\t\t\towl:versionIRI <http://www.geoscienceontology.org/svo/svl/{}/1.0.0> ;\n'
           '\t\t\t\trdfs:comment " Scientific Variables Lower Ontology, {} '
           'BETA VERSION 1.0.0" .\n'
           '#\t\t\t\towl:imports <http://www.geoscienceontology.org/svo/svu/1.0.0> .\n'
           '\n\n'
           '#################################################################\n'
           '#    {}   \n'
           '# \n'
           '#################################################################\n' )

# other ttl components
prefix        = '###  http://www.geoscienceontology.org/svo/svl/{}#{}\n'
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
    if 'unitless_ratio' in quantity.columns.values:
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
        factor, L, T, O, rad = calc_operator_units(op,operator)
        compound_operators.loc[i,'f_units'] = factor
        compound_operators.loc[i,'L']      = L
        compound_operators.loc[i,'O']      = O
        compound_operators.loc[i,'T']      = T
        compound_operators.loc[i,'radian'] = rad
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
    rad = 0
    for op in ops[::-1]:
        if op == '':
            continue
        try:
            fact = metadata.loc[metadata['operator_id']==op,'f_units'].iloc[0]
        except:
            print('WARNING! ', op ,' operator not found!')
            continue
        factor *= fact
        L *= fact
        T *= fact
        O *= fact
        units = metadata.loc[metadata['operator_id']==op,'units'].iloc[0]
        if 'L^' in units:
            temp = int(units.split('L^')[1].split(' ')[0])
            L += temp
        elif 'L' in units:
            L += 1
        if 'T^' in units:
            temp = int(units.split('T^')[1].split(' ')[0])
            T += temp
        elif 'T' in units:
            T += 1
        if 'O^' in units:
            temp = int(units.split('O^')[1].split(' ')[0])
            O += temp
        elif 'O' in units:
            O += 1
        if 'rad' in units:
            rad = 1
    return factor, L, T, O, rad

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
            quantity.loc[i,dim] = quantity.loc[ \
                        (quantity['quantity_id']==quantity.loc[i,'root_quantity']), \
                        dim].iloc[0]

    for i in dim:
        operator_quantity[i]=0
    operator_quantity['op factor']=1
    for i in operator_quantity.index:
        if operator_quantity.loc[i,'operator'] != '':
            try:
                operator_quantity.loc[ i, dim ] = quantity.loc[ \
                        ( quantity['quantity_id'] == \
                          operator_quantity.loc[i,'quantity_taxonomic'] ), dim ]\
                         .iloc[0]
            except:
                print('Warning, ', operator_quantity.loc[i,'quantity_taxonomic'],\
                      ' not found when determining units for ', \
                      operator_quantity.loc[i,'operator_quantity_id'])
                continue
            factor, L, T, O, rad = calc_operator_units( operator_quantity.loc[i,'operator'], \
                                                   operator )
            operator_quantity.loc[ i, 'op factor' ] = factor
            operator_quantity.loc[ i, 'op L' ]      = L
            operator_quantity.loc[ i, 'op O' ]      = O
            operator_quantity.loc[ i, 'op T' ]      = T
            operator_quantity.loc[ i, 'op rad' ]    = rad
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
    quantities.loc[ quantities['radian'] != 0, label ] += \
                    'rad^' + quantities.loc[quantities['radian']!=0,'radian']\
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
    fileptr.write( header.format(rep.lower(), rep.lower(), rep.lower(), rep, rep) )
    fileptr.write( '##Last generated on: ' + now.strftime( "%Y-%m-%d %H:%M %Z" ) )

# create building block (bb) file to output all of the relationships
# for core classes
def create_bb_file( vocab, ttl_file, classname, collabel, pref, label=None, \
                    wikifilename='wikipedia_page', part = False, \
                    process_vocab = None ):
    #Print out comment label for section, if provided
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
        element_esc = element_esc.replace('~','%7E')
        ttl_file.write( '\n' + prefix.format( pref, element_esc ) )
        ttl_file.write( declaration_instance.format( \
                        element_esc, 'svu', classname, ';' ) )

        ######################################################################
        ## Alternative class declarations
        # spatial, temporal, etc relationship class
        if 'relationship_type' in vocab.columns.values:
            types = vocab.loc[ index, 'relationship_type']
            if types != '':
                for t in types.split(', '):
                    ttl_file.write( declaration_classname.format( \
                        t.capitalize()+'Relationship', ';' ) )


###########################################################
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
            rel = urllib.quote( rel )
            ttl_file.write( attribute.format( rel_label, \
                '<'+rel_pref+'#' + rel.replace('~','%7E') +'>', ';' ) )
            phen = vocab.loc[ index, 'participant' ]
            pref_opt = vocab.loc[ index, 'participantclass' ].split(', ')
            if 'phenomenon' in pref_opt:
                pref_temp = 'phenomenon'
            elif 'body' in pref_opt:
                pref_temp = 'body'
            elif 'matter' in pref_opt:
                pref_temp = 'matter'
            elif 'form' in pref_opt:
                pref_temp = 'form'
            elif 'abstraction' in pref_opt or 'abstraction_part' in pref_opt:
                pref_temp = 'abstraction'
            elif 'role' in pref_opt:
                pref_temp = 'rolephenomenon'
            elif pref_opt == ['']:
                pref_temp = 'phenomenon'
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
            if classname == 'Reference':
                rel = 'hasReferencePhenomenon'
            elif classname == 'Context':
                rel = 'hasContextPhenomenon'
            elif classname == 'Participant':
                rel = 'hasParticipantPhenomenon'
            else:
                rel = 'hasObject'
            phen = urllib.quote(phen)
            ttl_file.write( attribute.format( rel, \
                '<'+pref_temp+'#' + phen.replace('~','%7E')+'>', ';' ) )
        if collabel == 'participant':
            if 'phenomenon' in vocab.columns.values and \
                vocab.loc[ index, 'phenomenon' ] != '' :
                phen = vocab.loc[ index, 'phenomenon' ]
                pref_temp = vocab.loc[ index, 'phenomenon_pref' ]
                phen = urllib.quote( phen )
                ttl_file.write( attribute.format( 'hasPhenomenon', \
                        '<'+pref_temp+'#' + phen.replace('~','%7E')+'>', ';' ) )
            if 'role' in vocab.columns.values and \
                vocab.loc[ index, 'role' ] != '' :
                role = urllib.quote(vocab.loc[ index, 'role' ])
                ttl_file.write( attribute.format( 'hasParticipantRole', \
                        '<role#' +  role.replace('~','%7E') +'>', ';' ) )

        ######################################################################
        ###Class specific printing
        # OPERATOR information written
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
                ttl_file.write( attribute.format( 'hasPowerFactor', \
                            str(units), ';' ) )
            if 'head_operator_id' in vocab.columns.values:
                hop = vocab.loc[ index, 'head_operator_id' ]
                ttl_file.write( attribute.format( 'hasHeadOperator', ':' + hop, ';' ))
            if 'root_operator_id' in vocab.columns.values and \
                vocab.loc[ index, 'root_operator_id' ] != '' :
                for derivation in vocab.loc[ index, 'root_operator_id' ].split(', '):
                    d = urllib.quote( derivation )
                    ttl_file.write( attribute.format( 'modifiesOperator', \
                            ':' + d.replace('~','%7E'), ';' ) )


        # QUANTITY information written
        if collabel == 'quantity':
            #property from which it is derived
            if vocab.loc[ index, 'property_taxonomic' ] != '' :
                if vocab.loc[ index, 'quantity_taxonomic' ] == '' :
                    derivation = urllib.quote( vocab.loc[ index, 'property_taxonomic' ] )
                    ttl_file.write( attribute.format( 'isTypeOf', \
                            ':' + derivation.replace('~','%7E') , ';' ) )
                else:
                    print('WARNING: ' + element + ' has both property and ' + \
                          'quantity derivation. Only quantity derivation ' + \
                          'written to file.' )
            # property type, property role, property quantification, units
            if vocab.loc[ index, 'property_type' ] != '' :
                ptype = urllib.quote( vocab.loc[ index, 'property_type' ] )
                ttl_file.write( attribute.format( 'hasPropertyType', \
                            ':' +  ptype.replace('~','%7E') , ';' ) )
            if vocab.loc[ index, 'property_role' ] != '' :
                prole = urllib.quote( vocab.loc[ index, 'property_role' ] )
                ttl_file.write( attribute.format( 'hasPropertyRole', \
                            '<role#' +  prole.replace('~','%7E') +'>', ';' ) )
            if vocab.loc[ index, 'property_quantification' ] != '' :
                pquant = urllib.quote( vocab.loc[ index, 'property_quantification' ] )
                ttl_file.write( attribute.format( 'hasPropertyQuantification', \
                            ':' +  pquant.replace('~','%7E') , ';' ) )
            if vocab.loc[ index, 'quantity_taxonomic' ] == '' :
                units = vocab.loc[ index, 'units_string' ]\
                        .replace('rad','').replace('unitless','')\
                        .rstrip(' ')
                ttl_file.write( attribute.format( 'hasUnits', \
                            '\"' + (units if units!='' else 'none') + \
                                    '\"', ';' ) )
            #find relevant processes and write to file
            if 'process_quantity' in vocab.columns.values:
                pquant = vocab.loc[ index, 'process_quantity' ]
                if pquant != '':
                    process2 = ''
                    plst = vocab.loc[ index, 'quantity_id' ].split('_')
                    if 'process2' in pquant:
                        process2_idx = pquant.split('_').index('process2')
                        process2 = plst[process2_idx]
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
                                process_id = urllib.quote( process_vocab.loc[ \
                                    process_vocab['process_nominalization']\
                                    .str.contains(' '+process2), 'process_id'].iloc[0] )
                        ttl_file.write( attribute.format( 'quantifiesProcess', \
                            '<process#' +  process_id.replace('~','%7E')  + '>', \
                            ';' ) )
                        pquant = pquant.replace('process2','').replace('__','_')
                    process_idx = pquant.split('_').index('process')
                    process = plst[process_idx]
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
                            try:
                                process_id = process_vocab.loc[ \
                                    process_vocab['process_nominalization'].str.contains(process), \
                                    'process_id'].iloc[0]
                            except:
                                print(process)
                                process_id = 'none'
                    process_id = urllib.quote( process_id )
                    ttl_file.write( attribute.format( 'quantifiesProcess', \
                        '<process#' + process_id.replace('~','%7E') + '>', \
                        ';' ) )

        if collabel == 'operator_quantity':
            if vocab.loc[ index, 'operator' ] != '' :
                derivation = urllib.quote( vocab.loc[ index, 'quantity_taxonomic' ] )
                ttl_file.write( attribute.format( 'isDerivedFrom', \
                            ':' + derivation.replace('~','%7E') , ';' ) )
                units = vocab.loc[ index, 'units_string' ]
                ttl_file.write( attribute.format( 'hasUnits', \
                            '\"' + (units if units!='' else 'none') + \
                            '\"', ';' ) )
                op = urllib.quote( vocab.loc[ index, 'operator' ] )
                ttl_file.write( attribute.format( 'hasOperator', \
                            '<operator#' +  op.replace('~','%7E')+'>', ';' ) )
            if vocab.loc[ index, 'two_quantity_operator' ] != '' :
                derivation = urllib.quote( vocab.loc[ index, 'quantity1_taxonomic' ] )
                ttl_file.write( attribute.format( 'isDerivedFrom', \
                            ':' +  derivation.replace('~','%7E') , ';' ) )
                derivation = urllib.quote( vocab.loc[ index, 'quantity2_taxonomic' ] )
                ttl_file.write( attribute.format( 'isDerivedFrom', \
                            ':' + derivation.replace('~','%7E'), ';' ) )
                op = urllib.quote( vocab.loc[ index, 'two_quantity_operator' ] )
                ttl_file.write( attribute.format( 'hasOperator', \
                            '<operator#' +  op.replace('~','%7E') +'>', ';' ) )

        #ATTRIBUTE relationships
        if collabel == 'attribute':
            if vocab.loc[ index, 'property_id' ] != '' :
                prop = vocab.loc[ index, 'property_id' ].split(', ')
                for p in prop:
                    p_temp = urllib.quote( p )
                    ttl_file.write( attribute.format( 'correspondsToProperty', \
                            '<property#' +  p_temp.replace('~','%7E') +'>', ';' ) )
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
                ttl_file.write( attribute.format( 'hasAssignedUnits', \
                            '\"' + unit + '\"', ';' ) )
            if 'matter_id' in vocab.columns.values and \
                vocab.loc[ index, 'matter_id' ] != '' :
                unit = vocab.loc[ index, 'matter_id' ]
                ttl_file.write( attribute.format( 'hasAssociatedMatter', \
                            '<matter#' + unit + '>', ';' ) )
            if 'noun' in vocab.columns.values and \
                ( vocab.loc[ index, 'noun' ] == 'noun' ):
                ttl_file.write( attribute.format( 'isNoun', \
                            'true', ';' ) )
            else:
                ttl_file.write( attribute.format( 'isNoun', \
                            'false', ';' ) )


        #PART relationships
        if collabel == 'part':
            if vocab.loc[ index, 'process' ] != '' :
                proc = urllib.quote( vocab.loc[ index, 'process' ] )
                ttl_file.write( attribute.format( 'isDefinedBy', \
                            '<process#' + proc.replace('~','%7E')+'>', ';' ) )

        #MATTER relationships
        if 'expressed-as' in vocab.columns.values and \
                vocab.loc[ index, 'expressed-as' ] != '' :
                mtype = urllib.quote( vocab.loc[ index, 'expressed-as' ] )
                ttl_file.write( attribute.format( 'isExpressedAs', \
                            '<matter#' + mtype.replace('~','%7E')+'>', ';' ) )

        #BODY and FORM and PHENOMENON and ABSTRACTION relationships
        if collabel in ['body','form','phenomenon','abstraction']:
            if 'part' in vocab.columns.values:
                if vocab.loc[ index, 'part' ] != '' :
                    attr = vocab.loc[ index, 'part' ].split(', ')
                    for a in attr:
                        a_temp = urllib.quote( a )
                        ttl_file.write( attribute.format( 'hasPart', \
                            '<part#' + a_temp.replace('~','%7E')+'>', ';' ) )

        #BODY and FORM and PHENOMENON relationships
        if collabel in ['body','form','phenomenon']:
            if 'form' in vocab.columns.values:
                if vocab.loc[ index, 'form' ] != '' :
                    attr = vocab.loc[ index, 'form' ].split(', ')
                    for a in attr:
                        a_temp = urllib.quote( a )
                        ttl_file.write( attribute.format( 'hasForm', \
                            '<form#' + a_temp.replace('~','%7E')+'>', ';' ) )

        #BODY and PHENOMENON RELATIONSHIPS
        if collabel in ['body','phenomenon']:
            if 'body' in vocab.columns.values:
                if vocab.loc[ index, 'body' ] != '' :
                    attr = vocab.loc[ index, 'body' ].split(', ')
                    for a in attr:
                        a_temp = urllib.quote( a )
                        ttl_file.write( attribute.format( 'hasBody', \
                            '<body#' + a_temp.replace('~','%7E') + '>', ';' ) )
            if 'matter' in vocab.columns.values:
                if vocab.loc[ index, 'matter' ] != '' :
                    attr = vocab.loc[ index, 'matter' ].split(', ')
                    for a in attr:
                        a_temp = urllib.quote( a )
                        ttl_file.write( attribute.format( 'hasMatter', \
                            '<matter#' + a_temp.replace('~','%7E') +'>', ';' ) )

        #ABSTRACTION RELATIONSHIP
        if collabel == 'abstraction':
            if 'abstraction_applied' in vocab.columns.values and \
                vocab.loc[ index, 'abstraction_applied' ] != '' :
                abst = urllib.quote( vocab.loc[ index, 'abstraction_applied' ] )
                ttl_file.write( attribute.format( 'isAbstractedBy', \
                        ':' + abst.replace('~','%7E'), ';' ) )
            if 'abstraction' in vocab.columns.values and \
                vocab.loc[ index, 'abstraction' ] != '' :
                abst = urllib.quote( vocab.loc[ index, 'abstraction' ] )
                ttl_file.write( attribute.format( 'hasAbstraction', \
                        ':' + abst.replace('~','%7E'), ';' ) )
            if 'process' in vocab.columns.values and \
                vocab.loc[ index, 'process' ] != '' :
                process = vocab.loc[ index, 'process' ].split(', ')
                for p in process:
                    p_temp = urllib.quote( p )
                    ttl_file.write( attribute.format( 'undergoesProcess', \
                        '<process#' + p_temp.replace('~','%7E')+'>', ';' ) )

        # PHENOMENON relationships
        if collabel == 'phenomenon':
            if 'process' in vocab.columns.values and \
                vocab.loc[ index, 'process' ] != '' :
                process = vocab.loc[ index, 'process' ].split(', ')
                for p in process:
                    p_temp = urllib.quote( p )
                    ttl_file.write( attribute.format( 'describesProcess', \
                        '<process#' + p_temp.replace('~','%7E')+'>', ';' ) )
            if 'role' in vocab.columns.values:
                if vocab.loc[ index, 'role' ] != '' :
                    attr = vocab.loc[ index, 'role' ].split(', ')
                    for a in attr:
                        a_temp = urllib.quote( a )
                        ttl_file.write( attribute.format( 'hasRole', \
                            '<rolephenomenon#' + a_temp.replace('~','%7E')+'>', ';' ) )
            if 'phenomenon' in vocab.columns.values and \
                vocab.loc[ index, 'phenomenon' ] != '' :
                phen = urllib.quote( vocab.loc[ index, 'phenomenon' ] )
                ttl_file.write( attribute.format( 'hasPhenomenon', \
                        ':' + phen.replace('~','%7E'), ';' ) )
            if 'abstraction' in vocab.columns.values and \
                vocab.loc[ index, 'abstraction' ] != '' :
                abstr = urllib.quote( vocab.loc[ index, 'abstraction' ] )
                ttl_file.write( attribute.format( 'isAbstractedBy', \
                        '<abstraction#' + abstr.replace('~','%7E')+'>', ';' ) )
            if 'trajectory' in vocab.columns.values and \
                vocab.loc[ index, 'trajectory' ] != '' :
                trajectory = urllib.quote( vocab.loc[ index, 'trajectory' ] )
                ttl_file.write( attribute.format( 'hasTrajectory', \
                        '<trajectory#' + trajectory.replace('~','%7E')+'>', ';' ) )
            if 'trajectory_direction' in vocab.columns.values and \
                vocab.loc[ index, 'trajectory_direction' ] != '' :
                direction = vocab.loc[ index, 'trajectory_direction' ]
                for d in direction.split(', '):
                    d_temp = urllib.quote( d )
                    ttl_file.write( attribute.format( 'hasTrajectoryDirection', \
                        '<trajectorydirection#' + d_temp.replace('~','%7E')+'>', ';' ) )

            if 'participant1' in vocab.columns.values:
                for i in range(1,6):
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
                            context = urllib.quote( context )
                            ttl_file.write( attribute.format( 'hasContext', \
                                '<context#' + context.replace('~','%7E') + '>', ';' ) )
                        if category == 'medium':
                            medium = phen
                            pref_opt = vocab.loc[ index, participant+'class' ]\
                                .split(', ')
                            if 'phenomenon' in pref_opt:
                                pref_temp = 'phenomenon'
                            elif 'body' in pref_opt:
                                pref_temp = 'body'
                            elif 'matter' in pref_opt:
                                pref_temp = 'matter'
                            elif 'form' in pref_opt:
                                pref_temp = 'form'
                            elif 'abstraction' in pref_opt  or 'abstraction_part' in pref_opt:
                                pref_temp = 'abstraction'
                            elif 'role' in pref_opt:
                                pref_temp = 'rolephenomenon'
                            elif pref_opt == ['']:
                                pref_temp = 'phenomenon'
                            else:
                                pref_temp = 'phenomenon'
                                print('Warning, class not found: '+phen, pref_opt)
                            medium = urllib.quote( medium )
                            ttl_file.write( attribute.format( 'hasObservedMediumPhenomenon', \
                                '<'+pref_temp+'#' + medium.replace('~','%7E') + '>', ';' ) )
                        if category == 'role':
                            if '_' in phen:
                                p = '('+phen+')@role~'+\
                                    vocab.loc[ index, participant + 'cattype']
                            else:
                                p = phen+'@role~'+\
                                    vocab.loc[ index, participant + 'cattype']
                            p = urllib.quote( p )
                            ttl_file.write( attribute.format( 'hasObservedParticipant', \
                                '<participant#' + p.replace('~','%7E') + '>', ';' ) )
                        if category == 'reference':
                            if '_' in phen:
                                reference = '('+phen+')@reference~'+\
                                    vocab.loc[ index, participant + 'cattype']
                            else:
                                reference = phen+'@reference~'+\
                                    vocab.loc[ index, participant + 'cattype']
                            #print(participant, reference)
                            reference = urllib.quote(reference)  
                            ttl_file.write( attribute.format( 'hasReference', \
                                '<reference#' + reference.replace('~','%7E') + '>', ';' ) )
                            #print(reference.replace('~','%7E'))
                        if category == '':
                            pref_opt = vocab.loc[ index, participant+'class' ]\
                                .split(', ')
                            if 'Context' in classname:
                                if 'phenomenon' in pref_opt:
                                    pref_temp = 'phenomenon'
                                elif 'body' in pref_opt:
                                    pref_temp = 'body'
                                elif 'matter' in pref_opt:
                                    pref_temp = 'matter'
                                elif 'form' in pref_opt:
                                    pref_temp = 'form'
                                elif 'abstraction' in pref_opt  or 'abstraction_part' in pref_opt:
                                    pref_temp = 'abstraction'
                                elif pref_opt == ['']:
                                    pref_temp = 'phenomenon'
                                elif 'role' in pref_opt:
                                    pref_temp = 'rolephenomenon'
                                else:
                                    pref_temp = 'phenomenon'
                                    print('Warning, class not found: '+phen, pref_opt)
                                phen = urllib.quote( phen )
                                ttl_file.write( attribute.format( 'hasObservedPhenomenon', \
                                    '<' + pref_temp + '#' + phen.replace('~','%7E') + '>', ';' ) )
                            if 'Medium' in classname:
                                rel = 'hasObservedPhenomenon'
                                if 'phenomenon' in pref_opt:
                                    pref_temp = 'phenomenon'
                                elif 'body' in pref_opt:
                                    pref_temp = 'body'
                                elif 'matter' in pref_opt:
                                    pref_temp = 'matter'
                                elif 'form' in pref_opt:
                                    pref_temp = 'form'
                                elif 'abstraction' in pref_opt  or 'abstraction_part' in pref_opt:
                                    pref_temp = 'abstraction'
                                elif pref_opt == ['']:
                                    pref_temp = 'phenomenon'
                                elif 'role' in pref_opt:
                                    pref_temp = 'rolephenomenon'
                                elif 'attribute' in pref_opt:
                                    pref_temp = 'attribute'
                                    rel = 'hasAttribute'
                                elif 'process' in pref_opt:
                                    pref_temp = 'process'
                                    rel = 'hasObservedProcess'
                                else:
                                    pref_temp = 'phenomenon'
                                    print('Warning, class not found: '+phen, pref_opt)
                                phen = urllib.quote( phen )
                                ttl_file.write( attribute.format( rel, \
                                    '<' + pref_temp + '#' + phen.replace('~','%7E') + '>', ';' ) )
                            if 'Reference' in classname:
                                if 'phenomenon' in pref_opt:
                                    pref_temp = 'phenomenon'
                                elif 'body' in pref_opt:
                                    pref_temp = 'body'
                                elif 'matter' in pref_opt:
                                    pref_temp = 'matter'
                                elif 'form' in pref_opt:
                                    pref_temp = 'form'
                                elif 'abstraction' in pref_opt  or 'abstraction_part' in pref_opt:
                                    pref_temp = 'abstraction'
                                elif 'role' in pref_opt:
                                    pref_temp = 'rolephenomenon'
                                elif pref_opt == ['']:
                                    pref_temp = 'phenomenon'
                                else:
                                    pref_temp = 'phenomenon'
                                    print('Warning, class not found: '+phen, pref_opt)
                                phen = urllib.quote( phen )
                                ttl_file.write( attribute.format( 'hasObservedPhenomenon', \
                                    '<' + pref_temp + '#' + phen.replace('~','%7E')+ '>', ';' ) )
                            if 'Compound' in classname:
                                rel = 'hasObservedPhenomenon'
                                if 'process' in pref_opt:
                                    pref_temp = 'process'
                                    rel = 'hasObservedProcess'
                                elif 'phenomenon' in pref_opt:
                                    pref_temp = 'phenomenon'
                                elif 'body' in pref_opt:
                                    pref_temp = 'body'
                                elif 'matter' in pref_opt:
                                    pref_temp = 'matter'
                                elif 'form' in pref_opt:
                                    pref_temp = 'form'
                                elif 'role' in pref_opt:
                                    pref_temp = 'rolephenomenon'
                                elif 'abstraction' in pref_opt  or 'abstraction_part' in pref_opt:
                                    pref_temp = 'abstraction'
                                elif pref_opt == ['']:
                                    pref_temp = 'phenomenon'
                                elif 'attribute' in pref_opt:
                                    pref_temp = 'attribute'
                                    rel = 'hasAttribute'
                                else:
                                    pref_temp = 'phenomenon'
                                    print('Warning, class not found: '+phen, pref_opt)
                                phen = urllib.quote( phen )
                                ttl_file.write( attribute.format( rel, \
                                    '<' + pref_temp + '#' + phen.replace('~','%7E') + '>', ';' ) )

        ######################################################################
        ###Elements that are universal across files
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
                attr = urllib.quote( attr )
                ttl_file.write( plurality.format( attr.replace('~','%7E')))

        # print what element is derived from, if present
        if collabel + '_taxonomic' in vocab.columns.values and \
            vocab.loc[ index, collabel + '_taxonomic' ] != '' :
            for derivation in vocab.loc[ index, collabel + '_taxonomic' ].split(', '):
                d_temp = urllib.quote( derivation )
                ttl_file.write( attribute.format( 'isTypeOf', \
                            ':' + d_temp.replace('~','%7E'), ';' ) )

        if 'attribute' in vocab.columns.values:
            attr = vocab.loc[ index, 'attribute' ]
            if attr != '':
                attr = attr.split(', ')
                rel = 'hasAttribute'
                if 'condition' in vocab.columns.values:
                    cond = vocab.loc[ index, 'condition' ]
                    if cond != '':
                        rel = 'hasConditionalAttribute'
                for a in attr:
                    a_temp = urllib.quote( a )
                    ttl_file.write( attribute.format( rel, \
                            '<attribute#' + a_temp.replace('~','%7E')+'>', ';' ) )

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

        if collabel + '_label' in vocab.columns.values:
            element = vocab.loc[ index, collabel + '_label' ]
        ttl_file.write( preflabel.format( element ) )

        ######################################################################

# create variable file
def create_variable_entries( vocab, ttl_file, label=None ):
    
    if label:
        ttl_file.write( label )
    for entry in vocab['variable_id'].tolist():
        lst = vocab.loc[vocab['variable_id']==entry]
        first = lst.iloc[0]
        element = first.loc[ 'variable_id' ]
        element_esc = urllib.quote( element )
        element_esc = element_esc.replace('~','%7E')
        ttl_file.write( '\n' + prefix.format( 'variable', element_esc ) )
        ttl_file.write( declaration_instance.format( \
                        element_esc, 'svu', 'Variable', ';' ) )
        quantity = urllib.quote(first[ 'quantity_id'])
        ttl_file.write( attribute.format( 'hasRecordedProperty', \
                            '<property#' + \
                            quantity.replace('~','%7E') + '>', ';'))
            
        obj = urllib.quote(first[ 'object_id'])
        pref = first[ 'object_pref']
        if obj != '':
            ttl_file.write( attribute.format( 'hasRecordedPhenomenon', \
                    '<'+pref+'#' + \
                    obj.replace('~','%7E') + '>', ';'))
        labels = np.unique(lst[ 'variable_label' ].tolist())
        pref_label_len = min([len(i) for i in labels])
        altl = ''
        prefl = ''
        for l in labels:
            if len(l) == pref_label_len:
                prefl += preflabel.format( l )
            else:
                altl += synonym.format( l )
        ttl_file.write(altl+prefl)