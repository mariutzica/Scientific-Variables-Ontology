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
csn['object_cat'] = ''
csn['object_pref'] = 'phenomenon'
csn['object_label'] = csn['object'].copy()
csn['quantity_id'] = ''

#Start cleanup of object part
#air
cond_obj0 = csn['object0'] == 'air'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'air'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'matter'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
cond_quant = csn['quantity'].str.contains('volume_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = 'volume_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'].str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = 'shear_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'].str.replace('shear_','')
cond_quant = csn['quantity'].str.contains('volume-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'quantity_label'] = \
                                    'isochoric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'object_id'] = \
                                    'air_isochoric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'object0']=''

#air_helium-plume
cond_obj0 = csn['object0'] == 'air'
cond_obj1 = csn['object1'] == 'helium-plume'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'air@context~in_helium-plume'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']]=''

#air_radiation~visible
cond_obj0 = csn['object0'] == 'air'
cond_obj1 = csn['object1'] == 'radiation~visible'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'air@context~in_radiation~visible'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = 'linear_speed'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#air_water~vapor
cond_obj0 = csn['object0'] == 'air'
cond_obj1 = csn['object1'] == 'water~vapor'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'air@medium_water~vapor'
cond_quant = csn['quantity'].str.contains('saturated')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
    'air@medium_saturated_water~vapor'
cond_quant = csn['quantity'].str.contains('dew_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
    'dew-point_temperature'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
                            'air@medium_dew-point_water~vapor'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#aircraft
cond_obj0 = csn['object0'] == 'aircraft'
csn.loc[ cond_obj0, 'object_id'] = 'aircraft_flight'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#airfoil
cond_obj0 = csn['object0'] == 'airfoil'
cond_obj1 = csn['object1'] == 'curve~enclosing'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'airfoil_curve~enclosing'
cond_quant = csn['quantity'].str.contains('coefficient')
csn.loc[ cond_obj0 & ~cond_quant, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = \
        'airfoil' + '_' + \
        csn.loc[ cond_obj0 & cond_quant, 'quantity_label'].str.split('_').str[0]\
        .str.replace('drag','dragging')
csn.loc[ cond_obj0, ['object0','object1']] = ''

#airplane(_wing)
cond_obj0 = csn['object0'] == 'airplane'
cond_obj1 = csn['object1'] == 'wing'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = 'length'
csn.loc[ cond_obj0, 'object_id'] = 'airplane'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'airplane_wingspan'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'airplane_wingspan'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#air~dry(_water~vapor)
cond_obj0 = csn['object0'] == 'air~dry'
cond_obj1 = csn['object1'] == 'water~vapor'
csn.loc[ cond_obj0, 'object_id'] = 'air~dry'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'air~dry@role~numerator_water~vapor@role~denominator'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'air~dry-to-water~vapor'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id']='gas_constant_ratio'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#aluminum
cond_obj0 = csn['object0'] == 'aluminum'
csn.loc[ cond_obj0, 'object_id'] = 'aluminum_isobaric-process'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'quantity_label'] = 'isobaric_mass-specific_heat_capacity'
csn.loc[ cond_obj0, 'object0']=''

#ammonia/ammonium-as-nitrogen
cond_obj0 = csn['object0'].str.contains('-as-') & ~csn['object0'].str.contains('fertilizer')
cond_quant = csn['quantity'].str.contains('_volatilization')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = csn.loc[ cond_obj0 & cond_quant, 'object0'] + '_volatilization'
cond_quant = csn['quantity'].str.contains('_leaching')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = csn.loc[ cond_obj0 & cond_quant, 'object0'] + '_leaching'
cond_quant = csn['quantity'].str.contains('_nitrification')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = csn.loc[ cond_obj0 & cond_quant, 'object0'] + '_nitrification'
cond_quant = csn['quantity'].str.contains('_denitrification')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = csn.loc[ cond_obj0 & cond_quant, 'object0'] + '_denitrification'
csn.loc[ cond_obj0, 'object0']=''

#anvil
cond_obj0 = csn['object0'] == 'anvil'
csn.loc[ cond_obj0, 'object_id'] = 'anvil_isobaric-process'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#appliance~electric
cond_obj0 = csn['object0'] == 'appliance~electric'
csn.loc[ cond_obj0, 'object_id'] = 'appliance~electric'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object0'] = ''

#aquifer~left/right_channel~stream_reach_water
cond_obj0 = csn['object0'].str.contains('aquifer')
csn.loc[ cond_obj0, 'object_id'] = csn.loc[ cond_obj0, 'object0']+'@role~source_'+\
    '(channel~stream@context~part_reach)@role~sink_(water_flowing)@role~main_baseflow'
csn.loc[ cond_obj0, ['object0','object1','object2','object3']] = ''

#atmosphere_aerosol_dust
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'aerosol'
cond_obj2 = csn['object2'] == 'dust'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
            'object_id'] = '(atmosphere@role~main_radiation@role~in_transmission)@role~first_((atmosphere@medium_dust~aerosol)@role~main_radiation@role~in_transmission)@role~second'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
            'object_label'] = 'atmosphere_dust~aerosol'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
            ['object0','object1','object2']]=''

#atmosphere_aerosol_radiation        
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'aerosol'
csn.loc[ cond_obj0 & cond_obj1, \
            'object_id'] = 'atmosphere@context~in_(aerosol'
cond_quant = csn['quantity'].str.endswith('ance')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
            'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
            'object_id']+'@role~main_'+csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
            'object2']
cond_obj2 = csn['object2'].str.contains('incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
            'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
            'object_id']+'@role~in'
cond_obj2 = csn['object2'].str.contains('outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
            'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
            'object_id']+'@role~out'
cond_quant = csn['quantity']=='energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
            'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
            'object_id']+'@context~source_'+csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
            'object2']+')'
cond_quant = csn['quantity'].str.contains('_energy')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
            'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
            'object_id']+'@role~sink_'+csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
            'object2']+'@role~main'
cond_quant = csn['quantity'].str.contains('absor')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] + '_absorption)'
cond_quant = csn['quantity'].str.contains('refl')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] + '_reflection)'
cond_quant = csn['quantity'].str.contains('transmit')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] + '_transmission)'
cond_quant = csn['quantity'].str.contains('emit')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] + '_emission)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#atmosphere_air
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'atmosphere@context~in_air'
cond_quant = csn['quantity'] == 'mass-specific_isobaric_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'isobaric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air_isobaric-process)'
cond_quant = csn['quantity'] == 'mass-specific_isochoric_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label']='isochoric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air_isochoric-process)'
cond_quant = csn['quantity'] == 'volume-specific_isobaric_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label']='isobaric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air_isobaric-process)'
cond_quant = csn['quantity']=='volume-specific_isochoric_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label']='isochoric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air_isochoric-process)'
cond_quant = csn['quantity'] == 'static_pressure_environmental_lapse_rate'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label']='environmental_static_pressure_lapse_rate'
cond_quant = csn['quantity'] == 'temperature_dry_adiabatic_lapse_rate'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label']='dry_adiabatic_temperature_lapse_rate'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air~dry_adiabatic-process)'
cond_quant = csn['quantity'] == 'temperature_saturated_adiabatic_lapse_rate'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label']='saturated_adiabatic_temperature_lapse_rate'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air_saturated_adiabatic-process)'
cond_quant = csn['quantity'] == 'temperature_environmental_lapse_rate'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label']='environmental_temperature_lapse_rate'
cond_quant = csn['quantity'] == 'isentropic_compressibility'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air_isentropic-process)'
cond_quant = csn['quantity'] == 'isothermal_compressibility'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air_isothermal-process)'
cond_quant = csn['quantity'].str.contains('convective')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air_convection)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#atmosphere_air-column_aerosol~dry
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air-column'
cond_obj2 = csn['object2'] == 'aerosol~dry'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(atmosphere_air_column)@context~in_ammonium~aerosol~dry'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'atmosphere_air-column_ammonium~aerosol~dry'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#atmosphere_air-column_...-as-...
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air-column'
cond_obj2 = csn['object2'].str.contains('-as-')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(atmosphere_air_column)@context~in_' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#atmosphere_air-column_~~~
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air-column'
cond_obj2 = csn['object2'].str.contains('vapor')
cond_quant = csn['quantity'] == 'liquid-equivalent_depth'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'leq_depth'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = '(atmosphere_air_column)@context~in_' + \
        csn.loc[ cond_obj0 & cond_obj1, 'object2']\
        .str.replace('aceto-nitrile','acetonitrile')\
        .str.replace('alpha-hexachlorocyclohexane','alpha-hch')
csn.loc[ cond_obj0 & cond_obj1,\
        ['object0','object1','object2']] = ''

#atmosphere_air_carbon-dioxide
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air'
cond_obj2 = csn['object2'] == 'carbon-dioxide'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'atmosphere@context~in_(air@medium_carbon-dioxide)'
cond_quant = csn['quantity'].str.contains('equilibrium')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_equilibrium_carbon-dioxide)'
cond_quant = csn['quantity'].str.contains('saturated')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_saturated_carbon-dioxide)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']]=''

#atmosphere_air_flow
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air'
cond_obj2 = csn['object2'] == 'flow'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'atmosphere@context~in_(air_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('total_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#atmosphere_air_flow_suspended-compound
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air'
cond_obj2 = csn['object2'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'atmosphere@context~in_((air_flowing)@medium_' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#atmosphere_air_mercury/nitrogen~...
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air'
cond_obj2 = csn['object2'].str.contains('mercury|nitrogen')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'atmosphere@context~in_(air@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,'object2']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#atmosphere_air_nmvoc~...
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air'
cond_obj2 = csn['object2'].str.contains('nmvoc')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'atmosphere@context~in_(air@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+'-as-'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'atmosphere_air_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+'-as-'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#atmosphere_air_radiation
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air'
cond_obj2 = csn['object2'] == 'radiation'
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'atmosphere@context~in_(air@medium_radiation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'atmosphere@context~in_(air@medium_(radiation_optical-path))'
cond_quant = csn['quantity'].str.contains('attenuation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_attenuation_radiation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'evaluation_method'] = 'beer-lambert-law'
cond_quant = csn['quantity'].str.contains('refractive')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_refraction_radiation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 , \
        ['object0','object1','object2','object3']] = ''

#atmosphere_air_radiation~...
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air'
cond_obj2 = csn['object2'].str.contains('radiation~')
cond_quant = csn['quantity'].str.contains('intensity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
        'object_id'] = '(atmosphere_air)@role~main_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, 'object2']\
        +'@role~in'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']='atmosphere@context~in_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']
cond_quant = csn['quantity'].str.contains('absorp')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_absorption'
cond_quant = csn['quantity'].str.contains('trans')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_transmission'
cond_quant = csn['quantity'].str.contains('reflect')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_reflection'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#atmosphere_air_water~vapor...
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'air'
cond_obj2 = csn['object2'] == 'water~vapor'
cond_quant = csn['quantity'].str.contains('density|virtual')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_water~vapor)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_water~vapor'
cond_quant = csn['quantity'].str.contains('dew_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_dew-point_water~vapor)'
cond_quant = csn['quantity'].str.contains('bubble_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_bubble-point_water~vapor)'
cond_quant = csn['quantity'].str.contains('frost_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_frost-point_water~vapor)'
cond_quant = csn['quantity'].str.contains('equilibrium')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_equilibrium_water~vapor)'
cond_quant = csn['quantity'].str.contains('saturated')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_saturated_water~vapor)'
cond_quant = csn['quantity'].str.contains('point')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'].str.replace('_point','-point')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#atmosphere_ball
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'ball'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'atmosphere@context~in_(ball_falling)'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#atmosphere_bottom_air
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == ''
cond_quant = csn['quantity'].str.contains('brutsaert')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
        'object_id'] = '(atmosphere_bottom)@context~in_air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@role~sink'
cond_quant = csn['quantity'].str.contains('isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'isobaric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('air','(air')+'_isobaric-process)'
cond_quant = csn['quantity'].str.contains('canopy')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id']+'_canopy@role~main_radiation@role~out_emission)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label']+'_canopy'
cond_quant = csn['quantity'].str.contains('cloud')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id']+'_cloud@role~main_radiation@role~out_emission)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label']+'_cloud'
cond_quant = csn['quantity']=='emissivity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('air','(air')+'@role~main_radiation@role~out_emission)'
cond_quant = csn['quantity'].str.contains('brutsaert')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'brutsaert_emissivity_factor'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'evaluation_method'] = 'brutsaert'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#atmosphere_bottom_air_carbon-dioxide
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == 'carbon-dioxide'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@medium_carbon-dioxide)'
cond_quant = csn['quantity'].str.contains('saturated')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@medium_saturated_carbon-dioxide)'
cond_quant = csn['quantity'].str.contains('equilibrium')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@medium_equilibrium_carbon-dioxide)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#atmosphere_bottom_air_flow(_something)
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == 'flow'
cond_obj4 = csn['object4'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(atmosphere_bottom)@context~in_((air_flowing)@role~exchange_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
                'object4']+'@role~exchange)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('total_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('of_velocity','of_linear_velocity')
cond_quant = csn['quantity'].str.contains('log-law')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'evaluation_method'] = 'log-law'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#atmosphere_bottom_air_heat_flow
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == 'heat'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = 'log-law_heat_roughness_length'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'evaluation_method'] = 'log-law'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#atmosphere_bottom_air_heat~...__flux
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'].str.contains('heat')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
        .str.split('~').str[1]+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'atmosphere_bottom_air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
        .str.split('~').str[1]+'_heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#atmosphere_bottom_air_land_heat~...__flux
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == 'land'
cond_obj4 = csn['object4'].str.contains('incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'atmosphere_bottom_air_land'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@role~source_land@role~sink)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'quantity_label'] = 'incoming_' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object4']\
        .str.replace('heat~incoming~','') + '_heat_energy_flux'
cond_obj4 = csn['object4'].str.contains('heat~net')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@role~exchange_land@role~exchange)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object4']\
        .str.replace('heat~net~','') + '_heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#atmosphere_bottom_air_water~vapor(_flow)
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == 'water~vapor'
cond_obj4 = csn['object4'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'atmosphere_bottom_air_water~vapor'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@context~in_water~vapor)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(atmosphere_bottom)@context~in_((air_flowing)@context~in_water~vapor)'
cond_quant = csn['quantity'].str.contains('_point_|saturation|conductance|pressure')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@medium_water~vapor)'
cond_quant = csn['quantity'].str.contains('dew_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@medium_dew-point_water~vapor)'
cond_quant = csn['quantity'].str.contains('frost_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@medium_frost-point_water~vapor)'
cond_quant = csn['quantity'].str.contains('saturated')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@medium_saturated_water~vapor)'
cond_quant = csn['quantity'].str.contains('equilibrium')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(atmosphere_bottom)@context~in_(air@medium_equilibrium_water~vapor)'
cond_quant = csn['quantity'].str.contains('_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'].str.replace('_point','-point')
cond_quant = csn['quantity'].str.contains('log-law')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'evaluation_method'] = 'log-law'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#atmosphere_carbon-dioxide
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'carbon-dioxide'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'atmosphere@context~in_(air@medium_carbon-dioxide)'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'atmosphere_air_carbon-dioxide'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#atmosphere_clouds_radiation~...
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'clouds'
cond_quant = csn['quantity'].str.endswith('ance')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
        'atmosphere@context~in_(clouds@role~main'
cond_obj2 = csn['object2'].str.contains('incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] + '_' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']+\
        '@role~in'
cond_obj2 = csn['object2'].str.contains('outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] + '_' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']+\
        '@role~out'
cond_quant = csn['quantity'].str.endswith('flux')
cond_obj2 = csn['object2'].str.contains('incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(clouds@role~sink'
cond_obj2 = csn['object2'].str.contains('outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(clouds@role~source'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] + '_' +\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object2']+'@role~main'
cond_quant = csn['quantity'] == 'energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(clouds@context~source_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object2']+')'
cond_quant = csn['quantity'].str.contains('absor')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] + '_absorption)'
cond_quant = csn['quantity'].str.contains('refl')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] + '_reflection)'
cond_quant = csn['quantity'].str.contains('transmit')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] + '_transmission)'
cond_quant = csn['quantity'].str.contains('emit')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] + '_emission)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#atmosphere_datum~.._air(_flow)
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'].str.contains('datum')
cond_obj3 = csn['object3'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = \
        '(atmosphere_'+csn.loc[ cond_obj0 & cond_obj1, 'object1']+')@context~in_(air_flowing)'
csn.loc[ cond_obj0 & cond_obj1, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1, \
        'quantity_label'].str.replace('total_','')
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1','object2','object3']] = ''

#atmosphere_graupel
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'graupel'
cond_quant = csn['quantity'].str.contains('precipitation')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
        'object_id'] = 'atmosphere@context~source_graupel'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@role~source_graupel@role~main_precipitation'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

##atmosphere_hail
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'hail'
cond_quant = csn['quantity'].str.contains('precipitation')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
        'object_id'] = 'atmosphere@context~source_hail'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@role~source_hail@role~main_precipitation'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#atmosphere_hydrometeor
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'hydrometeor'
cond_quant = csn['quantity'].str.contains('fall')
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'atmosphere@context~source_hydrometeor'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@context~source_(hydrometeor_falling)'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#atmosphere_ice
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'ice'
cond_quant = csn['quantity'].str.contains('precipitation')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
        'object_id'] = 'atmosphere@context~source_ice'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@role~source_ice@role~main_precipitation'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#atmosphere_radiation~...
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'].str.contains('radiation')
cond_quant = csn['quantity'].str.endswith('ance')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@role~main_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']+'@role~in'
cond_quant = csn['quantity'].str.endswith('flux')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@role~sink_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']+'@role~main'
cond_quant = csn['quantity'].str.contains('absor')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_absorption'
cond_quant = csn['quantity'].str.contains('refl')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_reflection'
cond_quant = csn['quantity'].str.contains('transm')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_transmission'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#atmosphere_raindrop
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'raindrop'
cond_quant = csn['quantity'].str.contains('fall')
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'atmosphere@context~source_raindrop'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@context~source_(raindrop_falling)'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#atmosphere_sleet
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'sleet'
cond_quant = csn['quantity'].str.contains('precipitation')
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'atmosphere@context~source_sleet'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@role~source_sleet@role~main_precipitation'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#atmosphere_snow
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'snow'
cond_quant = csn['quantity'].str.contains('precipitation')
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'atmosphere@context~source_snow'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@role~source_snow@role~main_precipitation'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#atmosphere_top_air
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == 'air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(atmosphere_top)@context~in_air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#atmosphere_top_radiation~...
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'].str.contains('radiation~incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'atmosphere_top_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
        .str.replace('~total','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(atmosphere_top)@context~sink_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
        .str.replace('~total','')
cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(atmosphere_top)@context~source_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
        .str.replace('~total','')
cond_obj2 = csn['object2'].str.contains('radiation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#atmosphere_top_surface_radiation~...
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(atmosphere_top_surface)@context~sink_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#atmosphere_water
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'water'
cond_quant = csn['quantity'].str.contains('density')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_id'] = \
        'atmosphere@role~source_water@role~main_precipitation'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
        'atmosphere@context~source_water'
cond_quant = csn['quantity'].str.contains('leq')
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']\
        .str.replace('leq-','leq_')
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']\
        .str.replace('snowfall','precipitation')\
        .str.replace('rainfall','precipitation')\
        .str.replace('icefall','precipitation')
cond_quant = csn['quantity'].str.contains('snowfall')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'].str.replace('water','snowfall')
cond_quant = csn['quantity'].str.contains('icefall')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'].str.replace('water','icefall')
cond_quant = csn['quantity'].str.contains('rainfall')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'].str.replace('water','rainfall')
cond_quant = csn['quantity'].str.contains('daily_time_integral')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity'].str.replace('daily','one-day')
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#atmosphere_water~vapor
cond_obj0 = csn['object0'] == 'atmosphere'
cond_obj1 = csn['object1'] == 'water~vapor'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_label'] = 'atmosphere_air_water~vapor'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'atmosphere@context~in_(air@medium_water~vapor)'
cond_quant = csn['quantity'].str.contains('dew_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_dew-point_water~vapor)'
cond_quant = csn['quantity'].str.contains('frost_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_frost-point_water~vapor)'
cond_quant = csn['quantity'].str.contains('saturated')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'atmosphere@context~in_(air@medium_saturated_water~vapor)'
cond_quant = csn['quantity'].str.contains('_point_')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'].str.replace('_point_','-point_')
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#automobile
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'].str.replace('of_velocity','of_linear_velocity')
cond_quant = csn['quantity'].str.contains('acceleration')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile_acceleration'
cond_quant = csn['quantity'].str.contains('0-to-60mph')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile_acceleration~0-to-60mph'
cond_quant = csn['quantity'].str.contains('braking')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile_braking'
cond_quant = csn['quantity'].str.contains('cargo')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'automobile@medium_cargo'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_label'] = 'automobile_cargo'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_cat'] = ''
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'number_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_id'] = 'number_capacity'
cond_quant = csn['quantity'].str.contains('seating_capacity')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile@medium_seating_human'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_label'] = 'automobile_human'
cond_quant = csn['quantity'].str.contains('stopping')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile_stopping'
cond_quant = csn['quantity'].str.contains('turning')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile_turning'
cond_quant = csn['quantity'].str.contains('wheelbase')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']='automobile_wheelbase'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_label']='automobile_wheelbase'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref']='phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = 'length'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_id'] = 'length'
cond_quant = csn['quantity'].str.contains('travel')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile_travel'
cond_quant = csn['quantity'].str.contains('lifetime')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile_lifetime-travel'
cond_quant = csn['quantity'].str.contains('travel')
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']\
        .str.replace('total_','')
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']
cond_quant = csn['quantity'].str.contains('drag_coefficient')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile_dragging'
cond_quant = csn['quantity'].str.contains('lift_coefficient')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile_lift'
cond_quant = csn['quantity'].str.contains('manufacture')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile_manufacture'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#automobile_axis~vertical
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'axis~vertical'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile_axis~vertical'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#automobile_battery
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'battery'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile@context~in_battery'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#automobile_bottom_ground
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'ground'
cond_quant = csn['quantity'].str.contains('angle')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_obj2 & ~cond_quant, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(automobile_bottom)_ground@reference~above'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'automobile_bottom_above-ground'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'object_id'] = '(automobile_bottom_'\
    +csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity'].str.split('_').str[0]+')_ground@reference~above'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'object_label'] = \
    'automobile_bottom_above-ground'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#automobile_bumper_bottom
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'bumper'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(automobile@context~part_(bumper_bottom))_ground@reference~above'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'automobile_bumper_bottom_above-ground'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = 'height'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#automobile_carbon-dioxide
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'carbon-dioxide'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile@role~source_carbon-dioxide@role~main_emission'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#automobile_door
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'door'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile@context~part_door'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#automobile_driver
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'driver'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile@role~sink_(driver_reaction)@role~main_driving'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#automobile_engine
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'engine'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'automobile@context~part_engine'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#automobile_engine_crankshaft/cylinder
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'engine'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
        'object_id'] = 'automobile@context~part_(engine@context~part_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, 'object2']+')'
