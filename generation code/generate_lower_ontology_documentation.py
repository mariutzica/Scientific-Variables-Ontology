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
        #print(label)
        altlabel = ''
        if 'http://www.w3.org/2004/02/skos/core#altLabel' in cols:
            altlabel = item['http://www.w3.org/2004/02/skos/core#altLabel']
        wikipedia = ''
        if svu_pref+'hasAssociatedWikipediaPage' in cols:
            wikipedia = item[svu_pref+'hasAssociatedWikipediaPage']
        nominalization = ''
        if svu_pref+'hasNominalization' in cols:
            nominalization = item[svu_pref+'hasNominalization']
        present_tense = ''
        if svu_pref+'hasPresentTense' in cols:
            present_tense = item[svu_pref+'hasPresentTense']
        present_participle = ''
        if svu_pref+'hasPresentParticiple' in cols:
            present_participle = item[svu_pref+'hasPresentParticiple']
        isnoun = ''
        if svu_pref+'isNoun' in cols:
            isnoun = item[svu_pref+'isNoun']

        trajectory = ''
        if svu_pref+'hasTrajectory' in cols:
            trajectory = item[svu_pref+'hasTrajectory']
        trajectorydir = ''
        if svu_pref+'hasTrajectoryDirection' in cols:
            trajectorydir = item[svu_pref+'hasTrajectoryDirection']        
        phenrole = ''
        if svu_pref+'hasRole' in cols:
            phenrole = item[svu_pref+'hasRole']
        phenomenon = ''
        if svu_pref+'hasPhenomenon' in cols:
            phenomenon = item[svu_pref+'hasPhenomenon']
        hasprocess = ''
        if svu_pref+'hasProcess' in cols:
            hasprocess = item[svu_pref+'hasProcess']
        part = ''
        if svu_pref+'hasPart' in cols:
            part = item[svu_pref+'hasPart']
        body = ''
        if svu_pref+'hasBody' in cols:
            body = item[svu_pref+'hasBody']
        matter = ''
        if svu_pref+'hasMatter' in cols:
            matter = item[svu_pref+'hasMatter']
        process = ''
        if svu_pref+'undergoesProcess' in cols:
            process = item[svu_pref+'undergoesProcess']
        desc_process = ''
        if svu_pref+'describesProcess' in cols:
            desc_process = item[svu_pref+'describesProcess']
        expras = ''
        if svu_pref+'isExpressedAs' in cols:
            expras = item[svu_pref+'isExpressedAs']
        form = ''
        if svu_pref+'hasForm' in cols:
            form = item[svu_pref+'hasForm']
        attributes = ''
        if svu_pref + 'hasAttribute' in cols:
            attributes = item[svu_pref+'hasAttribute']
        plurality = ''
        if svu_pref + 'isPluralityOf' in cols:
            plurality = item[svu_pref+'isPluralityOf']
        typeof = ''
        if svu_pref+'isTypeOf' in cols:
            typeof = item[svu_pref+'isTypeOf']
        corr_prop = ''
        if svu_pref+'correspondsToProperty' in cols:
            corr_prop = item[svu_pref+'correspondsToProperty']
        value = ''
        if svu_pref+'hasValue' in cols:
            value = item[svu_pref+'hasValue']
        assocmatr = ''
        if svu_pref+'hasAssociatedMatter' in cols:
            assocmatr = item[svu_pref+'hasAssociatedMatter']
        assunits = ''
        if svu_pref+'hasAssignedUnits' in cols:
            assunits = item[svu_pref+'hasAssignedUnits']
        units = ''
        if svu_pref+'hasUnits' in cols:
            units = item[svu_pref+'hasUnits']  
        context = ''
        if svu_pref+'hasContext' in cols:
            context = item[svu_pref+'hasContext']
        reference = ''
        if svu_pref+'hasReference' in cols:
            reference = item[svu_pref+'hasReference']
        contextrel = ''
        if svu_pref+'hasContextRelationship' in cols:
            contextrel = item[svu_pref+'hasContextRelationship']
        refrel = ''
        if svu_pref+'hasReferenceRelationship' in cols:
            refrel = item[svu_pref+'hasReferenceRelationship']
        partrole = ''
        if svu_pref+'hasParticipantRole' in cols:
            partrole = item[svu_pref+'hasParticipantRole']
        participant = ''
        if svu_pref+'hasParticipantObject' in cols:
            participant = item[svu_pref+'hasParticipantObject']
        medium = ''
        if svu_pref+'hasMediumObject' in cols:
            medium = item[svu_pref+'hasMediumObject']
        contextobj = ''
        if svu_pref+'hasObject' in cols:
            contextobj = item[svu_pref+'hasObject']
        headop = ''
        if svu_pref+'hasHeadOperator' in cols:
            headop = item[svu_pref+'hasHeadOperator']
        modop = ''
        if svu_pref+'modifiesOperator' in cols:
            modop = item[svu_pref+'modifiesOperator']
        multunits = ''
        if svu_pref+'hasMultiplierUnits' in cols:
            multunits = item[svu_pref+'hasMultiplierUnits'] 
        powfunits = ''
        if svu_pref+'hasPowerFactor' in cols:
            powfunits = item[svu_pref+'hasPowerFactor'] 
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
        assumpt = ''
        if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in cols and cl == 'Assumption':
            assumpt = item['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
        abstraction = ''
        if svu_pref+'hasAbstraction' in cols:
            abstraction = item[svu_pref+'hasAbstraction']  
        abstractedby = ''
        if svu_pref+'isAbstractedBy' in cols:
            abstractedby = item[svu_pref+'isAbstractedBy']  
        quantprocess = ''
        if svu_pref+'quantifiesProcess' in cols:
            quantprocess = item[svu_pref+'quantifiesProcess']  
        processdef = ''
        if svu_pref+'isDefinedBy' in cols:
            processdef = item[svu_pref+'isDefinedBy']  
        propertytype = ''
        if svu_pref+'hasPropertyType' in cols:
            propertytype = item[svu_pref+'hasPropertyType']  
        propertyrole = ''
        if svu_pref+'hasPropertyRole' in cols:
            propertyrole = item[svu_pref+'hasPropertyRole']  
        propertyquant = ''
        if svu_pref+'hasPropertyQuantification' in cols:
            propertyquant = item[svu_pref+'hasPropertyQuantification']  
        operator = ''
        if svu_pref+'hasOperator' in cols:
            operator = item[svu_pref+'hasOperator']  
        derivation = ''
        if svu_pref+'isDerivedFrom' in cols:
            derivation = item[svu_pref+'isDerivedFrom'] 
        condattr = ''
        if svu_pref+'hasConditionalAttribute' in cols:
            condattr = item[svu_pref+'hasConditionalAttribute']  
        hasproperty = ''
        if svu_pref+'hasProperty' in cols:
            hasproperty = item[svu_pref+'hasProperty']  

        
        containscontext = ''
        if svu_pref+'containsContext' in cols:
            containscontext = item[svu_pref+'containsContext']  
        containscontextobj = ''
        if svu_pref+'containsContextObject' in cols:
            containscontextobj = item[svu_pref+'containsContextObject']  
        containsmedobj = ''
        if svu_pref+'containsMediumObject' in cols:
            containsmedobj = item[svu_pref+'containsMediumObject']  

        wiki_context = ''
        if wikipedia!='' and not '#' in wikipedia:
            pagename = wikipedia.split('/')[-1]
            if 'index.php' in pagename:
                pagename = pagename.split('title=')[1].split('&')[0]
            query_url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles={}&exintro=&exsentences=2&explaintext=&redirects=&format=json".format(pagename)
            r = requests.get(url = query_url)
            temp = r.json()
            for _,val in temp['query']['pages'].items():
                try:
                    wiki_context = val['extract']
                except:
                    print('Wikipedia page {} not valid.'.format(wikipedia))
        if wiki_context!='':
            wiki_cont = """\n
            This instance has a related <a href="{}" target="_blank">Wikipedia page</a>. Short extract:<br/> 
            <em>{}</em>
            """.format(wikipedia,''.join(wiki_context))
        else:
            wiki_cont = ''

        
        typeof_cont = ''
        if typeof != '':
            for typ in typeof.split(', '):
                typeof_pref = typ.split('#')[0].split('/')[-1]
                typeof_id = typ.split('#')[1]
                if typeof_pref == cl.lower():
                    try:
                        typeof_label = items.loc[items['entity']==typeof_id,'http://www.w3.org/2004/02/skos/core#prefLabel'].iloc[0]            
                        typeof_cont = """\n
                            This instance is a narrower concept derived from <a href="#{}">{}</a>.
                            """.format(typeof_id,typeof_label)
                    except:
                        print('typeof {} inheritance not found.'.format(typeof_id))
                else:
                    typ_url = typ.split('/')[-1].replace('#','#')
                    typeof_cont = """\n
                        This instance is a narrower concept derived from <a href="http://www.geoscienceontology.org/svo/svl/{}">{}</a>.
                        """.format(typ_url,typeof_id)

        process_cont = ''
        if process != '':
            for p in process.split(', '):
                process_label = p.split('#')[1]
                process_cont += """\n
                    This instance describes something undergoing the process <a href="{}">{}</a>.
                """.format(p,process_label)
        if desc_process != '':
            for p in desc_process.split(', '):
                process_label = p.split('#')[1]
                process_cont += """\n
                    This instance describes the process <a href="{}">{}</a>.
                """.format(p,process_label)
        if quantprocess != '':
            for p in quantprocess.split(', '):
                process_label = p.split('#')[1]
                process_cont += """\n
                    This instance quantifies the process <a href="{}">{}</a>.
                """.format(p,process_label)
        if processdef != '':
            for p in processdef.split(', '):
                process_label = p.split('#')[1]
                process_cont += """\n
                    This instance is defined by the process <a href="{}">{}</a>.
                """.format(p,process_label)
        if hasprocess != '':
            for p in hasprocess.split(', '):
                process_label = p.split('#')[1]
                process_cont += """\n
                    This instance describes the process <a href="{}">{}</a>.
                """.format(p,process_label)
                
        plurality_cont = ''
        if plurality != '':
            plurality_id = plurality.split('#')[1]
            plurality_label = items.loc[items['entity']==plurality_id,'http://www.w3.org/2004/02/skos/core#prefLabel'].iloc[0]            
            plurality_cont = """\n
            This instance is a plurality of <a href="#{}">{}</a>.
            """.format(plurality_id,plurality_label)

        value_cont = ''
        if value != '':
            value_cont = """\n
            Attribute corresponds to property value {}.
            """.format(value)
        
        assunits_cont = ''
        if assunits != '':
            assunits_cont = """\n
            Attribute has the assigned units {}.
            """.format(assunits)
            
        pos_cont = ''
        if present_tense != '' or present_participle != '' or nominalization != '':
            pos_cont = """\n
            This instance has the following language cues:<div><ul>
            """
            if present_tense != '':
                pos_cont += """<li>present tense: {}</li>""".format(present_tense)
            if present_participle != '':
                pos_cont += """<li>present participle: {}</li>""".format(present_participle)
            if nominalization != '':
                pos_cont += """<li>nominalization: {}</li>""".format(nominalization)
            pos_cont += '</ul></div>'
            
        expras_cont = ''
        if expras != '':
            expras_id = expras.split('#')[1]
            try:
                expras_label = items.loc[items['entity']==expras_id,'http://www.w3.org/2004/02/skos/core#prefLabel'].iloc[0]
                expras_cont = """\n
                    The property of this substance is expressed with respect to the substance <a href="#{}">{}</a>.
                    """.format(expras_id,expras_label)
            except:
                expras_label = expras_id
                expras_cont = """\n
                The property of this substance is expressed with repspect to the substance <a href="http://www.geoscienceontology.org/matter#{}">{}</a>.
                """.format(expras_id,expras_label)
            

        altlabel_cont = ''
        if altlabel != '':
            altlabel_cont = """\n
            Alternative labels for this instance are: {}.
            """.format(altlabel)

        partrole_cont = ''
        if partrole != '':
            partrole_label = partrole.split('#')[1]
            partrole_cont = """\n
            The role for this participant is <a href="http://www.geoscienceontology.org/svo/svl/role#{}">{}</a>.
            """.format(partrole_label, partrole_label)

        corrprop_cont = ''
        if corr_prop != '':
            corr_prop_label = corr_prop.split('#')[1]                               
            corrprop_cont = """\n
            This attribute pertains to the property: <a href="http://www.geoscienceontology.org/svo/svl/property#{}">{}</a>.
            """.format(corr_prop_label, corr_prop_label)
        
        assocmatr_cont = ''
        if assocmatr != '':
            assocmatr_label = assocmatr.split('#')[1]                               
            assocmatr_cont = """\n
            This attribute inherently refers to a state of the matter instance: <a href="http://www.geoscienceontology.org/svo/svl/matter#{}">{}</a>.
            """.format(assocmatr_label, assocmatr_label)
        
        op_cont = ''
        if headop != '':
            headop_label = headop.split('#')[1] 
            modop_label = modop.split('#')[1]
            op_cont = """\n
            This compound operator has the head operator <a href="http://www.geoscienceontology.org/svo/svl/operator#{}">{}</a>
            and modifies the operator <a href="http://www.geoscienceontology.org/svo/svl/operator#{}">{}</a>.
            """.format(headop_label, headop_label, modop_label, modop_label)
            
        isnoun_cont = ''
        if isnoun != '':
            if isnoun == 'true':
                isnoun_cont = """\n
                This attribute is expressed as a noun.
                """
            else:
                isnoun_cont = """\n
                This attribute is expressed as an adjective.
                """
            
        attr_cont = ''
        if attributes != '':
            attr_cont = """\n
            This instance has the following attributes:<div><ul>
            """
            for attr in attributes.split(', '):
                attr_label = attr.split('#')[1]
                attr_cont += """<li><a href="{}">{}</a></li>""".format(attr,attr_label)
            attr_cont += '</ul></div>'

        units_cont = ''
        if units != '':
            for unit in units.split(', '):
                if unit != assunits:
                    units_cont = """\n
                    This instance has the dimensional units string {}.
                    """.format(unit)
        
        unitsmod_cont = ''
        if powfunits != '' and powfunits != 'none':
            unitsmod_cont = """\n
                    This operator modifies the units of the property it is applied to by
                    raising the units to the power of {}.
                    """.format(powfunits)
                    
        if multunits != '' and multunits != 'none':
            unitsmod_cont = """\n
                    This operator modifies the units of the property it is applied to by
                    multiplying those units by the units {}.
                    """.format(multunits)
        
        context_cont = ''
        if context != '':
            context_label = urllib.parse.unquote(context.split('#')[1])
            context_label = context_label.replace('%7E','~')                                                               
            context_cont = """\n
                    This instance has the context <a href="{}">{}</a>.
                    """.format(context,context_label)

        reference_cont = ''
        if reference != '':
            reference_label = urllib.parse.unquote(reference.split('#')[1])
            reference_label = reference_label.replace('%7E','~')
            reference_cont = """\n
                    This instance has the reference <a href="{}">{}</a>.
                    """.format(reference,reference_label)

        contains_cont = ''
        if containscontext != '':
            for c in containscontext.split(', '):
                context_label = urllib.parse.unquote(c.split('#')[1])
                context_label = context_label.replace('%7E','~')
                contains_cont += """\n
                    <p>This instance contains the context <a href="{}">{}</a>.</p>
                    """.format(c,context_label)
        if containscontextobj != '':
            for c in containscontextobj.split(', '):
                context_label = urllib.parse.unquote(c.split('#')[1])
                context_label = context_label.replace('%7E','~')
                contains_cont += """\n
                    <p>This instance contains context with respect to the object <a href="{}">{}</a>.</p>
                    """.format(c,context_label)
        if containsmedobj != '':
            for c in containsmedobj.split(', '):
                context_label = urllib.parse.unquote(c.split('#')[1])
                context_label = context_label.replace('%7E','~')
                contains_cont += """\n
                    <p>This instance contains context with respect to the medium <a href="{}">{}</a>.</p>
                    """.format(c,context_label)
                    
        contextrel_cont = ''
        if contextrel != '':
            rel_label = contextrel.split('#')[1]
            contextrel_cont = """\n
                    This instance represents the context relationship <a href="{}">{}</a>.
                    """.format(contextrel,rel_label)
        
        refrel_cont = ''
        if refrel != '':
            rel_label = refrel.split('#')[1]
            refrel_cont = """\n
                    This instance represents the reference relationship <a href="{}">{}</a>.
                    """.format(refrel,rel_label)
                    
        contextobj_cont = ''
        if contextobj != '' and cl != 'Phenomenon':
            obj_id = max(contextobj.split(', '), key=len)
            obj_label = urllib.parse.unquote(obj_id.split('#')[1])
            obj_label = obj_label.replace('%7E','~')
            contextobj_cont = """\n
                    This instance represents the object <a href="{}">{}</a>.
                    """.format(obj_id,obj_label)
        elif contextobj != '':
            contextobj_cont = """\n
                    This instance refers to the following objects: <div><ul>
                    """
            for c in contextobj.split(', '):
                obj_label = urllib.parse.unquote(c.split('#')[1])
                obj_label = obj_label.replace('%7E','~')
                contextobj_cont += """\n
                    <li><a href="{}">{}</a></li>
                    """.format(c,obj_label)
            contextobj_cont += '</ul></div>\n'
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

        participant_cont = ''
        if participant != '':
            participant_cont = """\n
            This phenomenon describes the following participants: <div><ul>
            """
            for p in participant.split(', '):
                p_label = urllib.parse.unquote(p.split('#')[1])
                p_label = p_label.replace('%7E','~')
                participant_cont += \
                """<li><a href="{}">{}</a></li>""".format(p,p_label)
            participant_cont += "</ul></div>"
            
        medium_cont = ''
        if medium != '':
            medium_label = urllib.parse.unquote(medium.split('#')[1])
            medium_label = medium_label.replace('%7E','~')
            medium_cont = """\n
            This phenomenon has the Medium Object:<a href="{}">{}</a>.
            """.format(medium,medium_label)

        proptype_cont = ''
        if propertytype != '':
            pt_label = urllib.parse.unquote(propertytype.split('#')[1])
            pt_label = pt_label.replace('%7E','~')
            proptype_cont = """\n
            This instance has the property type:<a href="{}">{}</a>.
            """.format(propertytype,pt_label)

        proprole_cont = ''
        if propertyrole != '':
            pr_label = urllib.parse.unquote(propertyrole.split('#')[1])
            pr_label = pr_label.replace('%7E','~')
            proprole_cont = """\n
            This instance has the property role:<a href="{}">{}</a>.
            """.format(propertyrole,pr_label)

        propquant_cont = ''
        if propertyquant != '':
            pq_label = urllib.parse.unquote(propertyquant.split('#')[1])
            pq_label = pq_label.replace('%7E','~')
            propquant_cont = """\n
            This instance has the property quantification:<a href="{}">{}</a>.
            """.format(propertyquant,pq_label)

        derivation_cont = ''
        if derivation != '':
            d_label = urllib.parse.unquote(derivation.split('#')[1])
            d_label = d_label.replace('%7E','~')
            derivation_cont = """\n
            This instance has is derived from:<a href="{}">{}</a>.
            """.format(derivation,d_label)

        operator_cont = ''
        if operator != '':
            o_label = urllib.parse.unquote(operator.split('#')[1])
            o_label = o_label.replace('%7E','~')
            operator_cont = """\n
            This instance has the applied operator:<a href="{}">{}</a>.
            """.format(operator,o_label)

        hasprop_cont = ''
        if hasproperty != '':
            p_label = urllib.parse.unquote(hasproperty.split('#')[1])
            p_label = p_label.replace('%7E','~')
            hasprop_cont = """\n
            This instance describes the property: <a href="{}">{}</a>.
            """.format(hasproperty,p_label)

#        condattr_cont = ''
#        if condattr != '':
#            ca_label = urllib.parse.unquote(condattr.split('#')[1])
#            ca_label = ca_label.replace('%7E','~')
#            condattr_cont = """\n
#            This instance is dependent on the conditional attribute:<a href="{}">{}</a>.
#            """.format(condattr,ca_label)

        abstr_cont = ''
        if abstractedby != '':
            abstractedby_label = abstractedby.split('#')[1]
            if abstraction != '':
                abstraction_label = abstraction.split('#')[1]
                abstr_cont = """\n
                    This abstraction represents <a href="#{}">{}</a> as abstracted by <a href="#{}">{}</a>.
                    """.format(abstraction_label, abstraction_label, abstractedby_label, abstractedby_label)
            else:
                abstr_cont = """\n
                    This phenomenon is abstracted by <a href="{}">{}</a>.
                    """.format(abstractedby, abstractedby_label)
        assumpt_cont = ''
        if assumpt != '':
            for a in assumpt.split(', '):
                if 'geoscienceontology' in a:
                    assumpt_label = a.split('#')[1]
                    if assumpt_label != 'Assumption':
                        assumpt_cont += """\n
                            <p>This assumption falls in the broader category <a href="#{}">{}</a>.</p>
                            """.format(assumpt_label, assumpt_label)
            
        parts_cont = ''
        if matter != '' or body != '' or part != '' or form != '' or trajectory != '' or trajectorydir != '' or phenrole != '' or phenomenon != '':
            parts_cont = """This instance has the following components:<div><ul>"""
        if phenomenon != '':
            phen_label = phenomenon.split('#')[1]
            parts_cont += """<li>phenomenon: <a href="{}">{}</a></li>""".format(phenomenon,phen_label)
        if matter != '':
            matter_label = matter.split('#')[1]
            parts_cont += """<li>matter (substance): <a href="{}">{}</a></li>""".format(matter,matter_label)
        if form != '':
            form_label = form.split('#')[1]                                    
            parts_cont += """<li>form: <a href="{}">{}</a></li>""".format(form,form_label)
        if body != '':
            body_label = body.split('#')[1]
            body_url = body.split('/')[-1].replace('#','#')
            parts_cont += """<li>body: <a href="http://www.geoscienceontology.org/svo/svl/{}">{}</a></li>""".format(body_url,body_label)
        if part != '':
            part_label = part.split('#')[1]
            part_url = part.split('/')[-1].replace('#','#')
            parts_cont += """<li>part: <a href="http://www.geoscienceontology.org/svo/svl/{}">{}</a></li>""".format(part_url,part_label)
        if trajectory != '':
            traj_label = trajectory.split('#')[1]
            parts_cont += """<li>trajectory (path): <a href="{}">{}</a></li>""".format(trajectory,traj_label)
        if trajectorydir != '':
            traj_label = trajectorydir.split('#')[1]
            parts_cont += """<li>trajectory direction: <a href="{}">{}</a></li>""".format(trajectorydir,traj_label)
        if phenrole != '':
            role_label = phenrole.split('#')[1]
            parts_cont += """<li>role: <a href="{}">{}</a></li>""".format(phenrole,role_label)
        if parts_cont != '':
            parts_cont += '</ul></div>'
    
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
        text_body += printp(wiki_cont)
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
        text_body += printp(contains_cont)
        text_body += printp(reference_cont)
        text_body += printp(participant_cont)
        text_body += printp(medium_cont)
        text_body += printp(proptype_cont)
        text_body += printp(proprole_cont)
        text_body += printp(propquant_cont)
        text_body += printp(derivation_cont)
        text_body += printp(operator_cont)
        text_body += printp(hasprop_cont)
#        text_body += printp(condattr_cont)
        if cl!='Phenomenon' and cl!='Property' and cl!='Variable':
            text_body += printp(contextrel_cont)
            text_body += printp(refrel_cont)
            text_body += printp(partrole_cont)
            text_body += printp(op_cont)
            text_body += printp(unitsmod_cont)
        if cl!='Property':
            text_body += printp(context_cont)
            text_body += printp(contextobj_cont)
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

ext = '../core ontology files/'
#test = write_to_file(ext+'body/','Body',desc_body)
#test = write_to_file(ext+'form/','Form',desc_form)
#test = write_to_file(ext+'matter/','Matter',desc_matter)
#test = write_to_file(ext+'process/','Process',desc_process)
#test = write_to_file(ext+'part/','Part',desc_part)
#test = write_to_file(ext+'attribute/','Attribute',desc_attribute)
#test = write_to_file(ext+'trajectory/','Trajectory',desc_trajectory)
#test = write_to_file(ext+'trajectorydirection/','TrajectoryDirection',desc_trajectorydir)
#test = write_to_file(ext+'role/','Role',desc_role)
#test = write_to_file(ext+'rolephenomenon/','RolePhenomenon',desc_rolephen)
#test = write_to_file(ext+'relationship/','Relationship',desc_relationship)
#test = write_to_file(ext+'abstraction/','Abstraction',desc_abstraction)
#test = write_to_file(ext+'assumption/','Assumption',desc_assumption)
#test = write_to_file(ext+'context/','Context',desc_context)
test = write_to_file(ext+'reference/','Reference',desc_reference)
#test = write_to_file(ext+'operator/','Operator',desc_operator)
#test = write_to_file(ext+'participant/','Participant',desc_participant)
#test = write_to_file(ext+'phenomenon/','Phenomenon',desc_phenomenon)
#test = write_to_file(ext+'property/','Property',desc_property)
#test = write_to_file(ext+'variable/','Variable',desc_variable)
