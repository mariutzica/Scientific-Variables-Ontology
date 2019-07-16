#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:00:48 2019

@author: mariutzica
"""

#import json
import pandas as pd
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON as sqjson
import numpy as np

#with open('varsNotFound.json') as json_file:  
#    data = json.load(json_file)
    
#varsnotfound = list(data.keys())

modelcatalogvars = pd.read_csv('VariablePresentation.csv')

#missingvars = modelcatalogvars.loc[ \
#    modelcatalogvars['https://w3id.org/mint/modelCatalog#hasStandardVariable']\
#                     .isin(varsnotfound)]
#print(len(np.unique(missingvars['https://w3id.org/mint/modelCatalog#hasStandardVariable'].tolist())))
                          
def query_ontology(variable):
    sparql = SPARQLWrapper("http://sparql.geoscienceontology.org")
    sparql.setQuery("""
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX svu: <http://www.geoscienceontology.org/svo/svu#>

                    SELECT ?entity ?rel ?obj
                    WHERE {{ ?entity a svu:Variable .
                             ?entity ?rel ?obj .
                           ?entity rdfs:label ?label .
                           FILTER regex(?label,"^{}$") .}}
                    """.format(variable))
    sparql.setReturnFormat(sqjson)
    results = sparql.query().convert()

    return results["results"]["bindings"]
    
def check_missing_vars(var):
    notfound = []
    for name in var:
        print(name)
        bad_gateway = True
        while bad_gateway:
            try:
                result = query_ontology(str(name))
                bad_gateway = False
            except:
                continue
        if not result:
            notfound.append(str(name))
    return notfound

unique_vars = list(np.unique(modelcatalogvars['https://w3id.org/mint/modelCatalog#hasStandardVariable'].tolist()))
varsnotfound = check_missing_vars(unique_vars)