cond_quant = csn['quantity'].str.contains('rotation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
        'object_id']=csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
        'object_id'].str.replace('crankshaft\)','(crankshaft')+'_rotation))'
cond_quant = csn['quantity'].str.contains('stroke')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
        'object_id']=csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
        'object_id'].str.replace('cylinder\)','(cylinder')+'_stroking))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
        ['object0','object1','object2']] = ''

#automobile_engine_crankshaft/cylinder_piston
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'engine'
cond_obj3 = csn['object3'] == 'piston'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, 'object_id'] = \
        'automobile@context~part_(engine@context~part_('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, 'object2']+\
        '@context~part_piston))'
cond_quant = csn['quantity'].str.contains('stroke')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj3 & cond_quant, \
        'object_id']=csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
        'object_id'].str.replace('piston','(piston_stroking)')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#automobile_front_x-section
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'front'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile_front_x-section'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#automobile_fuel__consumption_rate
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'fuel'
cond_quant = csn['quantity'].str.contains('consumption')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile@role~sink_fuel@role~main_consumption'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        ['object0','object1']] = ''

#automobile_fuel
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'fuel'
cond_obj2 = csn['object2'] == ''
cond_quant = csn['quantity'].str.contains('energy-per-mass')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'automobile@context~in_fuel'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'specific_energy'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#automobile_fuel_tank
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'fuel'
cond_obj2 = csn['object2'] == 'tank'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'automobile@context~part_fuel-tank'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'automobile_fuel-tank'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#automobile_fuel-tank
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'fuel-tank'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'automobile@context~part_fuel-tank'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#automobile_rear_axle
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'rear'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile@context~part_axle~rear'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'automobile_axle~rear'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#automobile_seat_belt
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'seat'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile@context~part_seat-belt'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'automobile_seat-belt'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#automobile_tire
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'tire'
cond_quant = csn['quantity'].str.contains('inflation')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile@context~part_tire'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'automobile@context~part_(tire_inflation)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#automobile_wheel
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'wheel'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile@context~part_wheel'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#automobile_wheelbase
cond_obj0 = csn['object0'] == 'automobile'
cond_obj1 = csn['object1'] == 'wheelbase'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'automobile_wheelbase'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#balloon
cond_obj0 = csn['object0'] == 'balloon'
csn.loc[ cond_obj0, 'object_id'] = 'balloon'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object0'] = ''

#baseball-bat_baseball
cond_obj0 = csn['object0'] == 'baseball-bat'
cond_obj1 = csn['object1'] == 'baseball'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'baseball-bat@role~main_baseball@role~main_impaction'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#basin
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'].str.contains('flint-law')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'basin~drainage'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'basin~drainage'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']\
        .str.replace('total_contributing','contributing')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'evaluation_model'] = 'flint-law'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#basin_boundary
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'boundary'
csn.loc[ cond_obj0 & cond_obj1,'object_id'] = 'basin~drainage_boundary'
csn.loc[ cond_obj0 & cond_obj1,'object_label'] = 'basin~drainage_boundary'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#basin_centroid
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'centroid'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'basin~drainage_centroid'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'basin~drainage_centroid'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#basin_channel-network
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'channel-network'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_channel-network'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'].str.replace('basin','basin~drainage')
cond_quant = csn['quantity'].str.contains('graph')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'basin~drainage@context~part_(channel-network_graph)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label']+'_graph'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label'].str.replace('graph_','')
cond_quant = csn['quantity'].str.contains('density')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'basin~drainage@medium_channel-network'
cond_quant = csn['quantity'].str.contains('usgs')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'usgs_hydrologic_unit_code'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'].str.replace('total_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#basin_channel-network_graph
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'channel-network'
cond_obj2 = csn['object2'] == 'graph'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_(channel-network_graph)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'basin~drainage_channel-network_graph'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#basin_channel-network_link~...
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'channel-network'
cond_obj2 = csn['object2'].str.contains('link')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_(channel-network@context~part_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'basin~drainage_channel-network_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#basin_channel-network_source
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'channel-network'
cond_obj2 = csn['object2'] == 'source'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_(channel-network@context~part_source)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'basin~drainage_channel-network_source'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#basin_channels/channel~...(_centerline)
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'].str.contains('channel')
cond_obj2 = csn['object2'] != ''
csn.loc[ cond_obj0 & cond_obj1 & ~cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_'+\
        csn.loc[ cond_obj0 & cond_obj1, 'object1']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
        'basin~drainage@context~part_('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+')'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_label'] = csn.loc[ cond_obj0 & cond_obj1, \
        'object_label'].str.replace('basin','basin~drainage')
cond_obj1 = csn['object1'].str.contains('channel')
cond_quant = csn['quantity'].str.contains('flint-law')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'evaluation_assumption'] = 'flint-law'
cond_quant = csn['quantity'].str.contains('hack-law')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'evaluation_assumption'] = 'hack-law'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1','object2']] = ''

#basin_land~...
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'].str.contains('land')
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'basin~drainage@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1, 'object1']\
        .str.replace('land~grassland','grassland')
csn.loc[ cond_obj0 & cond_obj1, \
        'object_label'] = 'basin~drainage_'+\
        csn.loc[ cond_obj0 & cond_obj1, 'object1']\
        .str.replace('land~grassland','grassland')
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1','object2']] = ''

#basin_outlet
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'outlet'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_outlet'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'basin~drainage_outlet'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']\
        .str.replace('total_contributing','contributing')
cond_quant = csn['quantity'] == 'bankfull_width'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(basin~drainage_bankfull)@context~part_outlet'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#basin_outlet_bank~...
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'outlet'
cond_obj2 = csn['object2'].str.contains('bank')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_(outlet@context~part_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'basin~drainage_outlet_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#basin_outlet_center
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'outlet'
cond_obj2 = csn['object2'] == 'center'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_(outlet_center)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'basin~drainage_outlet_center'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#basin_outlet_channel_bottom
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'outlet'
cond_obj2 = csn['object2'] == 'channel'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_(outlet@context~at_(channel_bottom))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'basin~drainage_outlet_channel_bottom'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#basin_outlet_sediment
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'outlet'
cond_obj2 = csn['object2'] == 'sediment'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_(outlet@context~at_sediment)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'basin~drainage_outlet_sediment'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = 'mass-per-time_yield'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#basin_outlet_water_flow
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'outlet'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'basin~drainage@context~part_(outlet@context~at_(water_flowing_friction))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'basin~drainage_outlet_water_flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#basin_outlet_water_sediment~...
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'outlet'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'].str.contains('sediment')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'basin~drainage@context~part_(outlet@context~at_((water_flowing)@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
                            'object3'].str.replace('~total','')+'))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'basin~drainage_outlet_water_flow_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
                            'object3'].str.replace('~total','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#basin_outlet_water_x-section(_top)
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'outlet'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'x-section'
cond_obj4 = csn['object4'] == 'top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'basin~drainage@context~part_(outlet@context~at_(water_x-section))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'basin~drainage_outlet_water_x-section'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'].str.rstrip(')')+'_top))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_label']+'_top'
cond_quant = csn['quantity'].str.contains('flow')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'].str.replace('water_','water_flowing_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'].str.replace('water_','water_flow_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#basin_outlet~terminal_water
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'outlet~terminal'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'basin~drainage@context~part_(outlet~terminal@context~at_(water_flowing))'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_label'] = 'basin~drainage_outlet~terminal_water_flow'
csn.loc[ cond_obj0 & cond_obj1,\
        ['object0','object1','object2','object3','object4']] = ''

#basin_rain-gage
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'rain-gauge'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'basin~drainage@context~in_rain-gauge'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_label'] = 'basin~drainage_rain-gauge'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#basin_sources
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'sources'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'basin~drainage@context~part_sources'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'basin~drainage_sources'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#basin_weather-station
cond_obj0 = csn['object0'] == 'basin'
cond_obj1 = csn['object1'] == 'weather-station'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'basin~drainage@context~in_weather-station'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'basin~drainage_weather-station'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#battery
cond_obj0 = csn['object0'] == 'battery'
csn.loc[ cond_obj0, 'object_id'] = 'battery'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#beam
cond_obj0 = csn['object0'] == 'beam'
csn.loc[ cond_obj0,'object_id']='beam'
csn.loc[ cond_obj0,'object_pref']='body'
csn.loc[ cond_obj0,'object_cat']='root'
csn.loc[ cond_obj0,'object0']=''

#bear_brain-to-body
cond_obj0 = csn['object0'] == 'bear'
csn.loc[ cond_obj0, 'object_id'] = '(bear@context~part_brain)@role~numerator_(bear@context~part_body)@role~denominator'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#bear~alaskan~black
cond_obj0 = csn['object0'] == 'bear~alaskan~black'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'bear~black~american'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'bear~black~american'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#bear~alaskan~black_brain-to-body
cond_obj0 = csn['object0'] == 'bear~alaskan~black'
cond_obj1 = csn['object1'] == 'brain-to-body'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = \
    '(bear~black~american@context~part_brain)@role~numerator_(bear~black~american@context~part_body)@role~denominator'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = \
    'bear~black~american_brain-to-body'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#bear~alaskan~black_head
cond_obj0 = csn['object0'] == 'bear~alaskan~black'
cond_obj1 = csn['object1'] == 'head'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'bear~black~american@context~part_head'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'bear~black~american_head'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#bedrock
cond_obj0 = csn['object0'] == 'bedrock'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'].str.contains('uplift')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant,'object_id']='bedrock'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'object_id']='bedrock_uplift'
cond_quant = csn['quantity'].str.contains('uplift|permeability|density')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant,'object_pref']='body'
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant,'object_cat']='root'
cond_quant = csn['quantity'].str.contains('permeability|density')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant,'object_id']='bedrock@context~in_material'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#bedrock_below-land-surface
cond_obj0 = csn['object0'] == 'bedrock'
cond_obj1 = csn['object1'] == 'below-land-surface'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'bedrock_(land_surface)@reference~below'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = 'depth'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#bedrock_material
cond_obj0 = csn['object0'] == 'bedrock'
cond_obj1 = csn['object1'] == 'material'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'bedrock@context~in_material'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#bedrock_surface(_land/sea-mask)
cond_obj0 = csn['object0'] == 'bedrock'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] != ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'bedrock_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
            csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] +\
            '_'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#benzene_molecule_c_c_c
cond_obj0 = csn['object0'] == 'benzene'
csn.loc[ cond_obj0, 'object_id'] = '(benzene_molecule)@context~part_bond~c-c-c'
csn.loc[ cond_obj0, 'object_label'] = 'benzene_molecule_bond~c-c-c'
csn.loc[ cond_obj0, 'quantity_label'] = 'angle'
csn.loc[ cond_obj0, ['object0','object1','object2','object3','object4']] = ''

#biomass_nitrogen_at-harvest__mass-per-area_accumulation_density
cond_obj0 = csn['object0'] == 'biomass'
cond_obj1 = csn['object1'] == 'nitrogen'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(biomass@context~in_(nitrogen_accumulation))_(crop_harvest)@reference~at'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#biomass~microbial-and-soil_pool~organic~stabilized-as-nitrogen__mass-per-area_density
cond_obj0 = csn['object0'] == 'biomass~microbial-and-soil'
csn.loc[ cond_obj0, 'object_id'] = 'biomass~microbial@context~in_(soil_pool~organic~stabilized)@context~in_nitrogen'
csn.loc[ cond_obj0, ['object0','object1','object2','object3','object4']] = ''

#biomass~microbial-and-soil~stabilized_carbon__decomposition_mass_respiration_rate
cond_obj0 = csn['object0'] == 'biomass~microbial-and-soil~stabilized'
csn.loc[ cond_obj0, 'object_id'] = '(biomass~microbial_decomposition)@role~source_(soil~stabilized_decomposition)@role~source_carbon@role~main_respiration'
csn.loc[ cond_obj0, ['object0','object1','object2','object3','object4']] = ''

#biomass~microbial-or-soil_pool~stabilized~organic_nitrogen__gross_immobilization_mass-per-area_density
cond_obj0 = csn['object0'] == 'biomass~microbial-or-soil'
csn.loc[ cond_obj0, 'object_id'] = 'biomass~microbial@context~in_(soil_pool~organic~stabilized)@context~in_nitrogen'
csn.loc[ cond_obj0, ['object0','object1','object2','object3','object4']] = ''

#biomass~removed_nitrogen__mass-per-area_density
cond_obj0 = csn['object0'] == 'biomass~removed'
csn.loc[ cond_obj0, 'object_id'] = 'biomass~removed@context~in_nitrogen'
csn.loc[ cond_obj0, ['object0','object1','object2','object3','object4']] = ''

#black-hole
cond_obj0 = csn['object0'] == 'black-hole'
csn.loc[ cond_obj0, 'object_id'] = 'black-hole'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#bridge
cond_obj0 = csn['object0'] == 'bridge'
csn.loc[ cond_obj0, 'object_id'] = 'bridge'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#building~empire-state
cond_obj0 = csn['object0'] == 'building~empire-state'
csn.loc[ cond_obj0, 'object_id'] = 'empire-state-building'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object0'] = ''

#cantor-set
cond_obj0 = csn['object0'] == 'cantor-set'
csn.loc[ cond_obj0, 'object_id'] = 'cantor-set'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#carbon_hydrogen__bond_length
cond_obj0 = csn['object0'] == 'carbon'
cond_obj1 = csn['object1'] == 'hydrogen'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'bond~c-h'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'bond~c-h'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = 'length'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#carbon_isotope_neutron
cond_obj0 = csn['object0'] == 'carbon'
cond_obj1 = csn['object1'] == 'isotope'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(carbon_isotope)@context~part_neutron'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#cesium
cond_obj0 = csn['object0'] == 'cesium'
cond_obj1 = csn['object1'] == 'atom'
cond_obj2 = csn['object2'] != ''
cond_quant = csn['quantity'].str.contains('emission')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_obj2 & ~cond_quant, \
        'object_id'] = 'cesium_atom'
csn.loc[ cond_obj0 & cond_obj1 & ~cond_obj2 & ~cond_quant, \
        'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = '(cesium_atom)@role~source_radiation@role~main_emission'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(cesium_atom)@context~part_'+\
    csn.loc[ cond_obj0, 'object2']
cond_quant = csn['quantity']=='relative_atomic_mass'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_id'] = 'atomic_mass_ratio'
csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#channel
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'channel'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'form'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
cond_quant = csn['quantity'].str.contains('station')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'station@context~at_channel'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_label'] = 'channel_station'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_cat'] = ''
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label']\
        .str.replace('station_','')
#channel_meander
cond_quant = csn['quantity'].str.contains('meander')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'channel_meandering'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity'].str.replace('meander','meandering')
cond_quant = csn['quantity'].str.contains('meander_amplitude')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_id'] = 'meandering_width'
cond_quant = csn['quantity'].str.contains('migration')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'channel_meandering_migration'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#channel_bank_sediment_water
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bank'
cond_obj2 = csn['object2'] == 'sediment'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel@context~part_bank)@context~on_(sediment@medium_saturated_water)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#channel_bank_water
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bank'
cond_obj2 = csn['object2'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel@context~part_bank)@role~denominator_(water_flowing)@role~numerator'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#channel~river_bed_channel~stream_reach_water
cond_obj0 = csn['object0'].str.contains('channel~')
cond_obj1 = csn['object1'] == 'bed'
cond_obj2 = csn['object2'].str.contains('channel~')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel~river_bed)@role~exchange_' +\
        '(channel~stream@context~part_reach)@role~exchange_(water_flowing)@role~main_leakage'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#channel~river_bed_water~incoming/outgoing
cond_obj0 = csn['object0'].str.contains('channel~')
cond_obj1 = csn['object1'] == 'bed'
cond_obj2 = csn['object2'].str.contains('water~incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel~river_bed)@context~sink_' +\
        '(water_flowing)'
cond_obj2 = csn['object2'].str.contains('water~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel~river_bed)@context~source_' +\
        '(water_flowing)'
cond_obj2 = csn['object2'].str.contains('water~')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#channel~river_bed_water
cond_obj0 = csn['object0'].str.contains('channel~')
cond_obj1 = csn['object1'] == 'bed'
cond_obj2 = csn['object2'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel~river_bed)@medium_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#channel_bed
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bed'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'channel_bed'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#channel_bed_below-channel-bank
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bed'
cond_obj2 = csn['object2'] == 'below-channel-bank'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel_bed)_(channel@context~part_bank)@reference~below'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#channel_bed_water
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bed'
cond_obj2 = csn['object2'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel_bed)@medium_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''
        
#channel_bottom_sediment
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'sediment'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(channel_bottom)@context~on_sediment'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#channel_bottom_sediment_grain
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'sediment'
cond_obj3 = csn['object3'] == 'grain'
cond_obj4 = csn['object4'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(channel_bottom)@context~on_(sediment_grain)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3']] = ''

#channel_bottom_sediment_grain_water
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'sediment'
cond_obj3 = csn['object3'] == 'grain'
cond_obj4 = csn['object4'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '((channel_bottom)@context~on_(sediment_grain))@medium_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3']] = ''

#channel_bottom_sediment_oxygen~dissolved
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'sediment'
cond_obj3 = csn['object3'] == 'oxygen~dissolved'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(channel_bottom)@context~on_(sediment@role~sink_oxygen~dissolved@role~main_consumption)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#channel_bottom_sediment_water
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'sediment'
cond_obj3 = csn['object3'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(channel_bottom)@context~on_(sediment@medium_saturated_water)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#channel_bottom_surface
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'channel_bottom_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#channel_bottom_water
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(channel_bottom)@context~at_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#channel_bottom_water_flow(_sediment(_grain))
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'flow'
cond_obj4 = csn['object4'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(channel_bottom)@context~at_(water_flowing)'
cond_obj4 = csn['object4'] == 'sediment'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(channel_bottom)@context~at_((water_flowing)@medium_sediment)'
cond_obj5 = csn['object5'] == 'grain'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
        'object_id'] = '(channel_bottom)@context~at_((water_flowing)@medium_(sediment_grain))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
        'quantity_label'].str.replace('total_','')
cond_quant = csn['quantity'].str.contains('log-law')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'evaluation_method'] = 'log-law'
cond_quant = csn['quantity']=='total_pressure'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'pressure'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_id'] = 'pressure'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#channel_centerline(_endpoints)
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'centerline'
cond_obj2 = csn['object2'] == 'endpoints'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'channel_centerline'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(channel_centerline_endpoint~upstream)@role~first_(channel_centerline_endpoint~downstream)@role~second'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1','object2']] = ''

#channel_entrance_basin
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'entrance'
cond_obj2 = csn['object2'] == 'basin'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_((channel@context~part_entrance)@role~sink)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'channel_entrance_basin~drainage'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']\
    .str.replace('total_contributing','contributing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#channel_entrance_center
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'entrance'
cond_obj2 = csn['object2'] == 'center'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'channel@context~part_(entrance_center)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#channel_entrance_water_x-section
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'entrance'
cond_obj2 = csn['object2'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel@context~part_entrance)@context~at_(water_x-section)'
cond_quant = csn['quantity'].str.contains('flow|flux')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(channel@context~part_entrance)@context~at_(water_flowing_x-section)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label'] = 'channel_entrance_water_flow_x-section'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#channel_exit_basin
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'exit'
cond_obj2 = csn['object2'] == 'basin'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'basin~drainage@context~part_((channel@context~part_exit)@role~sink)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'channel_exit_basin~drainage'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'].str.replace('total_contributing','contributing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#channel_exit_center
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'exit'
cond_obj2 = csn['object2'] == 'center'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'channel@context~part_(exit_center)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#channel_exit_water_x-section(_sediment) 
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'exit'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'x-section'
cond_obj4 = csn['object4'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(channel@context~part_exit)@context~at_((water_flowing_x-section)@medium_sediment~suspended)'
cond_obj4 = csn['object4'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(channel@context~part_exit)@context~at_(water_x-section)'
cond_quant = csn['quantity'].str.contains('_flow_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_id'] = '(channel@context~part_exit)@context~at_(water_flowing_x-section)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_label'] = 'channel_exit_water_flow_x-section'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''


#channel_valley_centerline
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'valley'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'channel@context~part_(valley_centerline)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#channel~river_water
cond_obj0 = csn['object0'] == 'channel~river'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'channel~river@medium_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']]=''

#channel~stream_reach_water~incoming/outgoing
cond_obj0 = csn['object0'] == 'channel~stream'
cond_obj1 = csn['object1'] == 'reach'
cond_obj2 = csn['object2'].str.contains('water~incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel~stream@context~part_reach)@context~sink_(water_flowing)'
cond_obj2 = csn['object2'].str.contains('water~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(channel~stream@context~part_reach)@context~source_(water_flowing)'
cond_obj2 = csn['object2'].str.contains('water~')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']]=''

#channel_water
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'channel@context~in_water'
cond_quant = csn['quantity'].str.contains('ic_volume')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'volume_' +csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'].str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'shear_' +csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'].str.replace('shear_','')
cond_quant = csn['quantity'].str.contains('_flow_|power')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']='channel@context~in_(water_flowing)'
cond_quant = csn['quantity'].str.contains('reaeration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']='channel@context~in_(water@role~main_reaeration)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1',]]=''

#channel_water_channel_bottom_surface
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'channel'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'channel@context~in_(water@role~first_(channel_bottom_surface)@role~second)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3','object4']] = ''

