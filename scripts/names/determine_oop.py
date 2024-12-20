#############################################################
#                         STEP 3                            #
#   Determine the order of operations nesting for tagged    #
#   terms. Output with relationship links inserted for _    #
#   and parantheses separating out inter-object terms       #
#   input: source/variable_name_tags.csv                    #
#   output: 'source/csdms_annotated_names.csv'              #
#                                                           #
#############################################################

import os
import pandas as pd
import csv

# Read in reformatted variable names.
script_path  = os.path.dirname(__file__)
src_path     = os.path.join(script_path,'../../source/')
var_filename = 'variable_name_tags.csv'
var_filepath = os.path.join(src_path,var_filename)


f = open(var_filepath, 'r')
reader = csv.reader(f)
next(reader)

def loop_on_pattern(pattern, pattern_replace, obj_pat_str, obj_name, pat_list, replace_str, combinations = None, printout = False):
    current_loc = 0
    while (current_loc >= 0) and (current_loc < len(obj_pat_str)):
        try:
            term_loc = obj_pat_str[current_loc:].index(pattern)
        except:
            break
        term_loc = current_loc + term_loc
        current_loc = term_loc + 1
        num_terms = len(pattern.split('_'))
        prev_terms = len(obj_pat_str[0:term_loc].split('_')) - 1
        found_pat = '_'.join(obj_name.split('_')[prev_terms:prev_terms+num_terms])

        if printout:
            print(found_pat, term_loc, current_loc, len(obj_pat_str), obj_pat_str, obj_name)
        if not combinations or found_pat in combinations:
            if found_pat not in pat_list:
                pat_list.append(found_pat)
            obj_pat_str = obj_pat_str[0:term_loc] + obj_pat_str[term_loc:].replace(pattern,pattern_replace,1)

            pat_replace = found_pat
            for replace_set in replace_str:
                pat_replace = pat_replace.replace(replace_set[0],replace_set[1])
            pat_replace = '(' + pat_replace + ')'
            obj_name = obj_name.replace(found_pat, pat_replace,1)
            if printout:
                print(found_pat, obj_name, obj_pat_str)

    return (obj_pat_str, obj_name, pat_list)

verbose = False

