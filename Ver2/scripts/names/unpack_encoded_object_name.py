#############################################################
#                      STEP 4                               #
#   Take annotated names and decompose them into atoms for  #
#   writing to the ontology file.                           #
#   input: source/csdms_annotated_names.csv                 #
#   output: source/csdms_atomized.csv                       #
#                                                           #
#############################################################

import csv
import pandas as pd
import os

# Read in reformatted variable names.
script_path  = os.path.dirname(__file__)
src_path     = os.path.join(script_path,'../../source/')
var_filename = 'csdms_annotated_names.csv'
var_filepath = os.path.join(src_path,var_filename)

debug_file = 'debug.txt'

f = open(var_filepath)
reader = csv.reader(f)
next(reader)

debug = open(debug_file,'w')
links = ['-contains-as-medium-','-contains-part-','-contains-',
         '-is-location-of-','-is-location-of-origin-of-',
         '-is-model-location-of-','-observes-','-models-',
         '-is-source-of-','-is-orbiting-center-of-',
         '-is-surrounded-by-','-is-driven-by-','-is-domain-of-',
         '-has-abstraction-','-has-model-abstraction-',
         '-has-part-','-has-form-','-has-matter-','-makes-up-',
         '-is-medium-matter-','-is-contained-matter-','-has-trajectory-',
         '-undergoes-process-','-as-main-','-as-main', '-as-first-main-',
         '-as-second-main-','-as-sink-','-as-source-','-as-source',
         '-as-in-','-as-in','-as-second-main',
         '-by-in-','-as-medium-','-as-medium','-as-numerator-',
         '-as-denominator-','-as-denominator','-as-minuend-',
         '-as-substrahend-','-as-subtrahend','-as-perspective-',
         '-as-origin-','-as-destination-','-participates-in-',
         '-measured-below-','-measured-above-','-measured-at-',
         '-measured-to-','-measured-from-','-measured-since-', '-measured-along-',
         '-going-over-','-into-','-out-of-','-wrt-',
         '-reference-for-computing-','-referenced-with-property-']

links.sort(key=len, reverse=True)

column_names = ['phenomenon_name']

lookup_dir = os.path.join(script_path,'../../source/quicklookup/')
categories_files = os.listdir(lookup_dir)
categories_files = [f for f in categories_files if f.endswith('txt') and '_' not in f]
categories = {}
for f in categories_files:
    filepath = os.path.join(lookup_dir,f)
    category_terms = [line.rstrip() for line in open(filepath)]
    category_name = f.split('.')[0]
    categories[category_name] = category_terms

categories_override = \
{
    'front': 'part',
    'cell':'abstraction',
    'expression':'abstraction',
    'building': 'phenomenon',
    'radiation': 'phenomenon',
    'vegetation': 'phenomenon',
    'link': 'form',
    'skin': 'phenomenon',
    'body': 'phenomenon',
    'neck': 'part',
    'grain': 'phenomenon',
}

intraobject_relations = ['-has-form-', '-has-abstraction-', '-has-matter-', '-has-part-', '-has-model-abstraction-']

def get_elements(encoded_object):

    # loop through characters in encoded_object
    open_paren = False
    contained_paren = 0
    subelement = []
    subelements = []
    add_to_stack = True
    stack = []
    for c in encoded_object:
        if (c == '(') and not open_paren:
            open_paren = True
            add_to_stack = False
        elif (c=='('):
            contained_paren += 1
            subelement.append(c)
        elif (c == ')') and (contained_paren > 0):
            contained_paren -= 1
            subelement.append(c)
        elif (c == ')'):
            open_paren = False
            add_to_stack = True
            subelements.append(''.join(subelement))
            stack.append('ELEMENT' + str(len(subelements)))
            subelement = []

        if c not in '()':
            if add_to_stack:
                stack.append(c)
            else:
                subelement.append(c)

    return (''.join(stack), subelements)

def get_all_elements(encoded_object):
    if encoded_object.count('(') == 0:
        return {encoded_object: []}
    outer_object, sub_elements = get_elements(encoded_object)
    all_sub_elements = {outer_object: sub_elements}
    for sub_element in sub_elements:
        sub_sub_elements = get_all_elements(sub_element)
        for k,v in sub_sub_elements.items():
            all_sub_elements[k] = v
    return all_sub_elements
    