#channel_water_flow
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'flow'
cond_quant = csn['quantity'].str.contains('dissipation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
        'object_id'] = 'channel@context~in_(water_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'channel@context~in_((water_flowing)@role~medium_dissipation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'energy-per-volume_dissipation_rate'
cond_quant = csn['quantity'].str.contains('friction')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'channel@context~in_((water_flowing)@role~exchange_friction)'
cond_quant = csn['quantity'].str.contains('manning')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'evaluation_method'] = 'manning-formula'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'].str.replace('total_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']]=''

#channel_water_hydraulic-jump
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'hydraulic-jump'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'channel@context~in_(water_hydraulic-jump)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#channel_water_oxygen~photosynthetic
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'oxygen~photosynthetic'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = \
        'channel@context~in_(water@context~in_(processes@role~source_oxygen~photosynthetic@role~main_production))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']]=''

#channel_water_sediment~...
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'].str.contains('sediment')
cond_quant = csn['quantity'].str.contains('concentration|flow|settling|immersed')
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'channel_water_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object2'].str.replace('~total','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'channel@context~in_(water@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object2'].str.replace('~total','')+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
        'object_id'] = 'channel@context~in_(water@context~in_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
        'object2'].str.replace('~total','')+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'].str.replace('sediment','(sediment').str.rstrip(')') +'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+'))'
cond_quant = csn['quantity'].str.contains('immersed')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water@medium','water@medium_immersed')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'weight'
cond_quant = csn['quantity'].str.contains('settling')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('medium','medium_settling')
cond_quant = csn['quantity'].str.contains('_flow_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water_flowing)')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#channel_water_surface_air
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'surface'
cond_obj3 = csn['object3'] == 'air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,\
    'object_id']='(channel@context~in_(water_surface))@context~above_air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,\
    ['object0','object1','object2','object3']]=''

#channel_water_surface
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'channel@context~in_(water_surface)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#channel_water_x-section(_top)
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'x-section'
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'channel@context~in_(water_x-section)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2& cond_obj3, \
        'object_id'] = 'channel@context~in_(water_x-section_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
cond_quant = csn['quantity'].str.contains('_flow_|flux')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2& cond_quant, \
        'object_id'].str.replace('water_','water_flowing_')
cond_quant = csn['quantity'].str.contains('wetted')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'channel~wetted_x-section'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#channel_weir
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'weir'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'channel@context~in_(weir@context~source_(water_discharging))'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#channel_x-section
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'x-section'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
    'object_id']='channel_x-section'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#channel_x-section_parabola
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'x-section'
cond_obj2 = csn['object2'] == 'parabola'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'channel_x-section_parabola'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_id'] = 'unspecified_coefficient'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#channel_x-section_top
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'x-section'
cond_obj2 = csn['object2'] == 'top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'channel_x-section_top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#channel_x-section_trapezoid
cond_obj0 = csn['object0'] == 'channel'
cond_obj1 = csn['object1'] == 'x-section'
cond_obj2 = csn['object2'] == 'trapezoid'
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'channel_x-section_trapezoid'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] + '_' +\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#chlorine_electron
cond_obj0 = csn['object0'] == 'chlorine'
cond_obj1 = csn['object1'] == 'electron'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'chlorine@role~main_electron@role~in'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'chlorine'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = 'electron_affinity'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#chocolate
cond_obj0 = csn['object0'] == 'chocolate'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1,'object_id']='chocolate'
csn.loc[ cond_obj0 & cond_obj1,'object_cat']='root'
csn.loc[ cond_obj0 & cond_obj1,'object_pref']='matter'
cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'isobaric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'chocolate_isobaric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'isochoric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'chocolate_isochoric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'isobaric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'chocolate_isobaric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'isochoric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'chocolate_isochoric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('thermal_inertia')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'volume-specific_heat_capacity'
cond_quant = csn['quantity'].str.contains('melting')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'chocolate_melting-point'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'melting-point_temperature'
cond_quant = csn['quantity'].str.contains('tempering')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'chocolate_tempering'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('conching')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'chocolate_conching'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('metabolizable')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'chocolate~metabolizable'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_label'] = 'chocolate~metabolizable'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'energy-per-mass_density'
csn.loc[ cond_obj0 & cond_obj1,'object0'] = ''

#chocolate_cacao/...
cond_obj0 = csn['object0'] == 'chocolate'
csn.loc[ cond_obj0, 'object_id'] = 'chocolate@medium_'+\
        csn.loc[ cond_obj0, 'object1']\
        .str.replace('~total','')
csn.loc[ cond_obj0, 'object_label'] = 'chocolate_'+\
        csn.loc[ cond_obj0, 'object1']\
        .str.replace('~total','')
csn.loc[ cond_obj0, ['object0','object1']] = ''

#chocolate~liquid
cond_obj0 = csn['object0'] == 'chocolate~liquid'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1,'object_id']='chocolate~liquid'
csn.loc[ cond_obj0 & cond_obj1,'object_pref']='matter'
cond_quant = csn['quantity'].str.contains('kinematic')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'shear_kinematic_viscosity'
cond_quant = csn['quantity'].str.contains('casson')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'evaluation_assumption'] = 'casson-model'
cond_quant = csn['quantity'].str.contains('herschel')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'evaluation_assumption'] = 'herschel-bulkley'
cond_obj1 = csn['object1'] == 'water'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'chocolate~liquid@medium_water'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#coal
cond_obj0 = csn['object0'] == 'coal'
csn.loc[ cond_obj0, 'object_id'] = 'coal'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, 'object0'] = ''

#concrete_rubber
cond_obj0 = csn['object0'] == 'concrete'
cond_obj1 = csn['object1'] == 'rubber'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'concrete@role~exchange_rubber@role~exchange_friction'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#consumer
cond_obj0 = csn['object0'] == 'consumer'
csn.loc[ cond_obj0, 'object_id'] = 'market-basket'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'object_label'] = 'market-basket'
csn.loc[ cond_obj0, 'quantity_label'] = 'consumer_price_index'
csn.loc[ cond_obj0, 'object0'] = ''

#crop_fertilizer~nitrogen
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'fertilizer~nitrogen'
cond_quant = csn['quantity'].str.contains('applied')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
        'crop@context~sink_(fertilizer~nitrogen_application)'
cond_quant = csn['quantity'].str.contains('elasticity')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
        '(crop_production)@role~numerator_(fertilizer~nitrogen_utilization)@role~denominator'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#crop
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'].str.contains('from-planting')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = '(crop_planting)@reference~from_crop'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object0'] = ''
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'].str.contains('produced')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'crop_production'
cond_quant = csn['quantity'].str.contains('planting')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'crop_planting'
cond_quant = csn['quantity'].str.contains('planting_or_sowing')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = '(crop_planting)@role~main_(crop_sowing)@role~main'
cond_quant = csn['quantity'].str.contains('transpiration')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'crop@role~source_water@role~main_transpiration'
cond_quant = csn['quantity'].str.contains('planting|produced|transpiration')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_id'] = 'crop'
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_pref'] = 'rolephenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#crop~mature~dry
cond_obj0 = csn['object0'] == 'crop~mature~dry'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'crop~mature~dry_harvest_production'
cond_obj1 = csn['object1'] == 'tops'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = \
    'crop~mature~dry_tops_production'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#crop_from-planting
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'from-planting'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(crop_planting)@reference~from_crop'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']] = ''

#crop_biomass
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'biomass'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'crop_biomass'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']] = ''

#crop_biomass_nitrogen
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'biomass'
cond_obj2 = csn['object2'] == 'nitrogen'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(crop_biomass)@context~sink_(nitrogen_application)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']] = ''

#crop_biomass~microbial-and-soil_carbon__time_integral_of_mass-per-area_decomposition_respiration_rate
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'biomass~microbial-and-soil'
cond_obj2 = csn['object2'] == 'carbon'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(crop_biomass~microbial_decomposition)@role~source_'+\
            '(soil_decomposition)@role~source_carbon@role~main_respiration'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']] = ''

#crop_canopy_radiation~solar__interception_energy_flux_fraction
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'canopy'
cond_obj2 = csn['object2'] == 'radiation~solar'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(crop_canopy)@role~sink_radiation~solar@role~main_interception'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#crop_canopy_water
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'canopy'
cond_obj2 = csn['object2'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(crop_canopy)@role~source_water@role~main_transpiration'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#crops~legume_nitrogen
cond_obj0 = csn['object0'] == 'crops~legume'
cond_obj1 = csn['object1'] == 'nitrogen'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'crops~legume@role~sink_nitrogen@role~main_fixation'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#crop_nitrogen
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'nitrogen'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'crop@role~main_nitrogen@role~exchange'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#crop_residue_pool_carbon
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'residue'
cond_obj2 = csn['object2'] == 'pool'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(crop@context~source_(residue_pool_decomposition))@role~source_carbon@role~main_respiration'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#crop_residue_pool_root-and-rhizodeposit_biomass/carbon
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'residue'
cond_obj2 = csn['object2'] == 'pool'
cond_obj3 = csn['object3'] == 'root-and-rhizodeposit'
cond_obj4 = csn['object4'] == 'biomass'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object_id'] = \
    '(crop@context~source_((residue_pool)@context~part_root-and-rhizodeposit))@role~sink_biomass@role~main_addition'
cond_obj4 = csn['object4'] == 'carbon'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object_id'] = \
    '(crop@context~source_((residue_pool)@context~part_root-and-rhizodeposit))@context~in_(carbon_decomposition)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, ['object0','object1','object2','object3','object4']] = ''

#crop_row__planting_spacing
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'row'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
        'crop_planting_row'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#crop_root_nitrogen_at-harvest__mass-per-area_accumulation_density
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'root'
cond_obj2 = csn['object2'] == 'nitrogen'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
        '((crop@context~part_root)@context~in_(nitrogen_accumulation))_(crop_harvest)@reference~at'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#crop_water__time_integral_of_transpiration_volume_flux
cond_obj0 = csn['object0'] == 'crop'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == ''
cond_quant = csn['quantity'].str.contains('transpiration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object_id'] = 'crop@role~source_water@role~main_transpiration'
cond_quant = csn['quantity'].str.contains('evapotranspiration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object_id'] = 'crop@role~source_water@role~main_evapotranspiration'
cond_quant = csn['quantity'].str.contains('stress')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object_id'] = 'crop@role~main_water@role~exchange'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#crop-or-weed
cond_obj0 = csn['object0'] == 'crop-or-weed'
csn.loc[ cond_obj0, 'object_id'] = 'crop-or-weed'
csn.loc[ cond_obj0, 'object_pref'] = 'rolephenomenon'
csn.loc[ cond_obj0, 'object0'] = ''

#cultivar
cond_obj0 = csn['object0'] == 'cultivar'
csn.loc[ cond_obj0, 'object_id'] = 'cultivar'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object0'] = ''

#delta
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'].str.contains('subsidence')
csn.loc[ cond_obj0 & cond_obj1,'object_id'] = 'delta'
csn.loc[ cond_obj0 & cond_obj1,'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'delta_subsidence'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#delta_apex
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'apex'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'delta_apex'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#delta_apex-to-shoreline
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'apex-to-shoreline'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(delta_apex)@role~first_(delta@context~part_shoreline)@role~second'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#delta_beds~...
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('beds')
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'delta_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#delta_beds~..._sediment_clay/...
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('beds')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(delta_' + \
        csn.loc[ cond_obj0 & cond_obj1, 'object1']+')@context~on_(sediment@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1, 'object3']+')'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2','object3']] = ''

#delta_channel~main_entrance
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'channel~main'
cond_obj2 = csn['object2'] == 'entrance'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'delta@context~part_(channel~main@context~part_entrance)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']]=''

#delta_channel~main_entrance_center
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'channel~main'
cond_obj2 = csn['object2'] == 'entrance'
cond_obj3 = csn['object3'] == 'center'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'delta@context~part_(channel~main@context~part_(entrance_center))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#delta_channel~main_entrance_water_sediment_clay/..._grain
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'channel~main'
cond_obj2 = csn['object2'] == 'entrance'
cond_obj3 = csn['object3'] == 'water'
cond_obj4 = csn['object4'] == 'sediment'
cond_obj6 = csn['object6'] == 'grain'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6, \
        'object_id'] = 'delta@context~part_((channel~main@context~part_entrance)@context~in_(water@context~in_(sediment@context~in_(' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & \
                cond_obj6, 'object5']+'_grain))))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6,\
        ['object0','object1','object2','object3','object4','object5',
         'object6']] = ''

#delta_channel~main_entrance_water_sediment_clay/...
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'channel~main'
cond_obj2 = csn['object2'] == 'entrance'
cond_obj3 = csn['object3'] == 'water'
cond_obj4 = csn['object4'] == 'sediment'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = 'delta@context~part_((channel~main@context~part_entrance)@context~in_(water@context~in_(sediment@medium_'\
        + csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & \
                            cond_obj3 & cond_obj4, 'object5']+')))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#delta_channel~main_entrance_water_sediment~...
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'channel~main'
cond_obj2 = csn['object2'] == 'entrance'
cond_obj3 = csn['object3'] == 'water'
cond_obj4 = csn['object4'].str.contains('sediment')
cond_quant = csn['quantity'].str.contains('concentration|_flow_|transport')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_id'] = 'delta@context~part_((channel~main@context~part_entrance)@context~in_(water@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
                'object4']+'))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
        'object_id'] = 'delta@context~part_((channel~main@context~part_entrance)@context~in_(water@context~in_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
                'object4']+'))'
cond_quant = csn['quantity'].str.contains('transport')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_id'].str.replace('medium','medium_transportation')
cond_quant = csn['quantity'].str.contains('flow|transport')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_id'].str.replace('water','(water_flowing)')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4,\
        ['object0','object1','object2','object3','object4']] = ''

#delta_channel~main_entrance_water_x-section
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'channel~main'
cond_obj2 = csn['object2'] == 'entrance'
cond_obj3 = csn['object3'] == 'water'
cond_obj4 = csn['object4'].str.contains('x')
cond_obj6 = csn['object6'] == 'top'
cond_quant = csn['quantity'].str.contains('wetted')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
        'object_id'] = 'delta@context~part_((channel~main@context~part_entrance)@context~in_(water_x-section))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_id'] = 'delta@context~part_(channel~main@context~part_(entrance~wetted_x-section))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj6, \
        'object_id'].str.rstrip(')')+'_top))'
cond_quant = csn['quantity'].str.contains('flow|flux')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_id'].str.replace('water','water_flowing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3','object4','object5',
         'object6']] = ''

#delta_channel~main_entrance_x-section
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'channel~main'
cond_obj2 = csn['object2'] == 'entrance'
cond_obj3 = csn['object3'].str.contains('x')
cond_obj5 = csn['object5'] == 'top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'delta@context~part_(channel~main@context~part_(entrance_x-section))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
        'object_id'] = 'delta@context~part_(channel~main@context~part_(entrance_x-section_top))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
         ['object0','object1','object2','object3','object4','object5']] = ''

#delta_distributary(-network)
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('distributary')
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'delta@context~part_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']\
        .str.replace('total_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#delta_distributary(-network)_water
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('distributary')
cond_obj2 = csn['object2'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'delta@context~part_(' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']+'@context~in_water)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1',
                                             'object2']] = ''

#delta_distributary(-network)_outlet
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('distributary')
cond_obj2 = csn['object2'] == 'outlet'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'delta@context~part_(' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1'] + \
        '@context~part_outlet)'
cond_quant = csn['quantity'].str.startswith('top_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('outlet','(outlet_top)')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'width'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#delta_distributary(-network)_outlet_center/side~...
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('distributary')
cond_obj2 = csn['object2'] == 'outlet'
cond_obj3 = csn['object3'].str.contains('center|side')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'delta@context~part_(' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']+\
        '@context~part_(outlet_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+'))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#delta_distributary(-network)_outlet_water_x-section
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('distributary')
cond_obj2 = csn['object2'] == 'outlet'
cond_quant = csn['quantity'].str.contains('flow|flux')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'delta@context~part_(('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']+'@context~part_outlet)@context~in_(water_x-section))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'].str.replace('water','water_flowing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3','object4']] = ''

#delta_front_sediment(_grain)
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'front'
cond_obj2 = csn['object2'] == 'sediment'
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(delta_front)@context~in_sediment'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'].str.replace('sediment','(sediment')+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#delta_front(_toe)
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'front'
cond_obj2 = csn['object2'] != ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'delta_front'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'delta_front_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#delta_plain~...
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('plain')
cond_quant = csn['quantity'].str.contains('fraction')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'delta@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']\
        .str.replace('~total','')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, ['object0','object1']] = ''

cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('plain')
cond_obj2 = csn['object2'] == 'vegetation'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'delta@context~part_('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']\
        .str.replace('~total','')+'@context~on_vegetation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('plain')
cond_obj2 = csn['object2'] == 'plain~total'        
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(delta@context~part_plain)@role~numerator_(delta@context~part_plain~subaqueous)@role~denominator'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'].str.contains('plain')
cond_obj2 = csn['object2'] != ''        
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'delta@context~part_'+\
    csn.loc[ cond_obj0 & cond_obj1, 'object1'].str.replace('~total','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'delta@context~part_('+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1'].str.replace('~total','')+\
    '_'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+')'
cond_obj1 = csn['object1'].str.contains('plain~lower-and-upper')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(delta@context~part_'+\
    'plain~lower)@role~main_(delta@context~part_plain~upper)@role~main'
cond_obj1 = csn['object1'].str.contains('plain')
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#delta_shoreline
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'shoreline'
cond_obj2 = csn['object2'] == 'sediment'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(delta@context~part_(shoreline@context~on_sediment))@role~main_(ocean@context~part_wave)@role~in_reworking'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'shoreline'
cond_obj2 = csn['object2'] == 'sediment'
cond_quant = csn['quantity'].str.contains('progradation')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'delta@context~part_shoreline'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'delta@context~part_(shoreline_progradation)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#delta_x-section
cond_obj0 = csn['object0'] == 'delta'
cond_obj1 = csn['object1'] == 'x-section'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'delta_x-section'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#delta~...
cond_obj0 = csn['object0'].str.contains('delta')
csn.loc[ cond_obj0, 'object_id'] = csn.loc[ cond_obj0, 'object0']
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object0'] = ''

#dihydrogen/dinitrogen..._molecule_...
cond_obj0 = csn['object0'].str.contains('dihydrogen|dinitrogen|dioxygen')
csn.loc[ cond_obj0, 'object_id'] = '('+\
        csn.loc[ cond_obj0, 'object0']+'_molecule)@context~part_'+\
        'bond~' + csn.loc[ cond_obj0, 'object2']
csn.loc[ cond_obj0, 'object_label'] = \
        csn.loc[ cond_obj0, 'object0']+'_molecule_'+\
        'bond~' + csn.loc[ cond_obj0, 'object2']
csn.loc[ cond_obj0, 'quantity_label'] = 'length'
csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#earth
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'] == 'standard_gravity_constant'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant , 'quantity_label'] = \
        'standard_gravitational_acceleration'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant , 'quantity_id'] = \
        'standard_gravitational_acceleration'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'earth'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
cond_quant = csn['quantity'].str.contains('orbital')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'earth_orbit'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('rotation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
         'object_id'] = 'earth_rotation'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
         'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('escape')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'earth@role~source_body@role~main_escape'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#earth-to-...
cond_obj0 = csn['object0'].str.contains('earth-to')
cond_quant = csn['quantity'].str.contains('travel')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = 'earth@role~source_'+\
    csn.loc[ cond_obj0 & cond_quant, 'object0'].str.split('-to-').str[1]+'@role~sink_(body_travel)@role~main'
csn.loc[ cond_obj0 & ~cond_quant, 'object_id'] = 'earth@role~first_'+\
        csn.loc[ cond_obj0 & ~cond_quant, 'object0'].str.split('-to-').str[1]+\
        '@role~second'
csn.loc[ cond_obj0, 'object0']=''

#earth_atmosphere
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'atmosphere'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'earth@context~surrounding_atmosphere'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#earth_axis/black-body
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'].str.contains('axis|body')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'earth_'+\
    csn.loc[ cond_obj0 & cond_obj1, 'object1']
cond_quant = csn['quantity'].str.contains('nutation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_nutation'
cond_quant = csn['quantity'].str.contains('precession')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_precession'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#earth_day~
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'].str.contains('day~')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'earth@context~on_'+\
    csn.loc[ cond_obj0 & cond_obj1, 'object1']
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#earth_..._boundary
cond_obj0 = csn['object0'] == 'earth'
cond_obj2 = csn['object2'] == 'boundary'
csn.loc[ cond_obj0 & cond_obj2, 'object_id'] = 'earth_'+\
    'boundary~' + csn.loc[ cond_obj0 & cond_obj2, 'object1']
csn.loc[ cond_obj0 & cond_obj2, ['object0','object1','object2']] = ''

#earth_core~...
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'].str.contains('core')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'earth_' + \
    csn.loc[ cond_obj0 & cond_obj1, 'object1']
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#earth_crust_material
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'crust'
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == ''
cond_quant = csn['quantity'].str.contains('wave|oxygen')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
        'object_id'] = '(earth_crust)@context~in_material'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_crust)@context~in_(material@context~in'
cond_quant = csn['quantity'].str.contains('oxygen')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_crust)@context~in_(material@context~in_oxygen)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_crust_material_oxygen'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'fugacity'
cond_quant = csn['quantity'].str.contains('volume_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_quant, 'quantity_label'] = 'volume_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_quant, 'quantity_label'].str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_quant, 'quantity_label'] = 'shear_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_quant, 'quantity_label'].str.replace('shear_','')
cond_quant = csn['quantity'].str.contains('sh-wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_crust)@context~in_(material@role~medium_wave~seismic~sh@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_crust_material_wave~seismic~sh'
cond_quant = csn['quantity'].str.contains('sp-wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_crust)@context~in_(material@role~medium_wave~seismic~sp@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_crust_material_wave~seismic~sp'
cond_quant = csn['quantity'].str.contains('sv-wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_crust)@context~in_(material@role~medium_wave~seismic~sv@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_crust_material_wave~seismic~sv'
cond_quant = csn['quantity'].str.contains('sp-wave|sh-wave|sv-wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'velocity'
cond_quant = csn['quantity'].str.contains('s-wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_crust)@context~in_(material@role~medium_wave~seismic~s@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_crust_material_wave~seismic~s'
cond_quant = csn['quantity'].str.contains('p-wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_crust)@context~in_(material@role~medium_wave~seismic~p@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_crust_material_wave~seismic~p'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label'].str.replace('p-wave_','')
cond_quant = csn['quantity'].str.contains('s-wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label'].str.replace('s-wave_','')
cond_quant = csn['quantity'].str.contains('power-law_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'].str.replace('power-law','power-law-fluid')
cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'isobaric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('material','(material') + '_isobaric-process)'
cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'isochoric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('material','(material') + '_isochoric-process)'
cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'isobaric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('material','(material') + '_isobaric-process)'
cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label']='isochoric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('material','(material') + '_isochoric-process)'
cond_quant = csn['quantity'].str.contains('isothermal')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('material','(material') + '_isothermal-process)'
cond_quant = csn['quantity'].str.contains('_over_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '((earth_crust)@context~in_(material@role~medium_wave~seismic~p@role~main))@role~numerator'+\
        '_((earth_crust)@context~in_(material@role~medium_wave~seismic~s@role~main))@role~denominator'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_crust_material_wave~seismic~p-to-wave~seismic~s'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'velocity_ratio'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''
        
#earth_mantle/crust_material_melt~partial
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'].str.contains('mantle|crust')
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == 'melt~partial'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']+\
        ')@context~in_(material@medium_(material_melt~partial))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#earth_mantle/crust_material_carbonatite_melt
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'].str.contains('mantle|crust')
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == 'carbonatite'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']+\
        ')@context~in_(material~melt@medium_(carbonatite_melt))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#earth_mantle/crust_material_water
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'].str.contains('mantle|crust')
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']+\
        ')@context~in_(material@medium_water)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#earth_datum_ellipsoid
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'datum'
cond_obj2 = csn['object2'] == 'ellipsoid'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'earth_datum_ellipsoid'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#earth_datum_ellipsoid_surface_point-pair_geodesic__distance ???
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'datum'
cond_obj2 = csn['object2'] == 'ellipsoid'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(earth_datum_ellipsoid_'+\
        'surface)@role~first_(earth_datum_geodesic)@role~second'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#earth_ellipsoid/equator
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'].str.contains('ellipsoid|equator|pole|surface')
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'earth_' + \
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']   
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#earth_equator_plane-to-sun
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'].str.contains('equator')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(earth_equator_plane)@role~first_sun@role~second'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#earth_gravity
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'gravity'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'earth@role~source_body@role~main_escape'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#earth_human
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'human'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'earth@medium_carrying_human'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#earth_interior
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'interior'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'earth_interior'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#earth_interior_earthquake
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'interior'
cond_obj2 = csn['object2'] == 'earthquake'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_interior)@context~in_earthquake'
cond_quant = csn['quantity'].str.contains('rupture')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_interior)@context~in_(earthquake@context~source_rupture)'
cond_quant = csn['quantity'].str.contains('slip')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_interior)@context~in_(earthquake@context~source_slip~seismic)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#earth_interior_earthquake_fault
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'interior'
cond_obj2 = csn['object2'] == 'earthquake'
cond_obj3 = csn['object3'] == 'fault'
cond_obj4 = csn['object4'] != ''
cond_obj5 = csn['object5'] == 'asperity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_interior)@context~in_(earthquake@context~source_fault)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(earth_interior)@context~in_(earthquake@context~source_(fault_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object4']+'))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_label'] = 'earth_interior_earthquake_fault_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object4']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
        'quantity_label'] = 'asperity_contact_area'
