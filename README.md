# Scientific Variables Ontology

This repository will contain all supporting materials for the Scientific 
Variables Ontology. More information about the origins of this ontology 
can be found [here](http://www.geoscienceontology.org).

Folder tree description:

* atomize and standardize csn contains the scripts that break down the CSN, assign context to each element, and recreate an 'order of operations' type syntax to generate ontology ids
* core ontology files are the TTL ontology files outputted by running scripts in the other folders
* documentation contains relevant diagrams and other descriptions of the ontology
* foundational vocabulary contains csv files that form the vocabulary of the lower ontology, categorized by type; these are input files to the scripts in generation code
* generation code contains code that takes the results of scripts from atomize and standardize csn and information from foundational vocabulary and creates the ontology RDF (TTL) files in core ontology files 
