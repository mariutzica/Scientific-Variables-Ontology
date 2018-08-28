# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 11:34:27 2017

@author: Maria Stoica
@description: read in CSN cleaned by fix_CSN_syntax.py and atomize components for processing into ontology.

"""

################################
#    IMPORT NEEDED PACKAGES    #
################################

#Pandas for data frames and data manipulation
import pandas as pd

################################
#   INITIAL DATA LOAD          #
################################

# Load CSN list, split up by '__' to yield object and quantity parts.

# List contains 3044 unique names
csn = pd.read_csv('CSN_VarNames_v0.85m2.csv',sep='__',index_col=False,\
    header=None,skiprows=1,engine='python',names=['object', 'quantity'])
csn.sort_values(['object','quantity'],inplace = True)
csn=csn.reset_index(drop=True)
csn['full_name']=csn['object']+'__'+csn['quantity']

# determine [current] object, operator, quantity
# split up into one per column for object, operator
# quantity without operator --> modified_quantity
csn_parse_object = csn['object'].str.split('_',expand=True).fillna('')
csn_parse_quantity = csn['quantity'].str.rsplit('_of_',1).str[-1]
csn_parse_operator = csn['quantity'].copy().rename('operator')
csn_parse_operator[~csn_parse_operator.str.contains('_of_')]=''
csn_parse_operator = csn_parse_operator.str.rsplit('_of_',1).str[0]

csn_parse_object.columns=['object'+str(x) for x in range(7)]
csn_parse_operator.columns=['operator']
csn_parse_quantity.rename('quantity_label',inplace=True)
csn = pd.concat([csn, csn_parse_object, csn_parse_operator, 
                 csn_parse_quantity], axis = 1)
csn['quantity_id'] = ''

#Start cleanup of object part
#air
cond_obj0 = csn['object0'] == 'air'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'air'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'air'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'matter'
cond_quant = csn['quantity'].str.contains('volume_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = 'volume_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity'].str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = 'shear_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity'].str.replace('shear_','')
cond_quant = csn['quantity'].str.contains('volume-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'quantity_label'] = \
                                    'isochoric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1,'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1,'quantity_label']
cond_quant = csn['quantity'].str.contains('relative')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] + '_ratio'
csn.loc[ cond_obj0 & cond_obj1, 'object0']=''

#air_helium-plume
cond_obj0 = csn['object0'] == 'air'
cond_obj1 = csn['object1'] == 'helium-plume'
csn.loc[ cond_obj0 & cond_obj1, 'object_context_id'] = 'air_in'
csn.loc[ cond_obj0 & cond_obj1, 'object_context_label'] = 'air'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'helium-plume'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'helium-plume'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']]=''

##air_radiation~visible
#cond_obj0 = csn['object0'] == 'air'
#cond_obj1 = csn['object1'] == 'radiation~visible'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_phen'] = 'radiation'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_phen_descriptor'] = 'visible'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##air_water~vapor
#cond_obj0 = csn['object0'] == 'air'
#cond_obj1 = csn['object1'] == 'water~vapor'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_matter'] = \
#                            'air'
#cond_quant = csn['quantity'].str.contains('saturated')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_phasestate'] = 'vapor'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_medium_condition'] = \
#                            'saturated'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = 'partial_pressure'
#cond_quant = csn['quantity'].str.contains('dew_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_medium_condition'] = \
#                            'dew-point'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = 'temperature'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#aircraft
cond_obj0 = csn['object0'] == 'aircraft'
csn.loc[ cond_obj0, 'object_id'] = 'aircraft_flight'
csn.loc[ cond_obj0, 'object_label'] = 'aircraft'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

##airfoil
#cond_obj0 = csn['object0'] == 'airfoil'
#cond_obj1 = csn['object1'] == 'curve~enclosing'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction_abstraction'] = \
#                            'curve'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction_abstraction_descriptor'] = \
#                            'encosing'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'airfoil'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
#cond_quant = csn['quantity'].str.contains('coefficient')
#csn.loc[ cond_obj0 & cond_quant, 'root_object_process'] = \
#        csn.loc[ cond_obj0 & cond_quant, 'quantity'].str.split('_').str[0]
#csn.loc[ cond_obj0 & cond_quant, 'modified_quantity'] = 'process_coefficient'        
#
##airplane(_wing)
#cond_obj0 = csn['object0'] == 'airplane'
#cond_obj1 = csn['object1'] == 'wing'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'length'
#csn.loc[ cond_obj0, 'root_object_form'] = 'airplane'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'wingspan'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##air~dry(_water~vapor)
#cond_obj0 = csn['object0'] == 'air~dry'
#cond_obj1 = csn['object1'] == 'water~vapor'
#csn.loc[ cond_obj0, 'root_object_matter'] = 'air'
#csn.loc[ cond_obj0, 'root_object_matter_descriptor'] = 'dry'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_matter_phasestate'] = 'vapor'
#csn.loc[ cond_obj0 & cond_obj1, 'two_object_operator']='ratio'
#csn.loc[ cond_obj0 & cond_obj1, 'root_quantity1']='gas_constant'
#csn.loc[ cond_obj0 & cond_obj1, 'root_quantity2']='gas_constant'
#csn.loc[ cond_obj0, ['object0','object1']] = ''

#aluminum
cond_obj0 = csn['object0'] == 'aluminum'
csn.loc[ cond_obj0, 'object_id'] = 'aluminum'
csn.loc[ cond_obj0, 'object_label'] = 'aluminum'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0']=''

#anvil
cond_obj0 = csn['object0'] == 'anvil'
csn.loc[ cond_obj0, 'object_id'] = 'anvil'
csn.loc[ cond_obj0, 'object_label'] = 'anvil'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

#appliance~electric
cond_obj0 = csn['object0'] == 'appliance~electric'
csn.loc[ cond_obj0, 'object_id'] = 'appliance~electric'
csn.loc[ cond_obj0, 'object_label'] = 'appliance~electric'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

##atmosphere_aerosol_dust
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'aerosol'
#cond_obj2 = csn['object2'] == 'dust'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#            'second_root_object_matter_configstate'] = 'aerosol~dust'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#            'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#            'second_root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#            'root_object_in_process_interaction'] = 'transmission'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#            'second_root_object_in_process_interaction'] = 'transmission'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#            'two_object_operator'] = 'reduction'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#            'operator0'] = ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_quantity1'] = 'transmittance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_quantity2'] = 'transmittance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#            ['object0','object1','object2']]=''
#
##atmosphere_aerosol_radiation        
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'aerosol'
#cond_quant = csn['quantity'].str.endswith('ance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#            'root_object_matter_configstate'] = 'aerosol'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#            'root_object_context_phen'] = 'atmosphere'
#cond_obj2 = csn['object2'].str.contains('incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#            'root_object_in_trajectory_direction'] = 'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#            'root_object_in_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~incoming','').str.replace('~shortwave','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#            'root_object_in_phen_descriptor'] = 'shortwave'
#cond_obj2 = csn['object2'].str.contains('outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#            'root_object_out_trajectory_direction'] = 'outgoing'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#            'root_object_out_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~outgoing','').str.replace('~longwave','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#            'root_object_out_phen_descriptor'] = 'longwave'
#cond_obj2 = csn['object2'].str.contains('incoming')
#cond_quant = csn['quantity'].str.endswith('flux')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#        'root_object_sink_matter_configstate'] = 'aerosol'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#        'root_object_sink_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#        'root_object_trajectory_direction'] = 'incoming'
#cond_obj2 = csn['object2'].str.contains('outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#    'root_object_source_matter_configstate'] = 'aerosol'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#    'root_object_source_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#        'root_object_trajectory_direction'] = 'outgoing'
#cond_obj2 = csn['object2'].str.contains('~upward')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#        'root_object_trajectory_direction'] = 'outgoing~upward'
#cond_obj2 = csn['object2'].str.contains('~downward')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#        'root_object_trajectory_direction'] = 'outgoing~downward'
#cond_obj2 = csn['object2'].str.contains('outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_phen_descriptor'] = 'longwave'
#cond_obj2 = csn['object2'].str.contains('incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_phen_descriptor'] = 'shortwave'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'object2']\
#        .str.replace('~outgoing','').str.replace('~upward','')\
#        .str.replace('~downward','').str.replace('~incoming','')\
#        .str.replace('~shortwave','').str.replace('~longwave','')
#cond_quant = csn['quantity'].str.contains('absorptance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('reflectance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.contains('transmittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'transmission'
#cond_quant = csn['quantity'].str.contains('emittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_out_process_interaction'] = 'emission'
#cond_quant = csn['quantity'].str.contains('absorbed')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'absorption'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'absorbed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'energy_flux'
#cond_quant = csn['quantity'].str.contains('reflected')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'reflection'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'reflected'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'energy_flux'
#cond_quant = csn['quantity'].str.contains('transmitted')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'transmission'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'transmitted'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'energy_flux'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##atmosphere_air
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_phen'] = 'atmosphere'
#cond_quant = csn['quantity'] == 'mass-specific_isobaric_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'mass-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition'] = 'isobaric'
#cond_quant = csn['quantity'] == 'mass-specific_isochoric_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity']='mass-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition'] = 'isochoric'
#cond_quant = csn['quantity'] == 'volume-specific_isobaric_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity']='volume-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition'] = 'isobaric'
#cond_quant = csn['quantity']=='volume-specific_isochoric_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity']='volume-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition'] = 'isochoric'
#cond_quant = csn['quantity'] == 'static_pressure_environmental_lapse_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity']='environmental_static_pressure_lapse_rate'
#cond_quant = csn['quantity'] == 'temperature_dry_adiabatic_lapse_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity']='temperature_lapse_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition']='adiabatic'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_matter_descriptor']='dry'
#cond_quant = csn['quantity'] == 'temperature_saturated_adiabatic_lapse_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity']='temperature_lapse_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition']='saturated_adiabatic'
#cond_quant = csn['quantity'] == 'temperature_environmental_lapse_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity']='environmental_temperature_lapse_rate'
#cond_quant = csn['quantity'] == 'temperature_lapse_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity']='temperature_lapse_rate'
#cond_quant = csn['quantity'] == 'isentropic_compressibility'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition']='isentropic'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity']='compressibility'
#cond_quant = csn['quantity'] == 'isothermal_compressibility'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition']='isothermal'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity']='compressibility'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##atmosphere_air-column_aerosol~dry
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air-column'
#cond_obj2 = csn['object2'] == 'aerosol~dry'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_abstraction'] = 'column'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'ammonium'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_descriptor'] = 'dry'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_configstate'] = 'aerosol'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##atmosphere_air-column_...-as-...
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air-column'
#cond_obj2 = csn['object2'].str.contains('-as-')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_abstraction'] = 'column'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_expressed-as'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.split('-as-').str[1]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.split('-as').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##atmosphere_air-column_~~~
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air-column'
#cond_obj2 = csn['object2'].str.contains('vapor')
#cond_quant = csn['quantity'] == 'liquid-equivalent_depth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_phasestate'] = 'vapor'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'leq_depth'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_abstraction'] = 'column'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object2']\
#        .str.split('~').str[0].str.replace('aceto-nitrile','acetonitrile')\
#        .str.replace('alpha-hexachlorocyclohexane','alpha-hch')
#csn.loc[ cond_obj0 & cond_obj1,\
#        ['object0','object1','object2']] = ''

##atmosphere_air_carbon-dioxide
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air'
#cond_obj2 = csn['object2'] == 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_phen'] = 'atmosphere'
#cond_quant = csn['quantity'].str.contains('equilibrium')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_condition'] = 'equilibrium'
#cond_quant = csn['quantity'].str.contains('saturated')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_condition'] = 'saturated'
#cond_quant = csn['quantity'].str.contains('equilibrium|saturated')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'partial_pressure'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']]=''
#
##atmosphere_air_flow
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air'
#cond_obj2 = csn['object2'] == 'flow'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'].str.replace('total_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##atmosphere_air_flow_suspended-compound
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air'
#cond_obj2 = csn['object2'] == 'flow'
#cond_obj3 = csn['object3'].str.contains('snow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj3, \
#        'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj3, 'object3']\
#        .str.split('~').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_state'] = 'suspended'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_phasestate'] = 'snow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##atmosphere_air_mercury/nitrogen~...
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air'
#cond_obj2 = csn['object2'].str.contains('mercury|nitrogen')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,'object2']\
#        .str.split('~').str[0]
#cond_obj2 = csn['object2'].str.contains('nitrogen')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_state'] = 'atomic'
#cond_obj2 = csn['object2'].str.contains('mercury')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_phasestate'] = 'gaseous'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_state'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,'object2']\
#        .str.rsplit('~',1).str[1]
#cond_obj2 = csn['object2'].str.contains('mercury|nitrogen')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##atmosphere_air_nmvoc~...
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air'
#cond_obj2 = csn['object2'].str.contains('nmvoc')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_expressed-as'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.split('~').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.split('~').str[1]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##atmosphere_air_radiation
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air'
#cond_obj2 = csn['object2'] == 'radiation'
#cond_obj3 = csn['object3'] != ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_phen'] = 'radiation'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
##        'root_object_trajectory'] = 'optical-path'
#cond_quant = csn['quantity'].str.contains('attenuation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_process_interaction'] = 'attenuation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'process_coefficient'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'evaluation_method'] = 'beer-lambert-law'
#cond_quant = csn['quantity'].str.contains('refractive')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_process_interaction'] = 'refraction'
#cond_quant = csn['quantity'].str.contains('optical-path')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'optical-path_length'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 , \
#        ['object0','object1','object2','object3']] = ''
#
##atmosphere_air_radiation~...
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air'
#cond_obj2 = csn['object2'].str.contains('radiation~')
#cond_quant = csn['quantity'].str.contains('intensity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_in_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, 'object2']\
#        .str.replace('~incoming','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_in_trajectory_direction'] = 'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_matter']='air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~incoming','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'incoming'
#cond_quant = csn['quantity'].str.contains('absorp')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('trans')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction']='transmission'
#cond_quant = csn['quantity'].str.contains('reflect')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction']='reflection'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##atmosphere_air_water~vapor...
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'air'
#cond_obj2 = csn['object2'] == 'water~vapor'
#cond_quant = csn['quantity'].str.contains('density|virtual')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_medium_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_medium_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_context_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_phasestate'] = 'vapor'
#cond_quant = csn['quantity'].str.contains('dew_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_condition'] = 'dew-point'
#cond_quant = csn['quantity'].str.contains('bubble_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_condition'] = 'bubble-point'
#cond_quant = csn['quantity'].str.contains('frost_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_condition'] = 'frost-point'
#cond_quant = csn['quantity'].str.contains('equilibrium')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_condition'] = 'equilibrium'
#cond_quant = csn['quantity'].str.contains('saturated')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_condition'] = 'saturated'
#cond_quant = csn['quantity'].str.contains('point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'temperature'
#cond_quant = csn['quantity'].str.contains('equilibrium|saturated')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'partial_pressure'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##atmosphere_ball
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'ball'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_form'] = 'ball'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_process'] = 'fall'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity']\
#        .str.replace('fall','process')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
##atmosphere_bottom_air
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'] == ''
##cond_quant = csn['quantity'].str.contains('bulk|brutsaert|heat')
#cond_quant = csn['quantity'].str.contains('brutsaert')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_context_phen'] = 'atmosphere'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
##        'root_object_matter'] = 'air'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
##        'root_object_context_part'] = 'bottom'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
##        'root_object_context_form'] = 'atmosphere'
#cond_quant = csn['quantity'].str.contains('isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'mass-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_process_condition'] = 'isobaric'
#cond_quant = csn['quantity'].str.contains('canopy')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_part'] = 'canopy'
#cond_quant = csn['quantity'].str.contains('cloud')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'cloud'
#cond_quant = csn['quantity'].str.contains('brutsaert')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'emissivity_factor'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'evaluation_method'] = 'brutsaert'
##cond_quant = csn['quantity'].str.contains('latent_heat')
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'modified_quantity'] = 'heat~latent'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'modified_quantity'] = \
##        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'modified_quantity'].str.replace('latent_heat_','')
##cond_quant = csn['quantity'].str.contains('sensible_heat')
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'root_object_matter'] = 'heat~sensible'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'modified_quantity'] = \
##        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'modified_quantity'].str.replace('sensible_heat_','')
##cond_quant = csn['quantity'].str.contains('bulk_transfer')
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'modified_quantity']= \
##        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'modified_quantity'].str.replace('bulk_transfer','bulk_heat_transfer')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##atmosphere_bottom_air_carbon-dioxide
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'] == 'carbon-dioxide'
#cond_quant = csn['quantity']=='partial_pressure'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_medium_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_medium_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_medium_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'carbon-dioxide'
#cond_quant = csn['quantity'].str.contains('saturated')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_condition'] = 'saturated'
#cond_quant = csn['quantity'].str.contains('equilibrium')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_condition'] = 'equilibrium'
#cond_quant = csn['quantity'].str.contains('equilibrium|saturate')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'partial_pressure'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##atmosphere_bottom_air_flow(_something)
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'] == 'flow'
#cond_obj4 = csn['object4'] != ''
#cond_quant = csn['quantity'].str.contains('roughness_length')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_exchange_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_exchange_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_exchange_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_exchange_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_exchange2_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#                'object4']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'quantity'].str.replace('total_','')
#cond_quant = csn['quantity'].str.contains('log-law')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'quantity'].str.replace('log-law_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'evaluation_method'] = 'log-law'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##atmosphere_bottom_air_heat_flow
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'] == 'heat'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'heat_roughness_length'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'evaluation_method'] = 'log-law'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##atmosphere_bottom_air_heat~...__flux
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'].str.contains('heat')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'process_heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_process'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
#        .str.split('~').str[1]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##atmosphere_bottom_air_land_heat~...__flux
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'] == 'land'
#cond_obj4 = csn['object4'].str.contains('incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_source_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_source_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_source_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_sink_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'modified_quantity'] = 'incoming_' + \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object4']\
#        .str.replace('heat~incoming~','') + '_heat_energy_flux'
#cond_obj4 = csn['object4'].str.contains('heat~net')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_exchange_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_exchange_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_exchange_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_exchange2_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object4']\
#        .str.replace('heat~net~','') + '_heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##atmosphere_bottom_air_water~vapor(_flow)
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'] == 'water~vapor'
#cond_obj4 = csn['object4'] == 'flow'
#cond_quant = csn['quantity'].str.contains('roughness')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_exchange_context_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_exchange_context_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_exchange_context_context_form'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_exchange_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_exchange_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_exchange_matter_phasestate'] = 'vapor'
#cond_quant = csn['quantity'].str.contains('_point_|equilibrium|saturated')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant,\
#        'root_object_context_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_matter_phasestate'] = 'vapor'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant,\
#        'root_object_medium_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_matter_phasestate'] = 'vapor'
#cond_quant = csn['quantity'].str.contains('dew_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_condition'] = 'dew-point'
#cond_quant = csn['quantity'].str.contains('frost_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_condition'] = 'frost-point'
#cond_quant = csn['quantity'].str.contains('saturated')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_condition'] = 'saturated'
#cond_quant = csn['quantity'].str.contains('equilibrium')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_condition'] = 'equilibrium'
#cond_quant = csn['quantity'].str.contains('equilibrium|saturate')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity']='partial_pressure'
#cond_quant = csn['quantity'].str.contains('_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'temperature'
#cond_quant = csn['quantity'].str.contains('log-law')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'roughness_length'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'evaluation_method'] = 'log-law'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##atmosphere_carbon-dioxide
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_phen'] = 'atmosphere'
##csn.loc[ cond_obj0 & cond_obj1, \
##    'root_object_medium_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
##atmosphere_clouds_radiation~...
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'clouds'
#cond_quant = csn['quantity'].str.endswith('ance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_phen'] = 'clouds'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_context_phen'] = 'atmosphere'
#cond_obj2 = csn['object2'].str.contains('incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~incoming','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_trajectory_direction'] = 'incoming'
#cond_obj2 = csn['object2'].str.contains('outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_trajectory_direction'] = 'outgoing'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~outgoing','')
#cond_quant = csn['quantity'].str.endswith('flux')
#cond_obj2 = csn['object2'].str.contains('incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_phen'] = 'clouds'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'incoming'
#cond_obj2 = csn['object2'].str.contains('outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_phen'] = 'clouds'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'outgoing'
#cond_obj2 = csn['object2'].str.contains('~upward')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'outgoing~upward'
#cond_obj2 = csn['object2'].str.contains('~downward')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'outgoing~downward'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object2']\
#        .str.replace('~outgoing','').str.replace('~incoming','')\
#        .str.replace('~upward','').str.replace('~downward','')
#cond_quant = csn['quantity'].str.contains('absorptance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('reflectance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.contains('transmittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'transmission'
#cond_quant = csn['quantity'].str.contains('emittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_out_process_interaction'] = 'emission'
#cond_quant = csn['quantity'].str.contains('absorbed')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'absorption'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'absorbed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'energy_flux'
#cond_quant = csn['quantity'].str.contains('reflected')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'reflection'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'reflected'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'energy_flux'
#cond_quant = csn['quantity'].str.contains('transmitted')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'transmission'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'transmitted'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'energy_flux'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##atmosphere_datum~.._air(_flow)
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'].str.contains('datum')
#cond_obj3 = csn['object3'] == 'flow'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object1'].str.replace('vertical~','')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_abstraction_descriptor'] = 'vertical'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1, \
#        'modified_quantity'].str.replace('total_','')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1','object2','object3']] = ''
#
##atmosphere_graupel
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'graupel'
#cond_quant = csn['quantity'].str.contains('precipitation')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_matter_phasestate'] = 'graupel'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_source_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_source_process_interaction'] = 'precipitation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#                .str.replace('precipitation','process')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
###atmosphere_hail
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'hail'
#cond_quant = csn['quantity'].str.contains('precipitation')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_matter_phasestate'] = 'hail'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_source_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_source_process_interaction']='precipitation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#                .str.replace('precipitation','process')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
##atmosphere_hydrometeor
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'hydrometeor'
#cond_quant = csn['quantity'].str.contains('fall')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_matter_phasestate'] = 'hydrometeor'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_source_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_process'] = 'fall'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#                .str.replace('fall','process')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
##atmosphere_ice
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'ice'
#cond_quant = csn['quantity'].str.contains('precipitation')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1,\
#        'root_object_source_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_source_process_interaction'] = 'precipitation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#                .str.replace('precipitation','process')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
##atmosphere_radiation~...
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'].str.contains('radiation')
#cond_quant = csn['quantity'].str.endswith('ance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']\
#        .str.replace('~incoming','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_trajectory_direction'] = 'incoming'
#cond_quant = csn['quantity'].str.endswith('flux')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_trajectory_direction'] = 'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']\
#        .str.replace('~incoming','')
#cond_quant = csn['quantity'].str.contains('absorptance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('reflectance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.contains('transmittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'transmission'
#cond_quant = csn['quantity'].str.contains('absorbed')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'absorption'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'absorbed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'energy_flux'
#cond_quant = csn['quantity'].str.contains('reflected')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'reflection'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'reflected'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'energy_flux'
#cond_quant = csn['quantity'].str.contains('transmitted')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'transmission'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'transmitted'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'energy_flux'
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
##atmosphere_raindrop
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'raindrop'
#cond_quant = csn['quantity'].str.contains('fall')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_matter_configstate'] = 'raindrop'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_source_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_process'] = 'fall'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#                .str.replace('fall','process')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
##atmosphere_sleet
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'sleet'
#cond_quant = csn['quantity'].str.contains('precipitation')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_matter_phasestate'] = 'sleet'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_source_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_source_process_interaction'] = 'precipitation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'modified_quantity']\
#                .str.replace('precipitation','process')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
##atmosphere_snow
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'snow'
#cond_quant = csn['quantity'].str.contains('precipitation')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_matter_phasestate'] = 'snow'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_source_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_source_process_interaction'] = 'precipitation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'modified_quantity']\
#                .str.replace('precipitation','process')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
##atmosphere_top_air
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##atmosphere_top_radiation~...
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'].str.contains('radiation~incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_trajectory_direction'] = 'incoming'
#cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_trajectory_direction'] = 'outgoing'
#cond_obj2 = csn['object2'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.replace('~total','').str.replace('~incoming','')\
#        .str.replace('~outgoing','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##atmosphere_top_surface_radiation~...
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_trajectory_direction'] = 'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']\
#        .str.replace('~incoming','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##atmosphere_water
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_source_phen'] = 'atmosphere'
#cond_quant = csn['quantity'].str.contains('precipitation')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_source_process_interaction'] = 'precipitation'
#cond_quant = csn['quantity'].str.contains('leq')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('precipitation','process')\
#        .str.replace('leq-','leq_')
#cond_quant = csn['quantity'].str.contains('snowfall')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_phen'] = 'snowfall'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'modified_quantity']=\
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#                'modified_quantity'].str.replace('snowfall','process')\
#        .str.replace('leq-','leq_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_matter_phasestate'] = 'snow'
#cond_quant = csn['quantity'].str.contains('icefall')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_phen'] = 'icefall'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('icefall_mass','mass').str.replace('icefall','process')\
#        .str.replace('leq-','leq_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_matter_phasestate'] = 'ice'
#cond_quant = csn['quantity'].str.contains('rainfall')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_phen'] = 'rainfall'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'].str.replace('rainfall','process')\
#        .str.replace('leq-','leq_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_matter_phasestate'] = 'liquid'
#cond_quant = csn['quantity'].str.contains('precipiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'quantity'].str.replace('precipiation','process')
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##atmosphere_water~vapor
#cond_obj0 = csn['object0'] == 'atmosphere'
#cond_obj1 = csn['object1'] == 'water~vapor'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_phasestate'] = 'vapor'
#cond_quant = csn['quantity'].str.contains('temperature|saturated')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_phen'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_context_phen'] = 'atmosphere'
#cond_quant = csn['quantity'].str.contains('dew_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_condition'] = 'dew-point'
#cond_quant = csn['quantity'].str.contains('frost_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_condition'] = 'frost-point'
#cond_quant = csn['quantity'].str.contains('saturated')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_condition'] = 'saturated'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'partial_pressure'
#cond_quant = csn['quantity'].str.contains('_point_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'temperature'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##automobile
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == ''
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'automobile'
#cond_quant = csn['quantity'].str.contains('acceleration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'acceleration'
#cond_quant = csn['quantity'].str.contains('0-to-60mph')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = '0-to-60mph'
#cond_quant = csn['quantity'].str.contains('acceleration_time')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'process_time'
#cond_quant = csn['quantity'].str.contains('braking')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'braking'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('braking','process')
#cond_quant = csn['quantity'].str.contains('cargo')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_form'] = ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_role'] = 'cargo'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'number_capacity'
#cond_quant = csn['quantity'].str.contains('seating_capacity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_form'] = ''
#cond_quant = csn['quantity'].str.contains('stopping')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'stopping'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('stopping','process')
#cond_quant = csn['quantity'].str.contains('turning')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'turning'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('turning','process')
#cond_quant = csn['quantity'].str.contains('wheelbase')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_abstraction']='wheelbase'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = 'length'
#cond_quant = csn['quantity'].str.contains('travel')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_undergoing_process'] = 'travel'
#cond_quant = csn['quantity'].str.contains('lifetime')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_process_condition'] = 'lifetime'
#cond_quant = csn['quantity'].str.contains('travel')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('total_travel','process').str.replace('travel','process')\
#        .str.replace('lifetime_','')
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity']\
#        .str.replace('total_','')
#cond_quant = csn['quantity'].str.contains('drag_coefficient')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_undergoing_process'] = 'drag'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity']\
#        .str.replace('drag','process')
#cond_quant = csn['quantity'].str.contains('lift_coefficient')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_undergoing_process'] = 'lift'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity']\
#        .str.replace('lift','process')
#cond_quant = csn['quantity'].str.contains('manufacture')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_undergoing_process'] = 'manufacture'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity']\
#        .str.replace('manufacture','process')
#csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''
#
##automobile_axis~vertical
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'axis~vertical'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'axis'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction_descriptor'] = 'vertical'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##automobile_battery
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'battery'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'battery'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##automobile_bottom_ground
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'ground'
#cond_quant = csn['quantity'].str.contains('angle')
#csn.loc[ cond_obj0 & cond_obj1,'root_object_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1,'root_object_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'process_angle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'quantity'].str.split('_').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_form'] = 'ground'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = 'clearance_height'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##automobile_bumper_bottom
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'bumper'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'bumper'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_reference_form'] = 'ground'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_reference_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'clearance_height'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##automobile_carbon-dioxide
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_source_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_source_process_interaction'] = 'emission'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'process_rate'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##automobile_door
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'door'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'door'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##automobile_driver
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'driver'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_role'] = 'driver'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_undergoing_process'] = 'reaction'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1,'modified_quantity']\
#        .str.replace('reaction','process')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##automobile_engine
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'engine'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'engine'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#        'root_object_context_form'] = 'automobile'
#cond_quant = csn['quantity'].str.contains('-to-')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_quantity1'] = 'power'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_quantity2'] = 'weight'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'two_quantity_operator'] = 'ratio'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1']] = ''
#
##automobile_engine_crankshaft/cylinder
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'engine'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
#        'root_object_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
#        'root_object_context_form'] = 'engine'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
#        'root_object_context_context_form'] = 'automobile'
#cond_quant = csn['quantity'].str.contains('rotation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process']='rotation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'process_rate'
#cond_quant = csn['quantity'].str.contains('stroke')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process']='stroke'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
#        'quantity'].str.replace('stroke','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##automobile_engine_crankshaft/cylinder_piston
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'engine'
#cond_obj3 = csn['object3'] == 'piston'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, 'root_object_form'] = 'piston'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
#        'root_object_context_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
#        'root_object_context_context_form'] = 'engine'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
#        'root_object_context_context_context_form'] = 'automobile'
#cond_quant = csn['quantity'].str.contains('stroke')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process']='stroke'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
#        'quantity'].str.replace('stroke','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##automobile_front_x-section
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'front'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = 'front'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##automobile_fuel__consumption_rate
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'fuel'
#cond_quant = csn['quantity'].str.contains('consumption')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_matter'] = 'fuel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'consumption'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity']='process_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        ['object0','object1']] = ''
#
##automobile_fuel
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'fuel'
#cond_obj2 = csn['object2'] == ''
#cond_quant = csn['quantity'].str.contains('energy-per-mass')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'fuel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'specific_energy'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1']] = ''
#
##automobile_fuel_tank
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'fuel'
#cond_obj2 = csn['object2'] == 'tank'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'fuel-tank'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##automobile_fuel-tank
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'fuel-tank'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'fuel-tank'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##automobile_rear_axle
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'rear'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'axle'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form_descriptor'] = 'rear'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##automobile_seat_belt
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'seat'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'seat-belt'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##automobile_tire
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'tire'
#cond_quant = csn['quantity'].str.contains('inflation')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'tire'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'inflation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'process_pressure'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##automobile_wheel
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'wheel'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'wheel'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##automobile_wheelbase
#cond_obj0 = csn['object0'] == 'automobile'
#cond_obj1 = csn['object1'] == 'wheelbase'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'wheelbase'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'automobile'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#balloon
cond_obj0 = csn['object0'] == 'balloon'
csn.loc[ cond_obj0, 'object_id'] = 'balloon'
csn.loc[ cond_obj0, 'object_label'] = 'balloon'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

##baseball-bat_baseball
#cond_obj0 = csn['object0'] == 'baseball-bat'
#cond_obj1 = csn['object1'] == 'baseball'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'baseball-bat'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_form'] = 'baseball'
#csn.loc[ cond_obj0 & cond_obj1, 'two_object_process_interaction'] = 'impact'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'process_impulse'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#basin
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'].str.contains('flint-law')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'basin~drainage'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'basin~drainage'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']\
        .str.replace('total_contributing','contributing')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'evaluation_model'] = 'flint-law'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

##basin_boundary
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'boundary'
#csn.loc[ cond_obj0 & cond_obj1,'root_object_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1,'root_object_abstraction'] = 'boundary'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##basin_centroid
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'centroid'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'centroid'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##basin_channel-network
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'channel-network'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_configstate'] = 'network'
#cond_quant = csn['quantity'].str.contains('graph')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_abstraction'] = 'graph'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('graph_','')
#cond_quant = csn['quantity'].str.contains('usgs')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'usgs_hydrologic_unit_code'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'].str.replace('total_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1']] = ''
#
##basin_channel-network_graph
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'channel-network'
#cond_obj2 = csn['object2'] == 'graph'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_configstate'] = 'network'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'graph'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##basin_channel-network_link~...
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'channel-network'
#cond_obj2 = csn['object2'].str.contains('link')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_configstate'] = 'network'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.split('~').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_part_descriptor'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.split('~').str[1]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##basin_channel-network_source
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'channel-network'
#cond_obj2 = csn['object2'] == 'source'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_matter_configstate'] = 'network'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_role'] = 'source'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##basin_channels/channel~...(_centerline)
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'].str.contains('channel')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_form']=csn.loc[ cond_obj0 & cond_obj1, 'object1']\
#        .str.split('~').str[0]
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_abstraction'] = csn.loc[ cond_obj0 & cond_obj1, 'object2']
#cond_obj1 = csn['object1'].str.contains('longest')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_form_descriptor']='longest'
#cond_obj1 = csn['object1'].str.contains('channel')
#cond_quant = csn['quantity'].str.contains('flint-law')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'evaluation_assumption'] = 'flint-law'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'quantity'].str.replace('flint-law_','')
#cond_quant = csn['quantity'].str.contains('hack-law')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'evaluation_assumption'] = 'hack-law'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'quantity'].str.replace('hack-law_','')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1','object2']] = ''
#
##basin_land~...
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'].str.contains('land')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_medium_form'] = 'basin~drainage'
#cond_obj1 = csn['object1'].str.contains('burned|forested')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_form'] = csn.loc[ cond_obj0 & cond_obj1, 'object1']\
#        .str.split('~').str[0]
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_form_descriptor'] = csn.loc[ cond_obj0 & cond_obj1, 'object1']\
#        .str.split('~').str[1]
#cond_obj1 = csn['object1'].str.contains('grassland')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_form'] = 'grassland'
#cond_obj1 = csn['object1'].str.contains('land')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1','object2']] = ''
#
##basin_outlet
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'outlet'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_role'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity']\
#        .str.replace('total_contributing','contributing')
#cond_quant = csn['quantity'] == 'bankfull_width'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'width'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition'] = 'bankfull'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1']] = ''
#
##basin_outlet_bank~...
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'outlet'
#cond_obj2 = csn['object2'].str.contains('bank')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_role'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.split('~').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_part_descriptor'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.split('~').str[1]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##basin_outlet_center
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'outlet'
#cond_obj2 = csn['object2'] == 'center'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_role'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'center'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##basin_outlet_channel_bottom
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'outlet'
#cond_obj2 = csn['object2'] == 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_role'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##basin_outlet_sediment
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'outlet'
#cond_obj2 = csn['object2'] == 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_role'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = 'mass-per-time_yield'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##basin_outlet_water_flow
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'outlet'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_role'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_undergoing_process'] = 'friction'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'half_of_fanning_process_factor'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##basin_outlet_water_sediment~...
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'outlet'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'].str.contains('sediment')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_context_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_context_role'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_matter'] = 'water'
#cond_obj3 = csn['object3'].str.contains('suspended')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_state'] = 'suspended'
#cond_obj3 = csn['object3'].str.contains('bedload')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_state'] = 'bedload'
#cond_obj3 = csn['object3'].str.contains('washload')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_state'] = 'washload'
#cond_obj3 = csn['object3'].str.contains('sediment')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#                            'object3'].str.replace('~suspended','')\
#                .str.replace('~total','').str.replace('~bedload','')\
#                .str.replace('~washload','')
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('flow','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##basin_outlet_water_x-section(_top)
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'outlet'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'x-section'
#cond_obj4 = csn['object4'] == 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_role'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'x-section'
#cond_quant = csn['quantity'].str.contains('width-to-depth')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_quantity1'] = 'width'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_quantity2'] = 'depth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'two_quantity_operator']='ratio'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_abstraction_part'] = 'top'
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('flow','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##basin_outlet~terminal_water
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'outlet~terminal'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_role'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_role_descriptor'] = 'terminal'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1, \
#                 'modified_quantity'].str.replace('flow','process')
#csn.loc[ cond_obj0 & cond_obj1,\
#        ['object0','object1','object2','object3','object4']] = ''
#
##basin_rain-gage
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'rain-gauge'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_form'] = 'rain-gauge'
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1']] = ''
#
##basin_sources
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'sources'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_role'] = 'sources'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##basin_weather-station
#cond_obj0 = csn['object0'] == 'basin'
#cond_obj1 = csn['object1'] == 'weather-station'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'weather-station'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##battery
#cond_obj0 = csn['object0'] == 'battery'
#csn.loc[ cond_obj0, 'root_object_form'] = 'battery'
#csn.loc[ cond_obj0, 'object0'] = ''
#
##beam
#cond_obj0 = csn['object0'] == 'beam'
#csn.loc[ cond_obj0,'root_object_form']='beam'
#csn.loc[ cond_obj0,'object0']=''
#
##bear_brain-to-body
#cond_obj0 = csn['object0'] == 'bear'
#csn.loc[ cond_obj0, 'root_object_context_form'] = 'bear'
#csn.loc[ cond_obj0, 'second_root_object_context_form'] = 'bear'
#csn.loc[ cond_obj0, 'root_object_form'] = 'brain'
#csn.loc[ cond_obj0, 'second_root_object_form'] = 'body'
#csn.loc[ cond_obj0, 'root_quantity1'] = 'mass'
#csn.loc[ cond_obj0, 'root_quantity2'] = 'mass'
#csn.loc[ cond_obj0, 'two_object_operator'] = 'ratio'
#csn.loc[ cond_obj0, ['object0','object1']] = ''

#bear~alaskan~black
cond_obj0 = csn['object0'] == 'bear~alaskan~black'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'bear~black~american'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'bear~black~american'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

##bear~alaskan~black_brain-to-body
#cond_obj0 = csn['object0'] == 'bear~alaskan~black'
#cond_obj1 = csn['object1'] == 'brain-to-body'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = \
#                                            'bear~black~american'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_context_form'] = \
#                                            'bear~black~american'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'brain'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_form'] = 'body'
#csn.loc[ cond_obj0 & cond_obj1, 'root_quantity1'] = 'mass'
#csn.loc[ cond_obj0 & cond_obj1, 'root_quantity2'] = 'mass'
#csn.loc[ cond_obj0 & cond_obj1, 'two_object_operator'] = 'ratio'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##bear~alaskan~black_head
#cond_obj0 = csn['object0'] == 'bear~alaskan~black'
#cond_obj1 = csn['object1'] == 'head'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = \
#                                            'bear~black~american'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'head'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#bedrock
cond_obj0 = csn['object0'] == 'bedrock'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1,'object_id']='bedrock'
csn.loc[ cond_obj0 & cond_obj1,'object_label']='bedrock'
csn.loc[ cond_obj0 & cond_obj1,'object_pref']='body'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

##bedrock_below-land-surface
#cond_obj0 = csn['object0'] == 'bedrock'
#cond_obj1 = csn['object1'] == 'below-land-surface'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'bedrock'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_reference_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_reference_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_reference_relationship'] = 'below'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'depth'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#bedrock_material
cond_obj0 = csn['object0'] == 'bedrock'
cond_obj1 = csn['object1'] == 'material'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'bedrock'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'bedrock'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

##bedrock_surface(_land/sea-mask)
#cond_obj0 = csn['object0'] == 'bedrock'
#cond_obj1 = csn['object1'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'bedrock'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_abstraction_abstraction'] = \
#            csn.loc[ cond_obj0 & cond_obj1, 'object2']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##benzene_molecule_c_c_c
#cond_obj0 = csn['object0'] == 'benzene'
#csn.loc[ cond_obj0, 'root_object_phen'] = 'bond~c-c-c'
#csn.loc[ cond_obj0, 'root_object_context_matter_configstate'] = 'molecule'
#csn.loc[ cond_obj0, 'root_object_context_matter'] = 'benzene'
#csn.loc[ cond_obj0, 'modified_quantity'] = 'angle'
#csn.loc[ cond_obj0, ['object0','object1','object2','object3','object4']] = ''

#black-hole
cond_obj0 = csn['object0'] == 'black-hole'
csn.loc[ cond_obj0, 'object_label'] = 'black-hole'
csn.loc[ cond_obj0, 'object_id'] = 'black-hole'
csn.loc[ cond_obj0, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

#bridge
cond_obj0 = csn['object0'] == 'bridge'
csn.loc[ cond_obj0, 'object_label'] = 'bridge'
csn.loc[ cond_obj0, 'object_id'] = 'bridge'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

#building~empire-state
cond_obj0 = csn['object0'] == 'building~empire-state'
csn.loc[ cond_obj0, 'object_id'] = 'building~empire-state'
csn.loc[ cond_obj0, 'object_label'] = 'building~empire-state'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

#cantor-set
cond_obj0 = csn['object0'] == 'cantor-set'
csn.loc[ cond_obj0, 'object_label'] = 'cantor-set'
csn.loc[ cond_obj0, 'object_id'] = 'cantor-set'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

#carbon_hydrogen__bond_length
cond_obj0 = csn['object0'] == 'carbon'
cond_obj1 = csn['object1'] == 'hydrogen'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'bond~c-h'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'bond~c-h'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = 'length'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = 'length'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

##carbon_isotope_neutron
#cond_obj0 = csn['object0'] == 'carbon'
#cond_obj1 = csn['object1'] == 'isotope'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_matter'] = 'carbon'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_matter_configstate'] = 'isotope'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'neutron'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##cesium
##cond_obj0 = csn['object0'] == 'cesium'
##cond_obj1 = csn['object1'] == ''
##cond_quant = csn['quantity'].str.contains('emission')
##csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
##        'root_object_matter'] = 'cesium'
##csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
##        'root_object_matter_configstate'] = 'atom'
##csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
##        'root_object_source_matter'] = 'cesium'
##csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
##        'root_object_source_matter_configstate']='atom'
##csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##cesium_atom(_neutron/proton)
#cond_obj0 = csn['object0'] == 'cesium'
#cond_quant = csn['quantity'].str.contains('emission')
#csn.loc[ cond_obj0, 'root_object_context_matter'] = 'cesium'
#csn.loc[ cond_obj0, 'root_object_context_matter_configstate'] = 'atom'
#csn.loc[ cond_obj0, 'root_object_matter'] = \
#        csn.loc[ cond_obj0, 'object2']
#csn.loc[ cond_obj0 & cond_quant, \
#        'root_object_source_process_interaction'] = 'emission'
#csn.loc[ cond_obj0 & cond_quant, \
#        'modified_quantity']='characteristic_process_frequency'
#csn.loc[ cond_obj0, ['object0','object1','object2']] = ''
#
##channel
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == ''
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'channel'
#cond_quant = csn['quantity'].str.contains('downstream')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_location'] = 'downstream'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('downstream_','')
#cond_quant = csn['quantity'].str.contains('station')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_context_form'] = 'station'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_context_relationship'] = 'at'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('station_','')
#csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''
#
##channel_bank_sediment_water
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'bank'
#cond_obj2 = csn['object2'] == 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_part'] = 'bank'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_condition'] = 'saturated'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'].str.replace('saturated_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##channel_bank_water
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'bank'
#cond_obj2 = csn['object2'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_part'] = 'bank'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = 'volume-per-length_process_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##channel_bottom_sediment
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'sediment'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##channel_bottom_sediment_grain
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'sediment'
#cond_obj3 = csn['object3'] == 'grain'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_configstate'] = 'grain'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##channel_bottom_sediment_oxygen~dissolved
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'sediment'
#cond_obj3 = csn['object3'] == 'oxygen~dissolved'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'oxygen'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_state'] = 'dissolved'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_process_interaction']='consumption'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'process_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##channel_bottom_sediment_water
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'sediment'
#cond_obj3 = csn['object3'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_condition'] = 'saturated'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'].str.replace('saturated_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##channel_bottom_surface
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##channel_bottom_water
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##channel_bottom_water_flow(_sediment(_grain))
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'flow'
#cond_obj4 = csn['object4'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_process'] = 'flow'
#cond_obj4 = csn['object4'] == 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_context_part'] = 'bottom'
#cond_obj5 = csn['object5'] == 'grain'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
#        'root_object_matter_configstate'] = 'grain'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
#        'modified_quantity'].str.replace('total_','')
#cond_quant = csn['quantity'].str.contains('log-law')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'evaluation_method'] = 'log-law'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'].str.replace('log-law_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##channel_centerline(_endpoints)
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'centerline'
#cond_obj2 = csn['object2'] == 'endpoints'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'centerline'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction'] = 'endpoints'
#cond_quant = csn['quantity'].str.contains('downvalley')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_location'] = 'downvalley'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'sinuosity'
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1','object2']] = ''
#
##channel_entrance_basin
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'entrance'
#cond_obj2 = csn['object2'] == 'basin'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity'] = \
#    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity']\
#    .str.replace('total_contributing','contributing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##channel_entrance_center
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'entrance'
#cond_obj2 = csn['object2'] == 'center'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'center'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##channel_entrance_water_x-section
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'entrance'
#cond_obj2 = csn['object2'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'volume_process_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##channel_exit_basin
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'exit'
#cond_obj2 = csn['object2'] == 'basin'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source_part'] = 'exit'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'basin~drainage'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'].str.replace('total_contributing','contributing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##channel_exit_center
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'exit'
#cond_obj2 = csn['object2'] == 'center'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = 'exit'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'center'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##channel_exit_water_x-section(_sediment) 
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'exit'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'x-section'
#cond_obj4 = csn['object4'] != ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter_state'] = 'suspended'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_context_part'] = 'exit'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'modified_quantity'] = 'mass_process_rate'
#
#cond_obj4 = csn['object4'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_part'] = 'exit'
#cond_quant = csn['quantity'].str.contains('_flow_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & \
#        cond_obj3 & cond_obj4 & cond_quant, 'modified_quantity']\
#        .str.replace('_flow_','_process_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##channel_meander
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'meander'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_process'] = 'meander'
#cond_quant = csn['quantity'].str.contains('migration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'migration'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'process_rate'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##channel_valley_centerline
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'valley'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'valley'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'centerline'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##channel_water
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#    'root_object_matter']='water'
#cond_quant = csn['quantity'].str.contains('ic_volume')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'volume_' +csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'].str.replace('volume_','')
#cond_quant = csn['quantity'].str.contains('shear')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'shear_' +csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'].str.replace('shear_','')
#cond_quant = csn['quantity'].str.contains('_flow_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process']='flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('flow','process')
#cond_quant = csn['quantity'].str.contains('reaeration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process']='reaeration'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'process_coefficient'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1',]]=''
#
##channel_water_channel_bottom_surface
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'two_object_operator'] = 'product'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_quantity1'] = 'depth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_quantity2'] = 'slope'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##channel_water_flow
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'flow'
#cond_quant = csn['quantity'].str.contains('dissipation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'dissipation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'energy-per-volume_process_rate'
#cond_quant = csn['quantity'].str.contains('manning')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#            'modified_quantity'].str.replace('manning_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'evaluation_method'] = 'manning-formula'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'].str.replace('total_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']]=''
#
##channel_water_hydraulic-jump
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'hydraulic-jump'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_phen'] = 'hydraulic-jump'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##channel_water_oxygen~photosynthetic
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'oxygen~photosynthetic'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source_context_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'oxygen'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source'] = 'photosynthetic'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source_process_interaction'] = 'production'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = 'process_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']]=''
#
##channel_water_sediment~...
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'].str.contains('suspended')
#cond_quant = csn['quantity'].str.contains('concentration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_state'] = 'suspended'
#cond_obj2 = csn['object2'].str.contains('bedload')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_state'] = 'bedload'
#cond_obj2 = csn['object2'].str.contains('washload')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_state'] = 'washload'
#cond_obj2 = csn['object2'].str.contains('sediment')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_context_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_context_matter']='water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.replace('~suspended','').str.replace('~total','')\
#        .str.replace('~bedload','').str.replace('~washload','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_descriptor'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#cond_quant = csn['quantity'].str.contains('immersed')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition'] = 'immersed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'weight'
#cond_quant = csn['quantity'].str.contains('settling')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'settling'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'stokes_process_speed'
#cond_quant = csn['quantity'].str.contains('_flow_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('flow','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##channel_water_surface_air
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'surface'
#cond_obj3 = csn['object3'] == 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,\
#    'root_object_matter']='air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,\
#    'object_context_matter']='water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,\
#    'object_context_context_form']='channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,\
#    'object_context_abstraction']='surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,\
#    'object_context_relationship']='above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,\
#    ['object0','object1','object2','object3']]=''
#
##channel_water_surface
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##channel_water_x-section(_top)
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'x-section'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'x-section'
#cond_quant = csn['quantity'].str.contains('ratio')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_quantity1'] = 'width'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_quantity2'] = 'depth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'two_quantity_operator'] = 'ratio'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#cond_quant = csn['quantity'].str.contains('_flow_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('flow','process')
#cond_quant = csn['quantity'].str.contains('wetted')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition'] = 'wetted'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'quantity'].str.replace('wetted_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##channel_weir
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'weir'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'weir'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##channel_x-section
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'x-section'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#    'root_object_form']='channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#    'root_object_abstraction']='x-section'
#cond_quant = csn['quantity'].str.contains('-to-')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_quantity1'] = 'width'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_quantity2'] = 'depth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'two_quantity_operator'] = 'ratio'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1']] = ''
#
##channel_x-section_parabola
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'x-section'
#cond_obj2 = csn['object2'] == 'parabola'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction'] = 'parabola'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##channel_x-section_top
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'x-section'
#cond_obj2 = csn['object2'] == 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##channel_x-section_trapezoid
#cond_obj0 = csn['object0'] == 'channel'
#cond_obj1 = csn['object1'] == 'x-section'
#cond_obj2 = csn['object2'] == 'trapezoid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'channel'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction'] = 'trapezoid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']\
#        .str.split('~').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction_part_descriptor'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']\
#        .str.split('~').str[1]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##chlorine_electron
#cond_obj0 = csn['object0'] == 'chlorine'
#cond_obj1 = csn['object1'] == 'electron'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'chlorine'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'electron_affinity'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##chocolate
#cond_obj0 = csn['object0'] == 'chocolate'
#cond_obj1 = csn['object1'] == ''
#csn.loc[ cond_obj0 & cond_obj1,'root_object_matter']='chocolate'
#cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'mass-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process_condition'] = 'isobaric'
#cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'mass-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process_condition'] = 'isochoric'
#cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'volume-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process_condition'] = 'isobaric'
#cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'volume-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process_condition'] = 'isochoric'
#cond_quant = csn['quantity'].str.contains('thermal_inertia')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'volume-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('melting')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'melting-point'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'temperature'
#cond_quant = csn['quantity'].str.contains('tempering')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'tempering'
#cond_quant = csn['quantity'].str.contains('conching')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'conching'
#cond_quant = csn['quantity'].str.contains('tempering|conching')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'process_time'
#cond_quant = csn['quantity'].str.contains('metabolizable')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'metabolizable'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'energy-per-mass_density'
#csn.loc[ cond_obj0 & cond_obj1,'object0'] = ''
#
##chocolate_cacao/...
#cond_obj0 = csn['object0'] == 'chocolate'
#csn.loc[ cond_obj0, 'root_object_medium_matter'] = 'chocolate'
#csn.loc[ cond_obj0, 'root_object_matter'] = csn.loc[ cond_obj0, 'object1']\
#        .str.replace('~total','').str.replace('~polyunsaturated','')\
#        .str.replace('~monounsaturated','').str.replace('~saturated','')
#cond_obj1 = csn['object1'].str.contains('~polyunsaturated')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_state'] = 'polyunsaturated'
#cond_obj1 = csn['object1'].str.contains('~monounsaturated')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_state'] = 'monounsaturated'
#cond_obj1 = csn['object1'].str.contains('~unsaturated')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_state'] = 'unsaturated'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##chocolate~liquid
#cond_obj0 = csn['object0'] == 'chocolate~liquid'
#cond_obj1 = csn['object1'] == ''
#csn.loc[ cond_obj0 & cond_obj1,'root_object_matter']='chocolate'
#csn.loc[ cond_obj0 & cond_obj1,'root_object_matter_phasestate']='liquid'
#cond_quant = csn['quantity'].str.contains('kinematic')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'shear_kinematic_viscosity'
#cond_quant = csn['quantity'].str.contains('casson')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'viscosity_coefficient'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'evaluation_assumption'] = 'casson-model'
#cond_quant = csn['quantity'].str.contains('herschel')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'quantity'].str.replace('herschel-bulkley_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'evaluation_assumption'] = 'herschel-bulkley'
#cond_obj1 = csn['object1'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_matter'] = 'chocolate'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_medium_matter_phasestate'] = 'liquid'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##coal
#cond_obj0 = csn['object0'] == 'coal'
#csn.loc[ cond_obj0, 'root_object_medium_matter'] = 'coal'
#csn.loc[ cond_obj0, 'object0'] = ''
#
##concrete_rubber
#cond_obj0 = csn['object0'] == 'concrete'
#cond_obj1 = csn['object1'] == 'rubber'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_exchange_matter'] = 'concrete'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_exchange2_matter'] = 'rubber'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_exchange_process_interaction'] = 'friction'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'kinetic_process_coefficient'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##consumer
#cond_obj0 = csn['object0'] == 'consumer'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'market-basket'
#csn.loc[ cond_obj0, 'modified_quantity'] = 'consumer_price_index'
#csn.loc[ cond_obj0, 'object0'] = ''

#delta
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'].str.contains('subsidence')
csn.loc[ cond_obj0 & cond_obj1,'object_label'] = 'delta'
csn.loc[ cond_obj0 & cond_obj1,'object_id'] = 'delta'
csn.loc[ cond_obj0 & cond_obj1,'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'delta_subsidence'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_label'] = 'delta_subsidence'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']    
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

##delta_apex
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'apex'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'apex'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##delta_apex-to-shoreline
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'apex-to-shoreline'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'apex'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_abstraction'] = 'shoreline'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##delta_beds~...
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('beds')
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##delta_beds~..._sediment_clay/...
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('beds')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_context_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object1']
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object3']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2','object3']] = ''
#
##delta_channel~main_entrance
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'channel~main'
#cond_obj2 = csn['object2'] == 'entrance'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = 'channel~main'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']]=''
#
##delta_channel~main_entrance_center
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'channel~main'
#cond_obj2 = csn['object2'] == 'entrance'
#cond_obj3 = csn['object3'] == 'center'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = 'channel~main'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'center'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##delta_channel~main_entrance_water_sediment_clay/..._grain
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'channel~main'
#cond_obj2 = csn['object2'] == 'entrance'
#cond_obj3 = csn['object3'] == 'water'
#cond_obj4 = csn['object4'] == 'sediment'
#cond_obj6 = csn['object6'] == 'grain'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6, \
#        'root_object_context_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6,\
#        'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & \
#                cond_obj6, 'object5']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6, \
#        'root_object_matter_configstate'] = 'grain'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6,\
#        'root_object_context_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6,\
#        'root_object_context_context_context_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6,\
#        'root_object_context_context_context_form'] = 'channel~main'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6,\
#        'root_object_context_context_context_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6,\
#        ['object0','object1','object2','object3','object4','object5',
#         'object6']] = ''
#
##delta_channel~main_entrance_water_sediment_clay/...
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'channel~main'
#cond_obj2 = csn['object2'] == 'entrance'
#cond_obj3 = csn['object3'] == 'water'
#cond_obj4 = csn['object4'] == 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & \
#                            cond_obj3 & cond_obj4, 'object5']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_context_context_form'] = 'channel~main'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_context_context_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_context_context_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##delta_channel~main_entrance_water_sediment~...
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'channel~main'
#cond_obj2 = csn['object2'] == 'entrance'
#cond_obj3 = csn['object3'] == 'water'
#cond_obj4 = csn['object4'].str.contains('sediment')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#                'object4'].str.replace('~suspended','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter_phasestate'] = 'suspended'
#cond_quant = csn['quantity'].str.contains('concentration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_medium_context_form'] = 'channel~main'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_medium_context_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_medium_context_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_context_context_form'] = 'channel~main'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_context_context_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_context_context_part'] = 'entrance'
#cond_quant = csn['quantity'].str.contains('transport')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_undergoing_process'] = 'transport'
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_undergoing_process'] = 'flow'
#cond_quant = csn['quantity'].str.contains('transport|flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'modified_quantity'] = 'mass_process_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4,\
#        ['object0','object1','object2','object3','object4']] = ''
#
##delta_channel~main_entrance_water_x-section
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'channel~main'
#cond_obj2 = csn['object2'] == 'entrance'
#cond_obj3 = csn['object3'] == 'water'
#cond_obj4 = csn['object4'].str.contains('x')
#cond_obj6 = csn['object6'] == 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = 'water'
#cond_quant = csn['quantity'].str.contains('wetted')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_context_form'] = 'channel~main'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_context_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_context_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_medium_form'] = 'channel~main'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_medium_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_medium_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6, \
#        'root_object_abstraction_part'] = 'top'
#cond_quant = csn['quantity'].str.contains('-to-')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_quantity1'] = 'width'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_quantity2'] = 'depth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'two_quantity_operator'] = 'ratio'
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'modified_quantity'] = 'volume_process_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        ['object0','object1','object2','object3','object4','object5',
#         'object6']] = ''
#
##delta_channel~main_entrance_x-section
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'channel~main'
#cond_obj2 = csn['object2'] == 'entrance'
#cond_obj3 = csn['object3'].str.contains('x')
#cond_obj5 = csn['object5'] == 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = 'channel~main'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = 'entrance'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
#        'root_object_abstraction_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#         ['object0','object1','object2','object3','object4','object5']] = ''
#
##delta_distributary(-network)
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('distributary')
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity']\
#        .str.replace('total_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##delta_distributary(-network)_water
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('distributary')
#cond_obj2 = csn['object2'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_context_form'] = \
#    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1',
#                                             'object2']] = ''
#
##delta_distributary(-network)_outlet
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('distributary')
#cond_obj2 = csn['object2'] == 'outlet'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'root_object_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = 'outlet'
#cond_quant = csn['quantity'].str.startswith('top_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_part_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'width'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##delta_distributary(-network)_outlet_center/side~...
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('distributary')
#cond_obj2 = csn['object2'] == 'outlet'
#cond_obj3 = csn['object3'].str.contains('center|side')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = 'outlet'
#cond_obj3 = csn['object3'].str.contains('center')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#cond_obj3 = csn['object3'].str.contains('side')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'root_object_part_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#cond_obj3 = csn['object3'].str.contains('center|side')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##delta_distributary(-network)_outlet_water_x-section
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('distributary')
#cond_obj2 = csn['object2'] == 'outlet'
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_part'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'volume_process_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##delta_front_sediment(_grain)
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'front'
#cond_obj2 = csn['object2'] == 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_part'] = 'front'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_configstate'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##delta_front(_toe)
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'front'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = 'front'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object2']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##delta_plain~...
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('plain')
#cond_quant = csn['quantity'].str.contains('fraction')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']\
#        .str.replace('~total','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, ['object0','object1']] = ''
#
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('plain')
#cond_obj2 = csn['object2'] == 'vegetation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']\
#        .str.replace('~total','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'vegetation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('plain')
#cond_obj2 = csn['object2'] == 'plain~total'        
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'plain~subaqueous'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_form'] = 'plain'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_quantity1'] = 'area'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_quantity2'] = 'area'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'two_object_operator'] = 'ratio'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'].str.contains('plain')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object1']\
#        .str.replace('~total','')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object2']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##delta_shoreline
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'shoreline'
#cond_obj2 = csn['object2'] == 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_abstraction'] = 'shoreline'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_in_context_form'] = 'ocean'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_in_phen'] = 'wave'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_in_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_in_process_interaction'] = 'reworking'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = 'process_depth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'shoreline'
#cond_obj2 = csn['object2'] == 'sediment'
#cond_quant = csn['quantity'].str.contains('progradation')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'shoreline'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'progradation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'process_rate'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##delta_x-section
#cond_obj0 = csn['object0'] == 'delta'
#cond_obj1 = csn['object1'] == 'x-section'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'delta'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##delta~...
#cond_obj0 = csn['object0'].str.contains('delta')
#csn.loc[ cond_obj0, 'root_object_form'] = csn.loc[ cond_obj0, 'object0']
#csn.loc[ cond_obj0, 'object0'] = ''
#
##dihydrogen/dinitrogen..._molecule_...
#cond_obj0 = csn['object0'].str.contains('dihydrogen|dinitrogen|dioxygen')
#csn.loc[ cond_obj0, 'root_object_context_matter'] = \
#        csn.loc[ cond_obj0, 'object0']
#csn.loc[ cond_obj0, 'root_object_context_matter_configstate'] = 'molecule'
#csn.loc[ cond_obj0, 'root_object_form'] = 'bond~' + \
#        csn.loc[ cond_obj0, 'object2']
#csn.loc[ cond_obj0, 'modified_quantity'] = 'length'
#csn.loc[ cond_obj0, ['object0','object1','object2']] = ''
#
##earth
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == ''
#cond_quant = csn['quantity'] == 'standard_gravity_constant'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant , 'modified_quantity'] = \
#        'standard_gravitational_acceleration'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'earth'
#cond_quant = csn['quantity'].str.contains('orbital')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_trajectory'] = 'orbit'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#                .str.replace('orbital_','')
#cond_quant = csn['quantity'].str.contains('rotation_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#         'root_object_undergoing_process'] = 'rotation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#                .str.replace('rotation_','process_')
#csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''
#
##earth-to-...
#cond_obj0 = csn['object0'].str.contains('earth-to')
#cond_quant = csn['quantity'].str.contains('travel')
#csn.loc[ cond_obj0 & ~cond_quant, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & ~cond_quant, 'second_root_object_form'] = \
#        csn.loc[ cond_obj0 & ~cond_quant, 'object0'].str.split('-to-').str[1]
#csn.loc[ cond_obj0 & cond_quant, 'root_object_source_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_quant, 'root_object_sink_form'] = \
#        csn.loc[ cond_obj0 & cond_quant, 'object0'].str.split('-to-').str[1]
#csn.loc[ cond_obj0 & cond_quant, 'root_object_process'] = 'travel'
#csn.loc[ cond_obj0 & cond_quant, 'modified_quantity'] = 'time'
#csn.loc[ cond_obj0, 'object0']=''
#
##earth_atmosphere
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1, 'object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1, 'object_context_relationship'] = 'surrounding'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'atmosphere'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##earth_axis/black-body
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'].str.contains('axis|body')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = \
#    csn.loc[ cond_obj0 & cond_obj1, 'object1']
#cond_quant = csn['quantity'].str.contains('nutation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'nutation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('nutation','process')
#cond_quant = csn['quantity'].str.contains('precession')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'precession'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('precession','process')
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##earth_day~
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'].str.contains('day~')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1,'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object1']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##earth_..._boundary
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj2 = csn['object2'] == 'boundary'
#csn.loc[ cond_obj0 & cond_obj2, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj2, 'root_object_abstraction'] = \
#        'boundary~' + csn.loc[ cond_obj0 & cond_obj2, 'object1']
#csn.loc[ cond_obj0 & cond_obj2, ['object0','object1','object2']] = ''
#
##earth_core~...
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'].str.contains('core')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object1']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##earth_crust_material
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'crust'
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == ''
##cond_quant = csn['quantity']\
##    .str.contains('thermal|heat|conductivity|permittivity|permeability|wave|oxygen')\
##    | csn['quantity'].str.contains('isothermal')
#cond_quant = csn['quantity'].str.contains('wave|oxygen')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_part'] = 'crust'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_matter'] = 'material'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'root_object_medium_form'] = 'earth'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'root_object_medium_part'] = 'crust'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'root_object_medium_matter'] = 'material'
##cond_quant = csn['quantity'].str.contains('oxygen|wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_context_part'] = 'crust'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_context_matter'] = 'material'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'root_object_medium_form'] = ''
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'root_object_medium_part'] = ''
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
##        'root_object_medium_matter'] = ''
#cond_quant = csn['quantity'].str.contains('oxygen')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_matter'] = 'oxygen'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'fugacity'
#cond_quant = csn['quantity'].str.contains('_over_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~p'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'second_root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'second_root_object_context_part'] = 'crust'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'second_root_object_context_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'second_root_object_phen'] = 'wave~seismic~s'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'two_object_operator'] = 'ratio'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_quantity1'] = 'velocity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_quantity2'] = 'velocity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'velocity_ratio'
#cond_quant = csn['quantity'].str.contains('dynamic_volume')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'volume_viscosity'
#cond_quant = csn['quantity'].str.contains('kinematic_shear')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'momentum_diffusivity'
#cond_quant = csn['quantity'].str.contains('kinematic_volume')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'volume_viscosity'
#cond_quant = csn['quantity'].str.contains('sh-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~sh'
#cond_quant = csn['quantity'].str.contains('sp-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~sp'
#cond_quant = csn['quantity'].str.contains('sv-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~sv'
#cond_quant = csn['quantity'].str.contains('sp-wave|sh-wave|sv-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'velocity'
#cond_quant = csn['quantity'].str.contains('s-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~s'
#cond_quant = csn['quantity'].str.contains('p-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~p'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('p-wave_','')
#cond_quant = csn['quantity'].str.contains('s-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('s-wave_','')
#cond_quant = csn['quantity'].str.contains('power-law_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'].str.replace('power-law','power-law-fluid')
#cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'isobaric_mass-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'isochoric_mass-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'isobaric_volume-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity']='isochoric_volume-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#        
##earth_mantle/crust_material_melt~partial
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'].str.contains('mantle|crust')
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == 'melt~partial'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_phasestate'] = 'melt~partial'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_mantle/crust_material_carbonatite_melt
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'].str.contains('mantle|crust')
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == 'carbonatite'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_phasestate'] = 'melt'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'carbonatite'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##earth_mantle/crust_material_water
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'].str.contains('mantle|crust')
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_datum_ellipsoid
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'datum'
#cond_obj2 = csn['object2'] == 'ellipsoid'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'datum'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction_abstraction'] = 'ellipsoid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_datum_ellipsoid_surface_point-pair_geodesic__distance ???
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'datum'
#cond_obj2 = csn['object2'] == 'ellipsoid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_abstraction'] = 'datum'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'second_root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_abstraction'] = 'datum'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction'] = 'ellipsoid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_abstraction']='geodesic'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##earth_ellipsoid/equator
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'].str.contains('ellipsoid|equator|pole|surface')
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_abstraction'] = \
#         csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']   
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##earth_equator_plane-to-sun
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'].str.contains('equator')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'equator'   
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction_abstraction'] = 'plane'   
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_form'] = 'sun'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##earth_gravity
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'gravity'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##earth_human
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'human'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'human'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_process_interaction'] = 'carrying'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##earth_interior
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'interior'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = 'interior'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##earth_interior_earthquake
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'interior'
#cond_obj2 = csn['object2'] == 'earthquake'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'interior'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_phen'] = 'earthquake'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##earth_interior_earthquake_fault
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'interior'
#cond_obj2 = csn['object2'] == 'earthquake'
#cond_obj3 = csn['object3'] == 'fault'
#cond_obj5 = csn['object5'] == 'asperity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'interior'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = 'fault'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object4']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
#        'modified_quantity'] = 'asperity_contact_area'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_phen'] = 'earthquake'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##earth_interior_earthquake_focus
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'interior'
#cond_obj2 = csn['object2'] == 'earthquake'
#cond_obj3 = csn['object3'] == 'focus'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'interior'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'focus'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_phen'] = 'earthquake'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##earth_interior_earthquake_hypocenter
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'interior'
#cond_obj2 = csn['object2'] == 'earthquake'
#cond_obj3 = csn['object3'] == 'hypocenter'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'interior'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'hypocenter'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_phen'] = 'earthquake'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##earth_interior_earthquake_wave~
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'interior'
#cond_obj2 = csn['object2'] == 'earthquake'
#cond_obj3 = csn['object3'].str.contains('wave~')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'interior'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_phen'] = 'earthquake'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
#        .replace('wave~s','wave~seismic~s').replace('wave~p','wave~seismic~p')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'].str.replace('angular_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_interior_earthquake_hypocenter-to-station
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'interior'
#cond_obj2 = csn['object2'] == 'earthquake'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_part'] = 'interior'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'hypocenter'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_phen'] = 'earthquake'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_form'] = 'station'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##earth_interior_particle(_motion)
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'interior'
#cond_obj2 = csn['object2'] == 'particle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_part'] = 'interior'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'particle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_process'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#cond_quant = csn['quantity'].str.contains('acceleration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process']='acceleration'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_interior_wave~...
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'interior'
#cond_obj2 = csn['object2'].str.contains('wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_part'] = 'interior'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'].str.replace('angular_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##earth_mantle_material
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'mantle'
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == ''
#cond_quant = ~csn['quantity'].str.contains('thermal|heat|oxygen|electrical|wave')|\
#          csn['quantity'].str.contains('isothermal')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_matter'] = 'material'
#cond_quant = csn['quantity'].str.contains('wave|oxygen')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_context_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_context_matter'] = 'material'
#cond_quant = csn['quantity'].str.contains('thermal|heat|electrical') & \
#          ~csn['quantity'].str.contains('isothermal')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_matter'] = 'material'
#cond_quant = csn['quantity'].str.contains('oxygen')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_matter'] = 'oxygen'
#cond_quant = csn['quantity'].str.contains('oxygen')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'fugacity'
#cond_quant = csn['quantity'].str.contains('dynamic_volume')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'volume_viscosity'
#cond_quant = csn['quantity'].str.contains('_over_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~p'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'second_root_object_phen'] = 'wave~seismic~s'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_quantity1'] = 'velocity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_quantity2'] = 'velocity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'two_object_operator'] = 'ratio'
#cond_quant = csn['quantity'].str.contains('p-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~p'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('p-wave_','')
#cond_quant = csn['quantity'].str.contains('s-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~s'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('s-wave_','')
#cond_quant = csn['quantity'].str.contains('sh-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~sh'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('sh-wave_','')
#cond_quant = csn['quantity'].str.contains('sv-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~sv'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('sv-wave_','')
#cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity']\
#                .str.replace('mass-specific_isobaric','isobaric_mass-specific')
#cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity']\
#                .str.replace('mass-specific_isochoric','isochoric_mass-specific')
#cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity']\
#        .str.replace('volume-specific_isobaric','isobaric_volume-specific')
#cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity']\
#        .str.replace('volume-specific_isochoric','isochoric_volume-specific')
#cond_quant = csn['quantity'].str.contains('kinematic_shear')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'momentum_diffusivity'
#cond_quant = csn['quantity'].str.contains('kinematic_volume')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'volume_viscosity'
#cond_quant = csn['quantity'].str.contains('power-law')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('power-law','power-law-fluid')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##earth_mantle_material_flow
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'mantle'
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_mantle_material_mineral-phase
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'mantle'
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == 'mineral-phase'
#cond_obj4 = csn['object4'] == ''
#cond_quant = csn['quantity'].str.contains('oxygen')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
#        'root_object_matter_phasestate'] = 'mineral-phase'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_context_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_context_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_context_matter_phasestate'] = 'mineral-phase'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'root_object_matter'] = 'oxygen'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'modified_quantity'] = 'fugacity'
#cond_quant = csn['quantity'].str.contains('chemical_composition')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'modified_quantity'] = 'chemical-composition_(en)'
#cond_quant = csn['quantity'].str.contains('physical_state')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
#        'modified_quantity'] = 'physical-state_(en)'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_mantle_material_mineral-phase_carbonatite_melt
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'mantle'
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == 'mineral-phase'
#cond_obj4 = csn['object4'] == 'carbonatite'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_matter_phasestate'] = 'mineral-phase'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = 'carbonatite'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter_phasestate'] = 'melt'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        ['object0','object1','object2','object3', 'object4','object5']] = ''
#
##earth_mantle_material_mineral-phase_melt_water
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'mantle'
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == 'mineral-phase'
#cond_obj4 = csn['object4'] == 'melt'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_matter_phasestate'] = 'mineral-phase~melt'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##earth_mantle_material_mineral-phase_water__solubility
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'mantle'
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == 'mineral-phase'
#cond_obj4 = csn['object4'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_medium_matter_phasestate'] = 'mineral-phase'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##earth_mantle_material_mineral-phase_melt~partial
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'mantle'
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == 'mineral-phase'
#cond_obj4 = csn['object4'] == 'melt~partial'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#         'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#         'root_object_medium_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#         'root_object_medium_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#         'root_object_medium_matter_phasestate'] = 'mineral-phase'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#         'root_object_matter_phasestate'] = 'melt~partial'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##earth_mantle_material_mohr-coulomb-plastic
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'mantle'
#cond_obj2 = csn['object2'] == 'material'
#cond_obj3 = csn['object3'] == 'mohr-coulomb-plastic'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = 'mantle'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_phasestate'] = 'mohr-coulomb-plastic'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_material
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'material'
#cond_quant = csn['quantity'].str.contains('p_wave')
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'root_object_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_context_matter'] = 'material'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_phen'] = 'wave~seismic~p'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = 'modulus'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##earth_orbit
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'orbit'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_trajectory'] = 'orbit'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_trajectory_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object2']
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_trajectory_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object3']
#cond_quant = csn['quantity'].str.contains('aphelion')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_trajectory_abstraction'] = 'aphelion'
#cond_quant = csn['quantity'].str.contains('perihelion')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_trajectory_abstraction'] = 'perihelion'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity']\
#        .str.replace('aphelion_','').str.replace('perihelion_','')
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_surface_earthquake_epicenter
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'earthquake'
#cond_obj3 = csn['object3'] == 'epicenter'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_phen'] = 'earthquake'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'epicenter'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_surface_earthquake_wave~..._station
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'earthquake'
#cond_obj3 = csn['object3'].str.contains('wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_phen'] = 'earthquake'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,'root_object_phen']=\
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
#        .replace('wave~s','wave~seismic~s').replace('wave~p','wave~seismic~p')
#cond_quant = csn['quantity'].str.contains('arrival')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_sink_form'] = 'station'
#cond_quant = csn['quantity'].str.contains('travel')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_sink_form'] = 'station'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##earth_surface_land/ocean
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'].str.contains('land|ocean')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form']= \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##earth_surface_radiation~
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_phen'] = \
#      csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#      .str.replace('~total','').str.replace('~net','')\
#      .str.replace('~incoming','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_trajectory_direction'] = \
#    'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_surface_station~
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'].str.contains('station')
#cond_obj3 = csn['object3'].str.contains('system')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_form']= 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_relationship'] = 'on'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']  
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'root_object_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'].str.contains('station')
#cond_quant = csn['quantity'].str.contains('s-wave|p-wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_phen'] = ('wave~' + \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.split('-').str[0])\
#        .replace('wave~s','wave~seismic~s').replace('wave~p','wave~seismic~p')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']  
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('s-wave_','')\
#                .str.replace('p-wave_','')
#cond_quant = csn['quantity'].str.contains('arrival|travel')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        ['object0','object1','object2']] = ''
#
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'].str.contains('station')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#    'object_context_form']='earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#    'object_context_abstraction']='surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#    'object_context_relationship']='on'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#    'root_object_form']=\
#      csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#    'object2'] 
#cond_obj3 = csn['object3'].str.contains('component')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj3, \
#        'root_object_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj3,'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,'object3']
#cond_quant = csn['quantity'].str.contains('shaking')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'shaking'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'process_amplitude'
#cond_quant = csn['quantity'].str.contains('filter_type')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'type_(en)'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_surface_water
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_medium_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_surface_wind
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'wind'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_context_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_phen'] = 'wind'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_context_relationship'] = \
#        'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##earth_surface_viewpoint(_planet)
#cond_obj0 = csn['object0'] == 'earth'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'viewpoint'
#cond_obj3 = csn['object3'] != ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'earth'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction'] = 'viewpoint'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'second_root_object_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##earthquake_hypocenter
#cond_obj0 = csn['object0'] == 'earthquake'
#csn.loc[ cond_obj0, 'root_object_phen'] = 'earthquake'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'hypocenter'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##ecosystem
#cond_obj0 = csn['object0'] == 'ecosystem'
#csn.loc[ cond_obj0, 'root_object_form'] = 'ecosystem'
#csn.loc[ cond_obj0, 'object0'] = ''
#
##electron
#cond_obj0 = csn['object0'] == 'electron'
#csn.loc[ cond_obj0,'root_object_matter']='electron'
#cond_quant = csn['quantity'].str.contains('ratio')
#csn.loc[ cond_obj0 & cond_quant, 'two_quantity_operator'] = 'ratio'
#cond_quant = csn['quantity'].str.contains('electric-charge-to')
#csn.loc[ cond_obj0 & cond_quant, 'root_quantity1'] = 'electric_charge'
#csn.loc[ cond_obj0 & cond_quant, 'root_quantity2'] = 'mass'
#cond_quant = csn['quantity'].str.contains('mass-to')
#csn.loc[ cond_obj0 & cond_quant, 'root_quantity2'] = 'electric_charge'
#csn.loc[ cond_obj0 & cond_quant, 'root_quantity1'] = 'mass'
#cond_quant = csn['quantity'] == 'electric-charge'
#csn.loc[ cond_obj0 & cond_quant, 'modified_quantity'] = 'electric_charge'
#csn.loc[ cond_obj0, 'object0'] = ''
#
##engine
#cond_obj0 = csn['object0'] == 'engine'
#cond_obj1 = csn['object1'] == ''
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'engine'
#csn.loc[ cond_obj0 & cond_obj1, 'object0']=''
#
##engine_air-to-fuel
#cond_obj0 = csn['object0'] == 'engine'
#cond_obj1 = csn['object1'] == 'air-to-fuel'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'engine'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_context_form'] = 'engine'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_matter'] = 'fuel'
#csn.loc[ cond_obj0 & cond_obj1, 'root_quantity2'] = 'mass'
#csn.loc[ cond_obj0 & cond_obj1, 'root_quantity1'] = 'mass'
#csn.loc[ cond_obj0 & cond_obj1, 'two_object_operator'] = 'ratio'
#csn.loc[ cond_obj0 & cond_obj1, ['object0', 'object1']] = ''
#
##ethane_molecule_h-c-c-h
#cond_obj0 = csn['object0'] == 'ethane'
#csn.loc[ cond_obj0, 'root_object_context_matter'] = 'ethane'
#csn.loc[ cond_obj0, 'root_object_context_matter_configstate'] = 'molecule'
#csn.loc[ cond_obj0, 'root_object_form'] = 'bond~h-c-c-h'
#csn.loc[ cond_obj0, ['object0','object1','object2']] = ''
#
##equation~...
#cond_obj0 = csn['object0'].str.contains('equation')
#csn.loc[ cond_obj0, 'root_object_abstraction'] = \
#        csn.loc[ cond_obj0, 'object0']
#csn.loc[ cond_obj0, 'object0'] = ''

#fence~electric
cond_obj0 = csn['object0'].str.contains('fence~electric')
csn.loc[ cond_obj0, 'object_id'] = 'fence~electric'
csn.loc[ cond_obj0, 'object_label'] = 'fence~electric'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0,'quantity_id']=csn.loc[ cond_obj0,'quantity_label']
csn.loc[ cond_obj0, ['object0','object1']] = ''

#flood
cond_obj0 = csn['object0'] == 'flood'
csn.loc[ cond_obj0,'object_id']='flood'
csn.loc[ cond_obj0,'object_label']='flood'
csn.loc[ cond_obj0,'object_pref']='phenomenon'
csn.loc[ cond_obj0,'quantity_id']=csn.loc[ cond_obj0,'quantity_label']
csn.loc[ cond_obj0, ['object0','object1']] = ''

##fuel-to-oxidizer
#cond_obj0 = csn['object0'] == 'fuel-to-oxidizer'
#csn.loc[ cond_obj0, 'root_object_matter'] = 'fuel'
#csn.loc[ cond_obj0, 'second_root_object_matter'] = 'oxidizer'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##gasoline
#cond_obj0 = csn['object0'] == 'gasoline'
#csn.loc[ cond_obj0, 'root_object_medium_matter'] = 'gasoline'
#csn.loc[ cond_obj0, ['object0','object1']] = ''

#glacier
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'glacier'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'glacier'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1,'quantity_id']=csn.loc[ cond_obj0 & cond_obj1,'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

##glacier_*-zone
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'].str.contains('zone')
#cond_quant = csn['quantity'].str.contains('fraction')
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'root_object_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object1']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##glacier_bed_
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'bed'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = 'bed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##glacier_bed_heat~geothermal
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'bed'
#cond_obj2 = csn['object2'] == 'heat~geothermal'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = 'geothermal_heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_exchange_part'] = 'bed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_exchange_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##glacier_bed_surface
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'bed'
#cond_obj2 = csn['object2'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = 'bed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##glacier_bottom
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_undergoing_process'] = 'sliding'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = 'process_speed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1']] = ''
#
##glacier_bottom_ice(_flow)
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_process'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,'object3']
#cond_quant = csn['quantity'].str.contains('sliding')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'sliding'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'process_speed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##glacier_bottom_surface(_heat)
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'surface'
#cond_obj3 = csn['object3'].str.contains('heat') 
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj3, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj3, \
#        'root_object_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj3, \
#        'root_object_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'process_heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_process_interaction'] = 'conduction'
#cond_obj3 = csn['object3'].str.contains('frictional')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_process_interaction'] = 'frictional_conduction'
#cond_obj3 = csn['object3'].str.contains('geothermal')  
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_process_interaction'] = 'geothermal_conduction'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##glacier_equillibrium-line/surface
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'].str.contains('line|surface')
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##glacier_ice
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'ice'
#cond_obj2 = csn['object2'] == ''
#cond_quant = csn['quantity'].str.contains('heat|thermal') & \
#            ~csn['quantity'].str.contains('isothermal|latent')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_context_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_context_form'] = 'glacier'
#cond_quant = csn['quantity'].str.contains('melting_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition'] = 'melting-point'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('melting_point_','')
#cond_quant = csn['quantity'].str.contains('ablation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'ablation'
#cond_quant = csn['quantity'].str.contains('accumulation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'accumulation'
#cond_quant = csn['quantity'].str.contains('ablation|accumulation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'process_rate'
#cond_quant = csn['quantity'].str.contains('melt_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_process'] = 'melt'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('melt_','')
#cond_quant = csn['quantity'].str.contains('dynamic_volume')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'volume_viscosity'
#cond_quant = csn['quantity'].str.contains('kinematic')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'momentum_diffusivity'
#cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity']\
#                .str.replace('mass-specific_isobaric','isobaric_mass-specific')
#cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity']\
#            .str.replace('mass-specific_isochoric','isochoric_mass-specific')
#cond_quant = csn['quantity'].str.contains('mass-specific_latent')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity']\
#    .str.replace('mass-specific_','').str.replace('_heat','_mass-specific_heat')
#cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity']\
#        .str.replace('volume-specific_isobaric','isobaric_volume-specific')
#cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity']\
#    .str.replace('volume-specific_isochoric','isochoric_volume-specific')
#cond_quant = csn['quantity'].str.contains('vaporization')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'vaporization'
#cond_quant = csn['quantity'].str.contains('fusion')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'fusion'
#cond_quant = csn['quantity'].str.contains('sublimation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'sublimation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity']\
#        .str.replace('vaporization','process').str.replace('fusion','process')\
#        .str.replace('sublimation','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##glacier_ice~
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'].str.contains('ice~')
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_part'] = 'bed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##glacier_ice_flow
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'ice'
#cond_obj2 = csn['object2'] == 'flow'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'].str.replace('total_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##glacier_ice_meltwater
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'ice'
#cond_obj2 = csn['object2'] == 'meltwater'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'meltwater'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_context_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##glacier_terminus(_side~...)
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'terminus'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = 'terminus'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part_part'] = \
#       csn.loc[ cond_obj0 & cond_obj1, 'object2'] 
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_undergoing_process'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity']\
#        .str.split('_').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity'] = 'process_rate'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##glacier_top
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##glacier_top_ice
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == 'ice'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_phasestate'] = 'ice'
#cond_quant = csn['quantity'].str.contains('desublimation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process'] = 'desublimation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant,\
#        'modified_quantity'].str.replace('desublimation','process')
#cond_quant = csn['modified_quantity'].str.contains('sublimation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant,\
#        'root_object_undergoing_process']='sublimation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant,\
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'].str.replace('sublimation','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']]=''
#
##glacier_top_ice_flow
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == 'ice'
#cond_obj3 = csn['object3'] == 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##glacier_top_ice_heat~net
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == 'ice'
#cond_obj3 = csn['object3'] == 'heat~net'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_context_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_context_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##glacier_top_ice_wind
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == 'ice'
#cond_obj3 = csn['object3'] == 'wind'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_in_phen'] = 'wind'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_in_process_interaction'] = 'scour'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'process_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##glacier_top_surface
#cond_obj0 = csn['object0'] == 'glacier'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == 'surface'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'surface'
#cond_obj3 = csn['object3'].str.contains('heat')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_abstraction'] = 'surface'
#cond_obj3 = csn['object3'].str.contains('incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_abstraction'] = 'surface'
#cond_obj3 = csn['object3'].str.contains('outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_form'] = 'glacier'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_abstraction'] = 'surface'
#cond_obj3 = csn['object3'].str.contains('radiation~incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'root_object_trajectory_direction'] = 'incoming'
#cond_obj3 = csn['object3'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'root_object_trajectory_direction'] = 'outgoing'
#cond_obj3 = csn['object3'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
#        .str.replace('~incoming','').str.replace('~outgoing','')
#cond_obj3 = csn['object3'].str.contains('latent')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'modified_quantity'] = 'latent_heat_energy_flux'
#cond_obj3 = csn['object3'].str.contains('sensible')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'modified_quantity'] = 'sensible_heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##gm_hummer
#cond_obj0 = csn['object0'] == 'gm'
#csn.loc[ cond_obj0, 'root_object_form'] = 'automobile~gm~hummer'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##graph~tree~rooted
#cond_obj0 = csn['object0'] == 'graph~tree~rooted'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'graph~tree~rooted'
#csn.loc[ cond_obj0, 'object0'] = ''
#
##human
#cond_obj0 = csn['object0'] == 'human'
#cond_obj1 = csn['object1'] == ''
#csn.loc[ cond_obj0 & cond_obj1,'root_object_form']='human'
#cond_quant = csn['quantity'].str.contains('hearing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'hearing'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('hearing','process')
#csn.loc[ cond_obj0 & cond_obj1,'object0'] = ''
#
##human_alcohol
#cond_obj0 = csn['object0'] == 'human'
#cond_obj1 = csn['object1'] == 'alcohol'
#csn.loc[ cond_obj0 & cond_obj1,'root_object_sink_form'] = 'human'
#csn.loc[ cond_obj0 & cond_obj1,'root_object_matter'] = 'alcohol'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_sink_process_interaction'] = \
#                'consumption'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'process_rate'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##human_blood_cell~...
#cond_obj0 = csn['object0'] == 'human'
#cond_obj1 = csn['object1'] == 'blood'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_context_form'] = 'human'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_form'] = 'blood'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object2']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##human_eye_photon
#cond_obj0 = csn['object0'] == 'human'
#cond_obj1 = csn['object1'] == 'eye'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'human'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'eye'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_in_matter'] = 'photon'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_in_process_interaction'] = 'detection'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = \
#    csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity']\
#    .str.replace('detection','process')
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##human_hair
#cond_obj0 = csn['object0'] == 'human'
#cond_obj1 = csn['object1'] == 'hair'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'human'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'hair'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##human_life
#cond_obj0 = csn['object0'] == 'human'
#cond_obj1 = csn['object1'] == 'life'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'human'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_phen'] = 'life'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##hydrogen_oxygen__bond
#cond_obj0 = csn['object0'] == 'hydrogen'
#csn.loc[ cond_obj0, 'root_object_form'] = 'bond~h-o'
#csn.loc[ cond_obj0, 'modified_quantity'] = 'energy'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##ice
#cond_obj0 = csn['object0'] == 'ice'
#cond_obj1 = csn['object1'] == ''
#cond_quant = csn['quantity'].str.contains('heat')
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
#        'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_matter_phasestate'] = 'ice'
#cond_quant = csn['quantity'].str.contains('melting')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#         'root_object_condition'] = 'melting-point'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#         'modified_quantity'] = 'temperature'
#cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('mass-specific_isobaric','isobaric_mass-specific')
#cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('mass-specific_isochoric','isochoric_mass-specific')
#cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#                'modified_quantity']\
#                .str.replace('volume-specific_isobaric','isobaric_volume-specific')
#cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('volume-specific_isochoric','isochoric_volume-specific')
#csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''
#
##image
#cond_obj0 = csn['object0'] == 'image'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'image'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##impact-crater
#cond_obj0 = csn['object0'] == 'impact-crater'
#csn.loc[ cond_obj0, 'root_object_cause_process'] = 'impact'
#csn.loc[ cond_obj0, 'root_object_form'] = 'crater'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = csn.loc[ cond_obj0, 'object1']
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##iron
#cond_obj0 = csn['object0'] == 'iron'
#cond_obj1 = csn['object1'] == ''
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'iron'
#cond_quant = csn['quantity'].str.contains('melting')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'melting-point'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'temperature'
#csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''
#
##iron_atom_...
#cond_obj0 = csn['object0'] == 'iron'
#csn.loc[ cond_obj0, 'root_object_context_matter'] = 'iron'
#csn.loc[ cond_obj0, 'root_object_context_matter_configstate'] = 'atom'
#csn.loc[ cond_obj0, 'root_object_matter'] = csn.loc[ cond_obj0, 'object2'] 
#csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#lake
cond_obj0 = csn['object0'] == 'lake'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'lake'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'lake'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

##lake_surface
#cond_obj0 = csn['object0'] == 'lake'
#cond_obj1 = csn['object1'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'lake'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##lake_water_fish
#cond_obj0 = csn['object0'] == 'lake'
#cond_obj1 = csn['object1'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'lake'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'fish'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_configstate'] = 'sample'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2','object3']] = ''
#
##lake_water~
#cond_obj0 = csn['object0'] == 'lake'
#cond_obj1 = csn['object1'].str.contains('water~incoming')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_sink_form'] = 'lake'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_trajectory_direction'] = 'incoming'
#cond_obj1 = csn['object1'].str.contains('water~outgoing')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_source_form'] = 'lake'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_trajectory_direction'] = 'outgoing'
#cond_obj1 = csn['object1'].str.contains('water~')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'volume_process_rate'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##land_domain_boundary
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'domain'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'boundary'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'domain'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_undergoing_process'] = 'lowering'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'elevation_process_rate'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##land_subsurface_sat-zone_top
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'subsurface'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = 'subsurface'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part_part'] = 'sat-zone'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part_part_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##land_surface
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == ''
#cond_quant = csn['quantity'].str.contains('infiltration|sunshine')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_abstraction'] = 'surface'
#cond_quant = csn['quantity'].str.contains('infiltration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'infiltration'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'process_rate'
#cond_quant = csn['quantity'].str.contains('sunshine')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_phen'] = 'sunshine'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'duration'
#cond_quant = csn['quantity'].str.contains('plan|profile|streamline')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'quantity'].str.split('_').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'curvature'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1']] = ''
#
##land_surface_contour/polygon/base-level/transect
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2']\
#        .str.contains('contour|polygon|base-level|transect')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'].str.replace('total_contributing','contributing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##land_surface_air_heat
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'].str.contains('surface')
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = (csn['object3'] == '') | (csn['object3'] == 'flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'air'
#cond_obj3 = csn['object3'] == 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_process'] = 'flow'
#cond_obj1 = csn['object1'].str.contains('surface~')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_relationship'] = '10m-above'
#cond_obj1 = csn['object1'].str.contains('surface')
#cond_obj3 = csn['object3'].str.contains('heat')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
#        .str.split('~').str[-1]+'_heat_energy_flux'
#cond_obj3 = csn['object3'].str.contains('heat~incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_trajectory_direction'] = 'incoming'
#cond_obj3 = csn['object3'].str.contains('heat~net')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange2_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##land_surface_energy~...
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'].str.contains('energy')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_exchange_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_exchange_abstraction'] = 'surface'
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = \
##        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,'object2']\
##        .str.replace('~net~total','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##land_surface_radiation~...
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'].str.contains('radiation')
#cond_quant = csn['quantity'].str.endswith('ance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_abstraction'] = 'surface'
#cond_obj2 = csn['object2'].str.contains('outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_trajectory_direction'] = 'outgoing'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~outgoing','')
#cond_obj2 = csn['object2'].str.contains('incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_trajectory_direction'] = 'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,'root_object_in_phen']=\
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,'object2']\
#        .str.replace('~total','').str.replace('~incoming','')
#cond_quant = csn['quantity'].str.endswith('flux')
#cond_obj2 = csn['object2'].str.contains('outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'outgoing'
#cond_obj2 = csn['object2'].str.contains('incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'incoming'
#cond_obj2 = csn['object2'].str.contains('net')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_exchange_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_exchange_abstraction'] = 'surface'
#cond_obj2 = csn['object2'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~outgoing','').str.replace('~incoming','')\
#        .str.replace('~total','').str.replace('~net','')
#cond_obj2 = csn['object2'].str.contains('incoming')
#cond_quant = csn['quantity'].str.contains('emittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction'] = 'emission'
#cond_quant = csn['quantity'].str.contains('reflectance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.contains('absorptance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('transmittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction'] = 'transmission'
#cond_quant = csn['quantity'].str.contains('emittance')
#cond_obj2 = csn['object2'].str.contains('outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_process_interaction'] = 'emission'
#cond_quant = csn['quantity'].str.contains('back')
#cond_obj2 = csn['object2'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'backscattering'
#cond_quant = csn['quantity'].str.contains('absorbed')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('reflected')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.contains('emitted')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_process_interaction'] = 'emission'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##land_surface_soil
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = 'process_heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_undergoing_process'] = 'conduction'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##land-or-sea_surface_radiation~...
#cond_obj0 = csn['object0'] == 'land-or-sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_form'] = 'land-or-sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_trajectory_direction'] = \
#        'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.replace('~incoming','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##land_surface_water
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == ''
#cond_quant = csn['quantity'].str.contains('infiltration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'object_context_relationship'] = 'on'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process'] = 'infiltration'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process2'] = 'ponding'
#cond_quant = csn['quantity'].str.contains('runoff')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process'] = 'runoff'
#cond_quant = csn['quantity'].str.contains('evaporation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process'] = 'evaporation'
#cond_quant = csn['quantity'].str.contains('baseflow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process'] = 'baseflow'
#cond_quant = csn['quantity'].str.contains('infiltration|runoff|evaporation|baseflow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('evaporation','process')\
#                .str.replace('baseflow','process')\
#                .str.replace('infiltration','process').\
#                str.replace('ponding','process2').str.replace('runoff','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##land_surface_water_flow
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_relationship'] = 'on'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##land_surface_water_sink/source
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'].str.contains('sink|source')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_relationship'] = 'on'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'volume_process_rate'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_undergoing_process'] = 'flow'
#cond_obj3 = csn['object3'].str.contains('sink')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#cond_obj3 = csn['object3'].str.contains('source')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#cond_obj3 = csn['object3'].str.contains('sink|source')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##land_surface_water_surface
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_relationship'] = 'on'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##land_surface_wind
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'wind'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_phen'] = 'wind'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##land_vegetation 
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'vegetation'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_relationship'] = 'on'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'vegetation'
##csn.loc[(csn['object0']=='land')&(csn['object1']=='vegetation')&(csn['object2']=='')&\
##    csn['quantity'].str.contains('leaf'),'root_object_form']='leaf'
##csn.loc[(csn['object0']=='land')&(csn['object1']=='vegetation')&(csn['object2']=='')&\
##    csn['quantity'].str.contains('stomata'),'root_object_form']='stomata'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##land_vegetation_canopy
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'vegetation'
#cond_obj2 = csn['object2'] == 'canopy'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_medium_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = 'vegetation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = 'canopy'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##land_vegetation_canopy_water
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'vegetation'
#cond_obj2 = csn['object2'] == 'canopy'
#cond_quant = csn['quantity'].str.contains('interception')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'object_context_relationship'] = 'on'
#cond_quant = csn['quantity'].str.contains('interception_capacity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_form'] = 'vegetation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_part'] = 'canopy'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_matter'] = 'water'
#cond_quant = csn['quantity'].str.contains('interception_volume')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_form'] = 'vegetation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_part'] = 'canopy'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'interception'
#cond_quant = csn['quantity'].str.contains('interception')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('interception','process')
#cond_quant = csn['quantity'].str.contains('throughfall')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'object_context_relationship'] = 'on'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_form'] = 'vegetation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_part'] = 'canopy'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'throughfall'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('throughfall','process')
##csn.loc[(csn['object0']=='land')&(csn['object1']=='vegetation')&(csn['object2']=='canopy')&\
##        csn['quantity'].str.contains('throughfall'),'quantity']=\
##        csn.loc[(csn['object0']=='land')&(csn['object1']=='vegetation')&(csn['object2']=='canopy')&\
##        csn['quantity'].str.contains('throughfall'),'quantity'].str.replace('throughfall','process')
#cond_quant = csn['quantity'].str.contains('transpiration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'object_context_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'object_context_relationship'] = 'on'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_form'] = 'vegetation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_part'] = 'canopy'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_process_interaction'] = 'transpiration'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'modified_quantity']\
#                .str.replace('transpiration','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##land_vegetation_floor_water
#cond_obj0 = csn['object0'] == 'land'
#cond_obj1 = csn['object1'] == 'vegetation'
#cond_obj2 = csn['object2'] == 'floor'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_form'] = 'land~vegetated'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_part'] = 'floor'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_sink_process_interaction'] = 'interception'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = 'process_volume_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''

#light-bulb~incandescent
cond_obj0 = csn['object0'] == 'light-bulb~incandescent'
csn.loc[ cond_obj0, 'object_id'] = 'light-bulb~incandescent'
csn.loc[ cond_obj0, 'object_label'] = 'light-bulb~incandescent'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

#lithosphere
cond_obj0 = csn['object0'] == 'lithosphere'
csn.loc[ cond_obj0, 'object_label'] = 'lithosphere'
csn.loc[ cond_obj0, 'object_id'] = 'lithosphere'
csn.loc[ cond_obj0, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

##location
#cond_obj0 = csn['object0'] == 'location'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'location'
#csn.loc[ cond_obj0, 'object0'] = ''
#
##magnesium-chloride_water
#cond_obj0 = csn['object0'] == 'magnesium-chloride'
#csn.loc[ cond_obj0, 'root_object_matter'] = 'magnesium-chloride'
#csn.loc[ cond_obj0, 'second_root_object_matter'] = 'water'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##math
#cond_obj0 = csn['object0'] == 'math'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'math'
#csn.loc[ cond_obj0, 'modified_quantity'] = \
#        csn.loc[ cond_obj0, 'modified_quantity']\
#        .str.replace('twin_prime','twin-prime')
#csn.loc[ cond_obj0, 'object0'] = ''
#
##model
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == ''
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''
#
##model_grid
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'grid'
#cond_quant = csn['quantity'].str.contains('average_node')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_abstraction_abstraction'] = 'node'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'modified_quantity'] = \
#                        'average_separation_distance'
#cond_quant = csn['quantity'].str.contains('cell|column|row|shell')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#            'modified_quantity'].str.split('_').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'count'
#cond_quant = csn['quantity'].str.contains('dual|primary')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_abstraction_abstraction'] = \
#        'node~' + csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                          'modified_quantity'].str.split('_').str[0]+'~'+\
#    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#            'modified_quantity'].str.split('_').str[2]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'count'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##model_grid_axis...
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'] == 'axis~x'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction'] = 'axis~x'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_abstraction'] = 'axis~east'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##model_grid_cell
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'] == 'cell'
#cond_obj3 = csn['object3'] == ''
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_abstraction_abstraction'] = 'cell'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_context_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_context_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_context_abstraction_abstraction'] = 'cell'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_process'] = 'flow'
#cond_quant = csn['quantity'].str.contains('column|row')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_abstraction_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.split('_').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'index'
#cond_quant = csn['quantity'].str.contains('surface')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_abstraction_abstraction_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'area'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'].str.replace('total_contributing','contributing')\
#        .str.replace('flow_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##model_grid_cell_center/centroid
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'] == 'cell'
#cond_obj3 = csn['object3'].str.contains('center|centroid')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction_abstraction'] = 'cell'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##model_grid_cell_edge/face(_center/centroid)
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'] == 'cell'
#cond_obj3 = csn['object3'].str.contains('edge|face')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#         'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#         'root_object_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction_abstraction'] = 'cell'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#         'root_object_abstraction_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#         'root_object_abstraction_abstraction_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object4']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#         ['object0','object1','object2','object3','object4']] = ''
#
##model_grid_cell~...
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'].str.contains('cell')
#cond_obj3 = csn['object3'].str.contains('water')&\
#            ~csn['object3'].str.contains('water~')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']
#cond_obj3 = csn['object3'].str.contains('water~incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_sink_abstraction_abstraction'] = 'cell'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_trajectory_direction'] = 'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#cond_obj3 = csn['object3'].str.contains('water~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_source_abstraction_abstraction'] = 'cell'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_trajectory_direction'] = 'outgoing'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#cond_obj3 = csn['object3'].str.contains('water~')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_undergoing_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'volume_process_rate'
#cond_obj3 = csn['object3'].str.contains('water')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']]= ''
#
##model_grid_cell        
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'].str.contains('cell')
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_abstraction_abstraction'] = \
#                csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_context_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_context_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_context_abstraction_abstraction'] = 'cell'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object4']
#cond_quant = csn['quantity'].str.contains('row_|column_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_abstraction_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.split('_').str[0]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'index'
#cond_quant = csn['quantity'].str.contains('surface')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_abstraction_abstraction_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'area'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'].str.replace('total_contributing','contributing')\
#        .str.replace('flow_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##model_grid_column/row
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'].str.contains('column|row')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1',
#                                            'object2']] = ''
#
##model_grid_edge~.
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'].str.contains('edge')
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##model_grid_edge~_sea_water
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'].str.contains('edge')
#cond_obj3 = csn['object3'] == 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_context_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_context_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_context_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##model_grid_node~
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'].str.contains('node')
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##model_grid_virtual~
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'].str.contains('virtual')
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'pole~north~virtual'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##model_grid_shell...
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'grid'
#cond_obj2 = csn['object2'].str.contains('shell')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_abstraction'] = 'grid'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction'] = 'shell'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_abstraction_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_relationship'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.split('-').str[1]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##model_soil_layer~
#cond_obj0 = csn['object0'] == 'model'
#cond_obj1 = csn['object1'] == 'soil'
#cond_obj2 = csn['object2'].str.contains('layer')
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'model'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##mars
#cond_obj0 = csn['object0'] == 'mars'
#cond_obj1 = csn['object1'] == ''
#cond_quant = csn['quantity'] == 'standard_gravity_constant'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        'standard_gravitational_acceleration'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'mars'
#csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''
#
##mars_atmosphere/moon
#cond_obj0 = csn['object0'] == 'mars'
#cond_obj1 = csn['object1'].str.contains('atmosphere|moon')
#csn.loc[ cond_obj0 & cond_obj1, 'object_context_form'] = 'mars'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = \
#    csn.loc[ cond_obj0 & cond_obj1, 'object1']
#cond_obj1 = csn['object1'].str.contains('atmosphere')
#csn.loc[ cond_obj0 & cond_obj1, 'object_context_relationship'] = 'surrounding'
#cond_obj1 = csn['object1'].str.contains('moon')
#csn.loc[ cond_obj0 & cond_obj1, 'object_context_relationship'] = 'orbiting'
#cond_obj1 = csn['object1'].str.contains('atmosphere|moon')
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##mars_axis/ellipsoid
#cond_obj0 = csn['object0'] == 'mars'
#cond_obj1 = csn['object1'].str.contains('axis|ellipsoid')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'mars'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = \
#    csn.loc[ cond_obj0 & cond_obj1, 'object1']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##mars_orbit
#cond_obj0 = csn['object0'] == 'mars'
#cond_obj1 = csn['object1'] == 'orbit'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'mars'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_trajectory'] = 'orbit'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##mars_surface_viewpoint_venus
#cond_obj0 = csn['object0'] == 'mars'
#cond_obj1 = csn['object1'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'mars'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_abstraction_abstraction'] = 'viewpoint'
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_form'] = 'venus'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2','object3']] = ''
#
##mercury_axis
#cond_obj0 = csn['object0'] == 'mercury'
#csn.loc[ cond_obj0, 'root_object_form'] = 'mercury'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'axis'
#csn.loc[ cond_obj0, 'root_object_undergoing_process'] = 'precession'
#csn.loc[ cond_obj0, 'modified_quantity'] = \
#        csn.loc[ cond_obj0, 'modified_quantity']\
#        .str.replace('precession','process')
#csn.loc[ cond_obj0, ['object0','object1']] = ''

#oscillator
cond_obj0 = csn['object0'] == 'oscillator'
csn.loc[ cond_obj0, 'object_id'] = 'oscillator'
csn.loc[ cond_obj0, 'object_label'] = 'oscillator'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

##ozone_molecule
#cond_obj0 = csn['object0'] == 'ozone'
#csn.loc[ cond_obj0, 'root_object_context_matter'] = 'ozone'
#csn.loc[ cond_obj0, 'root_object_context_matter_configstate'] = 'molecule'
#csn.loc[ cond_obj0, 'root_object_form'] = 'bond~o-o'
#csn.loc[ cond_obj0, 'modified_quantity'] = 'length'
#csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#paper
cond_obj0 = csn['object0'] == 'paper'
csn.loc[ cond_obj0, 'object_id'] = 'paper'
csn.loc[ cond_obj0, 'object_label'] = 'paper'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

##pavement_rubber
#cond_obj0 = csn['object0'] == 'pavement'
#csn.loc[ cond_obj0, 'root_object_matter'] = 'pavement'
#csn.loc[ cond_obj0, 'second_root_object_matter'] = 'rubber'
#csn.loc[ cond_obj0, 'two_object_process_interaction'] = 'friction'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##peano-curve
#cond_obj0 = csn['object0'] == 'peano-curve'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'peano-curve'
#csn.loc[ cond_obj0, 'object0'] = ''
#
##physics
#cond_obj0 = csn['object0'] == 'physics'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'physics'
#cond_quant = csn['quantity'].str.contains('vacuum_electrical')
#csn.loc[ cond_obj0 & cond_quant, 'root_object_abstraction'] = ''
#csn.loc[ cond_obj0 & cond_quant, \
#        'modified_quantity'] = 'electrical_impedance_constant'
#csn.loc[ cond_obj0 & cond_quant, \
#        'root_object_context_phen'] = 'vacuum'
#csn.loc[ cond_obj0 & cond_quant, \
#        'root_object_phen'] = 'radiation~electromagnetic'
#cond_quant = csn['quantity'].str.contains('vacuum_light')
#csn.loc[ cond_obj0 & cond_quant, 'root_object_abstraction'] = ''
#csn.loc[ cond_obj0 & cond_quant, \
#        'modified_quantity'] = 'speed_constant'
#csn.loc[ cond_obj0 & cond_quant, \
#        'root_object_context_phen'] = 'vacuum'
#csn.loc[ cond_obj0 & cond_quant, \
#        'root_object_phen'] = 'radiation~electromagnetic'
#cond_quant = csn['quantity'].str.contains('vacuum_magnetic')
#csn.loc[ cond_obj0 & cond_quant, 'root_object_abstraction'] = ''
#csn.loc[ cond_obj0 & cond_quant, \
#        'modified_quantity'] = 'magnetic_permeability_constant'
#csn.loc[ cond_obj0 & cond_quant, \
#        'root_object_phen'] = 'vacuum'
#cond_quant = csn['quantity'].str.contains('vacuum_permittivity')
#csn.loc[ cond_obj0 & cond_quant, 'root_object_abstraction'] = ''
#csn.loc[ cond_obj0 & cond_quant, \
#        'modified_quantity'] = 'permittivity_constant'
#csn.loc[ cond_obj0 & cond_quant, \
#        'root_object_phen'] = 'vacuum'
#csn.loc[ cond_obj0, 'modified_quantity' ] = \
#        csn.loc[ cond_obj0, 'modified_quantity' ]\
#        .str.replace('atomic_mass','atomic-mass')\
#        .str.replace('bohr_radius','bohr-radius')\
#        .str.replace('elementary_electric','elementary-electric')\
#        .str.replace('universal_gravitation','universal-gravitation')
#csn.loc[ cond_obj0, 'object0'] = ''
#
##pipe_water_flow
#cond_obj0 = csn['object0'] == 'pipe'
#csn.loc[ cond_obj0, 'root_object_context_form'] = 'pipe'
#csn.loc[ cond_obj0, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0, 'root_object_process'] = 'flow'
#csn.loc[ cond_obj0, ['object0','object1','object2']] = ''
#
##polynomial
#cond_obj0 = csn['object0'] == 'polynomial'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'polynomial'
#csn.loc[ cond_obj0, 'object0']=''
#
##polymer
#cond_obj0 = csn['object0'] == 'polymer'
#csn.loc[ cond_obj0, 'root_object_form'] = 'polymer'
#csn.loc[ cond_obj0, 'object0']=''
#
##porsche~911
#cond_obj0 = csn['object0'] == 'porsche~911'
#cond_quant = csn['quantity'].str.contains('price')
#csn.loc[ cond_obj0, 'root_object_form'] = 'automobile~porsche~911'
#csn.loc[ cond_obj0 & cond_quant, 'modified_quantity'] = 'msrp_price'
#csn.loc[ cond_obj0, 'object0'] = ''
#
##projectile
#cond_obj0 = csn['object0'] == 'projectile'
#cond_obj1 = csn['object1'] == ''
#cond_quant = csn['quantity'].str.contains('thermal')
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'root_object_form'] = 'projectile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_form'] = 'projectile'
#cond_quant = csn['quantity'].str.contains('firing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'firing'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('firing','process')
#cond_quant = csn['quantity'].str.contains('flight')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_process'] = 'flight'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = 'duration'
#cond_quant = csn['quantity'].str.contains('impact')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_process'] = 'impact'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('impact_','')
#cond_quant = csn['quantity'].str.contains('roll_rotation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_process'] = 'roll'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'rotation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('roll_rotation','process')
#cond_quant = csn['quantity'].str.contains('_plus_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_quantity1'] = 'kinetic_energy'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_quantity2'] = 'potential_energy'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'two_quantity_operator'] = 'sum'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = ''
#csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''
#
##projectile_impact-crater
#cond_obj0 = csn['object0'] == 'projectile'
#cond_obj1 = csn['object1'] == 'impact-crater'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'crater'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_source_form'] = 'projectile'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_cause_process'] = 'impact'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##projectile_origin
#cond_obj0 = csn['object0'] == 'projectile'
#cond_obj1 = csn['object1'] == 'origin'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'projectile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_trajectory_abstraction'] = 'origin'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##projectile_origin_land_surface
#cond_obj0 = csn['object0'] == 'projectile'
#cond_obj1 = csn['object1'] == 'origin'
#cond_obj2 = csn['object2'] == 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_form'] = 'projectile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_trajectory_abstraction'] = 'origin'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_relationship'] = 'at'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##projectile_origin_wind
#cond_obj0 = csn['object0'] == 'projectile'
#cond_obj1 = csn['object1'] == 'origin'
#cond_obj2 = csn['object2'] == 'wind'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_form'] = 'projectile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_trajectory_abstraction'] = 'origin'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_relationship'] = 'at'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_phen'] = 'wind'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##projectile_shaft(_x-section)
#cond_obj0 = csn['object0'] == 'projectile'
#cond_obj1 = csn['object1'] == 'shaft'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'projectile'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'shaft'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction']=\
#        csn.loc[ cond_obj0 & cond_obj1, 'object2']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##projectile_target
#cond_obj0 = csn['object0'] == 'projectile'
#cond_obj1 = csn['object1'] == 'target'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'projectile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_trajectory_abstraction'] = 'target'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##projectile_target_land_surface
#csn.loc[ cond_obj0 & cond_obj1, 'object_context_form'] = 'projectile'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'object_context_trajectory_abstraction'] = 'target'
#csn.loc[ cond_obj0 & cond_obj1, 'object_context_relationship'] = 'at'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'land'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2','object3']] = ''
#
##projectile_trajectory
#cond_obj0 = csn['object0'] == 'projectile'
#cond_obj1 = csn['object1'] == 'trajectory'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'projectile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_trajectory'] = 'trajectory'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##projectile_x-section
#cond_obj0 = csn['object0'] == 'projectile'
#cond_obj1 = csn['object1'] == 'x-section'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'projectile'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'x-section'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1']] = ''

#pump
cond_obj0 = csn['object0'] == 'pump'
csn.loc[ cond_obj0, 'object_id'] = 'pump'
csn.loc[ cond_obj0, 'object_label'] = 'pump'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

##railway_curve
#cond_obj0 = csn['object0'] == 'railway'
#csn.loc[ cond_obj0, 'root_object_form'] = 'railway'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'curve'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##region_state_land~
#cond_obj0 = csn['object0'] == 'region'
#csn.loc[ cond_obj0,'root_object_medium_form'] = 'region~state'
#csn.loc[ cond_obj0,'root_object_form'] = \
#        csn.loc[ cond_obj0,'object2']
#csn.loc[ cond_obj0, ['object0','object1','object2']] = ''
#
##rocket_payload
#cond_obj0 = csn['object0'] == 'rocket'
#cond_obj1 = csn['object1'] == 'payload'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_form'] = 'rocket'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'payload'
#cond_quant = csn['quantity'].str.contains('ratio')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_quantity1'] = 'mass'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_quantity2'] = 'mass'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'two_object_operator'] = 'ratio'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = ''
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##rocket_propellant
#cond_obj0 = csn['object0'] == 'rocket'
#cond_obj1 = csn['object1'] == 'propellant'
#cond_quant = csn['quantity'].str.contains('ratio')
#csn.loc[ cond_obj0 & cond_obj1,'root_object_medium_form'] = 'rocket'
#csn.loc[ cond_obj0 & cond_obj1,'root_object_matter'] = 'propellant'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_quantity1'] = 'mass'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_quantity2'] = 'mass'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'two_object_operator'] = 'ratio'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = ''
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##sea_bottom_radiation~..
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'].str.contains('radiation~incoming')
#cond_quant = csn['quantity'].str.endswith('flux')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_part']='bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'incoming'
#cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_form']='sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_part']='bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'outgoing'
#cond_obj2 = csn['object2'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#        'root_object_phen']=\
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~total','')\
#        .str.replace('~incoming','').str.replace('~outgoing','')
#cond_quant = csn['quantity'].str.endswith('ance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_form']='sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_part']='bottom'
#cond_obj2 = csn['object2'].str.contains('radiation~incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_trajectory_direction'] = 'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~incoming','').str.replace('~total','')
#cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_trajectory_direction'] = 'outgoing'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~outgoing','')
#cond_obj2 = csn['object2'].str.contains('radiation')
#cond_quant = csn['quantity'].str.contains('absorbed')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('reflected')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.contains('emitted')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_process_interaction'] = 'emission'
#cond_quant = csn['quantity'].str.contains('absorptance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('reflectance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.contains('emittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_process_interaction'] = 'emission'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
#        ['object0','object1','object2']] = ''
#
##sea_bottom_sediment
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'sediment'
#cond_obj3 = csn['object3'] == ''
#cond_quant = csn['quantity'].str.contains('porosity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##sea_bottom_sediment_bulk/layer/particle
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'sediment'
#cond_obj3 = csn['object3'].str.contains('bulk|layer|particle|grain')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'sediment'
#cond_obj3 = csn['object3'].str.contains('bulk|particle|grain')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_configstate'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#cond_obj3 = csn['object3'].str.contains('layer')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#cond_obj3 = csn['object3'].str.contains('bulk|layer|particle|grain')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_bottom_sediment_*
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'sediment'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_bottom_surface
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'surface'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##sea_bottom_surface_heat~net
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'surface'
#cond_obj3 = csn['object3'] == 'heat~net'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_bottom_surface_water
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'surface'
#cond_obj3 = csn['object3'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4']] = ''
#        
##sea_bottom_water
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == ''
#cond_quant = csn['quantity'].str.contains('salinity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant,\
#        'root_object_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant,\
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant,\
#        'root_object_medium_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant,\
#        'root_object_medium_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant,\
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,\
#        ['object0','object1','object2']] = ''
#
##sea_bottom_water_heat~net
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'heat~net'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange2_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'modified_quantity'] = 'heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_bottom_water_debris_flow
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'debris'
#cond_obj4 = csn['object4'] == 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = 'debris'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_process'] = 'flow'
#cond_obj5 = csn['object5'].str.contains('layer|top')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj5, \
#        'root_object_part'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & \
#                          cond_obj3 & cond_obj4 & cond_obj5, 'object5']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj5, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & \
#        cond_obj3 & cond_obj4 & cond_obj5,'modified_quantity']\
#        .str.replace('flow_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##sea_bottom_water_debris_deposit
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'debris'
#cond_obj4 = csn['object4'] == 'deposit'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_context_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter'] = 'debris'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        'root_object_matter_configstate'] = 'deposit'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##sea_bed_freshwater
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'bed'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_part'] = 'bed'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'freshwater'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'volume_flux'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##sea_ice
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'ice'
#cond_obj2 = csn['object2'] == ''
#cond_quant = csn['quantity'].str.contains('heat|salinity')|\
#              csn['quantity'].str.startswith('thermal')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_relationship'] = 'at'
#cond_quant = csn['quantity'].str.contains('melting_point')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_condition'] = 'melting-point'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('melting_point_','')
#cond_quant = csn['quantity'].str.contains('dynamic_volume')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'volume_viscosity'
#cond_quant = csn['quantity'].str.contains('kinematic')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'momentum_diffusivity'
#cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'isobaric_mass-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'isochoric_mass-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'isobaric_volume-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'isochoric_volume-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('mass-specific_latent_fusion')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'latent_fusion_mass-specific_heat'
#cond_quant = csn['quantity'].str.contains('mass-specific_latent_sublimation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'latent_sublimation_mass-specific_heat'
#cond_quant = csn['quantity'].str.contains('melt_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_process'] = 'melt'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 &\
#                           cond_obj2 & cond_quant, 'modified_quantity']\
#                            .str.replace('melt_','')
#cond_quant = csn['quantity'].str.contains('sublimation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'sublimation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('sublimation','process')
#cond_quant = csn['quantity'].str.contains('fusion')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'fusion'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#                'modified_quantity'].str.replace('fusion','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##sea_ice_bottom
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'ice'
#cond_obj2 = csn['object2'] == 'bottom'
#cond_obj4 = csn['object4'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        'object_context_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        'object_context_part'] = 'bottom'
#cond_quant = csn['quantity']=='temperature'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4 & cond_quant, \
#        'object_context_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4 & cond_quant, \
#        'object_context_object_context_relationship'] = 'at'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4 & cond_quant, \
#        'root_object_matter'] = 'water'
#cond_quant = csn['quantity'] == 'salinity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4 & cond_quant, \
#        'object_context_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4 & cond_quant, \
#        'object_context_object_context_relationship'] = 'at'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4 & cond_quant, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        'object_context_relationship'] = 'below'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_ice_bottom_water_salt
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'ice'
#cond_obj2 = csn['object2'] == 'bottom'
#cond_obj3 = csn['object3'] == 'water'
#cond_obj4 = csn['object4'] == 'salt'
#cond_quant = csn['quantity'] == 'salinity'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj4, \
#        'object_context_matter_phasestate']='ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj4, \
#        'object_context_part']='bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj4, \
#        'object_context_relationship']='below'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj4, \
#        'object_context_object_context_form']='sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj4, \
#        'object_context_object_context_relationship']='at'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj4 & cond_quant, \
#        'root_object_medium_matter']='water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj4 & ~cond_quant, \
#        'root_object_matter']='water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        'root_object_source_matter_phasestate']='ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        'root_object_source_part']='bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        'root_object_source_object_context_form']='sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        'root_object_source_object_context_relationship']='at'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        'root_object_sink_matter']='water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        'root_object_matter'] = 'salt'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##sea_ice_salt
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'ice'
#cond_obj2 = csn['object2'] == 'salt'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter_phasestate']='ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'salt'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_relationship'] = 'at'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_ice_surface_air
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'ice'
#cond_obj2 = csn['object2'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_object_context_relationship'] = 'at'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_ice_radiation~..
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'ice'
#cond_obj2 = csn['object2'].str.contains('radiation~incoming')
#cond_quant = csn['quantity'].str.endswith('flux')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#        'root_object_trajectory_direction']='incoming'
#cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#        'root_object_source_matter_phasestate']='ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
#        'root_object_trajectory_direction']='outgoing'
#cond_obj2 = csn['object2'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_relationship'] = 'at'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~incoming','').str.replace('~outgoing','')\
#        .str.replace('~total','')\
#        .str.replace('~upward','').str.replace('~downward','')
#cond_quant = csn['quantity'].str.endswith('ance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_matter_phasestate'] = 'ice'
#cond_obj2 = csn['object2'].str.contains('radiation~incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_trajectory_direction']='incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_phen']=\
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~total','').str.replace('~incoming','')\
#        .str.replace('~upward','').str.replace('~downward','')
#cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_trajectory_direction']='outgoing'
#cond_obj2 = csn['object2'].str.contains('radiation~outgoing~upward')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_trajectory_direction']='outgoing~upward'
#cond_obj2 = csn['object2'].str.contains('radiation~outgoing~downward')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_trajectory_direction']='outgoing~downward'
#cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~outgoing','').str.replace('~total','')\
#        .str.replace('~upward','').str.replace('~downward','')
#cond_obj2 = csn['object2'].str.contains('radiation')
#cond_quant = csn['quantity'].str.endswith('reflectance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.endswith('absorptance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.endswith('transmittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_process_interaction'] = 'transmission'
#cond_quant = csn['quantity'].str.endswith('emittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_process_interaction'] = 'emission'
#cond_quant = csn['quantity'].str.endswith('reflected')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.endswith('absorbed')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.endswith('transmitted')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'transmission'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_photic-zone_bottom
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'photic-zone'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = 'photic-zone'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##sea_shoreline
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'shoreline'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'shoreline'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##sea_shoreline_axis...
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'shoreline'
#cond_obj2 = csn['object2'].str.contains('axis')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'shoreline'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction_abstraction'] = 'axis~x'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_abstraction'] = 'axis~east'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_shoreline_wave~
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'shoreline'
#cond_obj2 = csn['object2'].str.contains('wave~')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_abstraction'] = 'shoreline'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.replace('~incoming','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_trajectory_direction'] = 'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_surface
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1']] = ''
#
##sea_surface_air
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##sea_surface_air_carbon-dioxide
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'] == 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_surface_air-vs-water
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'air-vs-water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'second_root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_quantity1'] = 'temperature'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_quantity2'] = 'temperature'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'two_object_operator'] = 'difference'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'operator0'] = ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_surface_air_flow
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'] == 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_surface_air_water~vapor
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'air'
#cond_obj3 = csn['object3'] == 'water~vapor'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'object_context_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter_phasestate'] = 'vapor'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_surface_radiation~...
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'].str.contains('radiation~incoming')
#cond_quant = csn['quantity'].str.endswith('flux')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'incoming'
#cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_source_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_trajectory_direction'] = 'outgoing'
#cond_obj2 = csn['object2'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~outgoing','').str.replace('~incoming','')
#cond_quant = csn['quantity'].str.contains('absorbed')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('reflected')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.endswith('ance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_abstraction'] = 'surface'
#cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_trajectory_direction'] = 'outgoing'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_out_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~outgoing','')
#cond_obj2 = csn['object2'].str.contains('radiation~incoming')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_trajectory_direction'] = 'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_in_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
#        .str.replace('~incoming','')
#cond_obj2 = csn['object2'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_surface_storm_water
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'storm'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_source_phen'] = 'storm'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_process'] = 'surge'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity'] = 'height'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_surface_water
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == ''
#cond_quant = csn['quantity'].str.contains('salinity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_matter'] = 'water'
#cond_quant = csn['quantity'].str.contains('precipitation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_sink_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_sink_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_source_process_interaction'] = 'precipitation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'].str.replace('precipitation','process')\
#                .str.replace('leq-','leq_')
#cond_quant = csn['quantity'].str.contains('evaporation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_source_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_source_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_source_process_interaction'] = 'evaporation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'].str.replace('evaporation','process')
#cond_quant = csn['quantity'].str.contains('salinity|precipitation|evaporation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
#        'root_object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2']] = ''
#
##sea_surface_water_carbon-dioxide
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_surface_water_heat~...
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'].str.contains('heat')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_exchange_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
#        .str.split('~').str[-1]+'_heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_surface_water_tide_constituent~...
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'] == 'tide'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_phen'] = 'tide'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object4']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object5']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##sea_surface_water_wave~...
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'surface'
#cond_obj2 = csn['object2'] == 'water'
#cond_obj3 = csn['object3'].str.contains('wave')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_context_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object4']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_abstraction_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object5']
#cond_quant = csn['quantity'].str.contains('vertex')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_abstraction_abstraction_abstraction'] = 'vertex'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'angle'
#cond_quant = csn['quantity'].str.contains('group-speed')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'two_quantity_operator'] = 'ratio'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_quantity1'] = 'group_speed'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_quantity2'] = 'phase_speed'
#cond_quant = csn['quantity'].str.contains('-times-')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_quantity1'] = 'angular_frequency'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_quantity2'] = 'time'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'two_quantity_operator'] = 'product'
#cond_quant = csn['quantity'].str.contains('orbital')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_trajectory'] = 'orbit'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'].str.replace('orbital_','')
#cond_quant = csn['quantity'].str.contains('steepness')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'slope'
#cond_quant = csn['quantity'].str.contains('angular_wavenumber')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = 'wavenumber'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        ['object0','object1','object2','object3','object4','object5']] = ''
#
##sea_water
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == ''
#cond_quant = csn['quantity'].str.contains('salinity|heat|thermal')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_medium_context_form'] = 'sea'
#cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'isobaric_mass-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'isochoric_mass-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('mass-specific_latent_fusion')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'latent_fusion_mass-specific_heat'
#cond_quant = csn['quantity'].str.contains('fusion')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process']='fusion'
#cond_quant = csn['quantity'].str.contains('mass-specific_latent_vaporization')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'latent_vaporization_mass-specific_heat'
#cond_quant = csn['quantity'].str.contains('vaporization')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_undergoing_process'] = 'vaporization'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity']\
#    .str.replace('vaporization','process').str.replace('fusion','process')
#cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'isobaric_volume-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'isochoric_volume-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('brunt')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'brunt-vaisala_frequency'
#cond_quant = csn['quantity'].str.contains('eddy')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_process'] = 'eddy'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'viscosity'
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'speed'
#cond_quant = csn['quantity'].str.contains('diffusion_coefficient')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'].str.replace('diffusion_coefficient','diffusivity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'].str.replace('total_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1']] = ''
#
##sea_water_above-bottom
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'above-bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_water_below-surface
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'below-surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_relationship'] = 'below'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_water_bottom (water unnecessary??)
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_relationship'] = 'below'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_reference_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_water_carbon-dioxide
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'carbon-dioxide'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_water_energy/heat
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'].str.contains('energy|heat')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.replace('energy~kinetic~turbulent','turbulent_kinetic_energy_diffusivity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_water_flow
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'].str.replace('total_','')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_water_diatoms-as-*
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'].str.contains('diatoms')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_form'] = 'diatoms'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_expressed-as'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,'object2']\
#        .str.split('-as-').str[1]
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_water_solute
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'].str.contains('chloride|sulfate|salt|oxygen|sediment|biota')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_medium_context_form'] = 'sea'
#cond_obj2 = csn['object2'].str.contains('chloride|sulfate|salt|oxygen|sediment')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.replace('~suspended','')
#cond_obj2 = csn['object2'].str.contains('biota')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'biota'
#cond_obj2 = csn['object2'].str.contains('suspended')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_matter_phasestate'] = 'suspended'
#cond_obj2 = csn['object2'].str.contains('chloride|sulfate|salt|oxygen|sediment|biota')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'modified_quantity'].str.split('diffusion_coefficient','diffusivity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_water_surface
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##sea_water_zone* -- water unnecessary
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'].str.contains('zone')
##csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##sea_water_wave/tide/current
#cond_obj0 = csn['object0'] == 'sea'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'].str.contains('wave|tide|current')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_context_form'] = 'sea'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.replace('wave~internal~gravity','wave~gravity~internal')\
#        .str.replace('wave~internal','wave~gravity~internal')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'mean_speed'
#cond_quant = csn['quantity'].str.contains('angular_wavenumber')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
#        'modified_quantity'] = 'wavenumber'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3']] = ''
#
##shale~burgess_stratum
#cond_obj0 = csn['object0'].str.contains('shale~burgess')
#csn.loc[ cond_obj0, 'root_object_matter'] = 'shale~burgess'
#csn.loc[ cond_obj0, 'root_object_part'] = 'stratum'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##skydiver/sierpinski-gasket/ship
#cond_obj0 = csn['object0'].str.contains('skydiver|ship')
#csn.loc[ cond_obj0, 'root_object_form'] = csn.loc[ cond_obj0, 'object0']
#cond_obj0 = csn['object0'].str.contains('sierpinski')
#csn.loc[ cond_obj0, 'root_object_abstraction'] = csn.loc[ cond_obj0, 'object0']
#cond_obj0 = csn['object0'].str.contains('skydiver|sierpinski|ship')
#csn.loc[ cond_obj0,'object0'] = ''
#
##snow
#cond_obj0 = csn['object0'] == 'snow'
#cond_obj1 = csn['object1'] == ''
#cond_quant = csn['quantity'].str.contains('heat|thermal')
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
#        'root_object_matter_phasestate'] = 'snow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_matter_phasestate'] = 'snow'
#cond_quant = csn['quantity'].str.contains('energy-per-area_cold')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'cold_energy-per-area_density'
#cond_quant = csn['quantity'].str.contains('blowing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'blowing'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'process_speed'
#cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        'isobaric_mass-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'isochoric_mass-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        'isobaric_volume-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        'isochoric_volume-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''
#
##snow~wet_X
#cond_obj0 = csn['object0'] == 'snow~wet'
#cond_obj1 = csn['object1'] == 'rubber'
#csn.loc[ cond_obj0, 'root_object_exchange_matter_phasestate'] = 'snow~wet'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_exchange2_matter'] = 'rubber'
#cond_obj1 = csn['object1'] == 'ski~waxed'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_exchange2_form'] = 'ski~waxed'    
#csn.loc[ cond_obj0, 'root_object_exchange_process_interaction'] = 'friction'    
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##snowpack
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == ''
#cond_quant = csn['quantity'].str.contains('heat')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'root_object_form'] = 'snowpack'
#cond_quant = csn['quantity'].str.contains('desublimation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'desublimation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('desublimation','process') 
#cond_quant = csn['modified_quantity'].str.contains('sublimation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'sublimation'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('sublimation','process') 
#cond_quant = csn['quantity'].str.contains('melt_')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process'] = 'melt'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'modified_quantity']\
#        .str.replace('melt','process')
#cond_quant = csn['quantity'].str.contains('mass-specific')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('mass-specific_isobaric','isobaric_mass-specific')
#cond_quant = csn['quantity'].str.contains('liquid-equivalent')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('liquid-equivalent','leq')
#cond_quant = csn['quantity'].str.contains('energy-per-area')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        'cold_energy-per-area_density'
#csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''
#
##snowpack_bottom
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'bottom'
#cond_quant = csn['quantity'] == 'temperature'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_part'] = 'bottom'
#cond_quant = csn['quantity'] == 'energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        'process_heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_undergoing_process'] = \
#        'conduction'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_exchange_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_exchange_part'] = 'bottom'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##snowpack_core
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'core'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = 'core'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##snowpack_crust_layer~
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'crust'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = 'crust'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object2']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##snowpack_ice-layer
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'ice-layer'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = 'layer'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##snowpack_snow~new
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'snow~new'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_phasestate'] = 'snow~new'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##snowpack_surface
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##snowpack_top
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''
#
##snowpack_top_air
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_context_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_context_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = 'air'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'object_context_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##snowpack_top_heat
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'].str.contains('heat')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_exchange_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_exchange_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
#        .str.split('~').str[-1]+'_heat_energy_flux'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##snowpack_top_surface
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'top'
#cond_obj2 = csn['object2'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        'root_object_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##snowpack_grains
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'grains'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_configstate'] = 'grains'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##snowpack_water~liquid
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'water~liquid'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_phasestate'] = 'liquid'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##snowpack_meltwater
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'] == 'meltwater'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_source_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'meltwater'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##snowpack_radiation
#cond_obj0 = csn['object0'] == 'snowpack'
#cond_obj1 = csn['object1'].str.contains('radiation~incoming')
#cond_quant = csn['quantity'].str.contains('flux')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_trajectory_direction'] = 'incoming'
#cond_obj1 = csn['object1'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_source_form'] = 'snowpack'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_trajectory_direction'] = 'outgoing'
#cond_obj1 = csn['object1'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']\
#        .str.replace('~total','')\
#        .str.replace('~incoming','').str.replace('~outgoing','')
#cond_obj1 = csn['object1'].str.contains('radiation~incoming')
#cond_quant = csn['quantity'].str.endswith('ance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_trajectory_direction'] = 'incoming'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_in_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']\
#        .str.replace('~incoming','').str.replace('~total','')
#cond_obj1 = csn['object1'].str.contains('radiation~outgoing')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_out_trajectory_direction'] = 'outgoing'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'root_object_out_phen']=\
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'object1']\
#        .str.replace('~outgoing','').str.replace('~total','')
#cond_obj1 = csn['object1'].str.contains('radiation')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_form'] = 'snowpack'
#cond_quant = csn['quantity'].str.contains('reflectance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.contains('absorptance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_in_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('emittance')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_out_process_interaction'] = 'emission'
#cond_quant = csn['quantity'].str.contains('reflected')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'reflection'
#cond_quant = csn['quantity'].str.contains('absorbed')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_sink_process_interaction'] = 'absorption'
#cond_quant = csn['quantity'].str.contains('emitted')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_source_process_interaction'] = 'emission'
#csn.loc[(csn['object0']=='snowpack'), ['object0','object1']] = ''
#
##soil
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == ''
#cond_quant = csn['quantity'].str.contains('heat|thermal|hydraulic|porosity|thaw')
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'root_object_matter'] = 'soil'
#cond_quant = csn['quantity'].str.contains('heat|thermal|hydraulic|porosity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_matter'] = 'soil'
#cond_quant = csn['quantity'].str.contains('thaw')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_context_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_process'] = 'thaw'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = 'depth'
#cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'isochoric_mass-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'isobaric_mass-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'isochoric_volume-specific_heat_capacity'
#cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'modified_quantity'] = 'isobaric_volume-specific_heat_capacity'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##soil_bulk
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'bulk'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_configstate'] = 'bulk'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##soil_macropores
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'macropores'
#cond_quant = csn['quantity'].str.contains('volume_fraction')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_form'] = 'macropores'
#cond_quant = csn['quantity'].str.contains('cutoff_depth')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_context_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_form'] = 'macropores'
#cond_quant = csn['quantity'].str.contains('conductivity')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_context_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_form'] = 'macropores'
##csn.loc[(csn['object0']=='soil')&(csn['object1']=='macropores')&\
##        csn['quantity'].str.contains('conductivity'),'root_object_matter']='water'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##soil_permafrost
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'permafrost'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_context_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_phen'] = 'permafrost'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = \
#       csn.loc[ cond_obj0 & cond_obj1, 'object2'] 
#csn.loc[ cond_obj0 & cond_obj1,['object0','object1','object2']] = ''
#
##soil_*-zone
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'].str.contains('zone')
#cond_quant = csn['quantity'].str.contains('recharge')
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'root_object_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'root_object_part_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_sink_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_sink_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_sink_part_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object2']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##soil_ice_thawing-front
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'ice'
#cond_obj2 = csn['object2'] == 'thawing-front'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_context_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_phen'] = 'thawing-front'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']] = ''
#
##soil_ice
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'ice'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_phasestate'] = 'ice'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##soil_bedrock_top
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'bedrock'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_reference_form'] = 'bedrock'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_reference_part'] = 'top'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_reference_relationship'] = 'above'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##soil_particle
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'particle'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter_configstate'] = 'particle'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##soil_layer/horizon
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'].str.contains('layer|horizon~')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object1']
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object1']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##soil_matter~organic/loam/air
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'].str.contains('matter|loam|sand|silt|air|clay')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_obj1, 'object1']
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##soil_surface_water
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'surface'
#cond_quant = csn['quantity'].str.contains('infiltration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_abstraction']='surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_matter']='water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_undergoing_process']='infiltration'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('infiltration','process')
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
#        'root_object_medium_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
#        'root_object_medium_abstraction'] = 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##soil_void
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'void'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_medium_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'void'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
#
##soil_water(_flow)
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'] == 'flow'
#cond_quant = csn['quantity']\
#        .str.contains('pressure_head|wilting-point|capillary|diffusivity')
#csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
#        'root_object_medium_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_context_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#cond_quant = csn['quantity'].str.contains('wilting')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'wilting-point'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('wilting-point_','')
#cond_quant = csn['quantity'].str.contains('saturated')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_condition'] = 'saturated'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('saturated_','')
#cond_quant = csn['quantity'].str.contains('infiltration')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
#        'root_object_medium_process_interaction']='infiltration'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity']\
#        .str.replace('infiltration','process')
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##soil_water_*front (water unnecessary)
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'].str.contains('front')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_phen'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2']] = ''
#
##soil_water_*zone (water unnecessary)
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj1 = csn['object1'] == 'water'
#cond_obj2 = csn['object2'].str.contains('zone')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_matter'] = 'soil'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_medium_matter'] = ''
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
#cond_obj3 = csn['object3'] == 'top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
#        'root_object_part_part'] = 'top'
#cond_obj4 = csn['object4'] == 'surface'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
#        'root_object_abstraction'] = 'surface'
#cond_quant = csn['quantity'].str.contains('recharge')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'root_object_undergoing_process'] = 'recharge'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#        'modified_quantity'] = \
#        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
#                'modified_quantity'].str.replace('recharge','process')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
#        ['object0','object1','object2','object3','object4']] = ''
#
##soil_x-section_macropores
#cond_obj0 = csn['object0'] == 'soil'
#cond_obj2 = csn['object2'] == 'macropores'
#csn.loc[ cond_obj0 & cond_obj2, 'root_object_medium_matter']='soil'
#csn.loc[ cond_obj0 & cond_obj2, 'root_object_medium_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj2, 'object1']
#csn.loc[ cond_obj0 & cond_obj2, 'root_object_form'] = 'macropores'
#csn.loc[ cond_obj0 & cond_obj2, ['object0','object1','object2']] = ''
#
##space-shuttle_tile
#cond_obj0 = csn['object0'] == 'space-shuttle'
#csn.loc[ cond_obj0, 'root_object_medium_context_form'] = 'space-shuttle'
#csn.loc[ cond_obj0, 'root_object_medium_form'] = 'tile'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##sphere_surface
#cond_obj0 = csn['object0'] == 'sphere'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'sphere'
#csn.loc[ cond_obj0, 'root_object_abstraction_abstraction'] = 'surface'
#csn.loc[ cond_obj0, ['object0','object1']] = ''

#spring~steel
cond_obj0 = csn['object0'] == 'spring~steel'
csn.loc[ cond_obj0, 'object_id'] = 'spring~steel'
csn.loc[ cond_obj0, 'object_label'] = 'spring~steel'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

##square
#cond_obj0 = csn['object0'] == 'square'
#csn.loc[ cond_obj0, 'root_object_abstraction'] = 'square'
#csn.loc[ cond_obj0, 'object0'] = ''
#
##star~
#cond_obj0 = csn['object0'].str.contains('star~')
#csn.loc[ cond_obj0,'root_object_form'] = \
#        csn.loc[ cond_obj0,'object0']
#csn.loc[ cond_obj0, 'modified_quantity'] = \
#        ['tolman-oppenheimer-volkoff-limit_mass', 'chandrasekhar-limit_mass']
#csn.loc[ cond_obj0, 'object0'] = ''
#
##submarine
#cond_obj0 = csn['object0'] == 'submarine'
#csn.loc[ cond_obj0, 'root_object_form'] = 'submarine'
#csn.loc[ cond_obj0, 'root_object_reference_form'] = 'sea'
#csn.loc[ cond_obj0, 'root_object_reference_part'] = 'floor'
#csn.loc[ cond_obj0, 'root_object_reference_relationship'] = 'above'
#csn.loc[ cond_obj0, ['object0','object1']] = ''

#sulfuric-acid
cond_obj0 = csn['object0'] == 'sulfuric-acid'
csn.loc[ cond_obj0, 'object_id'] = 'sulfuric-acid'
csn.loc[ cond_obj0, 'object_label'] = 'sulfuric-acid'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, ['object0','object1']] = ''

##sulfuric-acid
#cond_obj0 = csn['object0'] == 'sulphuric-acid'
#csn.loc[ cond_obj0, 'root_object_matter'] = 'sufuric-acid'
#csn.loc[ cond_obj0, 'second_root_object_matter'] = 'water'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##sun-lotion_skin
#cond_obj0 = csn['object0'] == 'sun-lotion'
#csn.loc[ cond_obj0, 'root_object_matter'] = 'sun-lotion'
#csn.loc[ cond_obj0, 'second_root_object_form'] = 'skin'
#csn.loc[ cond_obj0, 'two_object_process_interaction'] = 'protection'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##tank~storage~open-top
#cond_obj0 = csn['object0'] == 'tank~storage~open-top'
#cond_obj1 = csn['object1'] == 'water'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_form'] = 'tank~storage~open-top'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'water'
#cond_quant = csn['quantity'].str.contains('flow')
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'modified_quantity'] = 'speed'
#cond_obj1 = csn['object1'].str.contains('x-section')
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'tank~storage~open-top'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = \
#        (csn.loc[ cond_obj0 & cond_obj1, 'object1'] + '~' + \
#         csn.loc[ cond_obj0 & cond_obj1, 'object2']).str.rstrip('~')
#cond_obj1 = csn['object1'].str.contains('outlet')
#cond_obj2 = csn['object2'].str.contains('x-section')
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_form'] = 'tank~storage~open-top'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_part'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'root_object_abstraction'] = 'x-section'
#cond_obj2 = csn['object2'].str.contains('water')
#csn.loc[ cond_obj0 & cond_obj2, \
#        'root_object_source_form'] = 'tank~storage~open-top'
#csn.loc[ cond_obj0 & cond_obj2, \
#        'root_object_source_part'] = 'outlet'
#csn.loc[ cond_obj0 & cond_obj2, \
#        'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj2, \
#        'root_object_process'] = 'flow'
#csn.loc[ cond_obj0 & cond_obj2, 'modified_quantity'] = 'speed'
#csn.loc[ cond_obj0, ['object0','object1','object2']] = ''
#
##titan_atmosphere_methane
#cond_obj0 = csn['object0'] == 'titan'
#csn.loc[ cond_obj0, 'root_object_source_object_context_form'] = 'titan'
#csn.loc[ cond_obj0, \
#        'root_object_source_object_context_relationship'] = 'surrounding'
#csn.loc[ cond_obj0, 'root_object_source_form'] = 'atmosphere'
#csn.loc[ cond_obj0, 'root_object_matter'] = 'methane'
#csn.loc[ cond_obj0, 'root_object_source_process_interaction'] = 'precipitation'
#csn.loc[ cond_obj0, 'modified_quantity'] = 'process_leq_volume_flux'
#csn.loc[ cond_obj0, ['object0','object1','object2']] = ''
#
##toyota_corolla
#cond_obj0 = csn['object0'] == 'toyota'
#cond_obj2 = csn['object2'] == ''
#csn.loc[ cond_obj0 & cond_obj2, \
#        'root_object_form'] = 'automobile~toyota~corolla~2008'
#csn.loc[ cond_obj0 & cond_obj2, ['object0','object1']] = ''
#
##toyota_corolla_engine
#cond_obj0 = csn['object0'] == 'toyota'
#cond_obj2 = csn['object2'] == 'engine'
#csn.loc[ cond_obj0 & cond_obj2, \
#        'root_object_context_form'] = 'automobile~toyota~corolla~2008'
#csn.loc[ cond_obj0 & cond_obj2, 'root_object_form'] = 'engine'
#csn.loc[ cond_obj0 & cond_obj2, ['object0','object1','object2']] = ''
#
##toyota_corolla_fuel_tank
#cond_obj0 = csn['object0'] == 'toyota'
#cond_obj3 = csn['object3'] == 'tank'
#csn.loc[ cond_obj0 & cond_obj3, \
#        'root_object_context_form'] = 'automobile~toyota~corolla~2008'
#csn.loc[ cond_obj0 & cond_obj3, 'root_object_form'] = 'fuel-tank'
#csn.loc[ cond_obj0 & cond_obj3, ['object0','object1','object2','object3']] = ''
#
##toyota_corolla_fuel
#cond_obj0 = csn['object0'] == 'toyota'
#cond_obj2 = csn['object2'] == 'fuel'
#csn.loc[ cond_obj0 & cond_obj2, \
#        'root_object_sink_form'] = 'automobile~toyota~corolla~2008'
#csn.loc[ cond_obj0 & cond_obj2, 'root_object_matter'] = 'fuel'
#csn.loc[ cond_obj0 & cond_obj2, \
#        'root_object_sink_process_interaction'] = 'consumption'
#csn.loc[ cond_obj0 & cond_obj2, 'modified_quantity'] = 'process_rate'
#csn.loc[ cond_obj0 & cond_obj2, ['object0','object1','object2']] = ''
#
##tree~oak~bluejack
#cond_obj0 = csn['object0'] == 'tree~oak~bluejack'
#cond_obj1 = csn['object1'] == ''
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'tree~oak~bluejack'
#cond_obj1 = csn['object1'] == 'trunk'
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_context_form'] = 'tree~oak~bluejack'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'trunk'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
##universe
#cond_obj0 = csn['object0'] == 'universe~friedmann'
#csn.loc[ cond_obj0,'root_object_abstraction']='universe~friedmann'
#cond_obj0 = csn['object0'] == 'universe'
#csn.loc[ cond_obj0,'root_object_context_form'] = 'universe'
#csn.loc[ cond_obj0,'root_object_phen'] = 'radiation~background'
#csn.loc[ cond_obj0,'root_object_source'] = 'cosmic'
#csn.loc[ cond_obj0,'modified_quantity'] = 'frequency'
#cond_obj0 = csn['object0'].str.contains('universe')
#csn.loc[ cond_obj0, 'object0'] = ''
#
##venus
#cond_obj0 = csn['object0'] == 'venus'
#cond_obj1 = csn['object1'] == 'axis'
#csn.loc[ cond_obj0, 'root_object_form'] = 'venus'
#cond_quant = csn['quantity'] == 'standard_gravity_constant'
#csn.loc[ cond_obj0 & cond_quant , 'modified_quantity'] = \
#        'standard_gravitational_acceleration'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_abstraction'] = \
#        csn.loc[ cond_obj0 & cond_obj1,'object1']
#cond_obj1 = csn['object1'].str.contains('orbit')
#csn.loc[ cond_obj0 & cond_obj1,'root_object_trajectory'] = 'orbit'
#cond_obj1 = csn['object1'].str.contains('ecliptic')
#csn.loc[ cond_obj0 & cond_obj1, 'second_root_object_trajectory'] = 'ecliptic'
#cond_obj1 = csn['quantity'].str.contains('aphelion')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_trajectory_abstraction'] = 'aphelion'
#cond_obj1 = csn['quantity'].str.contains('perihelion')
#csn.loc[ cond_obj0 & cond_obj1, \
#        'root_object_trajectory_abstraction'] = 'perihelion'
#cond_obj1 = csn['quantity'].str.contains('perihelion|aphelion')
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'distance'
#csn.loc[ cond_obj0, ['object0','object1']] = ''
#
#virus~chicken-pox
cond_obj0 = csn['object0'] == 'virus'
csn.loc[ cond_obj0, 'object_id'] = 'virus~chicken-pox_incubation'
csn.loc[ cond_obj0, 'object_label'] = 'virus~chicken-pox'
csn.loc[ cond_obj0, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, ['object0','object1']] = ''

#water
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1,'object_id']='water'
csn.loc[ cond_obj0 & cond_obj1,'object_label']='water'
csn.loc[ cond_obj0 & cond_obj1,'object_pref']='matter'
cond_quant = csn['quantity'].str.contains('boiling_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'water~boiling-point'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'boiling-point_temperature'
cond_quant = csn['quantity'].str.contains('freezing_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'water~freezing-point'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'freezing-point_temperature'
cond_quant = csn['quantity'].str.contains('volume_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = 'volume_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity'].str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = 'shear_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity'].str.replace('shear_','')
cond_quant = csn['quantity'].str.contains('mass-specific_latent_fusion')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'latent_fusion_mass-specific_heat'
cond_quant = csn['quantity'].str.contains('mole-specific_latent_fusion')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'latent_fusion_mole-specific_heat'
cond_quant = csn['quantity'].str.contains('mass-specific_latent_sublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'latent_sublimation_mass-specific_heat'
cond_quant = csn['quantity'].str.contains('mole-specific_latent_sublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'latent_sublimation_mole-specific_heat'
cond_quant = csn['quantity'].str.contains('mass-specific_latent_vaporization')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'latent_vaporization_mass-specific_heat'
cond_quant = csn['quantity'].str.contains('mole-specific_latent_vaporization')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'latent_vaporization_mole-specific_heat'
cond_quant = csn['quantity'].str.contains('vaporization')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'water_vaporization'
cond_quant = csn['quantity'].str.contains('fusion')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'water_fusion'
cond_quant = csn['quantity'].str.contains('sublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'water_sublimation'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
cond_quant = csn['quantity'].str.contains('fusion|sublimation|vaporization')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'object_pref']='phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

##water_channel-network_source
#cond_obj0 = csn['object0'] == 'water'
#cond_obj1 = csn['object1'] == 'channel-network'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_form'] = 'channel-network'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_part'] = 'source~of-water'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''
#
##water_electron
#cond_obj0 = csn['object0'] == 'water'
#cond_obj1 = csn['object1'] == 'electron'
#csn.loc[ cond_obj0 & cond_obj1, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_obj1, 'modified_quantity'] = 'electron_affinity'
#csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#water_salt
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'salt'
csn.loc[ cond_obj0 & cond_obj1, 'object_context_id'] = 'water_in'
csn.loc[ cond_obj0 & cond_obj1, 'object_context_label'] = 'water'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'salt'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'salt'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'matter'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = 'mass_diffusivity'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#water_sand_grain
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'sand'
csn.loc[ cond_obj0 & cond_obj1, 'object_context_id'] = 'water_in'
csn.loc[ cond_obj0 & cond_obj1, 'object_context_label'] = 'water'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'sand_grain_settling'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'sand_grain'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#water_scuba-diver_dive__duration
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'scuba-diver'
csn.loc[ cond_obj0 & cond_obj1, 'object_context_id'] = 'water_in'
csn.loc[ cond_obj0 & cond_obj1, 'object_context_label'] = 'water'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'human_scuba-diver_dive'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'scuba-diver'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#water_molecule_bond~...
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'molecule'
cond_obj2 = csn['object2'].str.contains('-')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_context_id'] = 'water_molecule_part'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_context_label'] = 'water_molecule'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'bond~' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_label'] = 'bond~' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('dissociation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & \
        cond_quant, 'object_id'] + '_dissociation'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']\
        .str.replace('bond_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#water_molecule_hydrogen...
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'molecule'
cond_obj2 = csn['object2'] == 'hydrogen'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'hydrogen'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_label'] = 'hydrogen'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'matter'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_context_id'] = 'water_molecule_part'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_context_label'] = 'water_molecule'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_id']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

##water_...__solubility
#cond_obj0 = csn['object0'] == 'water'
#cond_quant = csn['quantity'] == 'solubility'
#csn.loc[ cond_obj0 & cond_quant, 'root_object_medium_matter'] = 'water'
#csn.loc[ cond_obj0 & cond_quant,'root_object_matter'] = \
#        csn.loc[ cond_obj0 & cond_quant, 'object1']
#csn.loc[ cond_obj0 & cond_quant, ['object0','object1']] = ''

#water~liquid
cond_obj0 = csn['object0'] == 'water~liquid'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1,'object_id']='water~liquid'
csn.loc[ cond_obj0 & cond_obj1,'object_label']='water~liquid'
csn.loc[ cond_obj0 & cond_obj1,'object_pref']='matter'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1,['object0','object1']]=''

##water~liquid_...
#cond_obj0 = csn['object0'] == 'water~liquid'
#csn.loc[ cond_obj0,'root_object_medium_matter']='water'
#csn.loc[ cond_obj0,'root_object_medium_matter_phasestate']='liquid'
#csn.loc[ cond_obj0,'root_object_matter']=\
#    csn.loc[ cond_obj0,'object1'].str.split('~',1).str[0]
#csn.loc[ cond_obj0,'root_object_matter_phasestate']=\
#    csn.loc[ cond_obj0,'object1'].str.split('~',1).str[1]
#csn.loc[ cond_obj0,['object0','object1']]=''

#water~liquid~20C
cond_obj0 = csn['object0'] == 'water~liquid~20C'
cond_obj1 = csn['object1'] == 'air'
csn.loc[ cond_obj0,'object_label']='water~liquid~20C'
csn.loc[ cond_obj0,'object_id']='water~liquid~20C'
csn.loc[ cond_obj0,'object_pref']='matter'
csn.loc[ cond_obj0 & cond_obj1,'object_context_label']='air'
csn.loc[ cond_obj0 & cond_obj1,'object_context_id']='air_in'
cond_quant = csn['quantity'].str.contains('volume_viscosity')
csn.loc[ cond_obj0 & cond_quant, 'quantity_label'] = 'volume_'+\
        csn.loc[ cond_obj0 & cond_quant, 'quantity']\
        .str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear_viscosity')
csn.loc[ cond_obj0 & cond_quant, 'quantity_label'] = 'shear_'+\
        csn.loc[ cond_obj0 & cond_quant, 'quantity'].str.replace('shear_','')
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, ['object0','object1']] = ''

#water~vapor
cond_obj0 = csn['object0'] == 'water~vapor'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'water~vapor'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'water~vapor'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'matter'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

##water~vapor_air~dry
#cond_obj0 = csn['object0'] == 'water~vapor'
#csn.loc[ cond_obj0, 'root_object_matter'] = 'water'
#csn.loc[ cond_obj0, 'root_object_matter_phasestate'] = 'vapor'
#csn.loc[ cond_obj0, 'second_root_object_matter'] = 'air'
#csn.loc[ cond_obj0, 'second_root_object_matter_phasestate'] = 'dry'
#csn.loc[ cond_obj0, 'root_quantity1'] = 'relative_molecular_mass'
#csn.loc[ cond_obj0, 'root_quantity2'] = 'relative_molecular_mass'
#csn.loc[ cond_obj0, 'two_object_operator'] = 'ratio'
#csn.loc[ cond_obj0, ['object0','object1']] = ''

#wave
cond_obj0 = csn['object0'].str.contains('wave')
csn.loc[ cond_obj0,'object_id'] = csn.loc[ cond_obj0, 'object0']
csn.loc[ cond_obj0,'object_label'] = csn.loc[ cond_obj0, 'object0']
csn.loc[ cond_obj0,'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

#wood~dry
cond_obj0 = csn['object0'].str.contains('wood')
csn.loc[ cond_obj0, 'object_id'] = 'wood~dry'
csn.loc[ cond_obj0, 'object_label'] = 'wood~dry'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, 'quantity_id'] = csn.loc[ cond_obj0, 'quantity_label']
csn.loc[ cond_obj0, 'object0'] = ''

cond_obj0 = csn['object0'] == ''
csn = csn.loc[ cond_obj0 ]
csn=csn.fillna('')

csn.loc[csn['operator']!='','quantity_id'] = csn.loc[csn['operator']!='','operator']+'_of_'+csn.loc[csn['operator']!='','quantity_id']
csn.loc[csn['operator']!='','quantity_label'] = csn.loc[csn['operator']!='','operator']+'_of_'+csn.loc[csn['operator']!='','quantity_label']
csn['variable_label'] = csn['object_label']+'__'+csn['quantity_label']
csn.loc[csn['object_context_label']!='','variable_label'] = \
        csn.loc[csn['object_context_label']!='','object_context_label'] + '_' +\
        csn.loc[csn['object_context_label']!='','variable_label']
cols_to_print = ['variable_label','object_id','object_label','object_pref','quantity_id','quantity_label','object_context_id','object_context_label']
csn[cols_to_print].to_csv('CSDMS_standard_names.csv',index=False)