cond_quant = csn['quantity'].str.contains('rupture')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_interior)@context~in_(earthquake@context~source_(fault_plane_rupture))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#earth_interior_earthquake_focus
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'interior'
cond_obj2 = csn['object2'] == 'earthquake'
cond_obj3 = csn['object3'] == 'focus'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_interior)@context~in_(earthquake_focus)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#earth_interior_earthquake_hypocenter
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'interior'
cond_obj2 = csn['object2'] == 'earthquake'
cond_obj3 = csn['object3'] == 'hypocenter'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_interior)@context~in_(earthquake_hypocenter)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#earth_interior_earthquake_wave~
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'interior'
cond_obj2 = csn['object2'] == 'earthquake'
cond_obj3 = csn['object3'].str.contains('wave~')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_interior)@context~in_(earthquake@context~source_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
        .replace('wave~s','wave~seismic~s').replace('wave~p','wave~seismic~p')+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('angular_','')
cond_quant = csn['quantity'].str.contains('arrival')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_interior)@context~in_((earthquake@context~source_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, 'object3']\
        .replace('wave~s','wave~seismic~s').replace('wave~p','wave~seismic~p')+\
        ')@role~main_arrival)'
cond_quant = (csn['quantity'] == 'frequency') | (csn['quantity_label'] == 'frequency')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_id'] = 'angular_frequency'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#earth_interior_earthquake_hypocenter-to-station
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'interior'
cond_obj2 = csn['object2'] == 'earthquake'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '((earth_interior)@context~in_(earthquake_hypocenter))@role~first_station@role~second'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#earth_interior_particle(_motion)
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'interior'
cond_obj2 = csn['object2'] == 'particle'
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(earth_interior)@context~in_particle'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_interior)@context~in_(particle_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
cond_quant = csn['quantity'].str.contains('acceleration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.rstrip(')')+'_acceleration)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#earth_interior_wave~...
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'interior'
cond_obj2 = csn['object2'].str.contains('wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(earth_interior)@context~in_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'].str.replace('angular_','')
cond_quant = csn['quantity'].str.contains('arrival')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(earth_interior)@context~in_('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']+\
        '@role~main_arrival)'
cond_quant = (csn['quantity'] == 'frequency') | (csn['quantity_label'] == 'frequency')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_id'] = 'angular_frequency'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#earth_mantle_material
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'mantle'
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_mantle)@context~in_material'
cond_quant = csn['quantity'].str.contains('wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_mantle)@context~in_(material@role~medium'
cond_quant = csn['quantity'].str.contains('oxygen')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(earth_mantle)@context~in_(material@context~in'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id']+'_oxygen)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_mantle_material_oxygen'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'fugacity'
cond_quant = csn['quantity'].str.contains('p-wave') & ~csn['quantity'].str.contains('_over_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id']+'_wave~seismic~p@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_mantle_material_wave~seismic~p'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label'].str.replace('p-wave_','')
cond_quant = csn['quantity'].str.contains('s-wave') & ~csn['quantity'].str.contains('_over_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id']+'_wave~seismic~s@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_mantle_material_wave~seismic~s'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label'].str.replace('s-wave_','')
cond_quant = csn['quantity'].str.contains('sh-wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id']+'_wave~seismic~sh@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_mantle_material_wave~seismic~sh'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label'].str.replace('sh-wave_','')
cond_quant = csn['quantity'].str.contains('sv-wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id']+'_wave~seismic~sv@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_mantle_material_wave~seismic~sv'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label'].str.replace('sv-wave_','')
cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label']\
                .str.replace('mass-specific_isobaric','isobaric_mass-specific')
cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label']\
                .str.replace('mass-specific_isochoric','isochoric_mass-specific')
cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label']\
        .str.replace('volume-specific_isobaric','isobaric_volume-specific')
cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label']\
        .str.replace('volume-specific_isochoric','isochoric_volume-specific')
cond_quant = csn['quantity'].str.contains('isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'object_id'].str.replace('material','(material')+'_isobaric-process)'
cond_quant = csn['quantity'].str.contains('isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'object_id'].str.replace('material','(material')+'_isochoric-process)'
cond_quant = csn['quantity'].str.contains('isothermal')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'object_id'].str.replace('material','(material')+'_isothermal-process)'
cond_quant = csn['quantity'].str.contains('volume_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_quant, 'quantity_label'] = 'volume_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_quant, 'quantity_label'].str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_quant, 'quantity_label'] = 'shear_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_quant, 'quantity_label'].str.replace('shear_','')
cond_quant = csn['quantity'].str.contains('power-law')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label'].str.replace('power-law','power-law-fluid')
cond_quant = csn['quantity'].str.contains('_over_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '((earth_mantle)@context~in_(material@role~medium_wave~seismic~p@role~main))@role~numerator_((earth_mantle)@context~in_(material@role~medium_wave~seismic~s@role~main))@role~denominator'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'earth_mantle_material_wave~seismic~p-to-wave~seismic~s'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'velocity_ratio'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#earth_mantle_material_flow
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'mantle'
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_mantle)@context~in_(material_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#earth_mantle_material_mineral-phase
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'mantle'
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == 'mineral-phase'
cond_obj4 = csn['object4'] == ''
cond_quant = csn['quantity'].str.contains('oxygen')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & ~cond_quant, \
        'object_id'] = '(earth_mantle)@context~in_(material_mineral-phase)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_id'] = '(earth_mantle)@context~in_((material_mineral-phase)@context~in_oxygen)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'object_label'] = 'earth_mantle_material_mineral-phase_oxygen'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'quantity_label'] = 'fugacity'
cond_quant = csn['quantity'].str.contains('chemical_composition')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'quantity_label'] = 'chemical-composition_(en)'
cond_quant = csn['quantity'].str.contains('physical_state')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_quant, \
        'quantity_label'] = 'physical-state_(en)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3']] = ''

#earth_mantle_material_mineral-phase_carbonatite_melt
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'mantle'
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == 'mineral-phase'
cond_obj4 = csn['object4'] == 'carbonatite'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(earth_mantle)@context~in_((material_mineral-phase)@medium_(carbonatite_melt))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3', 'object4','object5']] = ''

#earth_mantle_material_mineral-phase_melt_water
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'mantle'
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == 'mineral-phase'
cond_obj4 = csn['object4'] == 'melt'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(earth_mantle)@context~in_((material_mineral-phase~melt)@medium_water)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#earth_mantle_material_mineral-phase_water__solubility
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'mantle'
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == 'mineral-phase'
cond_obj4 = csn['object4'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(earth_mantle)@context~in_((material_mineral-phase)@medium_water)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3','object4']] = ''

#earth_mantle_material_mineral-phase_melt~partial
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'mantle'
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == 'mineral-phase'
cond_obj4 = csn['object4'] == 'melt~partial'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
         'object_id'] = '(earth_mantle)@context~in_((material_mineral-phase)@medium_(material_melt~partial))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3','object4']] = ''

#earth_mantle_material_mohr-coulomb-plastic
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'mantle'
cond_obj2 = csn['object2'] == 'material'
cond_obj3 = csn['object3'] == 'mohr-coulomb-plastic'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_mantle)@context~in_material~mohr-coulomb-plastic'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#earth_material
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'material'
cond_quant = csn['quantity'].str.contains('p_wave')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_id'] = 'earth@context~in_material'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'earth@context~in_(material@role~medium_wave~seismic~p@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = 'modulus'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#earth_orbit
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'orbit'
cond_obj2 = csn['object2'] != ''
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'earth_orbit'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'earth_orbit_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, 'object_id'] = 'earth_orbit_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, 'object2']+'_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj3, 'object3']
cond_quant = csn['quantity'].str.contains('aphelion')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_aphelion'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_label']+'_aphelion'
cond_quant = csn['quantity'].str.contains('perihelion')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_perihelion'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_label']+'_perihelion'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']\
        .str.replace('aphelion_','').str.replace('perihelion_','')
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1','object2','object3']] = ''

#earth_surface_earthquake_epicenter
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'earthquake'
cond_obj3 = csn['object3'] == 'epicenter'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_surface)@context~at_(earthquake_epicenter)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#earth_surface_earthquake_wave~..._station
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'earthquake'
cond_obj3 = csn['object3'].str.contains('wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_surface)@context~at_(earthquake@context~source_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
        .replace('wave~s','wave~seismic~s').replace('wave~p','wave~seismic~p')+')'
cond_quant = csn['quantity'].str.contains('arrival')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3&cond_quant, \
        'object_id'] = '(earth_surface)@context~at_((earthquake@context~source_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3&cond_quant, 'object3']\
        .replace('wave~s','wave~seismic~s').replace('wave~p','wave~seismic~p')+\
        ')@role~main_station@role~sink_arrival)'
cond_quant = csn['quantity'].str.contains('travel')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3&cond_quant, \
        'object_id'] = '(earth_surface)@context~at_((earthquake@context~source_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3&cond_quant, 'object3']\
        .replace('wave~s','wave~seismic~s').replace('wave~p','wave~seismic~p')+\
        ')@role~main_station@role~sink_travel)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#earth_surface_land/ocean
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'].str.contains('land|ocean')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(earth_surface)@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#earth_surface_radiation~
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'].str.contains('radiation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(earth_surface)@context~sink_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
      .str.replace('~total','').str.replace('~net','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#earth_surface_station~
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'].str.contains('station')
cond_obj3 = csn['object3'].str.contains('system|seismograph')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id']= '(earth_surface)@context~on_('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2'] +'@context~part_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
cond_quant = csn['quantity'].str.contains('shaking')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.rstrip(')').str.replace('seismograph','(seismograph')+'_shaking))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'].str.contains('station')
cond_quant = csn['quantity'].str.contains('s-wave|p-wave')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '((earth_surface)@context~on_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']+\
        ')@role~sink_'+('wave~' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label'].str.split('-').str[0])\
        .replace('wave~s','wave~seismic~s').replace('wave~p','wave~seismic~p')+\
        '@role~main_'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label'].str.split('_').str[1]
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label'].str.replace('s-wave_','')\
                .str.replace('p-wave_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        ['object0','object1','object2']] = ''

cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'].str.contains('station')
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
    'object_id']='(earth_surface)@context~on_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
    'object2'] 
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(earth_surface)@context~on_('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
    'object2'] +'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,'object3']+')'
cond_quant = csn['quantity'].str.contains('filter_type')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'type_(en)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('_instrument-response\)','@context~part_(instrument@context~part_response-filter))')
cond_obj3 = csn['object3'].str.contains('data-stream')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'].str.replace('_data-stream','@context~source_data-stream')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#earth_surface_water
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(earth_surface)@medium_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#earth_surface_wind
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'wind'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(earth_surface)@context~at_wind'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#earth_surface_viewpoint(_planet)
cond_obj0 = csn['object0'] == 'earth'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'viewpoint'
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'earth_surface_viewpoint'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id'] = \
        '(earth_surface_viewpoint)@reference~at_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
cond_quant = csn['quantity'].str.contains('rise_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object_id'] = \
        '(earth_surface_viewpoint)@reference~at_('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+'_rising)'
cond_quant = csn['quantity'].str.contains('set_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object_id'] = \
        '(earth_surface_viewpoint)@reference~at_('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+'_setting)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#earthquake_hypocenter
cond_obj0 = csn['object0'] == 'earthquake'
csn.loc[ cond_obj0, 'object_id'] = 'earthquake_hypocenter'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#ecosystem
cond_obj0 = csn['object0'] == 'ecosystem'
csn.loc[ cond_obj0, 'object_id'] = 'ecosystem'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#electron
cond_obj0 = csn['object0'] == 'electron'
csn.loc[ cond_obj0,'object_id']='electron'
csn.loc[ cond_obj0,'object_cat']='root'
csn.loc[ cond_obj0,'object_pref']='matter'
csn.loc[ cond_obj0 & cond_quant, 'quantity_label'] = 'electric_charge'
csn.loc[ cond_obj0, 'object0'] = ''

#engine
cond_obj0 = csn['object0'] == 'engine'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'engine'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'object0']=''

#engine_air-to-fuell
cond_obj0 = csn['object0'] == 'engine'
cond_obj1 = csn['object1'] == 'air-to-fuel'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(engine@context~in_air)@role~numerator_(engine@context~in_fuel)@role~denominator'
csn.loc[ cond_obj0 & cond_obj1, ['object0', 'object1']] = ''

#ethane_molecule_h-c-c-h
cond_obj0 = csn['object0'] == 'ethane'
csn.loc[ cond_obj0, 'object_id'] = '(ethane_molecule)@context~part_bond~h-c-c-h'
csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#equation~...
cond_obj0 = csn['object0'].str.contains('equation')
csn.loc[ cond_obj0, 'object_id'] = \
        csn.loc[ cond_obj0, 'object0']
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#farmer_crop
cond_obj0 = csn['object0'] == 'farmer'
csn.loc[ cond_obj0, 'object_id'] = 'farmer@role~sink_crop@role~exchange'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#fence~electric
cond_obj0 = csn['object0'].str.contains('fence~electric')
csn.loc[ cond_obj0, 'object_id'] = 'fence~electric'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#fertilizer~nitrogen
cond_obj0 = csn['object0'] == 'fertilizer~nitrogen'
cond_quant = csn['quantity'].str.contains('application')
csn.loc[ cond_obj0 & cond_quant,'object_id']='fertilizer~nitrogen_application'
cond_quant = csn['quantity'].str.contains('usage')
csn.loc[ cond_obj0 & cond_quant,'object_id']=\
    '(fertilizer~nitrogen_utilization)@role~numerator_(fertilizer~nitrogen_application)@role~denominator'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#fertilizer~applied-as-nitrogen
cond_obj0 = csn['object0'].str.startswith('fertilizer')
csn.loc[ cond_obj0,'object_id']='fertilizer~applied-as-nitrogen'
csn.loc[ cond_obj0,'object_pref']='rolephenomenon'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#field
cond_obj0 = csn['object0'] == 'field'
csn.loc[ cond_obj0,'object_id']='field'
csn.loc[ cond_obj0,'object_pref']='body'
csn.loc[ cond_obj0, ['object0']] = ''

#field_residue~remaining_nitrogen_at-harvest
cond_obj0 = csn['object0'] == 'field'
cond_obj01 = csn['object1'] == 'residue~remaining'
csn.loc[ cond_obj0 & cond_obj1,'object_id']='field@context~on_(residue~remaining@context~in_nitrogen)_(crop_harvest)@reference~at'
csn.loc[ cond_obj0, ['object0']] = ''

#flood
cond_obj0 = csn['object0'] == 'flood'
csn.loc[ cond_obj0,'object_id']='flood'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#forage-or-residue~removed_at-harvest
cond_obj0 = csn['object0'] == 'forage-or-residue~removed'
cond_obj1 = csn['object1'] == 'at-harvest'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'forage-or-residue~removed_(crop_harvest)@reference~at'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#forage-or-residue~removed_nitrogen(_at-harvest)
cond_obj0 = csn['object0'] == 'forage-or-residue~removed'
cond_obj1 = csn['object1'] == 'nitrogen'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'forage-or-residue~removed@medium_nitrogen'
cond_obj2 = csn['object2'] == 'at-harvest'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(forage-or-residue~removed@medium_nitrogen)_(crop_harvest)@reference~at'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#fuel-to-oxidizer
cond_obj0 = csn['object0'] == 'fuel-to-oxidizer'
csn.loc[ cond_obj0, 'object_id'] = 'fuel@role~numerator_oxidizer@role~denominator'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#gasoline
cond_obj0 = csn['object0'] == 'gasoline'
csn.loc[ cond_obj0, 'object_id'] = 'gasoline'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#glacier
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'glacier'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#glacier_*-zone
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'].str.contains('zone')
cond_quant = csn['quantity'].str.contains('fraction')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_id'] = 'glacier_'+\
    csn.loc[ cond_obj0 & cond_obj1, 'object1']
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'glacier@medium_(glacier_'+csn.loc[ cond_obj0 & cond_obj1, 'object1']+')'  
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#glacier_bed_
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'bed'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'glacier_bed'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#glacier_bed_heat~geothermal
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'bed'
cond_obj2 = csn['object2'] == 'heat~geothermal'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = 'geothermal_heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'glacier_bed'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'glacier_bed'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#glacier_bed_surface
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'bed'
cond_obj2 = csn['object2'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'glacier_bed_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#glacier_bottom
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'glacier_bottom_sliding'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#glacier_bottom_ice(_flow)
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'ice'
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(glacier_bottom)@context~in_ice'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = ('(glacier_bottom)@context~in_(ice_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,'object3']+')').str.replace('flow','flowing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,'quantity_label'].str.replace('velocity','linear_velocity')
cond_quant = csn['quantity'].str.contains('sliding')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_sliding)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#glacier_bottom_surface(_heat)
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'surface'
cond_obj3 = csn['object3'].str.contains('heat') 
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(glacier_bottom_surface)@role~medium_conduction'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj3, \
        'object_id'] = 'glacier_bottom_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = 'conduction_heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'glacier_bottom_surface'
cond_obj3 = csn['object3'].str.contains('frictional')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id']+'~frictional'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = 'frictional_conduction_heat_energy_flux'
cond_obj3 = csn['object3'].str.contains('geothermal')  
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id']+'~geothermal'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = 'geothermal_conduction_heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#glacier_equillibrium-line/surface
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'].str.contains('line|surface')
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'glacier_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#glacier_ice
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'ice'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'glacier@context~in_ice'
cond_quant = csn['quantity'].str.contains('melting_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_melting-point)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label'].str.replace('melting_point_','melting-point_')
cond_quant = csn['quantity'].str.contains('ablation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_ablation)'
cond_quant = csn['quantity'].str.contains('accumulation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_accumulation)'
cond_quant = csn['quantity'].str.contains('melt_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_melting)'
cond_quant = csn['quantity'].str.contains('volume_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity_label'] = 'volume_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity_label'].str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity_label'] = 'shear_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity_label'].str.replace('shear_','')
cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label']\
                .str.replace('mass-specific_isobaric','isobaric_mass-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isobaric-process)'
cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label']\
            .str.replace('mass-specific_isochoric','isochoric_mass-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isochoric-process)'
cond_quant = csn['quantity'].str.contains('mass-specific_latent')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label']\
    .str.replace('mass-specific_','').str.replace('_heat','_mass-specific_heat')
cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label']\
        .str.replace('volume-specific_isobaric','isobaric_volume-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isobaric-process)'
cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label']\
    .str.replace('volume-specific_isochoric','isochoric_volume-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isochoric-process)'
