# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:18:12 2016
Last edit on Mon May 13 15:04:00 2016

@author: Maria Stoica
@description: Take the "current" list of standard names (combined with
        make_CSN_list.py from the CSDMS website and Google Drive)
        and correct mistakes, inconsistencies, etc. Write to output file
        CSN_VarNames_Corrected.csv
"""
################################
#    IMPORT NEEDED PACKAGES    #
################################

#Pandas for data frames and data manipulation
import pandas as pd
import numpy as np

################################
#   INITIAL DATA LOAD          #
################################

# Load CSN list, split up by '__' to yield object and quantity parts.

# Combined list from Google Drive folder (0.85b) and CSDMS website (0.83), 3066 names.
csn = pd.read_csv('CSN_VarNames_v0.85m0.csv',sep='__',header=None,engine='python')
csn.rename(columns={0: 'object', 1: 'quantity'}, inplace=True)
csn.sort_values(['object','quantity'],inplace = True)
csn['full_name']=csn['object']+'__'+csn['quantity']

################################
#   DATA CLEANUP               #
################################

# misspellings
csn['full_name']=csn['full_name'].str.replace('suceptibility','susceptibility')\
    .str.replace('mercali','mercalli').str.replace('mass-to-volume','mass-per-volume')\
    .str.replace('spinup','spin-up').str.replace('metabolizable-','metabolizable_')\
    .str.replace('lame_parameters_lambda','lame_first_parameter')\
    .str.replace('detection_number','detection_number_count').str.replace('mass-per_','mass-per-')\
    .str.replace('casson_model_k','casson_model_a').str.replace('relative_roughness_ratio',\
    'relative_hydraulic_roughness').str.replace('refraction_index','refractive_index')\
                .str.replace('kelly','kelley').str.replace('d_infinity','d-infinity')

# add hyphenation to law names, etc to link concept into one entity
csn['full_name']=csn['full_name'].str.replace('richter_law','richter-law')\
    .str.replace('fine_structure','fine-structure')\
    .str.replace('volume_flow_rate_law','volume-flow-rate-law')\
    .str.replace('power_law','power-law')\
    .str.replace('antoine_vapor_pressure','antoine-vapor-pressure')\
    .str.replace('_vs_','-vs-').str.replace('herschel_bulkley','herschel-bulkley')\
    .str.replace('modified_omori_law','modified-omori-law')\
    .str.replace('van_genuchten','van-genuchten')\
    .str.replace('hack_law','hack-law').str.replace('log_law','log-law')\
    .str.replace('glen_law','glen-law').str.replace('area_law','area-law')\
    .str.replace('flint_law','flint-law').str.replace('hooke_law','hooke-law')\
    .str.replace('chezy_formula','chezy-formula')\
    .str.replace('ashton_et_al','ashton-et-al')\
    .str.replace('von_karman','von-karman').str.replace('golden_ratio','golden-ratio')\
    .str.replace('gravitational_coupling','gravitational-coupling')\
    .str.replace('beer_lambert_law','beer-lambert-law')\
    .str.replace('casson_model','casson-model').str.replace('stefan_boltzmann','stefan-boltzmann')

# move '(en)' to a separate word, represent string
csn['full_name']=csn['full_name'].str.replace('\(en\)','_(en)')

# shields_parameter and shields_number both occur; choose shields_parameter
csn['full_name']=csn['full_name'].str.replace('shields_number',\
    'shields_parameter')

# impedance needs to be disambiguated: electrical_impedance
csn['full_name']=csn['full_name'].str.replace('impedance','electrical_impedance')

# permeability needs to be disambiguated: absolute_permeability
csn['full_name']=csn['full_name'].str.replace('__permeability','__absolute_permeability')\
    .str.replace('specific_permeability','absolute_permeability')

# change electric_relative_permittivity to relative_electric_permittivity
#   electric_permittivity is the unit of measurement
# replace electric_permittivity with permittivity without ambiguity
# replace dielectric_constant with relative_permittivity because not a constant
csn['full_name']=csn['full_name'].str.replace('electric_relative','relative_electric')\
    .str.replace('electric_absolute','absolute_electric')\
    .str.replace('electric_permittivity','permittivity')\
    .str.replace('dielectric_constant','relative_permittivity')
#    .str.replace('absolute_permittivity','permittivity')\
    

# change viscosity_reference_value to reference_viscosity, viscosity_value to viscosity
#   viscosity is the unit of measurement
csn['full_name']=csn['full_name'].str.replace('viscosity_reference_value',\
    'reference_viscosity').str.replace('viscosity_value','viscosity')

# thermal_volume_expansion_coefficient is the volumetric thermal_expansion_coefficient
csn['full_name']=csn['full_name'].str.replace('thermal_volume','volumetric_thermal')

# h and b magnetic fields two type of magnetic field
#csn['full_name']=csn['full_name'].str.replace('magnetic-h-field','h_magnetic_field')\
#    .str.replace('magnetic-b-field','b_magnetic_field')\
#    .str.replace('magnetic-field-strength','h_magnetic_field')\
#    .str.replace('magnetic-field','b_magnetic_field')
csn['full_name']=csn['full_name'].str.replace('electric-field','electric-e-field')\
    .str.replace('magnetic-field-strength','magnetic-h-field')\
    .str.replace('magnetic-field','magnetic-b-field')

# magnetic relative permeability is the relative ... magnetic_permeability
csn['full_name']=csn['full_name'].str.replace('magnetic_relative','relative_magnetic')

# incompressibility is compressibility
csn['full_name']=csn['full_name'].str.replace('incompressibility','compressibility')

# electric-field-potential is electric_potential, electric-(e)-field is electric_field
#csn['full_name']=csn['full_name'].str.replace('electric-field-potential',\
#    'electric_potential').str.replace('electric-field','electric_field')\
#    .str.replace('electric-e-field','electric_field')
csn['full_name']=csn['full_name'].str.replace('electric-e-field-potential',\
    'electric_potential')

# electric-displacement is a field, electric-d-field is electric-displacement_field
#csn['full_name']=csn['full_name'].str.replace('electric-displacement',\
#    'electric-displacement_field').str.replace('electric-d-field',\
#    'electric-displacement_field')
csn['full_name']=csn['full_name'].str.replace('electric-displacement',\
    'electric-d-field')

# electric-polarization is electric_polarization (v magnetic_polarization)
#csn['full_name']=csn['full_name'].str.replace('electric-polarization',\
#    'electric_polarization').str.replace('electric-p-field','electric_polarization')
csn['full_name']=csn['full_name'].str.replace('electric-polarization',\
    'electric-p-field')
# synonym: magnetization, but polarization is more consistent with pattern since
#    electrization is not a term
#csn['full_name']=csn['full_name'].str.replace('magnetic-m-field','magnetic_polarization')\
#    .str.replace('magnetization','magnetic_polarization')
csn['full_name']=csn['full_name'].str.replace('magnetization','magnetic-m-field')

# electron charge is electric-charge
csn['full_name']=csn['full_name'].str.replace('charge-to-mass','electric-charge-to-mass')\
    .str.replace('mass-to-charge','mass-to-electric-charge').str.replace('charge_constant','electric-charge_constant')\
    .str.replace('electric_charge','electric-charge')

# thermal_energy_content is energy density, specific energy content is energy-per-mass
#   density
# weight content is interpreted to be weight_fraction
csn['full_name']=csn['full_name'].str.replace('thermal_energy_content',\
    'thermal_energy-per-volume_density').str.replace('specific_energy_content',\
    'energy-per-mass_density').str.replace('weight_content','weight_fraction')

# cold content does not have default units
csn['full_name']=csn['full_name'].str.replace('__cold_content','__energy-per-area_cold_content')
# per-unit-X is the same thing as per-X
csn['full_name']=csn['full_name'].str.replace('per-unit','per')

# length-to-are_ratio and length-per-area_density both present, choose the density
#    take out total because it is implied
csn['full_name']=csn['full_name'].str.replace('total-length','length')\
    .str.replace('length-to-area_ratio','length-per-area_density')

# count-per-volume is a density, same as power-per-length
csn['full_name']=csn['full_name'].str.replace('count-per-volume',\
    'count-per-volume_density').str.replace('power-per-length','power-per-length_density')

# mass-per-volume_bulk_density includes the object 'bulk', so move to object side
# same for particle
csn['full_name']=csn['full_name'].str.replace('__mass-per-volume_bulk_density',\
    '_bulk__mass-per-volume_density').str.replace('__mass-per-volume_particle_density',\
    '_particle__mass-per-volume_density')

# thermal_quality is a ratio, adding ratio to the name may confuse with ratio
#      of thermal_qualities
csn['full_name']=csn['full_name'].str.replace('thermal_quality_ratio','thermal_quality')

# seismic moment is a tensor, so tensor as part of the name is not necessary
csn['full_name']=csn['full_name'].str.replace('moment_tensor','seismic_moment')

# density is mass-per-volume_density
csn['full_name']=csn['full_name'].str.replace('__density','__mass-per-volume_density')

# water is an object, so water_content measures water mass or molar or volume fraction
# for now, replace with mass_fraction, proportion is also mass_fraction
csn['full_name']=csn['full_name'].str.replace('__water_content','_water__mass_fraction')\
    .str.replace('proportion','mass_fraction')

#carbonatite_melt_fraction: carbonatite is an object; melt fraction is shorthand for
# fraction in melt (of, presumably, the current object); therefore, change this to
# _melt_carbonatite__mass_fraction
# partial_melt_fraction is (presumably) the [partial] mass fraction of material
#  in melt form
csn['full_name']=csn['full_name'].str.replace('__carbonatite_melt_fraction',\
    '_carbonatite_melt__volume_fraction')
csn['full_name']=csn['full_name'].str.replace('__partial_melt_fraction',\
    '_melt~partial__volume_fraction')
# same for water solubility in melt
csn['full_name']=csn['full_name'].str.replace('__water_solubility_in_melt',\
    '_melt_water__solubility').str.replace('__water_solubility','_water__solubility')

# a meander is a kink in a channel, so an object
#csn['full_name']=csn['full_name'].str.replace('__meander','_meander_')

# void_ratio includes the object 'void', usually a volume fraction
csn['full_name']=csn['full_name'].str.replace('__void_ratio','_void__volume_fraction')

# bottom surface of channel is a second object
csn['full_name']=csn['full_name'].str.replace('__depth-times-bottom-surface-slope',\
    '_channel_bottom_surface__depth-times-slope')

# for times, group the two product components together
# this changes in the next processing code to product_of_...
csn['full_name']=csn['full_name'].str.replace('angular_frequency_times_',\
    'angular-frequency-times-')

# neutron is an object that is being counted, same with proton, hydrogen
csn['full_name']=csn['full_name'].str.replace('__neutron_number',\
    '_neutron__number_count').str.replace('__proton_number','_proton__number_count')\
    .str.replace('mass_number','mass_number_count').str.replace('__hydrogen_number',\
    '_hydrogen__number_count')

# fuel is an object and needs to be moved
csn['full_name']=csn['full_name'].str.replace('fuel-economy','fuel_economy')\
    .str.replace('__fuel_economy','_fuel__economy').str.replace('fuel__economy',\
    'fuel__consumption_rate')
# z-count is a count in the z-direction, same for x,y
csn['full_name']=csn['full_name'].str.replace('z-count','z_count')\
    .str.replace('x-count','x_count').str.replace('y-count','y_count')

# clarify that slip is seismic_slip, same for slip-vector
csn['full_name']=csn['full_name'].str.replace('slip-vector','seismic_slip')\
    .str.replace('__slip','__seismic_slip').str.replace('critical_slip','critical_seismic_slip')

# breaking-wave is a phenomenon, similar to helium-plume
# move breaking to adjective (already present this way in some names)
csn['full_name']=csn['full_name'].str.replace('__breaking','~breaking_')\
    .str.replace('__fraction','__count_fraction')

#sidereal day is a phenomenon
csn['full_name']=csn['full_name'].str.replace('__sidereal_day','_day~sidereal__duration')

# both mole_ and molar_concentration present; change all to molar_
csn['full_name']=csn['full_name'].str.replace('mole_concentration','molar_concentration')

# richter_magnitude is a scale, modified_mercalli_intensity also a scale,
#    also: moment_magnitude, apparent_magnitude
csn['full_name']=csn['full_name'].str.replace('richter_magnitude','richter-magnitude_scale')\
    .str.replace('modified_mercalli_intensity','modified-mercalli-intensity_scale')\
    .str.replace('moment_magnitude','moment-magnitude_scale')\
    .str.replace('apparent_magnitude','apparent-magnitude_scale')

# in the case where we want the azimuth angle of a vector, the vector becomes an abstraction
# of an object and goes on the left hand side
# csn['full_name']=csn['full_name'].str.replace('azimuth_angle_tangent-vector',\
#    'azimuth_angle_of_tangent-vector')

#indices with reference values are a bit tricky; for now, move them as a secondary
#   object to object part
csn['full_name']=csn['full_name'].str.replace('__index_from_top','-from-grid_top__index')\
    .str.replace('__index_from_bottom','-from-grid_bottom__index')\
    .str.replace('__depth_to_bottom','-to-grid_bottom__depth')\
    .str.replace('__depth_to_top','-to-grid_top__depth')

################################
#   WRITE OUTPUT               #
################################

pd.DataFrame({'full_name':np.unique(csn['full_name'])}).to_csv('CSN_VarNames_v0.85m2.csv',index=False)
