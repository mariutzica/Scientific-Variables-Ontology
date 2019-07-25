#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:27:13 2019

@author: mariutzica
"""

from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON as sqjson
import pandas as pd
import requests
# DateTime for getting the timestamp for the file
import datetime
import pytz
import urllib

def get_label_from_id(oid):
    label = urllib.parse.unquote(oid.split('#')[1])
    label = label.replace('%7E','~')
    return label

def get_rel_value(item, prop, cols, pref = 'http://www.geoscienceontology.org/svo/svu#'):
    rel_value = ''
    if pref+prop in cols:
        rel_value = item[pref+prop]
    return rel_value
        
def add_context(vals, txt):
    cont = ''
    if vals != '' and vals != 'none':
        if ', ' in vals and '#' in vals:
            cont += '<p>' + txt + ':</p>\n<div><ul>'
            for a in vals.split(', '):
                a_label = get_label_from_id(a)
                cont += """<li><a href="{}">{}</a></li>""".format(a,a_label)
            cont += "</ul></div>"
        elif '#' in vals:
            v_label = get_label_from_id(vals)
            cont += '<p>' + txt + \
                ' <a href={}>{}</a>'.format(vals,v_label) + '</p>'
        else:
            cont += '<p>' + txt + ' ' + vals + '.</p>'
    return cont

def get_wikipedia_content(link):
    wiki_context = ''
    if link != '' and not '#' in link:
        pagename = link.split('/')[-1]
        if 'index.php' in pagename:
            pagename = pagename.split('title=')[1].split('&')[0]
        query_url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles={}&exintro=&exsentences=2&explaintext=&redirects=&format=json".format(pagename)
        r = requests.get(url = query_url)
        temp = r.json()
        for _,val in temp['query']['pages'].items():
            try:
                wiki_context = val['extract']
            except:
                print('Wikipedia page {} not valid.'.format(link))
    return wiki_context

def print_index_html(cl,items,desc,date):
    svu_pref = "http://www.geoscienceontology.org/svo/svu#"
    head = \
    """<!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
        <link href="/svo/css/stylesheet.css" rel="stylesheet">
    </head>
    <body>
        <div id="header">
            <img src="/svo/images/svo_temp_logo.png">
            <h1 id="headline">{} Ontology</h1>
        </div>
 
        <div id='menu'>
            <ul>
                <li><a href="/svo" class="inactive"><span>SVO Doc</span></a></li>
                <li><a href="/svo/svu" class="inactive"><span>SVU Doc<span></a></li>
                <li><a href="/svo/svl" class="inactive"><span>SVL Doc</span></a></li>
                <li><a href="/" class="inactive"><span>Main Site</span></a></li>
            </ul>
        </div>
                    
        <p>
            {}
        </p>
        <p>
            If you detect an error in this or any other document, please 
            <a href="/contact.html">contact us</a> to let us know.
        </p>
        <p>
            Documentation last generated on {}.
        </p>
    """.format(cl,desc,date.strftime( "%Y-%m-%d %H:%M %Z" ))
    foot = \
    """
    </body>
    </html>"""
            
    text_body = ''
    cols = items.columns.values
    for _,item in items.iterrows():

        #Phenomena that are declared in other namespaces, not Phenomenon
        if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in cols and cl == 'Phenomenon':
            phen_class = item['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
            if svu_pref + 'Body' in phen_class or svu_pref + 'Form' in phen_class\
                or svu_pref + 'Matter' in phen_class or svu_pref + 'RolePhenomenon' in phen_class:
                continue
        #Parts that are Abstractions are declared in Abstraction namespace
        if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in cols and cl == 'Part':
            part_class = item['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
            if svu_pref + 'Abstraction' in part_class:
                continue

        address = item['entity']
        label = item['http://www.w3.org/2004/02/skos/core#prefLabel']


        # print universal properties for all entities
        altlabel  = get_rel_value(item, 'altLabel', cols, \
                                 pref = 'http://www.w3.org/2004/02/skos/core#')
        wikipedia = get_rel_value(item, 'hasAssociatedWikipediaPage', cols )

        wiki_content = get_wikipedia_content(wikipedia)
        wiki_context = ''
        if wiki_content != '':
            wiki_context = "<p>This instance has a related <a href='{}' target='_blank'>"+\
                        "Wikipedia page</a>. Short extract:<br/>" +\
                        "<em>{}</em>".format(wikipedia,''.join(wiki_content))
        altlabel_cont = add_context(altlabel, "Alternative labels for this instance are")

        # print core phenomenon components
        body          = get_rel_value(item, 'hasBody', cols )
        matter        = get_rel_value(item, 'hasMatter', cols )
        form          = get_rel_value(item, 'hasForm', cols )
        part          = get_rel_value(item, 'hasPart', cols )
        trajectory    = get_rel_value(item, 'hasTrajectory', cols )
        trajectorydir = get_rel_value(item, 'hasTrajectoryDirection', cols )
        phenrole      = get_rel_value(item, 'hasRole', cols )
        phenomenon    = get_rel_value(item, 'hasPhenomenon', cols )
        hasprocess    = get_rel_value(item, 'hasProcess', cols )
        process       = get_rel_value(item, 'undergoesProcess', cols )
        desc_process  = get_rel_value(item, 'describesProcess', cols )
        abstraction   = get_rel_value(item, 'hasAbstraction', cols )
        abstractionof = get_rel_value(item, 'isAbstractionOf', cols )
        containsabstraction   = \
                        get_rel_value(item, 'containsAbstraction', cols )
        containsabstractionof = \
                        get_rel_value(item, 'containsAbstractionOf', cols )
        abstractedby  = get_rel_value(item, 'isAbstractedBy', cols ) 
        expras        = get_rel_value(item, 'isExpressedAs', cols )
        attributes    = get_rel_value(item, 'hasAttribute', cols )
        plurality     = get_rel_value(item, 'isPluralityOf', cols )
        typeof        = get_rel_value(item, 'isTypeOf', cols )
        pluraltypeof  = get_rel_value(item, 'isPluralityTypeOf', cols )

        typeof_cont = add_context(typeof, "This instance is a narrower concept derived from")
        typeof_cont += add_context(pluraltypeof, "This instance is the plural narrower concept derived from")
        plurality_cont = add_context(plurality, "This instance is a plurality of")                        
        attr_cont = add_context(attributes, "This instance has the attribute")
        process_cont = ''
        process_cont += add_context(process, "This instance describes something undergoing the process")
        process_cont += add_context(desc_process, "This instance describes the process")

        parts_cont = ''
        parts_cont += add_context(phenomenon, "This instance has the phenomenon component")
        parts_cont += add_context(matter, "This instance has the matter component")
        parts_cont += add_context(form, "This instance has the form component")
        parts_cont += add_context(body, "This instance has the body component")
        parts_cont += add_context(abstraction, "This instance has the abstraction component")
        parts_cont += add_context(part, "This instance has the part component")
        parts_cont += add_context(trajectory, "This instance has the trajectory component")
        parts_cont += add_context(trajectorydir, "This instance has the trajectory direction component")
        parts_cont += add_context(phenrole, "This instance has the role component")
        expras_cont = add_context(expras, "The property of this substance is expressed with respect to the substance")            
        abstr_cont = add_context(abstractedby, "This instance is abstracted by")
        abstr_cont += add_context(abstractionof, "This instance is an abstraction of")
        abstr_cont += add_context(containsabstractionof, "This instance contains an abstraction of")

        # print process properties
        nominalization     = get_rel_value(item, 'hasNominalization', cols )
        present_tense      = get_rel_value(item, 'hasPresentTense', cols )
        present_participle = get_rel_value(item, 'hasPresentParticiple', cols )
        isnoun             = get_rel_value(item, 'isNoun', cols )

        pos_cont = add_context(nominalization, "This process has the nominalization language cue")
        pos_cont += add_context(present_tense, "This process has the present tense language cue")
        pos_cont += add_context(present_participle, "This process has the present participle language cue")
        isnoun_cont = ''
        if isnoun == 'true':
            isnoun_cont = """\n<p>This attribute is expressed as a noun.</p>"""
        elif isnoun == 'false':
            isnoun_cont = """\n<p>This attribute is expressed as an adjective.</p>"""
        
        # print attribute, operator and property specific properties
        corr_prop     = get_rel_value(item, 'correspondsToProperty', cols )
        value         = get_rel_value(item, 'hasValue', cols )
        assocmatr     = get_rel_value(item, 'hasAssociatedMatter', cols )
        assunits      = get_rel_value(item, 'hasAssignedUnits', cols )
        units         = get_rel_value(item, 'hasUnits', cols )
        headop        = get_rel_value(item, 'hasheadOperator', cols )
        modop         = get_rel_value(item, 'modifiesOperator', cols )
        indmodop      = get_rel_value(item, 'indirectlyModifiesOperator', cols )
        multunits     = get_rel_value(item, 'hasMultiplierUnits', cols )
        powfunits     = get_rel_value(item, 'hasPowerFactor', cols )
        quantprocess  = get_rel_value(item, 'quantifiesProcess', cols )
        processdef    = get_rel_value(item, 'isDefinedBy', cols )
        propertytype  = get_rel_value(item, 'hasPropertyType', cols )
        propertyrole  = get_rel_value(item, 'hasPropertyRole', cols )
        propertyquant = get_rel_value(item, 'hasPropertyQuantification', cols )
        apploperator  = get_rel_value(item, 'hasAppliedOperator', cols )
        containsapploperator = \
                        get_rel_value(item, 'containsAppliedOperator', cols )
        derivation    = get_rel_value(item, 'isDerivedFrom', cols )
        hasproperty   = get_rel_value(item, 'hasProperty', cols )

        value_cont     = add_context(value, "This attribute corresponds to property value")        
        assunits_cont  = add_context(assunits, "This attribute has the assigned units")
        corrprop_cont  = add_context(corr_prop, "This attribute pertains to the property")
        assocmatr_cont = add_context(assocmatr, \
                         "This attribute inherently refers to a state of the matter instance")
        
        op_cont = add_context(headop, "This compound operator has the head operator")
        op_cont += add_context(modop, "This compound operator modifies the operator")
        op_cont += add_context(indmodop, "This instance indirectly modifies the operator")
        units_cont = add_context(units, "This instance has the dimensional units string")
        process_cont += add_context(quantprocess, "This instance quantifies the process")
        process_cont += add_context(processdef, "This instance is defined by the process")
        unitsmod_cont = add_context(powfunits, "This operator modifies the units of the "+\
                                    "property it is applied to by raising the units to " +\
                                    "the power of")                    
        unitsmod_cont += add_context(multunits, "This operator modifies the units of "+\
                                     "the property it is applied to by multiplying " +\
                                     "those units by the units")
        
                    
        proptype_cont = add_context(propertytype, "This instance has the property type")
        proprole_cont = add_context(propertyrole, "This instance has the property role")
        propquant_cont = add_context(propertyquant, "This instance has the property quantification")
        derivation_cont = add_context(derivation, "This instance is derived from")
        operator_cont = add_context(apploperator, "This instance has the applied operator")
        operator_cont += add_context(containsapploperator, "This instance contains the applied operator")

        hasprop_cont = add_context(hasproperty, "This instance describes the property")

        # print assumption content
        assumpt = get_rel_value(item, 'type', cols, pref = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#' )

        assumpt_cont = ''
        if assumpt != '' and cl == 'Assumption':
            for a in assumpt.split(', '):
                if 'geoscienceontology' in a:
                    assumpt_label = get_label_from_id(a)
                    if assumpt_label != 'Assumption':
                        assumpt_cont += "\n<p>This assumption falls in the broader category "+\
                                        "<a href='#{}'>{}</a>.</p>"\
                                        .format(assumpt, assumpt_label)

        # print role and relationship content
        role = ''
        if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in cols and cl == 'Role':
            role = item['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
            if 'Property' in role:
                role = 'Quantitative Property'
                role_href = 'http://www.geoscienceontology.org/svo/svu#Property'
            else:
                role = 'Participant'
                role_href = 'http://www.geoscienceontology.org/svo/svu#Participant'
        
        relationship = ''
        if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in cols and cl == 'Relationship':
            relationship_temp = item['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
            if 'Spatial' in relationship_temp:
                relationship = 'spatial'
            if 'Spatiotemporal' in relationship_temp:
                relationship += ', spatiotemporal'
            if 'Temporal' in relationship_temp:
                relationship += ', temporal'
            relationship = relationship.lstrip(', ')                        

        role_cont = ''
        if role != '':
            role_cont = """\n
            This role can be applied to instances of the <a href="{}">{}</a> class.
            """.format(role_href,role)

        rel_cont = ''
        if relationship != '':
            rel_cont = """\n
            This relationship is applied to describe the following types of relationships: {}.
            """.format(relationship)

        # print specialty phenomenon properties
        has_context = ''

        for rellink in ['Medium','Reference','Context','Participant']:
            hasx           = get_rel_value(item, 'has{}'.format(rellink), cols)
            hasphenomenon  = get_rel_value(item, 'has{}Phenomenon'\
                                               .format(rellink), cols)
            hasbody        = get_rel_value(item, 'has{}Body'\
                                               .format(rellink), cols)
            hasmatter      = get_rel_value(item, 'has{}Matter'\
                                                .format(rellink), cols)
            hasform        = get_rel_value(item, 'has{}Form'\
                                                .format(rellink), cols)
            haspart        = get_rel_value(item, 'has{}Part'\
                                                .format(rellink), cols)
            hastrajectory  = get_rel_value(item, 'has{}Trajectory'\
                                                .format(rellink), cols)
            hastrajdir     = get_rel_value(item, 'has{}TrajectoryDirection'\
                                                .format(rellink), cols)
            hasprocess     = get_rel_value(item, 'has{}Process'\
                                                .format(rellink), cols)
            hasrole        = get_rel_value(item, 'has{}Role'\
                                                .format(rellink), cols)
            hasabstraction = get_rel_value(item, 'has{}Abstraction'\
                                                .format(rellink), cols)
            hasattribute   = get_rel_value(item, 'has{}Attribute'\
                                                .format(rellink), cols)
            hasrelationship = get_rel_value(item, 'has{}Relationship'\
                                               .format(rellink), cols)
            
            has_context += add_context(hasx, \
                        "This instance has the {}")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hasphenomenon, \
                        "This instance has the {}phenomenon")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hasbody, \
                        "This instance represents the {}body")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hasmatter, \
                        "This instance represents the {}matter")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hasform, \
                        "This instance represents the {}form")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(haspart, \
                        "This instance represents the {}part")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hasprocess, \
                        "This instance represents the {}process")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hastrajectory, \
                        "This instance represents the {}trajectory")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hastrajdir, \
                        "This instance represents the {}trajectory direction")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hasrole, \
                        "This instance represents the {}role")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hasabstraction, \
                        "This instance represents the {}abstraction")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hasattribute, \
                        "This instance represents the {}attribute")\
                                            .format(rellink.lower()+' ')  
            has_context += add_context(hasrelationship, \
                        "This instance represents the {}relationship")\
                                            .format(rellink.lower()+' ')  

                    
        # print all contains relationships
        contains_context = ''

        for rellink in ['','Medium','Reference','Context','Participant']:
            containsphenomenon  = get_rel_value(item, 'contains{}Phenomenon'\
                                               .format(rellink), cols)
            containsbody        = get_rel_value(item, 'contains{}Body'\
                                               .format(rellink), cols)
            containsmatter      = get_rel_value(item, 'contains{}Matter'\
                                                .format(rellink), cols)
            containsform        = get_rel_value(item, 'contains{}Form'\
                                                .format(rellink), cols)
            containspart        = get_rel_value(item, 'contains{}Part'\
                                                .format(rellink), cols)
            containstrajectory  = get_rel_value(item, 'contains{}Trajectory'\
                                                .format(rellink), cols)
            containstrajdir     = get_rel_value(item, 'contains{}TrajectoryDirection'\
                                                .format(rellink), cols)
            containsprocess     = get_rel_value(item, 'contains{}Process'\
                                                .format(rellink), cols)
            containsrole        = get_rel_value(item, 'contains{}Role'\
                                                .format(rellink), cols)
            containsabstraction = get_rel_value(item, 'contains{}Abstraction'\
                                                .format(rellink), cols)
            containsattribute   = get_rel_value(item, 'contains{}Attribute'\
                                                .format(rellink), cols)

        
            contains_context += add_context(containsphenomenon, \
                        "This variable contains the {}phenomenon")\
                                            .format(rellink.lower()+' ')  
            contains_context += add_context(containsbody, \
                        "This variable contains the {}body")\
                                            .format(rellink.lower()+' ')  
            contains_context += add_context(containsmatter, \
                        "This variable contains the {}matter")\
                                            .format(rellink.lower()+' ')  
            contains_context += add_context(containsform, \
                        "This variable contains the {}form")\
                                            .format(rellink.lower()+' ')  
            contains_context += add_context(containspart, \
                        "This variable contains the {}part")\
                                            .format(rellink.lower()+' ')  
            contains_context += add_context(containstrajectory, \
                        "This variable contains the {}trajectory")\
                                            .format(rellink.lower()+' ')  
            contains_context += add_context(containstrajdir, \
                        "This variable contains the {}trajectory direction")\
                                            .format(rellink.lower()+' ')  
            contains_context += add_context(containsprocess, \
                        "This variable contains the {}process")\
                                            .format(rellink.lower()+' ')  
            contains_context += add_context(containsrole, \
                        "This variable contains the {}role")\
                                            .format(rellink.lower()+' ')  
            contains_context += add_context(containsabstraction, \
                        "This variable contains the {}abstraction")\
                                            .format(rellink.lower()+' ')  
            contains_context += add_context(containsattribute, \
                        "This variable contains the {}attribute")\
                                            .format(rellink.lower()+' ')  

        # print all recorded relationships (Variable class)
        recorded_context = ''

        for rellink in ['','Medium','Reference','Context','Participant']:
            recordedphenomenon  = get_rel_value(item, 'hasRecorded{}Phenomenon'\
                                                .format(rellink), cols)
            recordedbody        = get_rel_value(item, 'hasRecorded{}Body'\
                                                .format(rellink), cols)
            recordedmatter      = get_rel_value(item, 'hasRecorded{}Matter'\
                                                .format(rellink), cols)
            recordedform        = get_rel_value(item, 'hasRecorded{}Form'\
                                                .format(rellink), cols)
            recordedpart        = get_rel_value(item, 'hasRecorded{}Part'\
                                                .format(rellink), cols)
            recordedtrajectory  = get_rel_value(item, 'hasRecorded{}Trajectory'\
                                                .format(rellink), cols)
            recordedtrajdir     = get_rel_value(item, 'hasRecorded{}TrajectoryDirection'\
                                                .format(rellink), cols)
            recordedprocess     = get_rel_value(item, 'hasRecorded{}Process'\
                                                .format(rellink), cols)
            recordedrole        = get_rel_value(item, 'hasRecorded{}Role'\
                                                .format(rellink), cols)
            recordedabstraction = get_rel_value(item, 'hasRecorded{}Abstraction'\
                                                .format(rellink), cols)
            recordedattribute   = get_rel_value(item, 'hasRecorded{}Attribute'\
                                                .format(rellink), cols)

        
            recorded_context += add_context(recordedphenomenon, \
                        "This variable has the recorded {}phenomenon")\
                                            .format(rellink.lower()+' ')  
            recorded_context += add_context(recordedbody, \
                        "This variable has the recorded {}body")\
                                            .format(rellink.lower()+' ')  
            recorded_context += add_context(recordedmatter, \
                        "This variable has the recorded {}matter")\
                                            .format(rellink.lower()+' ')  
            recorded_context += add_context(recordedform, \
                        "This variable has the recorded {}form")\
                                            .format(rellink.lower()+' ')  
            recorded_context += add_context(recordedpart, \
                        "This variable has the recorded {}part")\
                                            .format(rellink.lower()+' ')  
            recorded_context += add_context(recordedtrajectory, \
                        "This variable has the recorded {}trajectory")\
                                            .format(rellink.lower()+' ')  
            recorded_context += add_context(recordedtrajdir, \
                        "This variable has the recorded {}trajectory direction")\
                                            .format(rellink.lower()+' ')  
            recorded_context += add_context(recordedprocess, \
                        "This variable has the recorded {}process")\
                                            .format(rellink.lower()+' ')  
            recorded_context += add_context(recordedrole, \
                        "This variable has the recorded {}role")\
                                            .format(rellink.lower()+' ')  
            recorded_context += add_context(recordedabstraction, \
                        "This variable has the recorded {}abstraction")\
                                            .format(rellink.lower()+' ')  
            recorded_context += add_context(recordedattribute, \
                        "This variable has the recorded {}attribute")\
                                            .format(rellink.lower()+' ')  
                

        recordedunits        = get_rel_value(item, 'hasRecordedUnits', cols)
        recordedproperty     = get_rel_value(item, 'hasRecordedProperty', cols)
        recordedmodproperty  = get_rel_value(item, 'hasRecordedModifiedProperty', cols)
        recordedapploperator = get_rel_value(item, 'hasRecordedAppliedOperator', cols)

        recorded_context += add_context(recordedunits, \
                        "This variable has the recorded units")
        recorded_context += add_context(recordedproperty, \
                        "This variable has the recorded property")
        recorded_context += add_context(recordedmodproperty, \
                        "This variable has the recorded modified property")
        recorded_context += add_context(recordedapploperator, \
                        "This variable has the recorded applied operator")
    
        text_body += """
                    <h4 id='{}'>{}</h4>""".format(address,label)
        def printp(cont):
            if cont != '':
                return """<p>
                        {}
                        </p>
                        """.format(cont)
            return ''
        
        text_body += printp(altlabel_cont)
        text_body += printp(abstr_cont)
        text_body += printp(plurality_cont)
        text_body += printp(wiki_context)
        text_body += printp(typeof_cont)
        text_body += printp(expras_cont)
        text_body += printp(parts_cont)
        text_body += printp(corrprop_cont)
        text_body += printp(attr_cont)
        text_body += printp(pos_cont)
        text_body += printp(isnoun_cont)
        text_body += printp(process_cont)
        text_body += printp(value_cont)
        text_body += printp(assocmatr_cont)
        text_body += printp(assunits_cont)
        text_body += printp(units_cont)
        text_body += printp(role_cont)
        text_body += printp(rel_cont)
        text_body += printp(assumpt_cont)
        text_body += printp(contains_context)
        text_body += printp(proptype_cont)
        text_body += printp(proprole_cont)
        text_body += printp(propquant_cont)
        text_body += printp(derivation_cont)
        text_body += printp(operator_cont)
        text_body += printp(hasprop_cont)
        text_body += printp(op_cont)
        text_body += printp(has_context)
        text_body += printp(unitsmod_cont)
        text_body += printp(recorded_context)
    text = head + text_body + foot
    return text
                
# look up term in ontology, return its class if exact match found
def search_class(cl):
    rel_discard = ['http://www.geoscienceontology.org/svo/svu#subLabel',
                   'http://www.w3.org/2000/01/rdf-schema#comment',
                   'http://www.w3.org/2000/01/rdf-schema#label']
                   #'http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
    sparql = SPARQLWrapper("http://sparql.geoscienceontology.org")
    if cl == 'Assumption':
        sparql.setQuery("""
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX svu: <http://www.geoscienceontology.org/svo/svu#>

                    SELECT ?entity ?rel ?value
                    WHERE {{ {{?entity a svu:{} .
                           ?entity ?rel ?value . }}
                           UNION {{
                           ?entity rdfs:subClassOf svu:{} .
                           ?entity ?rel ?value .
                           }} }}
                    ORDER BY ?entity
                    """.format(cl,cl))
    else:
        sparql.setQuery("""
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX svu: <http://www.geoscienceontology.org/svo/svu#>

                    SELECT ?entity ?rel ?value
                    WHERE {{
                            ?entity a svu:{} .
                            ?entity ?rel ?value .
                            }}
                    ORDER BY ?entity
                    """.format(cl,cl))
    sparql.setReturnFormat(sqjson)
    results = sparql.query().convert()

    data = pd.DataFrame(columns=['entity'])
    prev_entity = ''
    for result in results["results"]["bindings"]:
        entity = result["entity"]["value"].split('#')[1]
        rel = result["rel"]["value"]
        value = result["value"]["value"]
        if rel in rel_discard:
            continue
        if not rel in data.columns.values:
            data[rel]=''  
        if entity != prev_entity:
            prev_entity = entity
            index = len(data)
            data.loc[index] = ''
            data.loc[index,'entity'] = entity
        data.loc[index,rel] = (data.loc[index,rel] + \
            ', ' + value).lstrip(', ')

    return data.sort_values(by=['entity'])
#    return results

def write_to_file(ext,cl,desc):
    now = datetime.datetime.now(pytz.timezone("America/New_York"))
    test = search_class(cl)
    text = print_index_html(cl,test,desc,now)
    with open(ext+'index.html', 'w') as file:  # Use file to refer to the file object
        file.write(text)
    return test

desc_abstraction = """This is the documentation for the Abstraction Ontology. All instances of the Abstraction class are 
                listed here. An abstraction is a mental mathematical model that is applied to observed phenomena
                to approximate the spatiotemporal behavior of that phenomenon. Abstractions that are derived from
                physical theories are physical abstractions."""    
desc_assumption = """This is the documentation for the Assumption Ontology. All instances of the Assumption class are 
                listed here. This class is a temporary catchall for restrictions, contextual information, or
                model settings that may be necessary in scientific modeling. The instances
                in this category will be merged into other classes and other ontological concepts
                in future versions of the ontology.
                <br/><br/>
                To read more about assumptions, please visit the <a href="https://csdms.colorado.edu/wiki/CSN_Assumption_Names" target="_blank">CSDMS Standard Names documentation</a>."""   
desc_attribute = """This is the documentation for the Attribute Ontology. All instances of the Attribute class are 
                listed here. An attribute is a Property Value pair that collapses the possible state space of a Phenomenon
                or Abstraction
                and thus identifies the characteristics of that Phenomenon during a specific observation."""    
desc_body = """This is the documentation for the Body Ontology. All instances of the Body class are 
                listed here. A Body may be made of a substance (<code>Matter</code>) and
                may have and explicit <code>Form</code>."""
desc_context = """This is the documentation for the Context Ontology. All instances of the Context class are 
                listed here. This is a "blank node" class. It is a triple construct that combines a Phenomenon with
                a spatiotemporal context relationship."""
desc_form = """This is the documentation for the Form Ontology. All instances of the Form class are 
                listed here. A Form has spatial extent, but no substance."""
desc_matter = """This is the documentation for the Matter Ontology. All instances of the Matter class are 
                listed here. Matter has substance but no explicit form."""
desc_operator = """This is the documentation for the Operator Ontology. All instances of the Operator class are 
                listed here. Operators are relatively simple models that transform a quantitative property into
                another quantitative property.<br/><br/>
                Visit the <a href="https://csdms.colorado.edu/wiki/CSN_Operation_Templates" target = "_blank">CSDMS Standard Names site</a> 
                to view the standard name documentation for operations."""
desc_process = """This is the documentation for the Process Ontology. All instances of the Process class are 
                listed here. Process is a temporal phenomenon that describes the trajectory of one ore more
                spatial phenomena in space and time. If you would like to browse some notes on the linguistic cues
                of the Process category, please refer to the <a href="https://csdms.colorado.edu/wiki/CSN_Process_Names">
                CSN documentation</a>."""
desc_part = """This is the documentation for the Part Ontology. All instances of the Part class are 
                listed here. The part class is reserved for concepts that can be applied to a Body or an Abstraction,
                but that in and of themselves do not hold meaning. Examples include 
                bottom and top. Entities that sufficiently describe
                concepts in and of themselves but that are parts of other concepts are 
                attached to those concepts using the <a href="http://www.geoscienceontology.org/svo/svl/context">context</a> construct."""
desc_participant = """This is the documentation for the Participant Ontology. All instances of the Participant class are 
                listed here. This is a "blank node" class. It is a triple construct that combines a Phenomenon with
                a role for that Phenomenon and can be attached to a complex Phenomenon."""
desc_phenomenon = """This is the documentation for the Phenomenon Ontology. All instances of the Phenomenon class are 
                listed here. The Phenomenon namespace contains all phenomena that are not in the Body, Matter, Form or RolePhenomenon classes.
                The Phenomenon Class is significantly evolved from the original Object category outlined for the CSDMS Standard Names.
                To see the original documentation for the Object category, please visit the <a href="https://csdms.colorado.edu/wiki/CSN_Object_Templates" target="_blank">CSN website</a>."""
desc_property = """This is the documentation for the Property Ontology. All instances of the Property class are 
                listed here. The Property namespace contains all qualitative, standardized, 
                and quantitative property instances. Quantitative Properties map to the
                Quantity Kind class in QUDT. To reference the Quantity documentation from the
                CSDMS Standard Names, please visit the <a href="https://csdms.colorado.edu/wiki/CSN_Quantity_Templates" target="_blank">CSN Documentation</a>."""
desc_reference = """This is the documentation for the Reference Ontology. All instances of the Reference class are 
                listed here. This is a "blank node" class. It is a triple construct that combines a Phenomenon with
                a spatiotemporal reference relationship."""
desc_relationship = """This is the documentation for the Relationship Ontology. All instances of the Relationship class are 
                listed here. Relationships can be temporal or spatial or both and are used to define the Relationship 
                between the Phenomenon of interest and the <a href="http://www.geoscienceontology.org/svo/svl/context">Context</a> or <a href="http://www.geoscienceontology.org/svo/svl/reference">Reference</a> phenomenon in those constructs.
                """
desc_role = """This is the documentation for the Role Ontology. All instances of the Role class are 
                listed here. Roles can be applied to properties or phenomena (within the participant construct) to denote
                the roles they play in different scenarios.
                """
desc_rolephen = """This is the documentation for the Role Phenomenon Ontology. All instances of the Role Phenomenon class are 
                listed here. Role Phenomena are temporal phenomena that can be combined with different spatial phenomena to identify
                the way a phenomenon behaves in a scenario of interest. Whereas the Role class is dedicated to describing the
                generic roles that participants take in a described process, the Role Phenomenon class is dedicated to describing
                mental construct that is applied to the functionality of a phenomenon for an intended application.
                """
desc_trajectory = """This is the documentation for the Trajectory Ontology. All instances of the Trajectory class are 
                listed here. Trajectory is a spatiotemporal phenomenon that describes the 
                motion trajectory of one ore more spatial phenomena in space and time."""
desc_trajectorydir = """This is the documentation for the Trajectory Direction Ontology. All instances of the TrajectoryDirection class are 
                listed here. A Trajectory Direction is a spatial direction in which a trajectory is covered."""
desc_variable = """This is the documentation for the Variable Ontology. All instances of the Variable class are 
                listed here. To reference the original list of CSDMS Standard Names, please visit the 
                <a href="https://csdms.colorado.edu/wiki/CSN_Searchable_List" target="_blank">CSN website</a>."""

ext = '../core ontology files/svl/'
test = write_to_file(ext+'body/1.0.0/','Body',desc_body)
test = write_to_file(ext+'form/1.0.0/','Form',desc_form)
test = write_to_file(ext+'matter/1.0.0/','Matter',desc_matter)
test = write_to_file(ext+'process/1.0.0/','Process',desc_process)
test = write_to_file(ext+'part/1.0.0/','Part',desc_part)
test = write_to_file(ext+'attribute/1.0.0/','Attribute',desc_attribute)
test = write_to_file(ext+'trajectory/1.0.0/','Trajectory',desc_trajectory)
test = write_to_file(ext+'trajectorydirection/1.0.0/','TrajectoryDirection',desc_trajectorydir)
test = write_to_file(ext+'role/1.0.0/','Role',desc_role)
test = write_to_file(ext+'rolephenomenon/1.0.0/','RolePhenomenon',desc_rolephen)
test = write_to_file(ext+'relationship/1.0.0/','Relationship',desc_relationship)
test = write_to_file(ext+'abstraction/1.0.0/','Abstraction',desc_abstraction)
test = write_to_file(ext+'assumption/1.0.0/','Assumption',desc_assumption)
test = write_to_file(ext+'context/1.0.0/','Context',desc_context)
test = write_to_file(ext+'reference/1.0.0/','Reference',desc_reference)
test = write_to_file(ext+'operator/1.0.0/','Operator',desc_operator)
test = write_to_file(ext+'participant/1.0.0/','Participant',desc_participant)
test = write_to_file(ext+'phenomenon/1.0.0/','Phenomenon',desc_phenomenon)
test = write_to_file(ext+'property/1.0.0/','Property',desc_property)
test = write_to_file(ext+'variable/1.0.0/','Variable',desc_variable)