cond_quant = csn['quantity'].str.contains('vaporization')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_vaporization)'
cond_quant = csn['quantity'].str.contains('fusion')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_fusion)'
cond_quant = csn['quantity'].str.contains('sublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_sublimation)'
cond_quant = csn['quantity'].str.contains('isentropic')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isentropic-process)'
cond_quant = csn['quantity'].str.contains('isothermal')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isothermal-process)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#glacier_ice~
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'].str.contains('ice~')
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(glacier@context~in_ice)_(glacier_bed)@reference~above'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'glacier_ice_above-bed'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#glacier_ice_flow
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'ice'
cond_obj2 = csn['object2'] == 'flow'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'glacier@context~in_(ice_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('total_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#glacier_ice_meltwater
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'ice'
cond_obj2 = csn['object2'] == 'meltwater'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(glacier@context~in_ice)@context~source_meltwater'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#glacier_terminus(_side~...)
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'terminus'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'glacier_terminus_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity'].str.split('_').str[0]
cond_obj2 = csn['object2'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'glacier_terminus_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#glacier_top
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'glacier_top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#glacier_top_ice
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == 'ice'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(glacier_top)@context~in_ice'
cond_quant = csn['quantity'].str.contains('desublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_desublimation)'
cond_quant = csn['quantity'].str.startswith('sublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_sublimation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']]=''

#glacier_top_ice_flow
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == 'ice'
cond_obj3 = csn['object3'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(glacier_top)@context~in_(ice_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#glacier_top_ice_heat~net
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == 'ice'
cond_obj3 = csn['object3'] == 'heat~net'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(glacier_top)@context~in_(ice@role~medium)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = 'heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'glacier_top_ice'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#glacier_top_ice_wind
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == 'ice'
cond_obj3 = csn['object3'] == 'wind'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '((glacier_top)@context~in_ice)@role~main_wind@role~in_scour'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#glacier_top_surface
cond_obj0 = csn['object0'] == 'glacier'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == 'surface'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'glacier_top_surface'
cond_obj3 = csn['object3'].str.contains('heat')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(glacier_top_surface)@role~medium'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'glacier_top_surface'
cond_obj3 = csn['object3'].str.contains('incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(glacier_top_surface)@context~sink'
cond_obj3 = csn['object3'].str.contains('outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(glacier_top_surface)@context~source'
cond_obj3 = csn['object3'].str.contains('radiation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id'] + '_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
cond_obj3 = csn['object3'].str.contains('latent')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'quantity_label'] = 'latent_heat_energy_flux'
cond_obj3 = csn['object3'].str.contains('sensible')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'quantity_label'] = 'sensible_heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#gm_hummer
cond_obj0 = csn['object0'] == 'gm'
csn.loc[ cond_obj0, 'object_id'] = 'gm-hummer'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#graph~tree~rooted
cond_obj0 = csn['object0'] == 'graph~tree~rooted'
csn.loc[ cond_obj0, 'object_id'] = 'graph~tree~rooted'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'object0'] = ''

#grain~dry
cond_obj0 = csn['object0'] == 'grain~dry'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'grain~dry'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object0'] = ''

#grain
cond_obj0 = csn['object0'] == 'grain'
cond_obj1 = csn['object1'] == 'nitrogen'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(grain@context~in_nitrogen)_(crop_harvest)@reference~at'
csn.loc[ cond_obj0, 'object0'] = ''

#ground~above_biomass~harvested_grain__mass_fraction
#ground~above_crop_biomass~dry__mass-per-area_density
#ground~above_crop_nitrogen__mass-per-area_density
#ground~above_crop_nitrogen__mass-per-mass_concentration
#ground~above_crop_residue~retained__mass-per-area_density
#ground~above_crop_residue-as-carbon__decomposition_mass
#ground~above_crop_roots-and-rhizodeposits-as-carbon
#ground~above_crop_residue_pool_carbon
#ground~above_residue~remaining_at-harvest__mass-per-area_density
#ground~above_soil_residue_pool_crop_residue__mass-per-area_addition_density
cond_obj0 = csn['object0'] == 'ground~above'
cond_obj1 = csn['object1'] == 'biomass~harvested'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'ground@context~above_(biomass~harvested@medium_grain)'
cond_obj1 = csn['object1'] == 'crop'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'ground@context~above_(crop_biomass~dry)'
cond_obj2 = csn['object2'] == 'nitrogen'
cond_quant = csn['quantity'].str.contains('density')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object_id'] = 'ground@context~above_(crop@context~in_nitrogen)'
cond_quant = csn['quantity'].str.contains('fraction')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object_id'] = 'ground@context~above_(crop@medium_nitrogen)'
cond_obj2 = csn['object2'] == 'residue~retained'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'ground@context~above_crop@context~source_residue~retained'
cond_obj2 = csn['object2'] == 'residue-as-carbon'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'ground@context~above_(crop@context~source_(residue-as-carbon_decomposition))'
cond_obj2 = csn['object2'] == 'roots-and-rhizodeposits-as-carbon'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'ground@context~above_(crop@context~source_(roots-and-rhizodeposits-as-carbon_decomposition))'
cond_obj2 = csn['object2'] == 'residue'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'ground@context~above_(crop_residue_pool_decomposition)@context~source_carbon'
cond_obj1 = csn['object1'] == 'residue~remaining'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(ground@context~above_residue~remaining)_(crop_harvest)@reference~at'
cond_obj1 = csn['object1'] == 'soil'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'ground@context~above_((soil@context~in_(residue_pool))@role~sink_(crop@context~source_residue)@role~main_addition)'
csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#groundwater
cond_obj0 = csn['object0'] == 'groundwater'
csn.loc[ cond_obj0, 'object_id'] = '(land_surface)@context~below_ground@context~in_water'
csn.loc[ cond_obj0, 'object0'] = ''

#human
cond_obj0 = csn['object0'] == 'human'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1,'object_id']='human'
cond_quant = csn['quantity'].str.contains('hearing')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'human_hearing'
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_pref']='body'
csn.loc[ cond_obj0 & cond_obj1,'object0'] = ''

#human_alcohol
cond_obj0 = csn['object0'] == 'human'
cond_obj1 = csn['object1'] == 'alcohol'
csn.loc[ cond_obj0 & cond_obj1,'object_id'] = 'human@role~sink_alcohol@role~main_consumption'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#human_blood_cell~...
cond_obj0 = csn['object0'] == 'human'
cond_obj1 = csn['object1'] == 'blood'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = \
    'human@context~part_(blood@medium_'+csn.loc[ cond_obj0 & cond_obj1, 'object2']\
    .str.replace('cell~platelet','platelet').str.replace('cell~white','white-blood-cell')\
    .str.replace('cell~red','red-blood-cell')+')'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#human_eye_photon
cond_obj0 = csn['object0'] == 'human'
cond_obj1 = csn['object1'] == 'eye'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(human@context~part_eye)@role~main_photon@role~in_detection'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#human_hair
cond_obj0 = csn['object0'] == 'human'
cond_obj1 = csn['object1'] == 'hair'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'human@context~part_hair'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#human_life
cond_obj0 = csn['object0'] == 'human'
cond_obj1 = csn['object1'] == 'life'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'human_life'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#hydrogen_oxygen__bond
cond_obj0 = csn['object0'] == 'hydrogen'
csn.loc[ cond_obj0, 'object_id'] = 'bond~h-o'
csn.loc[ cond_obj0, 'object_label'] = 'bond~h-o'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'quantity_label'] = 'energy'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#ice
cond_obj0 = csn['object0'] == 'ice'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'].str.contains('heat')
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'ice'
cond_quant = csn['quantity'].str.contains('melting')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
         'object_id'] = 'ice_melting-point'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
         'object_pref'] = 'matter'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
         'quantity_label'] = 'melting-point_temperature'
cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label']\
        .str.replace('mass-specific_isobaric','isobaric_mass-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
         'object_id'] = 'ice_isobaric-process'
cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label']\
        .str.replace('mass-specific_isochoric','isochoric_mass-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
         'object_id'] = 'ice_isochoric-process'
cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
                'quantity_label']\
                .str.replace('volume-specific_isobaric','isobaric_volume-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
         'object_id'] = 'ice_isobaric-process'
cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label']\
        .str.replace('volume-specific_isochoric','isochoric_volume-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
         'object_id'] = 'ice_isochoric-process'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#image
cond_obj0 = csn['object0'] == 'image'
csn.loc[ cond_obj0, 'object_id'] = 'image'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#impact-crater
cond_obj0 = csn['object0'] == 'impact-crater'
csn.loc[ cond_obj0, 'object_id'] = 'impaction@context~source_(crater_'+\
    csn.loc[ cond_obj0, 'object1']+')'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#iron
cond_obj0 = csn['object0'] == 'iron'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'iron'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'matter'
cond_quant = csn['quantity'].str.contains('melting')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'iron_melting-point'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'matter'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'melting-point_temperature'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#iron_atom_...
cond_obj0 = csn['object0'] == 'iron'
csn.loc[ cond_obj0, 'object_id'] = '(iron_atom)@context~part_'+\
    csn.loc[ cond_obj0, 'object2'] 
csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#lake
cond_obj0 = csn['object0'] == 'lake'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'lake'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#lake_surface
cond_obj0 = csn['object0'] == 'lake'
cond_obj1 = csn['object1'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'lake_surface'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#lake_water_fish
cond_obj0 = csn['object0'] == 'lake'
cond_obj1 = csn['object1'] == 'water'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'lake@context~in_(fish_sample)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2','object3']] = ''

#lake_water~
cond_obj0 = csn['object0'] == 'lake'
cond_obj1 = csn['object1'].str.contains('water~incoming')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'lake@role~sink_(water_flowing~incoming)@role~main'
cond_obj1 = csn['object1'].str.contains('water~outgoing')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'lake@role~source_(water_flowing~outgoing)@role~main'
cond_obj1 = csn['object1'].str.contains('water~')
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#land
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(crop_rotation)@reference~at_(land_tillage)'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#land_crop
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'crop'
cond_quant = csn['quantity'].str.contains('yield|production')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'land@medium_(crop_production)'
cond_quant = csn['quantity'].str.contains('allocated')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = '(land_allocation)@medium_crop'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#land_domain_boundary
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'domain'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'land@context~part_(domain_boundary_lowering)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#land_fertilizer~nitrogen
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'fertilizer~nitrogen'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'land@role~in_fertilizer~nitrogen@role~main_application'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#land_soil~dry_surface
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'soil~dry'
cond_obj2 = csn['object2'] == 'surface'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id'] = 'land_soil~dry_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#land_subsurface_water
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'subsurface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id'] = '(land_subsurface)@context~source_(water_runoff)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#land_subsurface_water_sat-zone_top
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'subsurface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'sat-zone'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id'] = 'land_subsurface_sat-zone_top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_label'] = 'land_subsurface_sat-zone_top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#land_subsurface_aquifer~left/right_channel~river_bed_water
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'subsurface'
cond_obj2 = csn['object2'].str.contains('aquifer')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
    '(land_subsurface)@context~at_'+ csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+\
    '@context~source_(channel~river_bed)@context~sink_(water_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#land_subsurface_sat-zone_top
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'subsurface'
cond_obj2 = csn['object2'] == 'sat-zone'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'land_subsurface_sat-zone_top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_label'] = 'land_subsurface_sat-zone_top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3','object4']] = ''

#land_surface
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == ''
cond_quant = csn['quantity'].str.contains('infiltration|sunshine')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
        'object_id'] = 'land_surface'
cond_quant = csn['quantity'].str.contains('infiltration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(land_surface)@medium_infiltration'
cond_quant = csn['quantity'].str.contains('sunshine')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(land_surface)@context~at_sunshine'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label'] = 'land_surface_sunshine'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'duration'
cond_quant = csn['quantity'].str.contains('plan|profile|streamline')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity'].str.split('_').str[0]
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label']+'_'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity'].str.split('_').str[0]
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'curvature'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#land_surface_contour/polygon/base-level/transect
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2']\
        .str.contains('contour|polygon|base-level|transect')
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'land_surface_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id']+\
        '_'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'].str.replace('total_contributing','contributing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#land_surface_air_radiation~
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'].str.contains('radiation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(land_surface)@context~at_air@context~in_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''
        

#land_surface_air_heat
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'].str.contains('surface')
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = ('(land_'+\
         csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']+\
         '_air').str.replace('surface','surface)@context~above').str.replace('10m-above','10m')
cond_obj3 = csn['object3'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = ('(land_'+\
         csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object1']+\
         '_(air_flowing)').str.replace('surface','surface)@context~above').str.replace('10m-above','10m')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
                     'quantity_label'].str.replace('velocity','linear_velocity')
cond_obj1 = csn['object1'].str.contains('surface')
cond_obj3 = csn['object3'].str.contains('heat')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'land_surface_air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
        .str.split('~').str[-1]+'_heat_energy_flux'
