#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 09:42:13 2019

@author: mariutzica
@description: script to fill in information about new labels and alternate iris
"""

import pandas as pd
new_names = pd.read_csv("names_to_add_to_SVO.csv")    
new_names = pd.read_csv("names_to_add_to_SVO.csv").fillna('')
new_names = pd.read_csv("names_to_add_to_SVO.csv").fillna('')
new_names['label change'] = False
new_names['iri change'] = False
new_names.loc[new_names['provided svo iri']!='','iri change'] = new_names.loc[new_names['provided svo iri']!='','provided svo iri'] != new_names.loc[new_names['provided svo iri']!='','current svo iri']
new_names.loc[new_names['provided label']!='','label change'] = new_names.loc[new_names['provided label']!='','provided label'] != new_names.loc[new_names['provided label']!='','current label']
iri_change = new_names.loc[new_names['iri change'] == True]
iri_change[['current svo iri','provided svo iri']].to_csv('duplicate_iris.csv',index=False)
labels_to_add = pd.DataFrame(columns=['label','iri'])
labels_to_add['label'] = new_names['current label'].tolist()
labels_to_add['iri'] = new_names['current svo iri'].tolist()
duplicate_label = pd.DataFrame(columns=['label','iri'])
duplicate_label['label'] = new_names.loc[new_names['label change']==True,'provided label'].tolist()
duplicate_label['iri'] = new_names.loc[new_names['label change']==True,'current svo iri'].tolist()
all_new_labels = pd.concat([duplicate_label, labels_to_add],ignore_index=True)
all_new_labels.to_csv('labels_to_add.csv',index=False)