all_elements = []
completed_elements = []
unlabeled_parts = []
for row in reader:
    old_varname,new_varname,object_name,quantity_name,encoded_obj_name = row
    sub_elements = get_all_elements(encoded_obj_name)
    for sub_element, element_list in sub_elements.items():
        temp_full_name = sub_element
        contained_links = {}
        for link in links:
            while link in temp_full_name:
                temp_full_name = temp_full_name.replace(link,'-',1)
                link_index = sub_element.find(link)
                while link_index in contained_links.keys():
                    link_index = sub_element.find(link,link_index+1)
                contained_links[link_index] = link
        contained_links = list(contained_links.items())
        contained_links.sort()
        remaining_full_name = sub_element
        contained_parts = []
        for link in contained_links:
            link_name = link[1]
            element = remaining_full_name.split(link_name,1)[0]
            remaining_full_name = remaining_full_name.split(link_name,1)[1]
            if 'ELEMENT' in element and len(element) > 8:
                element_parts = element.split('ELEMENT')
                element_parts = [element_parts[0], 'ELEMENT' + element_parts[1][0],
                                 element_parts[1][1:]]
                if '' in element_parts:
                    element_parts.remove('')
                contained_parts.extend(element_parts)
            else:
                contained_parts.append(element)
            contained_parts.append(link_name)
        if remaining_full_name != '':
            if 'ELEMENT' in remaining_full_name and len(remaining_full_name) > 8:
                element_parts = remaining_full_name.split('ELEMENT')
                element_parts = [element_parts[0], 'ELEMENT' + element_parts[1][0],
                                 element_parts[1][1:]]
                if '' in element_parts:
                    element_parts.remove('')
                contained_parts.extend(element_parts)
            else:
                contained_parts.append(remaining_full_name)

        name_elements = contained_parts[:]
        for number in range(len(element_list)):
            element_index = contained_parts.index(f'ELEMENT{number+1}')
            contained_parts[element_index] = element_list[number]
            name_elements[element_index] = '(' + element_list[number] + ')'

        complete_name = ''.join(name_elements)
        if not complete_name in completed_elements:
            completed_elements.append(complete_name)
            # skip outer elements around a single subobject, redundant
            if len(contained_parts) == 1:
                continue
            contained_parts_assigned = {}
            contained_parts_assigned['encoded_name'] = complete_name
            label_name = complete_name
            for link in links:
                label_name = label_name.replace(link,'_')
            label_name = label_name.strip('_')
            label_name = label_name.replace('(','').replace(')','')
            contained_parts_assigned['label_name'] = label_name

            indexes_added = []
            # parse the contained_parts list
            for link in links:
                link_index = 0
                while link_index!=-1:
                    if link in contained_parts[link_index:]:
                        link_index = contained_parts.index(link,link_index)
                    else:
                        link_index = -1
                    if link_index >= 0:
                        indexes_added.append(link_index)
                        if link == '-is-source-of-':
                            contained_parts_assigned['has-source-phenomenon'] = contained_parts[link_index - 1]
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-out-of-':
                            contained_parts_assigned['has-source-phenomenon'] = contained_parts[link_index + 1]
                            indexes_added.append(link_index + 1)
                        elif link == '-into-':
                            contained_parts_assigned['has-sink-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-going-over-':
                            contained_parts_assigned['has-adjacent-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-contains-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['has-containing-phenomenon'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-observes-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['is-observed-by'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-models-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['is-modeled-by'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-is-location-of-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['has-location'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-is-location-of-origin-of-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['has-location-of-origin'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-is-model-location-of-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['has-model-location'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-is-orbiting-center-of-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['orbits-around'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-is-surrounded-by-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['surrounds'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)  
                        elif link == '-is-domain-of-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['has-domain'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)  
                        elif link == '-is-driven-by-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['drives'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)                         
                        elif (link == '-as-medium-') and '-participates-in-' not in contained_parts:
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            indexes_added.append(link_index + 1)
                            contained_parts_assigned['has-medium-participant-phenomenon'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index - 1)
                        elif (link == '-as-medium-') and '-participates-in-' in contained_parts:
                            contained_parts_assigned['has-participating-medium-phenomenon'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index - 1)  
                        elif (link == '-participates-in-') and ('-as-medium-' not in contained_parts):
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['has-participating-primary-phenomenon'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-has-model-abstraction-':
                            contained_parts_assigned['is-modeled-by'] = contained_parts[link_index + 1]
                            indexes_added.append(link_index + 1)
                        elif link == '-contains-part-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['is-part-of-containing-phenomenon'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-contains-as-medium-':
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            contained_parts_assigned['has-containing-medium-phenomenon'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-makes-up-':
                            contained_parts_assigned['has-primary-matter'] = contained_parts[link_index - 1]
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-is-contained-matter-':
                            contained_parts_assigned['contains-matter'] = contained_parts[link_index - 1]
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index + 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        elif link == '-is-medium-matter-':
                            contained_parts_assigned['has-primary-matter'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index - 1)
                        elif link == '-by-in-':
                            contained_parts_assigned['has-in-participant-phenomenon'] = contained_parts[link_index + 1]
                            indexes_added.append(link_index + 1)
                        elif (link == '-as-main-') or (link == '-as-main'):
                            if 'has-primary-participant-phenomenon' in contained_parts_assigned.keys():
                                contained_parts_assigned['has-primary-participant-phenomenon2'] = contained_parts[link_index - 1]
                            else:
                                contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index - 1)
                        elif link.startswith('-as-'):
                            participant_type = link.replace('-as-','').strip('-').replace('-main','')
                            rel = f'has-{participant_type}-participant-phenomenon'
                            if rel in contained_parts_assigned.keys():
                                print('Error, two sources found.')
                                print(link, contained_parts)
                            else:
                                contained_parts_assigned[rel] = contained_parts[link_index - 1]
                                indexes_added.append(link_index - 1)
                        elif 'measured' in link or 'reference' in link:
                            rel = link.strip('-')
                            contained_parts_assigned[rel] = contained_parts[link_index + 1]
                            contained_parts_assigned['has-primary-participant-phenomenon'] = contained_parts[link_index - 1]
                            indexes_added.append(link_index + 1)
                            indexes_added.append(link_index - 1)
                        else: # -has-X- and -undergoes-process-
                            rel = link.strip('-').replace('wrt','measured-wrt')
                            if rel in contained_parts_assigned.keys():
                                rel = rel + '2'
                            contained_parts_assigned[rel] = contained_parts[link_index + 1]
                            indexes_added.append(link_index + 1)
                    if link_index >= 0:
                        link_index += 1
            printit = False
            if len(indexes_added) == (len(contained_parts) - 1):
                for i in range(len(contained_parts)):
                    if i not in indexes_added:
                        element = contained_parts[i]
                        element_root = element.split('~')[0]
                        rel = None
                        if element_root not in categories_override.keys() and element_root in categories['process']:
                            rel = 'undergoes-process'
                            printit = True
                        elif any(x in contained_parts for x in intraobject_relations) and '-undergoes-process-' not in contained_parts:
                            if element_root in categories_override.keys():
                                rel = 'has-' + categories_override[element]
                            else:
                                for cat,items in categories.items():
                                    if element_root in items:
                                        rel = 'has-' + cat
                                        break
                                if rel is None:
                                    rel = 'has-phenomenon'
                        else:
                            rel = 'has-primary-participant-phenomenon'
                        if rel in contained_parts_assigned.keys() and 'has-phenomenon' not in contained_parts_assigned.keys():
                            rel = 'has-phenomenon'
                        elif rel in contained_parts_assigned.keys():
                            print('ERROR')
                        contained_parts_assigned[rel] = contained_parts[i]
                        indexes_added.append(i)
                        break
            elif len(indexes_added) != len(contained_parts):
                continue # debug this

            indexes_added.sort()
            all_elements.append(contained_parts_assigned)
            if printit:
                debug.write(str(contained_parts_assigned) + '\n')

#print(all_elements)
#print(len(all_elements))
atomized_objects = pd.DataFrame()
for sub_phenomenon in all_elements:
    index = len(atomized_objects)
    for key, val in sub_phenomenon.items():
        atomized_objects.loc[index,key] = val

atomized_objects.to_csv(os.path.join(src_path,'csdms_atomized.csv'),index=False)
debug.close()