cond_obj3 = csn['object3'].str.contains('heat~incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(land_surface)@role~source_air@role~sink'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = 'incoming_' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
        .str.split('~').str[-1]+'_heat_energy_flux'
cond_obj3 = csn['object3'].str.contains('heat~net')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(land_surface)@role~exchange_air@role~exchange'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#land_surface_energy~...
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'].str.contains('energy')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(land_surface)@role~medium'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'land_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#land_surface~..._soil_water
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'].str.contains('surface~')
cond_obj2 = csn['object2'] == 'soil'
cond_obj3 = csn['object3'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(land_surface)@context~'+ \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object1'].str.split('~').str[1]+'_(soil@medium_water)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#land_surface~..._soil
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'].str.contains('surface~')
cond_obj2 = csn['object2'] == 'soil'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(land_surface)@context~'+ \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object1'].str.split('~').str[1]+'_soil'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#land_surface~..._air
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'].str.contains('surface~')
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(land_surface)@context~'+ \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object1'].str.split('~').str[1]+'_air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#land_surface_radiation~...
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'].str.contains('radiation')
cond_quant = csn['quantity'].str.endswith('ance')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(land_surface)@role~main'
cond_obj2 = csn['object2'].str.contains('outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
        +'@role~out'
cond_obj2 = csn['object2'].str.contains('incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
        .str.replace('~total','')+'@role~in'
cond_quant = csn['quantity'].str.endswith('flux')
cond_obj2 = csn['object2'].str.contains('outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(land_surface)@role~source'
cond_obj2 = csn['object2'].str.contains('incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(land_surface)@role~sink'
cond_obj2 = csn['object2'].str.contains('net')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(land_surface)@role~exchange'
cond_obj2 = csn['object2'].str.contains('radiation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
        .str.replace('~total','').str.replace('~net','')+'@role~main'
cond_obj2 = csn['object2'] == 'radiation~shortwave~downward'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(land_surface)@context~at_radiation~shortwave~downward'
cond_obj2 = csn['object2'] == 'radiation~solar'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(land_surface)@context~at_radiation~solar'
cond_obj2 = csn['object2'].str.contains('radiation')
cond_quant = csn['quantity'].str.contains('diffuse')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('shortwave','shortwave~diffuse')
cond_quant = csn['quantity'].str.contains('direct')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('shortwave','shortwave~direct')
cond_quant = csn['quantity'].str.contains('emit')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_emission'
cond_quant = csn['quantity'].str.contains('refl')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_reflection'
cond_quant = csn['quantity'].str.contains('absor')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_absorption'
cond_quant = csn['quantity'].str.contains('transmit')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_transmission'
cond_quant = csn['quantity'].str.contains('back')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_backscatter'
cond_quant = ~csn['quantity'].str.contains('transmit|absor|backscat|emit|refl')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('@role~','@context~').str.replace('@context~main','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#land_surface~horizontal_radiation~incoming~shortwave
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'].str.contains('surface~')
cond_obj2 = csn['object2'].str.contains('radiation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(land_'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object1']+')@context~sink_'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2','object3']] = ''

#land_surface_soil
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'soil'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(land_surface)@context~in_(soil@role~medium_conduction)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'land_surface_soil'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = 'conduction_heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#land-or-sea_surface_radiation~...
cond_obj0 = csn['object0'] == 'land-or-sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'].str.contains('radiation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(land_surface)@context~optional~sink_(sea_surface)@context~optional~sink_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#land_surface_snow
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'snow'
cond_quant = csn['quantity'].str.contains('accumulation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(land_surface)@context~on_(snow_accumulation)'
cond_quant = csn['quantity'].str.contains('sublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(land_surface)@context~on_(snow_sublimation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#land_surface_terrain~left/right_channel~stream_reach_water
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'].str.contains('terrain')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(land_surface)@context~on_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object2'] + '@context~source_(channel~stream@context~part_reach)@context~sink_'+\
                '(water_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#land_surface_water
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == ''
cond_quant = csn['quantity'].str.contains('infiltration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
        'object_id'] = '(land_surface)@context~on_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(land_surface)@medium_infiltration_(water_ponding)'
cond_quant = csn['quantity'].str.contains('runoff')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('water','(water')+'_runoff)'
cond_quant = csn['quantity'].str.contains('evaporation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(land_surface)@context~source_(water_evaporation)'
cond_quant = csn['quantity'].str.contains('evapotranspiration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(land_surface)@context~source_(water_evapotranspiration)'
cond_quant = csn['quantity'].str.contains('baseflow')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('water','(water')+'_baseflow)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#land_surface_water_flow
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(land_surface)@context~on_(water_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#land_surface_water_sink/source
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'].str.contains('sink|source')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(land_surface)@context~on_((water_flowing)@role~main_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+\
        '@role~'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#land_surface_water_surface
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(land_surface)@context~on_(water_surface)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#land_surface_wind
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'wind'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
    '(land_surface)@context~above_wind'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#land_vegetation 
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'vegetation'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
    '(land_surface)@context~on_(vegetation@context~part'
cond_quant = csn['quantity'].str.contains('leaf')
csn.loc[cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
    'object_id']=csn.loc[cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
    'object_id']+'_leaf)'
cond_quant = csn['quantity'].str.contains('stomata')
csn.loc[cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
    'object_id']=csn.loc[cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
    'object_id']+'_stomata)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#land_vegetation_canopy
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'vegetation'
cond_obj2 = csn['object2'] == 'canopy'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'land@medium_(vegetation_canopy)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#land_vegetation_canopy_water
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'vegetation'
cond_obj2 = csn['object2'] == 'canopy'
cond_quant = csn['quantity'].str.contains('interception_capacity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'land@context~on_((vegetation_canopy)@role~main_water@role~in_interception)'
cond_quant = csn['quantity'].str.contains('interception_volume')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'land@context~on_((vegetation_canopy)@role~sink_water@role~main_interception)'
cond_quant = csn['quantity'].str.contains('evaporation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'land@context~on_((vegetation_canopy)@context~source_(water_evaporation))'
cond_quant = csn['quantity'].str.contains('interception_storage')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'land@context~on_((vegetation_canopy)@role~main_water@role~in_interception)'
cond_quant = csn['quantity'].str.contains('throughfall')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'land@context~on_((vegetation_canopy)@medium_throughfall_water)'
cond_quant = csn['quantity'].str.contains('transpiration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'land@context~on_((vegetation_canopy)@role~source_water@role~main_transpiration)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#land_vegetation_floor_water
cond_obj0 = csn['object0'] == 'land'
cond_obj1 = csn['object1'] == 'vegetation'
cond_obj2 = csn['object2'] == 'floor'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(land~vegetated_floor)@role~sink_water@role~main_interception'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#light-bulb~incandescent
cond_obj0 = csn['object0'] == 'light-bulb~incandescent'
csn.loc[ cond_obj0, 'object_id'] = 'light-bulb~incandescent'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#lithosphere
cond_obj0 = csn['object0'] == 'lithosphere'
csn.loc[ cond_obj0, 'object_id'] = 'lithosphere'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object0'] = ''

#location
cond_obj0 = csn['object0'] == 'location'
csn.loc[ cond_obj0, 'object_id'] = 'location'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#magnesium-chloride_water
cond_obj0 = csn['object0'] == 'magnesium-chloride'
csn.loc[ cond_obj0, 'object_id'] = 'magnesium-chloride@role~first_water@role~second'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#math
cond_obj0 = csn['object0'] == 'math'
csn.loc[ cond_obj0, 'object_id'] = 'math'
csn.loc[ cond_obj0, 'quantity_label'] = \
        csn.loc[ cond_obj0, 'quantity_label']\
        .str.replace('twin_prime','twin-prime')
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#model
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'model'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#model_grid
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'model@context~in_grid'
cond_quant = csn['quantity'].str.contains('average_node')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('grid','(grid')+'_node)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label']+'_node'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity_label'] = \
                        'average_separation_distance'
cond_quant = csn['quantity'].str.contains('cell|column|row|shell')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('grid','(grid')+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
            'quantity_label'].str.split('_').str[0]+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
            'quantity_label'].str.split('_').str[0]
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'count'
cond_quant = csn['quantity'].str.contains('dual|primary')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('grid','(grid')+\
        '_node~' + csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                          'quantity_label'].str.split('_').str[0]+'~'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
            'quantity_label'].str.split('_').str[2]+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label'].str.replace('grid','(grid')+\
        '_node~' + csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                          'quantity_label'].str.split('_').str[0]+'~'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
            'quantity_label'].str.split('_').str[2]+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'count'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#model_grid_axis...
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'] == 'axis~x'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(model@context~in_(grid_axis~x))@role~first_(model@context~in_axis~east)@role~second'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#model_grid_cell
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'] == 'cell'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'model@context~in_(grid_cell)'
cond_quant = csn['quantity'].str.contains('column|row')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.rstrip(')')+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity'].str.split('_').str[0]+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity'].str.split('_').str[0]
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'index'
cond_quant = csn['quantity'].str.contains('surface')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = 'model@context~in_(grid_cell_surface)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'model_grid_cell_surface'
cond_quant = csn['quantity'].str.contains('flow')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.replace('\(grid','((grid')+'@context~in_(water_flowing))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'].str.replace('total_contributing','contributing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#model_grid_cell_center/centroid
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'] == 'cell'
cond_obj3 = csn['object3'].str.contains('center|centroid')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'model@context~in_(grid_cell_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
cond_quant = csn['quantity'].str.contains('velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, 'object_id']\
        .str.replace('\(','((')+\
        '@context~in)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#model_grid_cell_edge/face(_center/centroid)
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'] == 'cell'
cond_obj3 = csn['object3'].str.contains('edge|face')
cond_obj4 = csn['object4'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
         'object_id'] = 'model@context~in_(grid_cell_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
         'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object_id']\
        .str.rstrip(')')+\
        '_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object4']+')'
cond_quant = csn['quantity'].str.contains('velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, 'object_id']\
        .str.replace('\(','((')+\
        '@context~in)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
                'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
         ['object0','object1','object2','object3','object4']] = ''

#model_grid_cell~...
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'].str.contains('cell')
cond_obj3 = csn['object3']=='water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'model@context~in_((grid_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']+')@context~in_water)'
cond_obj3 = csn['object3'].str.contains('water~incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'model@context~in_((grid_cell)@role~sink_(water_flowing~incoming)@role~main)'
cond_obj3 = csn['object3'].str.contains('water~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'model@context~in_((grid_cell)@role~source_(water_flowing~outgoing)@role~main)'
cond_obj3 = csn['object3'].str.contains('water')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
                'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']]= ''

#model_grid_cell        
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'].str.contains('cell')
cond_obj3 = csn['object3'] != ''
cond_obj4 = csn['object4'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'model@context~in_(grid_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'].str.rstrip(')')+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
        'object_id'].str.rstrip(')')+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, 'object4']+')'
cond_quant = csn['quantity'].str.contains('row_|column_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.rstrip(')')+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label'].str.split('_').str[0]+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label'].str.split('_').str[0]
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'index'
cond_quant = csn['quantity'].str.contains('surface')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.rstrip(')')+'_surface)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_label']+'_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'area'
cond_quant = csn['quantity'].str.contains('flow')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('\(grid','((grid')+'@context~in_(water_flowing))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'].str.replace('total_contributing','contributing')
cond_quant = csn['quantity'].str.contains('velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('\(grid','((grid')+'@context~in)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3','object4']] = ''

#model_grid_column/row
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'].str.contains('column|row')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'model@context~in_(grid_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1',
                                            'object2']] = ''

#model_grid_edge~.
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'].str.contains('edge')
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'model@context~in_(grid_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#model_grid_edge~_sea_water
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'].str.contains('edge')
cond_obj3 = csn['object3'] == 'sea'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'model@context~in_((grid_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']+\
        ')@context~in_(sea@context~in_water))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''

#model_grid_node~
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'].str.contains('node')
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'model@context~in_(grid_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']+')'
cond_quant = csn['quantity'].str.contains('velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('\(grid','((grid')+'@context~in)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#model_grid_virtual~
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'].str.contains('virtual')
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'model@context~in_(grid@context~in_(earth_pole~north~virtual))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#model_grid_shell...
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'grid'
cond_obj2 = csn['object2'].str.contains('shell')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'model@context~in_((grid_shell)_(grid_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']+\
        ')@reference~'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
        .str.split('-').str[1]+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#model_soil_layer~
cond_obj0 = csn['object0'] == 'model'
cond_obj1 = csn['object1'] == 'soil'
cond_obj2 = csn['object2'].str.contains('layer')
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'model@context~in_(soil_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']+')'
cond_quant = csn['quantity'].str.contains('porosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.rstrip(')').str.replace('soil','(soil')+')@medium)'
cond_quant = csn['quantity'].str.contains('saturated')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.rstrip(')')+'_saturated)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#mars
cond_obj0 = csn['object0'] == 'mars'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'] == 'standard_gravity_constant'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'standard_gravitational_acceleration'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'mars'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
cond_quant = csn['quantity'].str.contains('local')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
        'location@reference~at_(mars_rising)'
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#mars_atmosphere/moon
cond_obj0 = csn['object0'] == 'mars'
cond_obj1 = csn['object1'].str.contains('atmosphere')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'mars@context~surrounding'
cond_obj1 = csn['object1'].str.contains('moon')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'mars@context~orbitting'
cond_obj1 = csn['object1'].str.contains('atmosphere|moon')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'object_id']+'_'+\
    csn.loc[ cond_obj0 & cond_obj1, 'object1']
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#mars_axis/ellipsoid
cond_obj0 = csn['object0'] == 'mars'
cond_obj1 = csn['object1'].str.contains('axis|ellipsoid')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'mars_'+\
    csn.loc[ cond_obj0 & cond_obj1, 'object1']
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#mars_orbit
cond_obj0 = csn['object0'] == 'mars'
cond_obj1 = csn['object1'] == 'orbit'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'mars_orbit'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#mars_surface_viewpoint_venus
cond_obj0 = csn['object0'] == 'mars'
cond_obj1 = csn['object1'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = \
        '(mars_surface_viewpoint)@reference~at_venus'
cond_quant = csn['quantity'].str.contains('rise')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id']\
        .str.replace('venus','(venus')+'_rising)'
cond_quant = csn['quantity'].str.contains('set')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id']\
        .str.replace('venus','(venus')+'_setting)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2','object3']] = ''

#mercury_axis
cond_obj0 = csn['object0'] == 'mercury'
csn.loc[ cond_obj0, 'object_id'] = 'mercury_axis_precession'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#nitrogen
cond_obj0 = csn['object0'] == 'nitrogen'
cond_quant = csn['quantity'].str.contains('mineralization')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = 'nitrogen_mineralization'
cond_quant = csn['quantity'].str.contains('immobilization')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = 'nitrogen_immobilization'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#oscillator
cond_obj0 = csn['object0'] == 'oscillator'
csn.loc[ cond_obj0, 'object_id'] = 'oscillator'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#ozone_molecule
cond_obj0 = csn['object0'] == 'ozone'
csn.loc[ cond_obj0, 'object_id'] = '(ozone_molecule)@context~part_bond~o-o'
csn.loc[ cond_obj0, 'quantity_label'] = 'length'
csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#paper
cond_obj0 = csn['object0'] == 'paper'
csn.loc[ cond_obj0, 'object_id'] = 'paper'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#pavement_rubber
cond_obj0 = csn['object0'] == 'pavement'
csn.loc[ cond_obj0, 'object_id'] = 'pavement@role~exchange_rubber@role~exchange_friction'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#peano-curve
cond_obj0 = csn['object0'] == 'peano-curve'
csn.loc[ cond_obj0, 'object_id'] = 'peano-curve'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#physics
cond_obj0 = csn['object0'] == 'physics'
csn.loc[ cond_obj0, 'object_id'] = 'physics'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
cond_quant = csn['quantity'].str.contains('vacuum_electrical')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = 'physics@context~in_(vacuum@context~in_radiation~electromagnetic)'
csn.loc[ cond_obj0 & cond_quant, \
        'quantity_label'] = 'electrical_impedance_constant'
csn.loc[ cond_obj0 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('vacuum_light')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = 'physics@context~in_(vacuum@context~in_radiation~electromagnetic)'
csn.loc[ cond_obj0 & cond_quant, \
        'quantity_label'] = 'speed_constant'
csn.loc[ cond_obj0 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('vacuum_magnetic')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = 'physics@context~in_vacuum'
csn.loc[ cond_obj0 & cond_quant, \
        'quantity_label'] = 'magnetic_permeability_constant'
csn.loc[ cond_obj0 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('vacuum_permittivity')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = 'physics@context~in_vacuum'
csn.loc[ cond_obj0 & cond_quant, \
        'quantity_label'] = 'permittivity_constant'
csn.loc[ cond_obj0 & cond_quant, \
        'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0, 'quantity_label' ] = \
        csn.loc[ cond_obj0, 'quantity_label' ]\
        .str.replace('atomic_mass','atomic-mass')\
        .str.replace('bohr_radius','bohr-radius')\
        .str.replace('elementary_electric','elementary-electric')\
        .str.replace('universal_gravitation','universal-gravitation')
csn.loc[ cond_obj0, 'object0'] = ''

#pipe_water_flow
cond_obj0 = csn['object0'] == 'pipe'
csn.loc[ cond_obj0, 'object_id'] = 'pipe@context~in_((water_flowing)@role~exchange_friction)'
csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#plant_at-grain-or-forage-harvest-or-death
cond_obj0 = csn['object0'] == 'plant'
cond_obj1 = csn['object1'] == 'at-grain-or-forage-harvest-or-death'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'plant_(grain_harvest)@reference~at_(grain_death)@reference~at_(forage_harvest)@reference~at_(forage_death)@reference~at'
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#plant_root_at-grain-or-forage-harvest-or-death
cond_obj0 = csn['object0'] == 'plant'
cond_obj1 = csn['object1'] == 'root'
cond_obj2 = csn['object2'] == 'at-grain-or-forage-harvest-or-death'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(plant@context~part_root)_(grain_harvest)@reference~at_(grain_death)@reference~at_(forage_harvest)@reference~at_(forage_death)@reference~at'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#plants~living_water
cond_obj0 = csn['object0'] == 'plants~living'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'plants~living@role~source_water@role~main_evaporation'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''
        
#polynomial
cond_obj0 = csn['object0'] == 'polynomial'
csn.loc[ cond_obj0, 'object_id'] = 'polynomial'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0']=''

#polymer
cond_obj0 = csn['object0'] == 'polymer'
csn.loc[ cond_obj0, 'object_id'] = 'polymer'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0']=''

#porsche~911
cond_obj0 = csn['object0'] == 'porsche~911'
cond_quant = csn['quantity'].str.contains('price')
csn.loc[ cond_obj0, 'object_id'] = 'porsche~911'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_quant, 'quantity_label'] = 'msrp_price'
csn.loc[ cond_obj0, 'object0'] = ''

#projectile
cond_obj0 = csn['object0'] == 'projectile'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'projectile'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_pref'] = 'rolephenomenon'
cond_quant = csn['quantity'].str.contains('acceleration')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_acceleration'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('drag_')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_dragging'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('lift_')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_lift'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('firing')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_firing'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('flight')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_flight'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('impact')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_impaction'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('roll_rotation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_rolling_rotation'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('_plus_')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
    'sum_of_kinetic_energy_and_potential_energy'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1, 'quantity_label']\
    .str.replace('of_velocity','of_linear_velocity')
cond_quant = csn['quantity']=='velocity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_id'] = \
    'linear_velocity'
cond_quant = csn['quantity']=='momentum'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_id'] = \
    'linear_momentum'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#projectile_impact-crater
cond_obj0 = csn['object0'] == 'projectile'
cond_obj1 = csn['object1'] == 'impact-crater'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(projectile_impaction)@context~source_crater'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#projectile_origin
cond_obj0 = csn['object0'] == 'projectile'
cond_obj1 = csn['object1'] == 'origin'
cond_obj2 = csn['object2'] == ''
cond_quant = csn['quantity'].str.contains('velocity|speed|acceleration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object_id'] = \
        '(projectile_trajectory_origin)@context~at_projectile'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, 'object_id'] = \
        'projectile_trajectory_origin'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#projectile_origin_land_surface
cond_obj0 = csn['object0'] == 'projectile'
cond_obj1 = csn['object1'] == 'origin'
cond_obj2 = csn['object2'] == 'land'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(projectile_trajectory_origin)@context~at_(land_surface)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#projectile_origin_wind
cond_obj0 = csn['object0'] == 'projectile'
cond_obj1 = csn['object1'] == 'origin'
cond_obj2 = csn['object2'] == 'wind'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(projectile_trajectory_origin)@context~at_wind'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#projectile_shaft(_x-section)
cond_obj0 = csn['object0'] == 'projectile'
cond_obj1 = csn['object1'] == 'shaft'
cond_obj2 = csn['object2'] != ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'projectile_shaft'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'projectile_shaft_x-section'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#projectile_target
cond_obj0 = csn['object0'] == 'projectile'
cond_obj1 = csn['object1'] == 'target'
cond_obj2 = csn['object2'] == ''
cond_quant = csn['quantity'].str.contains('velocity|speed|acceleration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object_id'] = \
        '(projectile_trajectory_target)@reference~at_projectile'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, 'object_id'] = \
        'projectile_trajectory_target'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#projectile_target_land_surface
cond_obj0 = csn['object0'] == 'projectile'
cond_obj1 = csn['object1'] == 'target'
cond_obj2 = csn['object2'] == 'land'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(projectile_trajectory_target)@context~at_(land_surface)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2','object3']] = ''

#projectile_trajectory
cond_obj0 = csn['object0'] == 'projectile'
cond_obj1 = csn['object1'] == 'trajectory'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'projectile_trajectory'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#projectile_x-section
cond_obj0 = csn['object0'] == 'projectile'
cond_obj1 = csn['object1'] == 'x-section'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'projectile_x-section'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#pump
cond_obj0 = csn['object0'] == 'pump'
csn.loc[ cond_obj0, 'object_id'] = 'pump'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#radiation~solar
cond_obj0 = csn['object0'] == 'radiation~solar'
csn.loc[ cond_obj0, 'object_id'] = 'radiation~solar'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#railway_curve
cond_obj0 = csn['object0'] == 'railway'
csn.loc[ cond_obj0, 'object_id'] = 'railway_curve'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#region_state_land~
cond_obj0 = csn['object0'] == 'region'
csn.loc[ cond_obj0,'object_id'] = 'region~state@medium_'+\
    csn.loc[ cond_obj0,'object2'].str.replace('land~grassland','grassland')\
    .str.replace('land~parkland','parkland')
cond_quant = csn['quantity'].str.contains('depth')
csn.loc[ cond_obj0 & cond_quant,'object_id'] = 'region~state@context~part_(land~flooded@context~on_water)'
csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#rocket_payload
cond_obj0 = csn['object0'] == 'rocket'
cond_obj1 = csn['object1'] == 'payload'
cond_quant = csn['quantity'].str.contains('ratio')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_id'] = 'rocket@medium_payload'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'rocket@role~numerator_payload@role~denominator'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#rocket_propellant
cond_obj0 = csn['object0'] == 'rocket'
cond_obj1 = csn['object1'] == 'propellant'
cond_quant = csn['quantity'].str.contains('ratio')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_id'] = 'rocket@medium_propellant'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'rocket@role~numerator_propellant@role~denominator'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#roots-and-rhizodeposits
cond_obj0 = csn['object0'] == 'roots-and-rhizodeposits'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'roots-and-rhizodeposits_production'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#sea_bottom_radiation~..
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'].str.contains('radiation~incoming')
cond_quant = csn['quantity'].str.endswith('flux')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(sea_bottom)@role~sink'
cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']='(sea_bottom)@role~source'
cond_obj2 = csn['object2'].str.contains('radiation')
cond_quant = csn['quantity']=='energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(sea_bottom)@context~at'
cond_quant = csn['quantity'].str.endswith('flux')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
        'object_id']=csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
        'object_id']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
        .str.replace('~total','')+'@role~main'
cond_quant = csn['quantity']=='energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
        'object_id']=csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
        'object_id'].str.replace('@role~main','')
cond_quant = csn['quantity'].str.endswith('ance')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']='(sea_bottom)@role~main_'
cond_obj2 = csn['object2'].str.contains('radiation~incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
        .str.replace('~total','')+'@role~in'
cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']+'@role~out'
cond_obj2 = csn['object2'].str.contains('radiation')
cond_quant = csn['quantity'].str.contains('absor')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_absorption'
cond_quant = csn['quantity'].str.contains('refl')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_reflection'
cond_quant = csn['quantity'].str.contains('emit')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_emission'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,\
        ['object0','object1','object2']] = ''

#sea_bottom_sediment
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'sediment'
cond_obj3 = csn['object3'] == ''
cond_quant = csn['quantity'].str.contains('porosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
        'object_id'] = '(sea_bottom)@context~on_sediment'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(sea_bottom)@context~on_(sediment@medium_void)'
cond_quant = csn['quantity'].str.contains('deposition')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(sea_bottom)@context~on_(sediment_deposition)'
cond_quant = csn['quantity'].str.contains('porosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(sea_bottom)@context~on_(sediment@medium)'
cond_quant = csn['quantity'].str.contains('immersed')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(sea_bottom)@context~at_(water@role~medium_immersed_sediment@role~main)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_label'] = 'sea_bottom_sediment~immersed'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'weight'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#sea_bottom_sediment_bulk/layer/particle
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'sediment'
cond_obj3 = csn['object3'].str.contains('bulk|layer|particle|grain')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_bottom)@context~on_(sediment_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#sea_bottom_sediment_*
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'sediment'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(sea_bottom)@context~on_(sediment@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object3']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#sea_bottom_surface
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'surface'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = 'sea_bottom_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#sea_bottom_surface_heat~net
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'surface'
cond_obj3 = csn['object3'] == 'heat~net'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_bottom_surface)@role~medium'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = 'heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'sea_bottom_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#sea_bottom_surface_water
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'surface'
cond_obj3 = csn['object3'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_bottom_surface)@context~at_(water_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4']] = ''
        
#sea_bottom_water
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == ''
cond_quant = csn['quantity'].str.contains('salinity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
        'object_id'] = '(sea_bottom)@context~at_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant,\
        'object_id'] = '(sea_bottom)@context~at_(water@medium)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,\
        ['object0','object1','object2']] = ''

#sea_bottom_water_heat~net
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'heat~net'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_bottom)@context~at_(water@role~medium)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'sea_bottom_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'quantity_label'] = 'heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#sea_bottom_water_debris_flow
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'debris'
cond_obj4 = csn['object4'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(sea_bottom)@context~at_((water_flowing)@context~in_debris)'
cond_obj5 = csn['object5'].str.contains('layer|top')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj5, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4 & cond_obj5, \
        'object_id'].str.replace('debris\)','(debris')+'_'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & \
                          cond_obj3 & cond_obj4 & cond_obj5, 'object5']+'))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#sea_bottom_water_debris_deposit
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bottom'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'debris'
cond_obj4 = csn['object4'] == 'deposit'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = '(sea_bottom)@context~at_(water@context~in_(debris_deposit))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        ['object0','object1','object2','object3','object4']] = ''

#sea_bed_freshwater
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'bed'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(sea_bed)@context~at_(freshwater_flowing)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#sea_ice
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'ice'
cond_obj2 = csn['object2'] == ''
cond_quant = csn['quantity'].str.contains('salinity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'sea@context~at_(ice@medium)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
        'object_id'] = 'sea@context~at_ice'
cond_quant = csn['quantity'].str.contains('fraction')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'sea@medium_ice'
cond_quant = csn['quantity'].str.contains('melting_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice') + '_melting-point)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
                'quantity_label'].str.replace('melting_point_','melting-point_')
cond_quant = csn['quantity'].str.contains('volume_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity_label'] = 'volume_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity_label'].str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity_label'] = 'shear_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'quantity_label'].str.replace('shear_','')
cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'isobaric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isobaric-process)'
cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'isochoric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isochoric-process)'
cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'isobaric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isobaric-process)'
cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'isochoric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isochoric-process)'
cond_quant = csn['quantity'].str.contains('mass-specific_latent_fusion')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'latent_fusion_mass-specific_heat'
cond_quant = csn['quantity'].str.contains('mass-specific_latent_sublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'latent_sublimation_mass-specific_heat'
cond_quant = csn['quantity'].str.contains('melt_')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_melting)'
cond_quant = csn['quantity'].str.contains('sublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_sublimation)'
cond_quant = csn['quantity'].str.contains('fusion')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_fusion)'
cond_quant = csn['quantity'].str.contains('isentropic')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isentropic-process)'
cond_quant = csn['quantity'].str.contains('isothermal')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('ice','(ice')+'_isothermal-process)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#sea_ice_bottom
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'ice'
cond_obj2 = csn['object2'] == 'bottom'
cond_obj4 = csn['object4'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
        'object_id'] = 'sea@context~at_(ice_bottom)'
cond_quant = csn['quantity']=='temperature'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4 & cond_quant, \
        'object_id'] = '(sea@context~at_(ice_bottom))@context~below_(sea@context~in_water)'
cond_quant = csn['quantity'] == 'salinity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4 & cond_quant, \
        'object_id'] = '(sea@context~at_(ice_bottom))@context~below_(sea@context~in_(water@medium))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
        ['object0','object1','object2','object3']] = ''

#sea_ice_bottom_water_salt
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'ice'
cond_obj2 = csn['object2'] == 'bottom'
cond_obj3 = csn['object3'] == 'water'
cond_obj4 = csn['object4'] == 'salt'
cond_quant = csn['quantity'] == 'salinity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj4, \
        'object_id']='(sea@context~at_(ice_bottom))@context~below_(sea@context~in_water)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj4 & cond_quant, \
        'object_id']=csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_obj4 & cond_quant, \
        'object_id'].str.replace('water','(water')+'@medium)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj4, \
        'object_id']='(sea@context~at_(ice_bottom))@role~source_(sea@context~in_water)@role~sink_salt@role~main'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3','object4']] = ''

#sea_ice_salt
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'ice'
cond_obj2 = csn['object2'] == 'salt'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id']='sea@context~at_(ice@medium_salt)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_ice_surface_air
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'ice'
cond_obj2 = csn['object2'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(sea@context~at_(ice_surface))@context~above_air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#sea_ice_radiation~..
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'ice'
cond_obj2 = csn['object2'].str.contains('radiation~incoming')
cond_quant = csn['quantity'].str.endswith('flux')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(sea@context~at_ice)@role~sink'
cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant,\
        'object_id']='(sea@context~at_ice)@role~source'
cond_obj2 = csn['object2'].str.contains('radiation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
        .str.replace('~total','')+'@role~main'
cond_quant = csn['quantity'].str.endswith('ance')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(sea@context~at_ice)@role~main'
cond_obj2 = csn['object2'].str.contains('radiation~incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']=csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
        .str.replace('~total','')+'@role~in'
cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']=csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']\
        .str.replace('~total','')+'@role~out'
