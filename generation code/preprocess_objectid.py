#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 21:01:58 2018

@author: mariutzica
@description: Process object ID and generate all complex phenomena.
"""

##################################
#   Import required packages     #
##################################

#utils
import utils as utils

import numpy as np
import pandas as pd

##################################
#   Variable Initialization      #
##################################

ext_csn_variable    = '../atomize and standardize csn/'
csn_variables_file  = 'CSDMS_standard_names.csv'
ext_vocabulary      = '../foundational vocabulary/'

phenomenon_file  = 'phenomenon.csv'
compound_phenomenon_file  = 'phenomenon_compound.csv'
matter_file  = 'matter.csv'
form_file  = 'form_and_configuration.csv'
inanimate_nat_body_file  = 'inanimate_natural_body.csv'
inanimate_fab_body_file  = 'inanimate_fabricated_body.csv'
animate_body_file  = 'animate_body.csv'
math_abstraction_file  = 'abstraction_mathematical.csv'
phys_abstraction_file  = 'abstraction_physical.csv'

part_file  = 'part.csv'
role_file  = 'role.csv'
process_file  = 'process.csv'
qualitative_attribute_file  = 'qualitative_attribute.csv'
quantitative_attribute_file  = 'quantitative_attribute.csv'

phys_abstraction_part_file  = 'abstraction_physical_part.csv'
math_abstraction_part_file  = 'abstraction_mathematical_part.csv'

trajectory_file  = 'trajectory.csv'

################################
#   INITIAL DATA LOAD          #
################################

phenomenon_vocabulary = \
            utils.load_data( ext_vocabulary, phenomenon_file, \
            usecols = ['phenomenon_id'] )  
compound_phenomenon_vocabulary = \
            utils.load_data( ext_vocabulary, compound_phenomenon_file, \
            usecols = ['phenomenon_id'] )  
matter_vocabulary = \
            utils.load_data( ext_vocabulary, matter_file, \
            usecols = ['matter_id'] ) 
form_vocabulary = \
            utils.load_data( ext_vocabulary, form_file, \
            usecols = ['form_id'] ) 
math_abstraction_vocabulary = \
            utils.load_data( ext_vocabulary, math_abstraction_file, \
            usecols = ['abstraction_id'] )
phys_abstraction_vocabulary = \
            utils.load_data( ext_vocabulary, phys_abstraction_file, \
            usecols = ['abstraction_id'] )
inanimate_nat_body_vocabulary = \
            utils.load_data( ext_vocabulary, inanimate_nat_body_file, \
            usecols = ['body_id'] ) 
inanimate_fab_body_vocabulary = \
            utils.load_data( ext_vocabulary, inanimate_fab_body_file, \
            usecols = ['body_id'] ) 
animate_body_vocabulary = \
            utils.load_data( ext_vocabulary, animate_body_file, \
            usecols = ['body_id'] ) 

role_vocabulary = \
            utils.load_data( ext_vocabulary, role_file, usecols = ['role_id'] ) 
part_vocabulary = \
            utils.load_data( ext_vocabulary, part_file, usecols = ['part_id'] )

process_vocabulary = \
            utils.load_data( ext_vocabulary, process_file, usecols = ['process_id'] )   
qualitative_attribute_vocabulary = \
            utils.load_data( ext_vocabulary, qualitative_attribute_file, usecols = ['attribute_id'] )   
quantitative_attribute_vocabulary = \
            utils.load_data( ext_vocabulary, quantitative_attribute_file, usecols = ['attribute_id'] )  
phys_abstraction_part_vocabulary = \
            utils.load_data( ext_vocabulary, phys_abstraction_part_file, usecols = ['abstraction_id']  )
math_abstraction_part_vocabulary = \
            utils.load_data( ext_vocabulary, math_abstraction_part_file, usecols = ['abstraction_id']  )
trajectory_vocabulary = \
            utils.load_data( ext_vocabulary, trajectory_file, usecols = ['trajectory_id'] ) 

object_id = \
            utils.load_data( ext_csn_variable, csn_variables_file, usecols = ['object_id'] )

def generate_phenomena(oid, phen):
    if not '(' in oid:
        phen.append(oid)
    else:
        phen.append(oid)
        index_start = 0
        for a in oid:
            if a == '(':
                counter = 0
                index_end = index_start+1
                for b in oid[index_start+1:]:
                    if b == '(':
                        counter += 1
                    if (b == ')') and (counter != 0):
                        counter -= 1
                    elif (b == ')'):
                        break
                    index_end += 1
                generate_phenomena(oid[index_start+1:index_end],phen)                        
            index_start += 1

# decompose object_id to extract all contained complex phenomena
all_phen = []                       
for name in object_id['object_id'].tolist():
    phen = []
    generate_phenomena(name, phen)
    all_phen.extend(phen)

# initialize columns for complex_phenomena (unique list)    
complex_phenomena = pd.DataFrame({'phenomenon_id':np.unique(all_phen)})
for i in range(1,6):
    complex_phenomena['participant'+str(i)]=''
    complex_phenomena['participant'+str(i)+'cat']=''
    complex_phenomena['participant'+str(i)+'cattype']=''
    complex_phenomena['participant'+str(i)+'class']=''

# parse all complex phenomena
for i in complex_phenomena.index:
    oid = complex_phenomena.loc[i,'phenomenon_id']
    #input("Press Enter to continue...")
    #print(oid)
    index_start = 0
    participant = 1    
    while( index_start < len(oid)):
        if oid[index_start] == '(':
            counter = 0
            index_end = index_start+1
            while (index_end < len(oid)):
                if oid[index_end] == '(':
                    counter += 1
                elif (oid[index_end] == ')') and (counter != 0):
                    counter -= 1
                elif (oid[index_end] == ')'):
                    break
                index_end += 1
            complex_phenomena.loc[i,'participant'+str(participant)]= oid[index_start+1:index_end]
            #print(participant, oid[index_start+1:index_end])
            index_start = index_end + 1
            if (index_start < len(oid)) and (oid[index_start]=='@'):
                index_end = index_start + oid[index_start:].find('_')
                if index_end == (index_start-1):
                    index_end = len(oid)
                complex_phenomena.loc[i,'participant'+str(participant)+'cat']= \
                        oid[index_start+1:index_end].split('~')[0]
                if '~' in oid[index_start:index_end]:
                        complex_phenomena.loc[i,'participant'+str(participant)+'cattype']= \
                            oid[index_start:index_end].split('~')[1]
                index_start = index_end + 1
            if (index_start < len(oid)) and (oid[index_start]=='_'):
                index_start += 1
        else:
            index_end = index_start + oid[index_start:].find('_')
            if index_end == (index_start-1):
                index_end = len(oid)
            complex_phenomena.loc[i,'participant'+str(participant)]= \
                oid[index_start:index_end].split('@')[0]
            #print(participant, oid[index_start:index_end].split('@')[0])
            if '@' in oid[index_start:index_end]:
                complex_phenomena.loc[i,'participant'+str(participant)+'cat']= \
                        oid[index_start:index_end].split('@')[1].split('~')[0]
                if '~' in oid[index_start:index_end].split('@')[1]:
                    complex_phenomena.loc[i,'participant'+str(participant)+'cattype']= \
                        oid[index_start:index_end].split('@')[1].split('~')[1]
            index_start = index_end + 1
#            if (index_start < len(oid)) and (oid[index_start]=='_'):
#                print('here')
#                index_start += 1
        participant += 1

complex_phenomena = complex_phenomena.fillna('')
context_phen = complex_phenomena.loc[(complex_phenomena['participant1cat']=='context') |(complex_phenomena['participant2cat']=='context') | (complex_phenomena['participant3cat']=='context')].copy()
medium_phen = complex_phenomena.loc[(complex_phenomena['participant1cat']=='medium') |(complex_phenomena['participant2cat']=='medium') | (complex_phenomena['participant3cat']=='medium')].copy()
role_phen = complex_phenomena.loc[(complex_phenomena['participant1cat']=='role') |(complex_phenomena['participant2cat']=='role') | (complex_phenomena['participant3cat']=='role')].copy()
ref_phen = complex_phenomena.loc[(complex_phenomena['participant1cat']=='reference') |(complex_phenomena['participant2cat']=='reference') | (complex_phenomena['participant3cat']=='reference')].copy()
compound_phen = complex_phenomena.loc[(complex_phenomena['participant1cat']=='') &(complex_phenomena['participant2cat']=='') & (complex_phenomena['participant3cat']=='')& complex_phenomena['phenomenon_id'].str.contains('_')].copy()
simple_phen = complex_phenomena.loc[(complex_phenomena['participant1cat']=='') &(complex_phenomena['participant2cat']=='') & (complex_phenomena['participant3cat']=='')& ~complex_phenomena['phenomenon_id'].str.contains('_')].copy()

#determine classes of each id ...
def determine_category(phen_list):
    not_found = []
    multiple_match = []
    for i in phen_list.index:
        for j in range(1,6):
            participant = 'participant'+str(j)
            cat = participant + 'class'
            category = ''
            p = phen_list.loc[i,participant]
            if p != '':
                if (p in phenomenon_vocabulary['phenomenon_id']\
                    .tolist()) or (p in compound_phenomenon_vocabulary['phenomenon_id']\
                    .tolist()):
                    category += 'phenomenon, '
                if (p in matter_vocabulary['matter_id']\
                    .tolist()):
                    category += 'matter, '
                if (p in form_vocabulary['form_id']\
                    .tolist()):
                    category += 'form, '
                if (p in math_abstraction_vocabulary['abstraction_id']\
                    .tolist()) or (p in phys_abstraction_vocabulary['abstraction_id']\
                    .tolist()):
                    category += 'abstraction, '
                if (p in math_abstraction_part_vocabulary['abstraction_id']\
                    .tolist()) or (p in phys_abstraction_part_vocabulary['abstraction_id']\
                    .tolist()):
                    category += 'abstraction_part, '
                if (p in inanimate_nat_body_vocabulary['body_id']\
                    .tolist()) or (p in inanimate_fab_body_vocabulary['body_id']\
                    .tolist())\
                      or (p in animate_body_vocabulary['body_id']\
                    .tolist()):
                    category += 'body, '
                if (p in role_vocabulary['role_id']\
                    .tolist()):
                    category += 'role, '
                if (p in part_vocabulary['part_id']\
                    .tolist()):
                    category += 'part, '
                if (p in process_vocabulary['process_id']\
                    .tolist()):
                    category += 'process, '
                if (p in trajectory_vocabulary['trajectory_id']\
                    .tolist()):
                    category += 'trajectory, '
                if (p in qualitative_attribute_vocabulary['attribute_id']\
                    .tolist()) or (p in quantitative_attribute_vocabulary['attribute_id']\
                    .tolist()):
                    category += 'attribute, '                
                phen_list.loc[i,cat] = category
                if category=='':
                    not_found.append(str(i)+' '+p)
                if ',' in category.rstrip(', '):
                    multiple_match.append(p+' '+category)
    return not_found, multiple_match

def determine_id_cat(df):
    match = []
    for i in df.index:
        category = ''
        p = df.loc[i,'phenomenon_id']
        if (p in phenomenon_vocabulary['phenomenon_id']\
            .tolist()) or (p in compound_phenomenon_vocabulary['phenomenon_id']\
            .tolist()):
            category += 'phenomenon, '
        if (p in matter_vocabulary['matter_id']\
            .tolist()):
            category += 'matter, '
        if (p in form_vocabulary['form_id']\
            .tolist()):
            category += 'form, '
        if (p in math_abstraction_vocabulary['abstraction_id']\
            .tolist()) or (p in phys_abstraction_vocabulary['abstraction_id']\
            .tolist()):
            category += 'abstraction, '
        if (p in math_abstraction_part_vocabulary['abstraction_id']\
            .tolist()) or (p in phys_abstraction_part_vocabulary['abstraction_id']\
            .tolist()):
            category += 'abstraction_part, '
        if (p in inanimate_nat_body_vocabulary['body_id']\
            .tolist()) or (p in inanimate_fab_body_vocabulary['body_id']\
            .tolist())\
            or (p in animate_body_vocabulary['body_id'].tolist()):
            category += 'body, '
        if (p in role_vocabulary['role_id'].tolist()):
            category += 'role, '
        if (p in part_vocabulary['part_id'].tolist()):
            category += 'part, '
        if (p in process_vocabulary['process_id'].tolist()):
            category += 'process, '
        if (p in trajectory_vocabulary['trajectory_id'].tolist()):
            category += 'trajectory, '
        if (p in qualitative_attribute_vocabulary['attribute_id']\
            .tolist()) or (p in quantitative_attribute_vocabulary['attribute_id']\
            .tolist()):
            category += 'attribute, '                
        match.append(p+' '+category)    
    return match

compound_phen_classes = determine_id_cat(compound_phen)
simple_phen_classes = determine_id_cat(simple_phen)

context_not_found, multiple_match = determine_category(context_phen)
medium_not_found, temp = determine_category(medium_phen)
multiple_match.extend(temp)
role_not_found, temp = determine_category(role_phen)
multiple_match.extend(temp)
ref_not_found, temp = determine_category(ref_phen)
multiple_match.extend(temp)
compound_not_found, temp = determine_category(compound_phen)
multiple_match.extend(temp)
simple_not_found, temp = determine_category(simple_phen)
multiple_match.extend(temp)
print(np.unique(multiple_match))

#figure out if any simple or compound phenomena are not in the vocabulary
simple_not_found.extend(compound_not_found)
simple_not_found.extend(ref_not_found)
simple_not_found.extend(role_not_found)
simple_not_found.extend(medium_not_found)
simple_not_found.extend(context_not_found)
not_found = [nf for nf in simple_not_found if not '@' in nf]
not_found = np.unique(not_found)

def check_grouping(df):
    for i in df.index:
        categories = df.loc[i,['participant'+str(p)+'cat' for p in range(1,6)]].tolist()
        participants = df.loc[i,['participant'+str(p) for p in range(1,6)]].tolist()
        num_categories = len([cat for cat in categories if cat!=''])
        num_participants = len([p for p in participants if p!=''])
        if num_categories != num_participants - 1:
            print('Possible problem detected with ... ',str(i),' ',df.loc[i,'phenomenon_id'])
            
#check_grouping(context_phen)
#check_grouping(medium_phen)
#check_grouping(role_phen)
#check_grouping(ref_phen)
                      
#create files for complex phenomena            
context_phen.to_csv(ext_vocabulary+'context_phenomena.csv',index=False)            
medium_phen.to_csv(ext_vocabulary+'medium_phenomena.csv',index=False)            
role_phen.to_csv(ext_vocabulary+'role_phenomena.csv',index=False)            
ref_phen.to_csv(ext_vocabulary+'reference_phenomena.csv',index=False)            
            
#grab context, medium, role, reference
def extract_part(df,cat):
    temp = pd.DataFrame(columns = ['participant','participantrel','participantclass'])
    for i in df.index:
        for participant in range(1,6):
            if df.loc[i,'participant'+str(participant)+'cat']==cat:
                cols = ['participant'+str(participant),\
                        'participant'+str(participant)+'cattype',\
                        'participant'+str(participant)+'class' ]
                temp.loc[len(temp)]=df.loc[i,cols].tolist()
    return temp.drop_duplicates()
            
context = extract_part(context_phen, 'context')
medium = extract_part(medium_phen, 'medium')
role = extract_part(role_phen, 'role')
reference = extract_part(ref_phen, 'reference')

context.to_csv(ext_vocabulary+'context.csv',index=False)            
medium.to_csv(ext_vocabulary+'medium.csv',index=False)            
role.to_csv(ext_vocabulary+'participant.csv',index=False)            
reference.to_csv(ext_vocabulary+'reference.csv',index=False)            