phen_phen_list = []
all_object_patterns = []
final_data = []
for row in reader:
    original_name,variable_name,object_name,quantity_name,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,object_pattern,quantity_pattern = row

    current_data_row = [original_name, variable_name, object_name, quantity_name]
    object_pattern_expanded = object_pattern.split('_')
    object_pattern_simple = [obj.split('~')[0] for obj in object_pattern_expanded]
    object_pattern_simple_str = '_'.join(object_pattern_simple)
    #if '-or-' in variable_name:
    #    print(variable_name, object_pattern_simple_str)        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_ABSTRACTION_ABSTRACTION_ABSTRACTION_ABSTRACTION':
        while 'PHENOMENON_ABSTRACTION' in object_pattern_simple_str:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
    
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_PHENOMENON_PART_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-medium-matter-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
    
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_PHENOMENON_PHENOMENON_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['wave_seismic-station_arrival','wave-as-main-seismic-station-as-sink-arrival'],
                                              ['wave_seismic-station_travel','wave-as-main-seismic-station-as-sink-travel']], printout=False )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_PART_PHENOMENON_FORM_PHENOMENON_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        groupings = ['(stream-has-form-channel)_reach']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-sink-water-undergoes-process-'],
                                              ['_','-as-source-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_FORM_PHENOMENON_FORM_PHENOMENON_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        groupings = ['(stream-has-form-channel)_reach']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'ROLE_ROLE_FORM_PHENOMENON-and-PHENOMENON-as-MATTER_PROCESS':
        object_pattern_simple_str = 'ROLE_ROLE_FORM_PHENOMENON-and-PHENOMENON_as-MATTER_PROCESS'
        object_name = object_name.replace('-as-','_as-')
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON-and-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_as-MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_', '-expressed-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_PHENOMENON_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_tide_','-is-medium-matter-tide-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'ROLE_ROLE_FORM_PHENOMENON-and-PHENOMENON_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON-and-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_biomass_','-as-sink-biomass-undergoes-process-']] )
        
    if object_pattern_simple_str == 'MATTER_ABSTRACTION_PART_MATTER_PROCESS_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_profile_','-has-abstraction-profile-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        groupings = ['(water-undergoes-process-drainage)_(ammonium-undergoes-process-leaching)',
                     '(water-undergoes-process-drainage)_(nitrate-undergoes-process-leaching)']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-as-medium-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_FORM_ABSTRACTION_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        groupings = ['(fault-has-abstraction-plane)_asperity']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']], combinations=groupings )
        groupings = ['earthquake_((fault-has-abstraction-plane)-contains-asperity)']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']], combinations=groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']])
        
    if object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_PHENOMENON_FORM_PART_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']])
        groupings = ['(land-has-part-subsurface)_aquifer~left','(land-has-part-subsurface)_aquifer~right']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']], combinations=groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_channel_','-has-form-channel-has-part-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [[')_(',')-as-source-('],
                                                ['_','-as-sink-']])
         
    if object_pattern_simple_str == 'PHENOMENON_FORM_PHENOMENON_ABSTRACTION_MATTER_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_FORM_PHENOMENON_PART_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-sink-water-undergoes-process-'],
                                              ['_','-as-source-']])

    if (object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_FORM_ABSTRACTION_ABSTRACTION_ABSTRACTION') or \
        (object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_FORM') or \
        (object_pattern_simple_str == 'PROCESS_PHENOMENON_ABSTRACTION_MATTER_FORM') or \
        (object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_FORM_PROCESS') or \
        (object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_FORM_ABSTRACTION'):
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['shoreline)_','shoreline)-is-location-of-'],
                                                ['_','-contains-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PROCESS_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-observes-']])

    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_at-PROPERTY':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROPERTY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_at-speed','-reference-for-determination-of-property-speed'],
                                                ['_at-','-determined-at-property-']])
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_ABSTRACTION_PHENOMENON_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_ABSTRACTION_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_plane','-has-abstraction-plane'],
                                                ['_','-is-location-of-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_rising','-undergoes-process-rising'],
                                              ['_setting','-undergoes-process-setting'],
                                                ['_','-as-perspective-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['plane)_','plane)-wrt-'],
                                                ['_','-as-perspective-']])
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_ROLE_MATTER_PROCESS_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']])
        groupings = ['distributary_(outlet-contains-((water-undergoes-process-flowing)-has-abstraction-x-section))']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations=groupings)
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']])

    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_ROLE_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_projectile_','-as-source-projectile-undergoes-process-']])
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_PHENOMENON_PROCESS':
        if 'seismic-wave' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_seismic-station_arrival','-as-main-seismic-station-as-sink-arrival'],
                                              ['_seismic-station_travel','-as-main-seismic-station-as-sink-travel']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
               object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        if 'seismograph' in object_name:
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-is-location-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_ABSTRACTION_PHENOMENON' or \
        object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        groupings = ['(earth-has-part-interior)_(earthquake-has-abstraction-hypocenter)',
                     '(earth-has-part-interior)_(earthquake-has-abstraction-focus)']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_seismic-station','-as-main-seismic-station-as-main']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_ROLE_MATTER_MATTER_MATTER_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        groupings = ['sediment_(sand-has-form-grain)']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']], combinations = groupings)
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        groupings = ['(channel~main-has-part-entrance)_(water-contains-(sediment-contains-(sand-has-form-grain)))']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_FORM_PHENOMENON_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        groupings = ['(stream-has-form-channel)_reach']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-sink-water-undergoes-process-'],
                                                ['_','-as-source-']])
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_PHENOMENON_MATTER' or \
        object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
       
    if object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_FORM_ABSTRACTION_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_ABSTRACTION_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_FORM_ABSTRACTION_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_channel_','-has-form-channel-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_ABSTRACTION_ROLE':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ABSTRACTION_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'ROLE_TRAJECTORY_ABSTRACTION_PHENOMENON_ABSTRACTION' or \
        object_pattern_simple_str == 'ROLE_TRAJECTORY_ABSTRACTION_PHENOMENON' or \
        object_pattern_simple_str == 'ROLE_TRAJECTORY_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_TRAJECTORY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-trajectory-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_(land-has-abstraction-surface)','-as-main-(land-has-abstraction-surface)-as-main'],
                                                ['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_MATTER_PROCESS_at-PROPERTY':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        if 'reference' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROPERTY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_at-','-reference-for-determination-of-property-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROPERTY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-at-property-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_MATTER_PROCESS':
        groupings = ['storm_water']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-source-water-undergoes-process-']] )
        groupings= ['(storm-is-source-of-water)_surge']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']], combinations=groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [[')_(',')-as-source-('],
                                                ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [[')_(v',')-is-location-of-(v'],
                                                ['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_ROLE_MATTER_PROCESS_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        groupings = ['(channel~main-has-part-entrance)_((water-undergoes-process-flowing)-has-abstraction-x-section)']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_PHENOMENON_MATTER_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PHENOMENON_MATTER_PROCESS':
        groupings = ['vegetation_canopy']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations = groupings )
        if 'titan' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-surrounded-by-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_evaporation','-as-source-water-undergoes-process-evaporation'],
                                              ['_water_transpiration','-as-source-water-undergoes-process-transpiration'],
                                              ['_methane_','-as-source-methane-undergoes-process-'],
                                              ['_water_','-as-sink-water-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_ABSTRACTION_ABSTRACTION' or \
        object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_ABSTRACTION':
        while 'PHENOMENON_ABSTRACTION' in object_pattern_simple_str:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_viewpoint','-is-location-of-viewpoint'],
                                              ['_base-level','-has-model-abstraction-base-level'],
                                              ['_axis~east','-as-first-main-axis~east-as-second-main'],
                                              ['_','-has-abstraction-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_PHENOMENON_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )

    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_PROCESS_PHENOMENON_MATTER_FORM':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_reworking','-undergoes-process-reworking'],
                                              ['_','-has-in-']] )

    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_PROCESS_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-sink-water-undergoes-process-'],
                                              ['_','-undergoes-process-']] )       
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_data-stream','-is-source-of-data-stream'],
                                                ['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_(earth','-contains-(earth'],
                                                ['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_TRAJECTORY_ABSTRACTION_ABSTRACTION' or \
        object_pattern_simple_str == 'PHENOMENON_TRAJECTORY_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_TRAJECTORY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-trajectory-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_ROLE_MATTER_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        groupings = ['distributary_(outlet-contains-(water-has-abstraction-x-section))']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'MODEL_PROCESS_PHENOMENON_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_nitrogen-fertilizer_','-as-sink-nitrogen-fertilizer-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MODEL_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-models-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-source-water-undergoes-process-']] )

    if object_pattern_simple_str == 'PHENOMENON_FORM_ROLE_MATTER_ABSTRACTION_PART' or \
        object_pattern_simple_str == 'PHENOMENON_FORM_ROLE_MATTER_ABSTRACTION' or \
       object_pattern_simple_str == 'FORM_ROLE_MATTER_ABSTRACTION' :
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_x-section_','-has-abstraction-x-section-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'ROLE_TRAJECTORY_ROLE_PHENOMENON_ABSTRACTION' or \
        object_pattern_simple_str == 'ROLE_TRAJECTORY_ROLE':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_TRAJECTORY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-trajectory-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-first-main-'],
                                              ['surface)','surface)-as-second-main']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_FORM_ABSTRACTION' or \
        object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_FORM':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'FORM_ROLE_MATTER_PROCESS_ABSTRACTION_MATTER' or \
        object_pattern_simple_str == 'FORM_ROLE_MATTER_PROCESS_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_PHENOMENON_PHENOMENON':
        groupings = ['cylinder_piston']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations = groupings )
        groupings = ['engine_(cylinder-contains-part-piston)']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_PART_above-PHENOMENON' or \
        object_pattern_simple_str == 'PHENOMENON_above-PHENOMENON' or \
        object_pattern_simple_str == 'PHENOMENON_PHENOMENON_PART' :
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_above-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )

    if object_pattern_simple_str == 'MODEL_PROCESS_PHENOMENON_ROLE_PROCESS' or \
        object_pattern_simple_str == 'MODEL_PROCESS_PHENOMENON_ROLE' or \
        object_pattern_simple_str == 'PROCESS_PHENOMENON_ROLE_PROCESS' or \
        object_pattern_simple_str == 'PROCESS_PHENOMENON_ROLE':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_crop_','-as-main-crop-as-in-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MODEL_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-models-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PROCESS_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-observes-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_ABSTRACTION_MATTER_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PART_ABSTRACTION_PHENOMENON' or \
        object_pattern_simple_str == 'PHENOMENON_PART_ABSTRACTION_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PART_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_bottom_','-has-part-bottom-has-abstraction-'],
                                              ['_front_','-has-part-front-has-abstraction-'],
                                              ['_top_','-has-part-top-has-abstraction-'],
                                              ['_bed_','-has-part-bed-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_PROCESS_ROLE':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['water_flowing_sink','sink-as-sink-water-undergoes-process-flowing'],
                                              ['water_flowing_source','source-as-source-water-undergoes-process-flowing']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )

    if object_pattern_simple_str == 'PHENOMENON_FORM_ROLE_MATTER_MATTER_PROCESS' or \
        object_pattern_simple_str == 'FORM_ROLE_MATTER_MATTER_PROCESS_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_sediment~suspended_','-as-medium-sediment~suspended-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'FORM_PART_MATTER_PROCESS_MATTER_PHENOMENON' or \
        object_pattern_simple_str == 'FORM_PART_MATTER_PROCESS_MATTER' or \
        object_pattern_simple_str == 'FORM_PART_MATTER_PROCESS':

        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ROLE_MATTER_PROCESS_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'ROLE_PHENOMENON_MATTER_PROCESS_at-PROCESS' or \
        object_pattern_simple_str == 'ROLE_PHENOMENON_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-source-water-undergoes-process-'],
                                              ['_nitrogen_','-as-sink-water-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        
    if object_pattern_simple_str == 'MATTER_MATTER_PHENOMENON_PART_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PHENOMENON_PART_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-is-medium-matter-water-is-contained-matter-'],
                                              ['_top_','-has-part-top-has-abstraction-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_MATTER_ROLE_PROCESS_MODEL':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_debris_','-as-medium-debris-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MODEL', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-model-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_PART_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-sink-water-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )

    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        if 'absor' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['surface)_','surface)-as-sink-'],
                                              ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['surface)_','surface)-as-source-'],
                                              ['_','-undergoes-process-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_MATTER_PHENOMENON_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PART_MATTER_PHENOMENON' or \
        object_pattern_simple_str == 'PHENOMENON_PART_MATTER_PHENOMENON_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_phreatic-zone_','-is-contained-matter-phreatic-zone-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        if 'sediment' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']])
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_wind_','-as-main-wind-as-in-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_land','_land-as-source'],
                                              ['subsurface)_','subsurface)-contains-part-'],
                                              ['_','-as-sink-'],
                                              ['canopy','canopy-as-source'],
                                              ['cloud','cloud-as-source']] )
   
    if object_pattern_simple_str == 'PHENOMENON_FORM_ROLE_MATTER_MATTER_MATTER' or \
        object_pattern_simple_str == 'PHENOMENON_FORM_ROLE_MATTER_MATTER':
        groupings = ['sediment_clay', 'sediment_sand', 'sediment_silt']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']], combinations = groupings)
        if 'concentration' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_MATTER_PROCESS_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-going-over-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_ABSTRACTION_FORM_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-matter-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        groupings = ['(air-has-form-column)_(aerosol~dry-has-matter-ammonium)']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'MATTER_FORM_below-PHENOMENON_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_below-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        object_name = object_name.replace('determined-(below-','determined-below-(')
        
    if object_pattern_simple_str == 'MATTER_ABSTRACTION_ROLE_MATTER_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_nitrogen','-as-numerator-nitrogen-as-denominator']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_MATTER_ROLE_PROCESS_PART' or \
        object_pattern_simple_str == 'PHENOMENON_PART_MATTER_ROLE_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PART_MATTER_ROLE_ROLE' or \
        object_pattern_simple_str == 'MATTER_ROLE_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_debris_','-as-medium-debris-undergoes-process-'],
                                              ['_fertilizer_','-as-sink-fertilizer-undergoes-process-'],
                                              ['_scuba-diver_','-as-medium-scuba-diver-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_PHENOMENON_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PHENOMENON_PROCESS':
        if 'rotation' in object_name or 'falling' in object_name or 'isochoric' in object_name:
           (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        if 'link' in object_name:
           (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        if 'eye' in object_name:
           (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        if 'atmosphere' in object_name and 'clouds' not in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        elif 'absor' in object_name or 'trans' in object_name or 'detection' in object_name:
           (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['clouds_','clouds-as-sink-'],
                                              ['eye)_','eye)-as-sink-'],
                                              ['atmosphere_','atmosphere-as-sink-'],
                                              ['snowpack_','snowpack-as-sink-'],
                                                ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['clouds_','clouds-as-source-'],
                                              ['snowpack_','snowpack-as-source-'],
                                              ['atmosphere_','atmosphere-as-source-'],
                                              ['_acoustic-wave_','-as-main-acoustic-wave-as-in-'],
                                              ['_gravity_','-creates-gravity-as-source-'],
                                              ['_baseball_','-as-main-baseball-as-main-'],
                                              ['ground_','ground-as-medium-'],
                                              ['groundwater_well','well-as-medium-groundwater'],
                                              ['earth_mars_','earth-as-source-mars-as-sink-'],
                                                ['_','-undergoes-process-']] )
        groupings = ['engine_(crankshaft-undergoes-process-rotation)']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['drainage-basin_','drainage-basin-contains-part-'],
                                              ['automobile_','automobile-contains-part-'],
                                                ['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['water_','water-is-medium-matter-'],
                                              ['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_(water','-contains-part-(water'],
                                              ['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_MATTER_ABSTRACTION_PART' or \
        object_pattern_simple_str == 'PHENOMENON_FORM_MATTER_ABSTRACTION' or \
        object_pattern_simple_str == 'FORM_MATTER_ABSTRACTION_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_x-section_','-has-abstraction-x-section-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'MATTER_ABSTRACTION_PART_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_profile_','-has-abstraction-profile-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-source-water-undergoes-process-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_ABSTRACTION' or \
        object_pattern_simple_str == 'PHENOMENON_MATTER_ABSTRACTION_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_surface','-has-abstraction-surface'],
                    ['_','-has-model-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )

    if object_pattern_simple_str == 'PHENOMENON_MATTER_PHENOMENON-as-MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON-as-MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['-as-','-expressed-as-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_PHENOMENON_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-numerator-']] )
        object_name = object_name.rstrip(')') + '-as-denominator)'
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )

    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_PHENOMENON_ABSTRACTION_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water','-contains-water'],
                                              ['_','-is-location-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-minuend-']] )
        object_name = object_name.replace('water))','water)-as-subtrahend)')

    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_ABSTRACTION_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_below-PHENOMENON_ABSTRACTION' or \
        object_pattern_simple_str == 'MATTER_below-PHENOMENON_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_below-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_below-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        object_name = object_name.replace('determined-(below-','determined-below-(')
        
    if object_pattern_simple_str == 'PHENOMENON_ROLE_MATTER_ABSTRACTION_PART' or \
        object_pattern_simple_str == 'PHENOMENON_ROLE_MATTER_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_x-section_','-has-abstraction-x-section-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_PHENOMENON_TRAJECTORY':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_TRAJECTORY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-trajectory-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_MATTER_PROCESS_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PART_MATTER_PROCESS_FORM' or \
        object_pattern_simple_str == 'PHENOMENON_PART_MATTER_PROCESS':
        contains = True
        if 'land_region' in object_name:
            contains = False
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_bulk','-has-form-bulk'],
                                                ['_','-going-over-']] )
        if contains:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
      
    if object_pattern_simple_str == 'ROLE-as-MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE-as-MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['-as-','-expressed-as-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_PART' or \
        object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON_FORM':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-belongs-to-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
            
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_ROLE_ABSTRACTION' or \
        object_pattern_simple_str == 'PHENOMENON_ROLE_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        groupings = ['distributary_(outlet-has-abstraction-center)']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'ROLE_ROLE_PROCESS_FORM_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        
    if object_pattern_simple_str == 'MATTER_PHENOMENON_ROLE_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-source-water-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'MATTER_PHENOMENON_PART_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_phreatic-zone_','-is-medium-matter-phreatic-zone-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-sink-water-as-in-']] )
        
    if object_pattern_simple_str == 'MATTER_MATTER_PHENOMENON_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-is-medium-matter-water-is-contained-matter-'],
                                              ['_','-has-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_ROLE_ABSTRACTION_PART' or \
        object_pattern_simple_str == 'PHENOMENON_FORM_ROLE_ABSTRACTION' or \
        object_pattern_simple_str == 'FORM_ROLE_ABSTRACTION' or \
        object_pattern_simple_str == 'PHENOMENON_FORM_ROLE' or \
        object_pattern_simple_str == 'ROLE_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_ABSTRACTION_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_x-section_','-has-abstraction-x-section-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'FORM_MATTER_MATTER_PHENOMENON_PROCESS' or \
        object_pattern_simple_str == 'MATTER_MATTER_PHENOMENON_PROCESS' or \
        object_pattern_simple_str == 'FORM_MATTER_MATTER_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['water_','water-as-medium-'],
                                                ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ROLE_MATTER_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['water_','water-as-medium-'],
                                                ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )

    if object_pattern_simple_str == 'PHENOMENON_ROLE_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_MATTER_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water~vapor_','-as-medium-water~vapor-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        if 'evapo' in object_name or 'runoff' in object_name or 'baseflow' in object_name or 'transpiration' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [[')_',')-as-source-'],
                                                ['_','-undergoes-process-']] )
        if 'infil' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [[')_',')-as-sink-'],
                                                ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['level)_','level)-contains-'],
                                              ['_(soil','-contains-(soil'],
                                              ['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_FORM_PROCESS_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PART_FORM_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_TRAJECTORY_PHENOMENON_ABSTRACTION' or \
        object_pattern_simple_str == 'PHENOMENON_TRAJECTORY':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_TRAJECTORY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-trajectory-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-first-main-']] )
        object_name = object_name.replace('))',')-as-second-main)')

    if object_pattern_simple_str == 'PHENOMENON_MATTER_PART_MATTER_MATTER' or \
        object_pattern_simple_str == 'PHENOMENON_MATTER_PART_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-origin-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-source-water-as-sink-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_at-MATTER_PROPERTY':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROPERTY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-property-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        object_name = object_name.replace('determined-(at-','determined-at-variable-(')
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_PHENOMENON_PROCESS':
        groupings = ['sea_ice']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-origin-of-']], combinations = groupings )
        if 'atmosphere_air_radiation' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-contains-']] )
        if 'absor' in object_name or 'trans' in object_name:
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_radiation~incoming~longwave_','-as-sink-radiation~incoming~longwave-undergoes-process-'],
                                                      ['_radiation~incoming~shortwave_','-as-sink-radiation~incoming~shortwave-undergoes-process-'],
                                                      ['_radiation~incoming_','-as-sink-radiation~incoming-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_radiation~incoming~longwave_','-as-source-radiation~incoming~longwave-undergoes-process-'], 
                                                        ['_radiation','-as-source-radiation'],
                                                      ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_ABSTRACTION_MATTER' or \
       object_pattern_simple_str == 'PHENOMENON_MATTER_ABSTRACTION_MATTER-as-MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('MATTER-as-MATTER', 'MATTER', object_pattern_simple_str, \
                        object_name, phen_phen_list, [
                                              ['-as-','-expressed-as-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_column','-has-form-column'],
                                              ['_mohr','-has-model-abstraction-mohr'],
                                              ['_','-has-abstraction-']] )
        if 'sea' in object_name:
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-is-location-of-origin-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_air','-is-location-of-air'],
                                              ['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_meltwater','-as-source-meltwater'],
                                                ['_','-as-medium-']] )
        if 'sea' in object_name and 'air' in object_name:
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-is-location-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-contains-']] )

    if object_pattern_simple_str == 'FORM_ABSTRACTION_ABSTRACTION_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-model-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        
    if object_pattern_simple_str == 'MATTER_FORM-and-FORM_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM-and-FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_carbon~decomposed_','-as-sink-carbon~decomposed-undergoes-process-']] )
        object_name = object_name.replace('soil-has-form-(pool-and-pool~microbial)',
                                          '(soil-has-form-pool)-and-(soil-has-form-pool~microbial)')
        
    if object_pattern_simple_str == 'PHENOMENON-and-PHENOMENON_PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON-and-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        
    if object_pattern_simple_str == 'ROLE_PROCESS_TRAJECTORY_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS_TRAJECTORY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_trajectory','-has-trajectory-trajectory'],
                                              ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_FORM_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_compaction','-undergoes-process-compaction'],
                                              ['_','-as-medium-']] )
        
    if object_pattern_simple_str == 'ROLE_MATTER_PROCESS_MATTER_PROCESS' or \
        object_pattern_simple_str == 'MATTER_PROCESS_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['crop_biomass~microbial-and-soil','(crop-has-matter-biomass~microbial)-and-soil']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        groupings = ['biomass~microbial-and-soil~stabilized_decomposition']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['biomass~microbial-and-soil~stabilized_','(biomass~microbial-and-soil~stabilized)-undergoes-process-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_carbon_','-as-source-carbon-undergoes-process-']] )
        object_name = object_name.replace('((crop-has-matter-biomass~microbial)-and-soil)-undergoes-process-decomposition',
                                          '((crop-has-matter-biomass~microbial)-undergoes-process-decomposition)-and-(soil-undergoes-process-decomposition)')\
                                .replace('(biomass~microbial-and-soil~stabilized)-undergoes-process-decomposition',
                                         '(biomass~microbial-undergoes-process-decomposition)-and-(soil~stabilized-undergoes-process-decomposition)')

    if object_pattern_simple_str == 'ROLE_PHENOMENON_PHENOMENON_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_radiation~solar_','-as-sink-radiation~solar-undergoes-process-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        if 'seismic' in object_name:
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-undergoes-process-']] )
        if 'absorp' in object_name:
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_radiation','-as-sink-radiation'],
                                                      ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_radiation','-as-source-radiation'],
                                                ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )

    if object_pattern_simple_str == 'PHENOMENON_PART_MATTER_MATTER_FORM' or \
        object_pattern_simple_str == 'PHENOMENON_PART_MATTER_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_PHENOMENON_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        if 'emission' in object_name or 'refl' in object_name:
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_radiation','-as-source-radiation'],
                                              ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_radiation','-as-sink-radiation'],
                                              ['_','-undergoes-process-']] )
        
    if object_pattern_simple_str == 'FORM_PART_MATTER_PHENOMENON_MATTER' or \
        object_pattern_simple_str == 'FORM_PART_MATTER_PHENOMENON' or \
        object_pattern_simple_str == 'MATTER_PHENOMENON_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['soil_','soil-is-medium-matter-'],
                                                ['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )

    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_FORM_MATTER' or \
        object_pattern_simple_str == 'PHENOMENON_PHENOMENON_FORM' or \
        object_pattern_simple_str == 'PHENOMENON_FORM_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_link','-contains-part-link'],
                                              ['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ROLE_MATTER_at-PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ROLE_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'above-PHENOMENON_ROLE_MATTER' or \
        object_pattern_simple_str == 'above-PHENOMENON_MATTER_PHENOMENON' or \
        object_pattern_simple_str == 'above-PHENOMENON_ROLE_at-PROCESS' or \
        object_pattern_simple_str == 'above-PHENOMENON_ROLE_ROLE' or \
        object_pattern_simple_str == 'above-PHENOMENON_ROLE_ROLE-as-MATTER_PROCESS' or \
        object_pattern_simple_str == 'above-PHENOMENON_ROLE_PHENOMENON-and-PHENOMENON-as-MATTER_PROCESS' or \
        object_pattern_simple_str == 'above-PHENOMENON_ROLE_ROLE_FORM-as-MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON-and-PHENOMENON-as-MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['-as-','-expressed-as-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE-as-MATTER', 'ROLE', object_pattern_simple_str, \
                object_name, phen_phen_list, [['-as-','-expressed-as-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_FORM-as-MATTER', 'ROLE', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-'],
                                              ['-as-','-expressed-as-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_FORM', 'ROLE', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS', 'ROLE', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'ROLE', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        if 'density' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['crop_biomass','crop-has-matter-biomass'],
                                                ['_','-contains-']] )
        else:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('above-PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('above-PHENOMENON_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        if 'rhizodeposits' in object_name:
            object_name = object_name.replace('-is-source-of-','-contains-')

    if object_pattern_simple_str == 'above-PHENOMENON_MATTER_ROLE_FORM_ROLE_ROLE_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_addition','-undergoes-process-addition'],
                                              ['_','-as-sink-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('above-PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'MATTER_MATTER_FORM_MATTER_PROCESS' or \
        object_pattern_simple_str == 'MATTER_MATTER_FORM_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_carbon~decomposed_','-as-sink-carbon~decomposed-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        object_name = object_name.replace('carbon-has-form-pool~microbial-and-stabilized',
                                          '(carbon-has-form-pool~microbial)-and-(carbon-has-form-pool~stabilized)')
        
    if object_pattern_simple_str == 'MATTER_ABSTRACTION_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_evap','-as-source-water-undergoes-process-evap'],
                                              ['_water_runoff','-as-source-water-undergoes-process-runoff'],
                                              ['_water_','-as-sink-water-undergoes-process-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_PHENOMENON_PART' or \
        object_pattern_simple_str == 'MATTER_PHENOMENON_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['water_','water-is-medium-matter-'],
                                              ['soil_','soil-is-medium-matter-'],
                                              ['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_PHENOMENON_FORM':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'FORM_MATTER_FORM_PART_ABSTRACTION' or \
        object_pattern_simple_str == 'FORM_PART_ABSTRACTION' or \
        object_pattern_simple_str == 'FORM_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PART_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_bottom_','-has-part-bottom-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-main-']] )
        if 'product' in quantity_name:
            object_name = object_name.replace('))',')-as-main)')

    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_ABSTRACTION':
        if 'plain' in object_name or 'graph' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_front_','-has-part-front-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_PHENOMENON_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water~outgoing','-as-source-water'],
                                                ['_water~incoming','-as-sink-water']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PHENOMENON' or \
        object_pattern_simple_str == 'PHENOMENON-or-PHENOMENON_ABSTRACTION_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON-or-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_MATTER_PROCESS':
        if 'air' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['air_','air-as-medium-'],
                                              ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_soil_','-as-sink-soil-as-source-'],
                                              ['_','-undergoes-process-']] )
        
    if object_pattern_simple_str == 'MATTER_MATTER_PROCESS_at-PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_nitrogen_','-as-sink-nitrogen-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        
    if object_pattern_simple_str == 'MATTER_MATTER_at-PROPERTY' or \
        object_pattern_simple_str == 'MATTER_MATTER_at-PHENOMENON_PROPERTY':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROPERTY', 'PROPERTY', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-property-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        if 'reference' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROPERTY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_at-','-reference-for-determination-of-property-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROPERTY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_(at-','-determined-at-variable-('],
                                                ['_at-','-determined-at-property-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_PHENOMENON':
        if 'clouds' in object_name:
            groupings = ['clouds_radiation~incoming~shortwave~reflected',
                         'clouds_radiation~incoming~shortwave~absorbed',
                         'clouds_radiation~incoming~shortwave~transmitted',
                         'clouds_radiation~outgoing~longwave~downward',
                         'clouds_radiation~outgoing~longwave~upward']
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_radiation~incoming','-as-sink-radiation~incoming'],
                                              ['_','-is-source-of-']], combinations = groupings )
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        groupings = ['engine_crankshaft','engine_cylinder','plain~upper_vegetation','vegetation_canopy',
                     'plain_plain~subaqueous']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_plain','-as-medium-plain'],
                                              ['_vegetation','-is-location-of-vegetation'],
                                               ['_','-contains-part-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['bear_','bear-contains-part-'],
                                              ['bear~alaskan_','bear~alaskan-contains-part-'],
                                                ['river-delta_','river-delta-contains-part-'],
                                                ['land_','land-as-medium-'],
                                                ['automobile_','automobile-contains-part-'],
                                                ['_','-contains-']] )
        if 'black-bear' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_body','-as-numerator-(black-bear~alaskan-contains-part-body)-as-denominator']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_body','-as-numerator-(bear-contains-part-body)-as-denominator']] )
        
    if object_pattern_simple_str == 'MODEL_PROCESS_ROLE_PROCESS' or \
        object_pattern_simple_str == 'ABSTRACTION_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MODEL_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-models-']] )
        
    if object_pattern_simple_str == 'ROLE_PROCESS_PHENOMENON_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] ) # ???
        
    if object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_ROLE_PART' or \
        object_pattern_simple_str == 'PHENOMENON_PHENOMENON_ROLE':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        groupings = ['distributary_(outlet-has-part-top)','distributary_(outlet-has-part-side~left)',
                     'distributary_(outlet-has-part-side~right)']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']], combinations = groupings ) 
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']])
        
    if object_pattern_simple_str == 'FORM_MATTER_PROCESS_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'FORM_PART_MATTER_MATTER_PROCESS' or \
        object_pattern_simple_str == 'FORM_PART_MATTER_MATTER_PHENOMENON_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        if 'water' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['water_','water-as-medium-'],
                                                ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_oxygen~dissolved_','-as-sink-oxygen~dissolved-undergoes-process-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_MATTER_MATTER':
        groupings = ['nmvoc~anthropogenic_carbon','nmvoc~biogenic_carbon']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )

    if object_pattern_simple_str == 'PHENOMENON_FORM_MATTER_PROCESS' or \
        object_pattern_simple_str == 'FORM_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'ROLE-or-ROLE_MATTER_at-PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE-or-ROLE', 'ROLE', object_pattern_simple_str, \
                object_name, phen_phen_list, [] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
       
    if object_pattern_simple_str == 'FORM_MATTER_ABSTRACTION_MATTER' or \
        object_pattern_simple_str == 'FORM_MATTER_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        if 'air' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'MATTER_FORM_PHENOMENON_PROCESS' or \
        object_pattern_simple_str == 'MATTER_FORM_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        if 'bond' in object_name:
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_radiation_','-as-source-radiation-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ABSTRACTION_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        if ('sea' in object_name and 'water' in object_name) or \
                ('surface~' in object_name and 'soil' in object_name):
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'ROLE_PROCESS_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_at-PROCESS_PROPERTY':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PROCESS_PROPERTY', 'PROCESS', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-property-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_(at-','-reference-for-determination-of-variable-(']] )
        
    if object_pattern_simple_str == 'ROLE_PROCESS-or-PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS-or-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['crop_planting-or-sowing',
                                               '(crop-undergoes-process-planting)-or-(crop-undergoes-process-sowing)']] )
        
    if object_pattern_simple_str == 'ROLE_PROCESS_TRAJECTORY_ROLE':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS_TRAJECTORY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_acceleration_','-undergoes-process-acceleration-has-trajectory-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        
    if object_pattern_simple_str == 'DOMAIN_PHENOMENON_PHENOMENON' or \
        object_pattern_simple_str == 'DOMAIN_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('DOMAIN_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-domain-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_above-PART' or \
        object_pattern_simple_str == 'PHENOMENON_MATTER_above-PHENOMENON_PART' or \
        object_pattern_simple_str == 'PHENOMENON_MATTER_below-PHENOMENON_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        if 'glacier' in object_name:
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_above-PART', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_above-','-determined-above-(glacier-has-part-']] )
                object_name = object_name + ')'
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_above-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_(above-','-determined-above-(']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_below-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_(below-','-determined-below-(']] )
        
    if object_pattern_simple_str == 'FORM_ABSTRACTION_ABSTRACTION' or \
        object_pattern_simple_str == 'PHENOMENON_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_black-body','-has-model-abstraction-black-body'],
                                                ['_','-has-abstraction-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_PHENOMENON':
        if 'sea_ice' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['air_radiation~incoming~shortwave','air-contains-radiation~incoming~shortwave'],
                                              ['_longshore','-is-medium-matter-longshore'],
                                              ['_rip','-is-medium-matter-rip'],
                                              ['_tide','-is-medium-matter-tide'],
                                              ['_internal','-is-medium-matter-internal'],
                                              ['_surf','-is-medium-matter-surf'],
                                                ['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['ground~above_','ground~above-is-location-of-'],
                                              ['_(water-is-medium-matter','-contains-part-(water-is-medium-matter'],
                                                ['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON_MATTER' or \
        object_pattern_simple_str == 'PHENOMENON_PHENOMENON_MATTER_MATTER':
        if 'front' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['atmosphere_','atmosphere-is-source-of-'],
                                              ['river-delta_','river-delta-contains-part-'],
                                              ['_','-contains-']] )
        
    if object_pattern_simple_str == 'FORM_MATTER_PROCESS_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'FORM_PHENOMENON_ABSTRACTION':
        object_name = 'valley_channel_centerline'
        variable_name = object_name + '__' + quantity_name
        object_pattern_simple_str = 'PHENOMENON_FORM_ABSTRACTION'
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_ABSTRACTION' or \
        object_pattern_simple_str == 'FORM_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['impact-crater_circle','impact-crater-has-model-abstraction-circle'],
                                                ['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_MATTER_FORM' or \
        object_pattern_simple_str == 'PHENOMENON_PART_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        if 'atmosphere' in object_name or 'glacier' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_PART_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_channel_','-has-form-channel-has-part-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water~outgoing','-as-source-water'],
                                              ['_water~incoming','-as-sink-water'],
                                              ['_','-as-medium-']])
        
    if object_pattern_simple_str == 'PROCESS_ROLE_MATTER_PROCESS' or \
        object_pattern_simple_str == 'ROLE_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_nitrogen-fertilizer_','-as-sink-nitrogen-fertilizer-undergoes-process-'],
                                              ['_water_','-as-source-water-undergoes-process-'],
                                              ['_nitrogen_','-as-sink-nitrogen-undergoes-process-']])
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PROCESS_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-observes-']] )
    
    if object_pattern_simple_str == 'ROLE_MATTER_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-matter-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_nitrogen_','-as-sink-nitrogen-undergoes-process-']] )
        
    if object_pattern_simple_str == 'MATTER_FORM_MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        if 'infiltration' in object_name:
                (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_water_','-as-medium-water-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_(water','-as-medium-(water'],
                                                ['_','-contains-']] )
        object_name = object_name.replace('biomass~microbial-or-soil-has-form-pool~organic~stabilized',
                                          '(biomass~microbial-has-form-pool~organic~stabilized)-or-(soil-has-form-pool~organic~stabilized)')
        
    if object_pattern_simple_str == 'FORM_MATTER_MATTER_PROCESS':
        if 'flowing' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['water_','water-as-medium-'],
                                              ['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ROLE_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        if 'atmosphere' in object_name or 'sea' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        if 'automobile' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-above-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM_PHENOMENON':
        if 'dust' not in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_dust','-as-medium-dust'],
                                                ['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_radiation~incoming~shortwave~absorbed','-as-sink-radiation~incoming~shortwave~absorbed'],
                                              ['_radiation~incoming~shortwave~reflected','-as-source-radiation~incoming~shortwave~reflected'],
                                              ['_radiation~incoming~shortwave~transmitted','-as-sink-radiation~incoming~shortwave~transmitted'],
                                                ['_','-contains-']] )
        
    if object_pattern_simple_str == 'FORM_PART_below-PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_below-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        
    if object_pattern_simple_str == 'MATTER_PHENOMENON_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_well_','-as-in-well-undergoes-process-'],
                                              ['_skin_','-as-in-skin-as-main-']] )
        
    if object_pattern_simple_str == 'MATTER_ABSTRACTION_MATTER' or \
       object_pattern_simple_str == 'MATTER_ABSTRACTION_MATTER-as-MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER-as-MATTER', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['-as-','-expressed-as-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water','-as-medium-water'],
                                              ['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ROLE_FORM_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_PROCESS':
        if ('atmosphere' in object_name and 'air' in object_name) or 'river-bank' in object_name or \
                'glacier' in object_name or 'pipe' in object_name or ('sea' in object_name and 'water' in object_name) or \
                'snowpack' in object_name or 'earth' in object_name or 'drainage-basin' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['river-bank_', 'river-bank-is-location-of-'],
                                                ['_','-contains-']] )
        elif 'precipitation' in object_name or 'emission' in object_name or 'evaporation' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_precipitation','-undergoes-process-precipitation'],
                                              ['_emission','-undergoes-process-emission'],
                                              ['_evaporation','-undergoes-process-evaporation'],
                                                ['_','-as-source-']] )
        elif 'consumption' in object_name or 'lake_water~incoming' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_flowing','-undergoes-process-flowing'],
                                                ['_consumption','-undergoes-process-consumption'],
                                              ['_','-as-sink-']] )
        elif 'lake_water~outgoing' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_flowing','-undergoes-process-flowing'],
                                              ['_','-as-source-']] )
        elif 'sea_ice' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_flowing','-undergoes-process-flowing'],
                                                ['_','-undergoes-process-']] )
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
            
    if object_pattern_simple_str == 'ROLE_PROCESS_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )

    if object_pattern_simple_str == 'MATTER_ABSTRACTION_FORM':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )

    if object_pattern_simple_str == 'MATTER_MATTER_PHENOMENON':
        if 'front' in object_name:
             (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-participates-in-']] ) 
             (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-is-medium-matter-water-is-contained-matter-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_MATTER':
        if 'meltwater' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['sea_','sea-is-location-of-'],
                                                ['_','-contains-']] )
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        if 'sea_ice' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
            loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
            object_name, phen_phen_list, [['air_fuel','air-as-numerator-fuel-as-denominator'],
                                          ['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
            loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
            object_name, phen_phen_list, [['_','-contains-']] )
        
        if 'saturation' in quantity_name or 'concentration' in quantity_name or 'fraction' in quantity_name or \
                'solubility' in quantity_name or 'diffusivity' in quantity_name or 'conductivity' in quantity_name or \
                'temperature' in quantity_name or 'mixing_ratio' in quantity_name or 'density' in quantity_name or \
                'psychrometric' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        if 'partial_pressure' in quantity_name or 'fugacity' in quantity_name or 'fraction' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'ROLE-or-ROLE_at-PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE-or-ROLE', 'ROLE', object_pattern_simple_str, \
                object_name, phen_phen_list, [] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_at-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        
    if (object_pattern_simple_str == 'PHENOMENON_PART_PROCESS'):
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        
    if object_pattern_simple_str == 'FORM_PART_MATTER_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )

    if object_pattern_simple_str == 'ABSTRACTION_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ABSTRACTION_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ROLE_PROCESS':
        if 'driver' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
            object_name = object_name.rstrip(')') + ')-undergoes-process-driving)'
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_crop_','-as-medium-crop-undergoes-process-'],
                                              ['_fertilizer_','-as-sink-fertilizer-undergoes-process-']])
        
    if object_pattern_simple_str == 'PHENOMENON_PART_from-MATTER_ABSTRACTION' or \
        object_pattern_simple_str == 'MATTER_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_from-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        object_name = object_name.replace('-(from-','-from-(')
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER_to-PHENOMENON_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_to-PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        object_name = object_name.replace('-(to-','-to-(')
        
    if object_pattern_simple_str == 'FORM_MATTER_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-participates-in-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'MATTER_PROCESS_MATTER' or \
        object_pattern_simple_str == 'MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['soil_', 'soil-as-medium-'],
                                                ['_','-expressed-as-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        object_name = object_name.replace('water~incoming-and-outgoing-undergoes-process-flowing',
                                          '(water~incoming-undergoes-process-flowing)-and-(water~outgoing-undergoes-process-flowing)')
        
    if object_pattern_simple_str == 'MATTER_at-PROPERTY':
        if 'reference' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_at-PROPERTY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_at-','-reference-for-determination-of-property-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_at-PROPERTY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-at-property-']] )

    if object_pattern_simple_str == 'ROLE_PART_ABSTRACTION':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PART_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_shaft_','-has-part-shaft-has-abstraction-']] )
        
    if object_pattern_simple_str == 'FORM_ABSTRACTION_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_ABSTRACTION_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_x-section_','-has-abstraction-x-section-has-part-']] )
        
    if object_pattern_simple_str == 'MATTER_MATTER_PROCESS' or \
        object_pattern_simple_str == 'MATTER_MATTER-as-MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER-as-MATTER', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['-as-','-expressed-as-']] )
        if 'flowing' in object_name:
             (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water_','-as-sink-water-undergoes-process-'],
                                              ['_(nitrous-oxide-expressed-as-nitrogen)_','-as-source-(nitrous-oxide-expressed-as-nitrogen)-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART_FORM':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'ROLE_PROCESS_PROCESS' or \
        object_pattern_simple_str == 'FORM_PROCESS_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        
    if object_pattern_simple_str == 'FORM_MATTER_MATTER' or \
        object_pattern_simple_str == 'FORM_PHENOMENON':
        if 'density' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )

    if object_pattern_simple_str == 'MATTER_FORM_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_macropores','-contains-macropores'],
                                                ['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water','-as-medium-water'],
                                              ['_carbon~stabilized', '-as-medium-carbon~stabilized'],
                                                ['_','-contains-']] )
        
    if object_pattern_simple_str == 'MATTER_MATTER_FORM':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        
    if object_pattern_simple_str == 'FORM_PART_MATTER' or \
        object_pattern_simple_str == 'FORM_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        if 'conductivity' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_water','-is-location-of-water'],
                                                ['_','-contains-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PHENOMENON':
        if 'dust~aerosol' in object_name:
            object_name = 'atmosphere_(dust-has-form-aerosol)'
        if 'fraction' in quantity_name or 'capacity' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        elif 'frequency' in quantity_name or 'atmosphere' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['earth_atmosphere','earth-is-surrounded-by-atmosphere'],
                                              ['mars_atmosphere','mars-is-surrounded-by-atmosphere'],
                                              ['_','-contains-']] )
        elif 'energy_flux' in quantity_name or 'vegetation' in object_name or \
                'rain-gauge' in object_name or 'weather-station' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        elif 'mars' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-orbiting-center-of-']] )
        elif 'life' in object_name or 'day' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-participates-in-']] )
        else:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['sun_earth','sun-as-main-earth-as-main'],
                                              ['sun_venus','sun-as-main-venus-as-main'],
                                              ['earth_sun','earth-as-main-sun-as-main'],
                                                ['_','-contains-part-']] )
        if 'dust-has-form-aerosol' in object_name:
            object_name = '(' + object_name + '-as-medium)'
        
    if object_pattern_simple_str == 'ROLE-or-ROLE_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE-or-ROLE', 'ROLE', object_pattern_simple_str, \
                object_name, phen_phen_list, [] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        
    if object_pattern_simple_str == 'ROLE_since-PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_since-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_MATTER':
        if 'atmosphere_air' in object_name or 'material' in object_name or \
                'glacier_ice' in object_name or 'sea_water' in object_name or \
                'snowpack_snow' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-contains-']] )
        elif 'ground_water' in object_name or 'snowpack_water' in object_name or \
                'efficiency' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-as-medium-']] )
        elif 'meltwater' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-is-source-of-']] )
        elif 'sea_ice' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                        loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                        object_name, phen_phen_list, [['_','-is-location-of-origin-of-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'MATTER_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_ski~waxed','-as-main-ski~waxed-as-main'],
                                              ['_radiation','-as-medium-radiation'],
                                                ['_','-is-medium-matter-']] )

    if object_pattern_simple_str == 'ROLE_TRAJECTORY':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_TRAJECTORY', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-trajectory-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_FORM':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['station_','station-is-location-of-'],
                                              ['downstream_','downstream-is-location-of-'],
                                                ['snowpack_melt','snowpack-is-source-of-meltwater'],
                                                ['river_channel','river-has-form-channel'],
                                                ['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_beds','-contains-part-beds'],
                                                ['_stratum','-contains-part-stratum'],
                                                ['_','-has-part-']] )
        
    if object_pattern_simple_str == 'PHENOMENON_ROLE':
        if 'automobile' in object_name or 'rocket' in object_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        
    if object_pattern_simple_str == 'ROLE_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        
    if object_pattern_simple_str == 'FORM_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        
    if object_pattern_simple_str == 'MATTER-as-MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER-as-MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['-as-','-expressed-as-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        
    if object_pattern_simple_str == 'MATTER_PROCESS-vs-PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS-vs-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        object_name = object_name.replace('nitrogen-fertilizer-undergoes-process-usage-vs-application',
                                          '(nitrogen-fertilizer-undergoes-process-usage)-vs-(nitrogen-fertilizer-undergoes-process-application)')

        
    if object_pattern_simple_str == 'MATTER_FORM':
        object_name = object_name.replace('-as-','-expressed-as-')
        if 'volume_fraction' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_macropores','-contains-macropores'],
                                                ['_void','-as-medium-void'],
                                                ['_','-has-form-']] )
        if 'macropores~saturated' in object_name:
            object_name += '-as-medium'
        object_name = object_name.replace('biomass~microbial-and-soil-has-form-pool~organic~stabilized',
                                          '((biomass~microbial-has-form-pool~organic~stabilized)-and-(soil-has-form-pool~organic~stabilized))')
        
    if object_pattern_simple_str == 'ROLE_PART':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_shaft','-contains-part-shaft'],
                                                ['_','-has-part-']] )
        
    if object_pattern_simple_str == 'ROLE_FORM':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-source-of-']] )
        
    if object_pattern_simple_str == 'ROLE_ROLE':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_crop','-as-main-crop-as-source']] )

    if object_pattern_simple_str == 'MATTER_MATTER' or \
        object_pattern_simple_str == 'MATTER_MATTER-as-MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER-as-MATTER', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['-as-','-expressed-as-']] )
        if ('soil' in object_name and 'water' in object_name) or 'concentration' in quantity_name or \
                'fraction' in quantity_name or 'surface_tension' in quantity_name or \
                'solubility' in quantity_name or 'diffusivity' in quantity_name or 'temperature' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        elif 'relative' in quantity_name or 'ratio' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-numerator-']] )
            object_name = object_name.strip(')') + '-as-denominator)'
        elif 'affinity' in quantity_name or 'friction' in quantity_name:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-main-']] )
            object_name = object_name.strip(')') + '-as-main)'
        else:
            (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
            
    if object_pattern_simple_str == 'ROLE_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ROLE_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_biomass','-has-matter-biomass'],
                                              ['_nitrogen-fertilizer','-as-main-nitrogen-fertilizer-as-in'],
                                              ['_water','-as-main-water-as-in'],
                                              ['_nitrogen','-as-main-nitrogen-as-in']] )
        
    if object_pattern_simple_str == 'MATTER_ROLE':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_ROLE', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_oxidizer','-as-numerator-oxidizer-as-denominator']] )
        
    if object_pattern_simple_str == 'PROCESS_PHENOMENON':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PROCESS_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-observes-']] )

    if object_pattern_simple_str == 'MODEL_ABSTRACTION_ABSTRACTION_PART_ABSTRACTION_MATTER' or \
        object_pattern_simple_str == 'MODEL_ABSTRACTION_ABSTRACTION_ABSTRACTION_MATTER' or \
        object_pattern_simple_str == 'MODEL_ABSTRACTION_ABSTRACTION_ABSTRACTION_PHENOMENON' or \
        object_pattern_simple_str == 'MODEL_ABSTRACTION_ABSTRACTION_MATTER' or \
        object_pattern_simple_str == 'MODEL_ABSTRACTION_ABSTRACTION_MATTER_PROCESS' or \
        object_pattern_simple_str == 'MODEL_ABSTRACTION_ABSTRACTION_ABSTRACTION' or \
        object_pattern_simple_str == 'MODEL_ABSTRACTION_ABSTRACTION_PART_ABSTRACTION' or \
        (object_pattern_simple_str == 'MODEL_ABSTRACTION_PART_PHENOMENON_MATTER') or \
        object_pattern_simple_str == 'MODEL_ABSTRACTION_ABSTRACTION_PART' or \
        object_pattern_simple_str == 'MODEL_ABSTRACTION_ABSTRACTION' or \
        object_pattern_simple_str == 'MODEL_ABSTRACTION_PART' or \
        object_pattern_simple_str.startswith('MODEL_ABSTRACTION_ABSTRACTION'):
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        groupings = ['cell_centroid', 'dual-cell_centroid', 'primary-cell_centroid',
                     'cell_center', 'cell_centroid']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ABSTRACTION_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-abstraction-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ABSTRACTION_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ABSTRACTION_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_ABSTRACTION', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_axis~east','-as-main-axis~east-as-main'],
                                                ['_','-has-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ABSTRACTION_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MODEL_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-models-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-models-']] )
        if '_' in object_name:
            object_pattern_simple_str = 'PHENOMENON'
            object_name = object_name.replace('_(from-','-determined-from-(')\
                .replace('_(to-','-determined-from-(').replace('_','-determined-')
            object_name = '(' + object_name + ')'
        
    if object_pattern_simple_str.startswith('MODEL_ABSTRACTION_FORM'):
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PART', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ABSTRACTION_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('ABSTRACTION_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MODEL_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-models-']] )
        
    if (object_pattern_simple_str == 'MODEL_MATTER_FORM') or \
        (object_pattern_simple_str == 'MODEL_PHENOMENON'):
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MODEL_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-models-']] )
        
    if object_pattern_simple_str == 'MATTER_MATTER_MODEL':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MODEL', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-model-abstraction-']] )
        
    if object_pattern_simple_str.startswith('PHENOMENON_MATTER_MODEL'):
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MODEL', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-model-abstraction-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'MODEL_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MODEL_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )

    if object_pattern_simple_str.startswith('MATTER_FORM_FORM'):
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )

    if object_pattern_simple_str == 'PHENOMENON_at-FORM-or-ROLE_PROCESS-or-PROCESS' or \
        object_pattern_simple_str == 'PHENOMENON_PHENOMENON_at-FORM-or-ROLE_PROCESS-or-PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM-or-ROLE_PROCESS-or-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['grain-or-forage_harvest-or-death',
                                               '(grain-undergoes-process-harvest)-or-(forage-undergoes-process-harvest)-or-' + \
                                                '(grain-undergoes-process-death)-or-(forage-undergoes-process-death)']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-part-']] )
        object_pattern_simple_str = 'PHENOMENON'
        object_name = object_name.replace('_(at-','-determined-at-(')
        
    if object_pattern_simple_str == 'MATTER_FORM_MATTER_MATTER':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-has-form-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        
    if object_pattern_simple_str == 'MODEL_FORM_PHENOMENON_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MODEL_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-models-']] )
        
    if object_pattern_simple_str == 'above-PHENOMENON_MATTER_FORM':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_FORM', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('above-PHENOMENON_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-is-location-of-']] )
        
    if object_pattern_simple_str == 'FORM_MATTER_at-PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('FORM_MATTER', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_at-PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-determined-']] )

    if object_pattern_simple_str == 'MATTER_as-MATTER_PROCESS':
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('as-MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-as-medium-']] )
    
    if object_pattern_simple_str == 'MATTER_as-MATTER_PROCESS_MATTER-as-MATTER_PROCESS':
        groupings = ['as-nitrogen']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('as-MATTER', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['as-', 'expressed-as-']], combinations = groupings )
        groupings = ['(expressed-as-nitrogen)_denitrification', '(expressed-as-nitrogen)_nitrification']
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-undergoes-process-']], combinations = groupings )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER_PHENOMENON', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_','-contains-as-medium-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('MATTER-as-MATTER', 'MATTER', object_pattern_simple_str, \
                object_name, phen_phen_list, [['-as-','-expressed-as-']] )
        (object_pattern_simple_str, object_name, phen_phen_list) = \
                loop_on_pattern('PHENOMENON_MATTER_PROCESS', 'PHENOMENON', object_pattern_simple_str, \
                object_name, phen_phen_list, [['_(nitrous-oxide-expressed-as-nitrogen)_','-as-source-(nitrous-oxide-expressed-as-nitrogen)-undergoes-process-']] )
    
    if object_pattern_simple_str != 'PHENOMENON':
        object_pattern_simple_str = 'PHENOMENON'
        object_name = '(' + object_name + ')'

    object_name = object_name.replace('plain~lower-and-plain~upper','(plain~lower-and-plain~upper)')\
                        .replace('pool~microbial-and-stabilized','(pool~microbial-and-pool~stabilized)')\
                        .replace('(biomass~microbial-and-soil)~stabilized', '(biomass~microbial~stabilized-and-soil~stabilized)')
    
    if object_pattern_simple_str not in all_object_patterns:
        all_object_patterns.append(object_pattern_simple_str)

    if verbose:
        print(variable_name, object_name, quantity_name)
        input('Press enter to continue ...')

    current_data_row.append(object_name)
    final_data.append(current_data_row)

csdms_names = pd.DataFrame(final_data, columns = ['original_varname', 'new_varname', 'object_name','quantity_name','annotated_object_name'])
csdms_names.to_csv(os.path.join(src_path,'csdms_annotated_names.csv'), index=False)

all_object_patterns.sort(key=lambda s: len(s))
printall = False
if printall:
    for pat in all_object_patterns:
        print(pat)