cond_obj2 = csn['object2'].str.contains('radiation')
cond_quant = csn['quantity'] == 'energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']='(sea@context~at_ice)@context~source_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']
cond_quant = csn['quantity'].str.contains('refl')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_reflection'
cond_quant = csn['quantity'].str.contains('absor')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_absorption'
cond_quant = csn['quantity'].str.contains('transmit')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_transmission'
cond_quant = csn['quantity'].str.contains('emit')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_emission'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_photic-zone_bottom
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'photic-zone'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'sea_photic-zone_bottom'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#sea_shoreline
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'shoreline'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'sea@context~adjacent_shoreline'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#sea_shoreline_axis...
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'shoreline'
cond_obj2 = csn['object2'].str.contains('axis')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(sea@context~adjacent_(shoreline_axis~x))@role~first_axis~east@role~second'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_shoreline_wave~
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'shoreline'
cond_obj2 = csn['object2'].str.contains('wave~')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(sea@context~adjacent_shoreline)@context~sink_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_surface
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'sea_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#sea_surface_air
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_surface)@context~above_air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#sea_surface_air_carbon-dioxide
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == 'carbon-dioxide'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_surface)@context~above_(air@medium_carbon-dioxide)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#sea_surface_air-vs-water
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'air-vs-water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
    '((sea_surface)@context~above_air)@role~first_((sea_surface)@context~in_water)@role~second'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_surface_air_flow
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_surface)@context~above_(air_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'quantity_label']\
    .str.replace('of_velocity','of_linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#sea_surface_air_water~vapor
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'air'
cond_obj3 = csn['object3'] == 'water~vapor'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_surface)@context~above_(air@medium_water~vapor)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#sea_surface_radiation~...
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'].str.contains('radiation~incoming')
cond_quant = csn['quantity'].str.endswith('flux')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(sea_surface)@role~sink_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']+'@role~main'
cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(sea_surface)@context~source_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']
cond_obj2 = csn['object2'].str.contains('radiation')
cond_quant = csn['quantity'].str.endswith('ance')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = '(sea_surface)@role~main'
cond_obj2 = csn['object2'].str.contains('radiation~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']+'@role~out'
cond_obj2 = csn['object2'].str.contains('radiation~incoming')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, 'object2']+'@role~in'
cond_obj2 = csn['object2'].str.contains('radiation')
cond_quant = csn['quantity'].str.contains('absor')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_absorption'
cond_quant = csn['quantity'].str.contains('refl')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id']+'_reflection'
cond_quant = csn['quantity']=='energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('@role~main','').str.replace('@role~','@context~')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_surface_storm_water
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'storm'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(sea_surface)@context~at_storm@context~source_(water_surging)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#sea_surface_water
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == ''
cond_quant = csn['quantity'].str.contains('salinity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(sea_surface)@context~in_(water@medium)'
cond_quant = csn['quantity'].str.contains('precipitation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(sea_surface)@context~sink_(atmosphere@role~source_water@role~main_precipitation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'].str.replace('leq-','leq_')
cond_quant = csn['quantity'].str.contains('evaporation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '(sea_surface)@role~source_water@role~main_evaporation'
cond_quant = csn['quantity'].str.contains('salinity|precipitation|evaporation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & ~cond_quant, \
        'object_id'] = '(sea_surface)@context~in_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#sea_surface_water_carbon-dioxide
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'carbon-dioxide'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_surface)@context~in_(water@medium_carbon-dioxide)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#sea_surface_water_heat~...
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'].str.contains('heat')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_surface)@context~in_(water@role~medium)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_label'] = 'sea_surface_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']\
        .str.split('~').str[-1]+'_heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3']] = ''

#sea_surface_water_tide_constituent~...
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'] == 'tide'
cond_obj5 = csn['object5'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_surface)@context~in_(water_tide_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object4']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, \
        'object_id'].str.rstrip(')')  +'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj5, 'object5']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#sea_surface_water_wave~...
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'water'
cond_obj3 = csn['object3'].str.contains('wave')
cond_obj4 = csn['object4'] != ''
cond_obj5 = csn['object5'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(sea_surface)@context~in_(water_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_obj4, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_obj4, \
        'object_id'].str.rstrip(')') +'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_obj4, 'object4']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_obj5, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_obj5, \
        'object_id'].str.rstrip(')') +'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3& cond_obj5, 'object5']+')'
cond_quant = csn['quantity'].str.contains('vertex')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.rstrip(')')+'_vertex)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'angle'
cond_quant = csn['quantity'].str.contains('orbital')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'].str.rstrip(')')+'_orbit)'
cond_quant = csn['quantity'].str.contains('steepness')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'slope'
cond_quant = csn['quantity'].str.contains('angular_wavenumber')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_label'] = 'wavenumber'
cond_quant = csn['quantity'].str.contains('-times-')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'quantity_id'] = 'cumulative_time_integral_of_cosine_of_product_of_angular_frequency_and_time'
cond_quant = csn['quantity'].str.contains('refraction')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '('+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] + ')@role~sink_radiation@role~main_refraction'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2','object3','object4','object5']] = ''

#sea_water
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == ''
cond_quant = csn['quantity'].str.contains('salinity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
        'object_id'] = 'sea@context~in_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'sea@context~in_(water@medium)'
cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'isobaric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water')+'_isobaric-process)'
cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'isochoric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water')+'_isochoric-process)'
cond_quant = csn['quantity'].str.contains('isentropic')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water')+'_isentropic-process)'
cond_quant = csn['quantity'].str.contains('isothermal')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water')+'_isothermal-process)'
cond_quant = csn['quantity'].str.contains('mass-specific_latent_fusion')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'latent_fusion_mass-specific_heat'
cond_quant = csn['quantity'].str.contains('fusion')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water')+'_fusion)'
cond_quant = csn['quantity'].str.contains('mass-specific_latent_vaporization')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'latent_vaporization_mass-specific_heat'
cond_quant = csn['quantity'].str.contains('vaporization')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water')+'_vaporization)'
cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'isobaric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water')+'_isobaric-process)'
cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'isochoric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water')+'_isochoric-process)'
cond_quant = csn['quantity'].str.contains('brunt')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'brunt-vaisala_frequency'
cond_quant = csn['quantity'].str.contains('eddy')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water_eddy)')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'viscosity'
cond_quant = csn['quantity'].str.contains('flow')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','(water_flowing)')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'speed'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'].str.replace('total_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'].str.replace('velocity','linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1']] = ''

#sea_water_above-bottom
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'above-bottom'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(sea@context~in_water)_(sea_bottom)@reference~above'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_water_below-surface
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'below-surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(sea@context~in_water)_(sea_surface)@reference~below'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_water_bottom (water unnecessary??)
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'bottom'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(sea_water)_(sea_bottom)@reference~to'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_water_carbon-dioxide
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'carbon-dioxide'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'sea@context~in_(water@medium_carbon-dioxide)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_water_energy/heat
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'].str.contains('energy|heat')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'sea@context~in_(water@role~medium_diffusion)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'sea_water'
cond_obj2 = csn['object2'].str.contains('energy')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']\
        .str.replace('diffusion','turbulent_kinetic_energy_diffusion')
cond_obj2 = csn['object2'].str.contains('heat')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']\
        .str.replace('diffusion','heat_diffusion')
cond_obj2 = csn['object2'].str.contains('energy|heat')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_water_flow
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'sea@context~in_(water_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'quantity_label'].str.replace('total_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']\
    .str.replace('of_velocity','of_linear_velocity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_water_diatoms-as-*
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'].str.contains('diatoms')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'sea@context~in_((water@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,'object2'].str.split('-as-').str[0]+\
        ')@context~in_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,'object2'].str.split('-as-').str[1]+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_water_solute
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'].str.contains('chloride|sulfate|salt|oxygen|sediment|biota')
cond_quant = csn['quantity'].str.contains('density')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'sea@context~in_(water@context~in'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
        'object_id'] = 'sea@context~in_(water@medium'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id']+\
        '_'+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+')'
cond_obj2 = csn['object2'].str.contains('salt')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'].str.replace('medium','medium_diffusion')
cond_obj2 = csn['object2'].str.contains('chloride|sulfate|salt|oxygen|sediment|biota')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_water_surface -- water unnecessary
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'sea_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#sea_water_zone* -- water unnecessary
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'].str.contains('zone')
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'sea_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id'] = 'sea_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']\
    .str.replace('zone~photic','photic-zone')+'_'+ \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#sea_water_wave/tide/current
cond_obj0 = csn['object0'] == 'sea'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'].str.contains('wave|tide|current')
cond_obj3 = csn['object3'] != ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'sea@context~in_(water_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
        .str.replace('wave~internal~gravity','wave~gravity~internal')\
        .str.replace('wave~internal','wave~gravity~internal')+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_label'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_label']\
        .str.replace('wave~internal~gravity','wave~gravity~internal')\
        .str.replace('wave~internal','wave~gravity~internal')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id'] =\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id']\
        .str.rstrip(')')+'_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object3']+')'
cond_quant = csn['quantity'].str.contains('flow')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.rstrip(')')+'_flowing)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'mean_speed'
cond_quant = csn['quantity'].str.contains('angular_wavenumber')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'wavenumber'
cond_quant = csn['quantity'].str.contains('frequency')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_id'] = 'angular_frequency'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3']] = ''

#shale~burgess_stratum
cond_obj0 = csn['object0'].str.contains('shale~burgess')
csn.loc[ cond_obj0, 'object_id'] = 'burgess-shale_stratum'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#skydiver/sierpinski-gasket/ship
cond_obj0 = csn['object0'].str.contains('skydiver|ship')
csn.loc[ cond_obj0, 'object_id'] = csn.loc[ cond_obj0, 'object0']
csn.loc[ cond_obj0, 'object_pref'] = 'body'
cond_obj0 = csn['object0'].str.contains('skydiver')
csn.loc[ cond_obj0, 'object_pref'] = 'rolephenomenon'
cond_obj0 = csn['object0'].str.contains('sierpinski')
csn.loc[ cond_obj0, 'object_id'] = csn.loc[ cond_obj0, 'object0']
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
cond_obj0 = csn['object0'].str.contains('skydiver|sierpinski|ship')
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0,'object0'] = ''

#snow
cond_obj0 = csn['object0'] == 'snow'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'snow'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_pref'] = 'matter'
cond_quant = csn['quantity'].str.contains('energy-per-area_cold')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'cold_energy-per-area_density'
cond_quant = csn['quantity'].str.contains('blowing')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_blowing'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'isobaric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isobaric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'isochoric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isochoric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'isobaric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isobaric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'isochoric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isochoric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#snow-or-ice
cond_obj0 = csn['object0'] == 'snow-or-ice'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0, 'object_id'] = 'snow-or-ice_melting'
csn.loc[ cond_obj0, 'object0'] = ''

#snow~wet_X
cond_obj0 = csn['object0'] == 'snow~wet'
cond_obj1 = csn['object1'] == 'rubber'
csn.loc[ cond_obj0, 'object_id'] = 'snow~wet@role~exchange_rubber@role~exchange_friction'
cond_obj1 = csn['object1'] == 'ski~waxed'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'ski~waxed@role~exchange_rubber@role~exchange_friction'    
csn.loc[ cond_obj0, ['object0','object1']] = ''

#snowpack
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'snowpack'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
cond_quant = csn['quantity'].str.contains('desublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'@context~in_(snow_desublimation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity_label'].str.startswith('sublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'@context~in_(snow_sublimation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('melt_')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'@context~in_(snow_melting)'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label']\
        .str.replace('mass-specific_isobaric','isobaric_mass-specific')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isobaric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('isothermal')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isothermal-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('isentropic')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isentropic-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('liquid-equivalent')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label']\
        .str.replace('liquid-equivalent','leq')
cond_quant = csn['quantity'].str.contains('energy-per-area')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'cold_energy-per-area_density'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#snowpack_bottom
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'bottom'
cond_quant = csn['quantity'] == 'temperature'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'snowpack_bottom'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
cond_quant = csn['quantity'] == 'energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_label'] = 'snowpack_bottom'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = \
        'conduction_heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = '(snowpack_bottom)@role~medium_conduction'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#snowpack_core
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'core'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'snowpack_core'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#snowpack_crust_layer~
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'crust'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'snowpack_crust_'+\
    csn.loc[ cond_obj0 & cond_obj1, 'object2']
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#snowpack_ice-layer
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'ice-layer'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'snowpack@context~part_ice-layer'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#snowpack_snow~new
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'snow~new'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'snowpack@context~in_snow~new'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#snowpack_surface
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(snowpack_surface)@role~main_indentation'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#snowpack_top
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'snowpack_top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#snowpack_top_air
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == 'air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(snowpack_top)@context~above_air'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#snowpack_top_heat
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'].str.contains('heat')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(snowpack_top)@role~medium'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_label'] = 'snowpack_top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
        .str.split('~').str[-1]+'_heat_energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#snowpack_top_surface
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'top'
cond_obj2 = csn['object2'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(snowpack_top_surface)@role~main_indentation'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#snowpack_grains
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'grains'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'snowpack@context~part_(snow_grains)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#snowpack_water~liquid
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'water~liquid'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'snowpack@medium_water~liquid'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#snowpack_meltwater
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'] == 'meltwater'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'snowpack@context~source_meltwater'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#snowpack_radiation
cond_obj0 = csn['object0'] == 'snowpack'
cond_obj1 = csn['object1'].str.contains('radiation~incoming')
cond_quant = csn['quantity'].str.contains('flux')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'snowpack@role~sink_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object1'].str.replace('~total','')+'@role~main'
cond_obj1 = csn['object1'].str.contains('radiation~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'snowpack@role~source_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object1'].str.replace('~total','')+'@role~main'
cond_obj1 = csn['object1'].str.contains('radiation~incoming')
cond_quant = csn['quantity'] == 'energy_flux'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'snowpack@context~sink_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object1'].str.replace('~total','')
cond_obj1 = csn['object1'].str.contains('radiation~incoming')
cond_quant = csn['quantity'].str.endswith('ance')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
        'snowpack@role~main_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']\
        .str.replace('~total','')+'@role~in'
cond_obj1 = csn['object1'].str.contains('radiation~outgoing')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
        'snowpack@role~main_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1']\
        .str.replace('~total','')+'@role~out'
cond_obj1 = csn['object1'].str.contains('radiation')
cond_quant = csn['quantity'].str.contains('refl')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_reflection'
cond_quant = csn['quantity'].str.contains('absor')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_absorption'
cond_quant = csn['quantity'].str.contains('emit')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_emission'
csn.loc[(csn['object0']=='snowpack'), ['object0','object1']] = ''

#soil
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == ''
cond_quant = csn['quantity'].str.contains('hydraulic|porosity')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_id'] = 'soil'
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, 'object_pref'] = 'matter'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'soil@medium'
cond_quant = csn['quantity'].str.contains('saturated')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'soil@medium_saturated'
cond_quant = csn['quantity'].str.contains('thaw')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'soil_thaw'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('freeze')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'soil_freezing'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('mass-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'isochoric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isochoric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('mass-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'isobaric_mass-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isobaric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('volume-specific_isochoric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'isochoric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isochoric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('volume-specific_isobaric')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'isobaric_volume-specific_heat_capacity'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id']+'_isobaric-process'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#soil_air
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'air'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil@medium_air'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#soil_bulk
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'bulk'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil_bulk'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#soil_carbon_pool~stabilized_carbon
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'carbon'
cond_obj2 = csn['object2'] == 'pool~stabilized'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'soil@context~in_((carbon_pool~stabilized)@context~in_carbon)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']] = ''

#soil_carbon_pool~microbial-and-stabilized_carbon~decomposed
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'carbon'
cond_obj2 = csn['object2'] == 'pool~microbial-and-stabilized'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(soil@context~in_(carbon_pool~stabilized))@role~sink_(soil@context~in_(carbon_pool~microbial))@role~sink_carbon~decomposed@role~main_addition'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']] = ''

#soil_clay_particle
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'clay'
cond_obj2 = csn['object2'] == 'particle'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'soil@medium_(clay_particle)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']] = ''

#soil_fertilizer
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'fertilizer'
cond_quant = csn['quantity'].str.contains('fertilization')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'soil@role~main_fertilizer@role~in_fertilization'
cond_quant = csn['quantity'].str.contains('application')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'soil@role~sink_fertilizer@role~main_application'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#soil_layer
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'layer'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'soil_layer'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#soil_layer_carbon~stabilized
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'layer'
cond_obj2 = csn['object2'] == 'carbon~stabilized'
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(soil_layer)@medium_carbon~stabilized'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''

#soil_layer_matter~organic~stabilized_carbon
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'layer'
cond_obj2 = csn['object2'] == 'matter~organic~stabilized'
cond_obj3 = csn['object3'] == 'carbon'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = '(soil_layer)@context~in_(matter~organic~stabilized@medium_carbon)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        ['object0','object1','object2']] = ''
        
#soil_macropores_water
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'macropores'
cond_obj2 = csn['object2'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(soil@context~medium_macropores)@medium_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#soil_macropores_below-land-surface
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'macropores'
cond_obj2 = csn['object2'] == 'below-land-surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(soil@context~medium_macropores)_(land_surface)@reference~below'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#soil_macropores
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'macropores'
cond_obj2 = csn['object2'] == ''
cond_quant = csn['quantity'].str.contains('volume_fraction')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'soil@medium_macropores'
cond_quant = csn['quantity'].str.contains('cutoff_depth')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'soil@context~in_macropores'
cond_quant = csn['quantity'].str.contains('conductivity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'soil@medium_saturated'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']] = ''

#soil_nitrogen
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'nitrogen'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil@role~main_nitrogen@role~in'
cond_quant = csn['quantity'].str.contains('denitrification')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id']+\
    '_denitrification'
cond_quant = csn['quantity'].str.contains('_nitrification')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id']+\
    '_nitrification'
csn.loc[ cond_obj0 & cond_obj1,['object0','object1','object2']] = ''

#soil_nitrous-oxide-as-nitrogen
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'nitrous-oxide-as-nitrogen'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil@role~source_nitrous-oxide-as-nitrogen@role~main_emission'
cond_quant = csn['quantity'].str.contains('nitrification')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = '(soil_nitrification)@role~source_nitrous-oxide-as-nitrogen@role~main_emission'
cond_quant = csn['quantity'].str.contains('denitrification')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = '(soil_denitrification)@role~source_nitrous-oxide-as-nitrogen@role~main_emission'
csn.loc[ cond_obj0 & cond_obj1,['object0','object1']] = ''

#soil_permafrost
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'permafrost'
cond_obj2 = csn['object2'] != ''
csn.loc[ cond_obj0 & cond_obj1 & ~cond_obj2, 'object_id'] = 'soil_permafrost'
csn.loc[ cond_obj0 & cond_obj1 & ~cond_obj2, 'object_pref'] = 'matter'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'soil_permafrost_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2'] 
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1,['object0','object1','object2']] = ''

#soil_pool~stabilized_carbon
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'pool~stabilized'
cond_obj2 = csn['object2'] == 'carbon'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(soil_pool~stabilized)@context~in_carbon'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,['object0','object1','object2']] = ''

#soil_pool-and-pool~microbial_carbon~decomoposed__addition_mass
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'pool-and-pool~microbial'
cond_obj2 = csn['object2'] == 'carbon~decomposed'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(soil_pool)@role~sink_pool~microbial@role~sink_carbon~decomposed@role~main_addition'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2,['object0','object1','object2']] = ''

#soil_profile_bottom_water__drainage_volume_flux
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'profile'
cond_obj2 = csn['object2'] == 'bottom'
cond_obj3 = csn['object3'] == 'water'
cond_obj4 = csn['object4'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object_id'] = '(soil_profile_bottom)@role~source_water@role~main_draining'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4,['object0','object1','object2']] = ''

#soil_profile_bottom_water_ammonium/nitrate__time_integral_of_drainage_leaching_mass_flux
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'profile'
cond_obj2 = csn['object2'] == 'bottom'
cond_obj3 = csn['object3'] == 'water'
cond_obj4 = csn['object4'].str.contains('ammonium|nitrate')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object_id'] = '(soil_profile_bottom)@role~source_(water_draining)@role~medium_('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, 'object4']+'_leaching)@role~main'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4,['object0','object1','object2','object3','object4']] = ''

#soil_profile_nitrate/ammonium-as-nitrogen
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'profile'
cond_obj2 = csn['object2'].str.contains('-as-nitrogen')
cond_obj3 = csn['object3'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_id'] = '(soil_profile)@context~in_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3,['object0','object1','object2']] = ''

#soil_*-zone
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'].str.contains('zone')
cond_obj2 = csn['object2'] != ''
cond_quant = csn['quantity'].str.contains('recharge')
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil_'+\
    csn.loc[ cond_obj0 & cond_obj1, 'object1']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'soil_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']\
    .str.replace('zone~photic','photic-zone')+'_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
    csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id']+'@medium_(water_recharge)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#soil_ice_thawing-front
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'ice'
cond_obj2 = csn['object2'] == 'thawing-front'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'soil@context~in_(ice_thawing-front)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2']] = ''

#soil_ice
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'ice'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil@medium_ice'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

##soil_bedrock_top
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'bedrock'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil_(bedrock_top)@reference~above'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#soil_particle
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'particle'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil_particle'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#soil_rock
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'rock'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil@medium_rock'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#soil_layer/horizon
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'].str.contains('layer|horizon~')
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'soil_'+\
        csn.loc[ cond_obj0 & cond_obj1, 'object1']
cond_obj2 = csn['object2'] == 'water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(soil_'+\
    csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object1']+')@medium_water'
cond_quant = csn['quantity'].str.contains('saturated')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'soil_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1'] + '_saturated'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#soil_matter~organic/loam/air
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'].str.contains('matter|loam|sand|silt|clay')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1, 'object1']
cond_quant = csn['quantity'].str.contains('oven-dried')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'soil@medium_('+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object1'] + '_oven-dried)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#soil_plant_residue_water
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'plant'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = '(soil@context~on_(plant_residue))@role~source_water@role~main_evaporation'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2','object3']] = ''

#soil_surface_residue~standing_carbon-to-nitrogen
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'surface'
cond_obj2 = csn['object2'] == 'residue~standing'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = '(soil_surface)@context~on_(residue~standing@context~in_(carbon@role~numerator_nitrogen@role~denominator))'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1','object2','object3']] = ''

#soil_surface_water
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'surface'
cond_quant = csn['quantity'].str.contains('infiltration')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = '(soil_surface)@role~sink_water@role~main_infiltration'
cond_quant = csn['quantity'].str.contains('irrigation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = '(soil_surface)@role~sink_water@role~main_irrigation'
cond_quant = csn['quantity'].str.contains('evaporation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = '(soil_surface)@role~source_water@role~main_evaporation'
cond_quant = csn['quantity'].str.contains('runoff')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = '(soil_surface)@context~on_(water_runoff)'
cond_quant = csn['quantity'].str.contains('evaporation|infiltration|runoff|irrigation')
csn.loc[ cond_obj0 & cond_obj1 & ~cond_quant, \
        'object_id'] = '(soil_surface)@medium_water'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#soil_void
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'void'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil@medium_void'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#soil_water(_flow)
cond_obj0 = csn['object0'].str.contains('soil')
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'] == '' 
cond_quant = csn['quantity']\
        .str.contains('conductivity|fraction|infiltration|wilting-point|concentration|capacity')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object0']+'@medium_water'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & ~cond_quant, \
        'object_id'] = 'soil@context~in_water'
cond_quant = csn['quantity'].str.contains('interception')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = 'soil@role~main_water@role~in_interception'
cond_obj2 = csn['object2'] == 'flow'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'soil@context~in_(water_flowing)'
cond_obj2 = (csn['object2'] == '') | (csn['object2'] == 'flow')
cond_quant = csn['quantity'].str.contains('wilting')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('medium','medium_wilting-point')
cond_quant = csn['quantity'].str.contains('saturated')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('medium','medium_saturated')
cond_quant = csn['quantity'].str.contains('bubbling')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('medium','medium_bubbling-point')
cond_quant = csn['quantity'].str.contains('infiltration')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('water','infiltration_water')
cond_quant = csn['quantity'].str.contains('oven-dried')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('medium','medium_oven-dried')
cond_quant = csn['quantity'].str.contains('air-dried')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'].str.replace('medium','medium_air-dried')
cond_quant = csn['quantity'].str.contains('beta_parameter')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_id'] = 'van-genuchten_alpha_parameter'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'quantity_label'] = 'van-genuchten_alpha_parameter'        
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#soil_water_*front (water unnecessary)
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'].str.contains('front')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'soil@context~in_(water_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']+')'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#soil_*-as-*
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'].str.contains('-as-')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'soil@medium_'+\
        csn.loc[ cond_obj0 & cond_obj1, 'object1']
csn.loc[ cond_obj0 & cond_obj1, \
        ['object0','object1']] = ''

#soil_water_*zone (water unnecessary)
cond_obj0 = csn['object0'] == 'soil'
cond_obj1 = csn['object1'] == 'water'
cond_obj2 = csn['object2'].str.contains('zone')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = 'soil_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']\
        .str.replace('zone~photic','photic-zone')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_pref'] = 'body'
cond_obj3 = csn['object3'] == 'top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, \
        'object_id']+'_top'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3, 'object_pref'] = 'body'
cond_obj4 = csn['object4'] == 'surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_id']+'_surface'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_obj4, \
        'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('recharge')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id'] = '('+csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, \
        'object_id']+')@role~main_water@role~in_recharge'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_obj3 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2','object3','object4']] = ''

#soil_x-section_macropores
cond_obj0 = csn['object0'] == 'soil'
cond_obj2 = csn['object2'] == 'macropores'
csn.loc[ cond_obj0 & cond_obj2, 'object_id']='soil@medium_(macropores_'+\
    csn.loc[ cond_obj0 & cond_obj2, 'object1']+')'
csn.loc[ cond_obj0 & cond_obj2, 'object_label']='soil_macropores_'+\
    csn.loc[ cond_obj0 & cond_obj2, 'object1']
csn.loc[ cond_obj0 & cond_obj2, ['object0','object1','object2']] = ''

#soil~moist_layer
cond_obj0 = csn['object0'] == 'soil~moist'
csn.loc[ cond_obj0, 'object_id']='soil~moist_layer'
csn.loc[ cond_obj0, 'object_pref']='body'
csn.loc[ cond_obj0, 'object0'] = ''

#soil~no-rock_silt
cond_obj0 = csn['object0'] == 'soil~no-rock'
csn.loc[ cond_obj0, 'object_id']='soil~no-rock@medium_silt'
csn.loc[ cond_obj0, 'object0'] = ''

#soil~no-rock~dry
cond_obj0 = csn['object0'] == 'soil~no-rock~dry'
csn.loc[ cond_obj0, 'object_id']='soil~no-rock~dry'
csn.loc[ cond_obj0, 'object_pref']='matter'
csn.loc[ cond_obj0, 'object0'] = ''

#space-shuttle_tile
cond_obj0 = csn['object0'] == 'space-shuttle'
csn.loc[ cond_obj0, 'object_id'] = 'space-shuttle@context~part_(tile_isochoric-process)'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#sphere_surface
cond_obj0 = csn['object0'] == 'sphere'
csn.loc[ cond_obj0, 'object_id'] = 'sphere_surface'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#spring~steel
cond_obj0 = csn['object0'] == 'spring~steel'
csn.loc[ cond_obj0, 'object_id'] = 'spring~steel'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#square
cond_obj0 = csn['object0'] == 'square'
csn.loc[ cond_obj0, 'object_id'] = 'square'
csn.loc[ cond_obj0, 'object_pref'] = 'abstraction'
csn.loc[ cond_obj0, 'object0'] = ''

#star~
cond_obj0 = csn['object0'].str.contains('star~')
csn.loc[ cond_obj0,'object_id'] = \
        csn.loc[ cond_obj0,'object0']
csn.loc[ cond_obj0, 'quantity_label'] = \
        ['tolman-oppenheimer-volkoff-limit_mass', 'chandrasekhar-limit_mass']
csn.loc[ cond_obj0,'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object0'] = ''

#submarine
cond_obj0 = csn['object0'] == 'submarine'
csn.loc[ cond_obj0, 'object_id'] = 'submarine_(sea_floor)@reference~above'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#substrates~organic_nitrogen__gross_decomposition_mass-per-area_mineralization_density
cond_obj0 = csn['object0'] == 'substrates~organic'
csn.loc[ cond_obj0, 'object_id'] = '(substrates~organic_decomposition)@context~source_(nitrogen_mineralization)'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#sulfuric-acid
cond_obj0 = csn['object0'] == 'sulfuric-acid'
csn.loc[ cond_obj0, 'object_id'] = 'sulfuric-acid'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#sulfuric-acid
cond_obj0 = csn['object0'] == 'sulphuric-acid'
csn.loc[ cond_obj0, 'object_id'] = 'sulfuric-acid@role~first_water@role~second'
csn.loc[ cond_obj0, 'object_label'] = 'sulfuric-acid_water'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#sun-lotion_skin
cond_obj0 = csn['object0'] == 'sun-lotion'
csn.loc[ cond_obj0, 'object_id'] = 'skin@role~sink_sun-lotion@role~main_protection'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#tank~storage~open-top
cond_obj0 = csn['object0'] == 'tank~storage~open-top'
cond_obj1 = csn['object1'] == 'water'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'tank~storage~open-top@context~in_water'
cond_quant = csn['quantity'].str.contains('flow')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = \
    'tank~storage~open-top@context~in_(water_flowing)'
cond_obj1 = csn['object1'].str.contains('x-section')
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'tank~storage~open-top_'+\
    (csn.loc[ cond_obj0 & cond_obj1, 'object1'] + '_' + \
         csn.loc[ cond_obj0 & cond_obj1, 'object2']).str.rstrip('_')
cond_obj1 = csn['object1'].str.contains('outlet')
cond_obj2 = csn['object2'].str.contains('x-section')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = \
    'tank~storage~open-top@context~part_(outlet_x-section)'
cond_obj2 = csn['object2'].str.contains('water')
csn.loc[ cond_obj0 & cond_obj2, \
        'object_id'] = '(tank~storage~open-top@context~part_outlet)@role~source_(water_flowing)@role~main'
csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#titan_atmosphere_methane
cond_obj0 = csn['object0'] == 'titan'
csn.loc[ cond_obj0, 'object_id'] = '(titan@context~surrounding_atmosphere)@role~source_methane@role~main_precipitation'
csn.loc[ cond_obj0, ['object0','object1','object2']] = ''

#toyota_corolla
cond_obj0 = csn['object0'] == 'toyota'
cond_obj1 = csn['object1'] == 'corolla~2008'
cond_obj2 = csn['object2'] == ''
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_id'] = 'toyota-corolla~2008'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, ['object0','object1']] = ''

#toyota_corolla_engine
cond_obj0 = csn['object0'] == 'toyota'
cond_obj2 = csn['object2'] == 'engine'
csn.loc[ cond_obj0 & cond_obj2, \
        'object_id'] = 'toyota-corolla~2008@context~part_engine'
csn.loc[ cond_obj0 & cond_obj2, ['object0','object1','object2']] = ''

#toyota_corolla_fuel_tank
cond_obj0 = csn['object0'] == 'toyota'
cond_obj3 = csn['object3'] == 'tank'
csn.loc[ cond_obj0 & cond_obj3, \
        'object_id'] = 'toyota-corolla~2008@context~part_fuel-tank'
csn.loc[ cond_obj0 & cond_obj3, ['object0','object1','object2','object3']] = ''

#toyota_corolla_fuel
cond_obj0 = csn['object0'] == 'toyota'
cond_obj2 = csn['object2'] == 'fuel'
csn.loc[ cond_obj0 & cond_obj2, \
        'object_id'] = 'toyota-corolla~2008@role~sink_fuel@role~main_consumption'
csn.loc[ cond_obj0 & cond_obj2, ['object0','object1','object2']] = ''

#tree~oak~bluejack
cond_obj0 = csn['object0'] == 'tree~oak~bluejack'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'bluejack-oak'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'body'
cond_obj1 = csn['object1'] == 'trunk'
csn.loc[ cond_obj0 & cond_obj1, \
        'object_id'] = 'bluejack-oak@context~part_trunk'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#universe
cond_obj0 = csn['object0'] == 'universe~friedmann'
csn.loc[ cond_obj0,'object_id']='friedmann-universe'
csn.loc[ cond_obj0,'object_pref']='abstraction'
csn.loc[ cond_obj0, 'object0'] = ''
cond_obj0 = csn['object0'] == 'universe'
csn.loc[ cond_obj0,'object_id'] = 'universe@context~in_radiation~background~cosmic'
csn.loc[ cond_obj0,'object_label'] = 'universe_radiation~background~cosmic'
csn.loc[ cond_obj0,'quantity_label'] = 'frequency'
csn.loc[ cond_obj0, 'object0'] = ''

#venus
cond_obj0 = csn['object0'] == 'venus'
cond_obj1 = csn['object1'] == 'axis'
csn.loc[ cond_obj0, 'object_id'] = 'venus'
csn.loc[ cond_obj0, 'object_pref'] = 'body'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'venus_'+\
    csn.loc[ cond_obj0 & cond_obj1,'object1']
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'] == 'standard_gravity_constant'
csn.loc[ cond_obj0 & cond_quant , 'quantity_label'] = \
        'standard_gravitational_acceleration'
cond_obj1 = csn['object1'].str.contains('orbit')
csn.loc[ cond_obj0 & cond_obj1,'object_id'] = 'venus_orbit'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'phenomenon'
cond_obj1 = csn['object1'].str.contains('-to-')
csn.loc[ cond_obj0 & cond_obj1,'object_id'] = '(venus_orbit)@role~first_(venus_ecliptic)@role~second'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('aphelion')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = \
    csn.loc[ cond_obj0 & cond_quant, 'object_id']+'_aphelion'
csn.loc[ cond_obj0 & cond_quant, 'object_label'] = \
    csn.loc[ cond_obj0 & cond_quant, 'object_label']+'_aphelion'
cond_quant = csn['quantity'].str.contains('perihelion')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = \
    csn.loc[ cond_obj0 & cond_quant, 'object_id']+'_perihelion'
csn.loc[ cond_obj0 & cond_quant, 'object_label'] = \
    csn.loc[ cond_obj0 & cond_quant, 'object_label']+'_perihelion'
cond_quant = csn['quantity'].str.contains('ecliptic')
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = \
    csn.loc[ cond_obj0 & cond_quant, 'object_id']+'_ecliptic'
csn.loc[ cond_obj0 , 'quantity_label'] = \
    csn.loc[ cond_obj0, 'quantity_label'].str.replace('perihelion_','')\
    .str.replace('aphelion_','')
csn.loc[ cond_obj0, ['object0','object1']] = ''

#virus~chicken-pox
cond_obj0 = csn['object0'] == 'virus'
csn.loc[ cond_obj0, 'object_id'] = 'virus~chicken-pox_incubation'
csn.loc[ cond_obj0, 'object_label'] = 'virus~chicken-pox'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#water
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1,'object_id']='water'
csn.loc[ cond_obj0 & cond_obj1,'object_pref']='matter'
csn.loc[ cond_obj0 & cond_obj1,'object_cat']='root'
cond_quant = csn['quantity'].str.contains('boiling_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'water_boiling-point'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'boiling-point_temperature'
cond_quant = csn['quantity'].str.contains('freezing_point')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'object_id'] = 'water_freezing-point'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, \
        'quantity_label'] = 'freezing-point_temperature'
cond_quant = csn['quantity'].str.contains('volume_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = 'volume_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'].str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear_viscosity')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'] = 'shear_'+\
        csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'quantity_label'].str.replace('shear_','')
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
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('fusion')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'water_fusion'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
cond_quant = csn['quantity'].str.contains('sublimation')
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_id'] = 'water_sublimation'
csn.loc[ cond_obj0 & cond_obj1 & cond_quant, 'object_pref'] = 'phenomenon'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#water_below-land-surface
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'below-land-surface'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'water_(land_surface)@reference~below'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#water_channel-network_source
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'channel-network'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'channel-network@context~part_source~of-water'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#water_electron
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'electron'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'water@role~main_electron@role~in'
csn.loc[ cond_obj0 & cond_obj1, 'object_label'] = 'water'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = 'electron_affinity'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#water_salt
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'salt'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'water@context~in_salt'
csn.loc[ cond_obj0 & cond_obj1, 'quantity_label'] = 'mass_diffusivity'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#water_sand_grain
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'sand'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'water@role~medium_(sand_grain)@role~main_settling'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1','object2']] = ''

#water_scuba-diver_dive__duration
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'scuba-diver'
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'water@context~in_(scuba-diver_diving)'
csn.loc[ cond_obj0 & cond_obj1, ['object0','object1']] = ''

#water_molecule_bond~...
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'molecule'
cond_obj2 = csn['object2'].str.contains('-')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(water_molecule)@context~part_bond~' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_label'] = 'water_molecule_bond~' + \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object2']
cond_quant = csn['quantity'].str.contains('dissociation')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & cond_quant, \
        'object_id'] = csn.loc[ cond_obj0 & cond_obj1 & cond_obj2 & \
        cond_quant, 'object_id'].str.replace('bond','(bond') + '_dissociation)'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label'] = \
        csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'quantity_label']\
        .str.replace('bond_','')
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#water_molecule_hydrogen...
cond_obj0 = csn['object0'] == 'water'
cond_obj1 = csn['object1'] == 'molecule'
cond_obj2 = csn['object2'] == 'hydrogen'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, 'object_id'] = '(water_molecule)@context~part_hydrogen'
csn.loc[ cond_obj0 & cond_obj1 & cond_obj2, \
        ['object0','object1','object2']] = ''

#water_...__solubility
cond_obj0 = csn['object0'] == 'water'
cond_quant = csn['quantity'] == 'solubility'
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = 'water@medium_'+\
        csn.loc[ cond_obj0 & cond_quant, 'object1']
csn.loc[ cond_obj0 & cond_quant, ['object0','object1']] = ''

#water~incoming-and-outgoing
cond_obj0 = csn['object0'] == 'water~incoming-and-outgoing'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1,'object_id']='water_flow~incoming-and-outgoing'
csn.loc[ cond_obj0 & cond_obj1,['object0','object1']]=''

#water~liquid
cond_obj0 = csn['object0'] == 'water~liquid'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1,'object_id']='water~liquid'
csn.loc[ cond_obj0 & cond_obj1,'object_cat']='root'
csn.loc[ cond_obj0 & cond_obj1,'object_pref']='matter'
csn.loc[ cond_obj0 & cond_obj1,['object0','object1']]=''

#water~liquid_...
cond_obj0 = csn['object0'] == 'water~liquid'
csn.loc[ cond_obj0,'object_id']='water~liquid@medium_'+\
    csn.loc[ cond_obj0,'object1']
csn.loc[ cond_obj0,['object0','object1']]=''

#water~liquid~20C
cond_obj0 = csn['object0'] == 'water~liquid~20C'
cond_obj1 = csn['object1'] == 'air'
csn.loc[ cond_obj0,'object_id']='water~liquid~20C'
csn.loc[ cond_obj0 & ~cond_obj1,'object_pref']='matter'
csn.loc[ cond_obj0,'object_cat']='root'
csn.loc[ cond_obj0 & cond_obj1,'object_label']='air_water~liquid~20C'
csn.loc[ cond_obj0 & cond_obj1,'object_id']='air@context~in_water~liquid~20C'
csn.loc[ cond_obj0 & cond_obj1,'object_cat']=''
cond_quant = csn['quantity'].str.contains('volume_viscosity')
csn.loc[ cond_obj0 & cond_quant, 'quantity_label'] = 'volume_'+\
        csn.loc[ cond_obj0 & cond_quant, 'quantity_label']\
        .str.replace('volume_','')
cond_quant = csn['quantity'].str.contains('shear_viscosity')
csn.loc[ cond_obj0 & cond_quant, 'quantity_label'] = 'shear_'+\
        csn.loc[ cond_obj0 & cond_quant, 'quantity_label'].str.replace('shear_','')
cond_quant = csn['quantity'].str.contains('vapor_pressure')
csn.loc[ cond_obj0 & cond_quant, 'quantity_id'] = 'pressure'
csn.loc[ cond_obj0 & cond_quant, 'object_id'] = 'water~vapor~20C'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#water~vapor
cond_obj0 = csn['object0'] == 'water~vapor'
cond_obj1 = csn['object1'] == ''
csn.loc[ cond_obj0 & cond_obj1, 'object_id'] = 'water~vapor'
csn.loc[ cond_obj0 & cond_obj1, 'object_pref'] = 'matter'
csn.loc[ cond_obj0 & cond_obj1, 'object_cat'] = 'root'
csn.loc[ cond_obj0 & cond_obj1, 'object0'] = ''

#water~vapor_air~dry
cond_obj0 = csn['object0'] == 'water~vapor'
csn.loc[ cond_obj0, 'object_id'] = 'water~vapor@role~numerator_air~dry@role~denominator'
csn.loc[ cond_obj0, ['object0','object1']] = ''

#wave
cond_obj0 = csn['object0'].str.contains('wave')
csn.loc[ cond_obj0,'object_id'] = csn.loc[ cond_obj0, 'object0']
cond_obj0 = csn['object0'].str.contains('wave~sine')
csn.loc[ cond_obj0,'object_pref'] = 'abstraction'
cond_obj0 = csn['object0'].str.contains('wave')
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

#weather-station
cond_obj0 = csn['object0'] == 'weather-station'
csn.loc[ cond_obj0,'object_id'] = \
        csn.loc[ cond_obj0,'object0']
csn.loc[ cond_obj0,'object_pref'] = 'body'
csn.loc[ cond_obj0, 'object0'] = ''

#wind
cond_obj0 = csn['object0'] == 'wind'
csn.loc[ cond_obj0, 'object_id'] = 'wind'
csn.loc[ cond_obj0, 'object0'] = ''

#wood~dry
cond_obj0 = csn['object0'].str.contains('wood')
csn.loc[ cond_obj0, 'object_id'] = 'wood~dry'
csn.loc[ cond_obj0, 'object_pref'] = 'matter'
csn.loc[ cond_obj0, 'object_cat'] = 'root'
csn.loc[ cond_obj0, 'object0'] = ''

cond_obj0 = csn['object0'] == ''
csn2 = csn.loc[ ~cond_obj0 ].copy()
csn = csn.loc[ cond_obj0 ]
csn=csn.fillna('')

csn.loc[csn['quantity_id']=='','quantity_id'] = \
    csn.loc[csn['quantity_id']=='','quantity_label']

csn.loc[(csn['operator']!='') & ~csn['quantity_id'].str.contains('_of_'),'quantity_id'] = \
    csn.loc[(csn['operator']!='') & ~csn['quantity_id'].str.contains('_of_'),'operator']+\
    '_of_'+csn.loc[(csn['operator']!='') & ~csn['quantity_id'].str.contains('_of_'),'quantity_id']
csn.loc[csn['operator']!='','quantity_label'] = csn.loc[csn['operator']!='','operator']+'_of_'+csn.loc[csn['operator']!='','quantity_label']

csn['quantity_id'] = \
    csn['quantity_id']\
    .str.replace('salinity','absolute_salinity')\
    .str.replace('heat_diffusion_coefficient','thermal_diffusivity')\
    .str.replace('diffusion_coefficient','diffusivity')\
    .str.replace('relative_molecular_mass_ratio','molecular_mass_ratio')\
    .str.replace('relative_atomic_mass_ratio','atomic_mass_ratio')\
    .str.replace('extensional_viscosity','extensional_kinematic_viscosity')\
    .str.replace('leq-','leq_')\
    .str.replace('relative_hydraulic_conductivity','hydraulic_conductivity_ratio')\
    .str.replace('dynamic_shear_viscosity','shear_dynamic_viscosity')\
    .str.replace('magazine-safety','magazine_safety')\
    .str.replace('relative_hydraulic_roughness','hydraulic_roughness_ratio')\
    .str.replace('relative_saturation','saturation_ratio')\
    .str.replace('specific_saturation','mass_saturation_ratio')\
    .str.replace('depth-times-slope','product_of_depth_and_slope')\
    .str.replace('precipitation_mass-per-volume_density','mass-per-volume_density')\
    .str.replace('manning','manning-formula')\
    .str.replace('relative_magnetic_permeability','magnetic_permeability_ratio')\
    .str.replace('of_momentum','of_linear_momentum')\
    .str.replace('of_viscosity','of_dynamic_viscosity')\
    .str.replace('of_speed','of_linear_speed')\
    .str.replace('of_velocity','of_linear_velocity')\
    .str.replace('one-hour','hourly').str.replace('one-day','daily')\
    .str.replace('one-month','monthly').str.replace('one-year','yearly')\
    .str.replace('relative_permittivity','permittivity_ratio')\
    .str.replace('_\(en\)','').str.replace('network','network_name')\
    .str.replace('surface_area','area')

#corrections    
csn.loc[csn['quantity_id']=='emittance','quantity_id']='emissivity'
csn.loc[csn['quantity_id']=='speed','quantity_id']='linear_speed'

csn['variable_label'] = csn['object_label']+'__'+csn['quantity_label']
csn['variable_id'] = csn['object_id']+'__'+csn['quantity_id']
cols_to_print = ['full_name','variable_id','variable_label','object_cat','object_id','object_label','object_pref','quantity_id','quantity_label']
#cols_to_print = ['full_name','variable_label','object_id','object_label']
csn[cols_to_print].to_csv('CSDMS_standard_names.csv',index=False)
