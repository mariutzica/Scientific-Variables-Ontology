#############################################################
#                      STEP1                                #
#   Rearrange vocabulary from CSN, CFSN, SRSN to make       #
#   easier to parse, atomize, and tag with atomic element   #
#   relationships.                                          #
#   Output file has format orginial_name, formatted_name    #
#   with no header                                          #
#   input: source/raw/csdms_standard_names.csv              #
#   output: source/csdms_standard_names.csv                 #
#                                                           #
#############################################################

import os

script_path  = os.path.dirname(__file__)
src_path     = os.path.join(script_path,'../../source/raw/')
csn_filename = 'csdms_standard_names.csv'
csn_filepath = os.path.join(src_path,csn_filename)

dst_path     = os.path.join(script_path,'../../source/')
csn_dst_file = os.path.join(dst_path,csn_filename)
#cf_filename = 'cf_standard_names.csv'
#srs_filename = 'nwis_srs_names.csv'

def split_variable(name):
    return name.split('__')

# Move terms around in csn for easier categorization.

wordy = False
# parse CSN
with open(csn_filepath) as f:
    with open(csn_dst_file,'w') as dst_f:
        for variable in f:

            # strip \n
            variable = variable.strip()
            variable_original = variable
            [object,quantity] = split_variable(variable)

            # remove -to- to make oop analysis easier
            variable = variable.replace('hypocenter-to-','hypocenter_')\
                        .replace('brain-to-body','brain_body')\
                        .replace('apex-to-shoreline','apex_shoreline')\
                        .replace('earth-to-','earth_')\
                        .replace('plane-to-sun','plane_sun')\
                        .replace('air-to-fuel','air_fuel')\
                        .replace('fuel-to-oxidizer','fuel_oxidizer')\
                        .replace('axis~x-to-axis~east','axis~x_axis~east')\
                        .replace('orbit-to-ecliptic','orbit_venus_ecliptic')\
                        .replace('carbon-to-nitrogen','carbon_nitrogen')

            # add missing object
            variable = variable.replace('air-vs-water','air_sea_surface_water')

            if object == 'soil_bedrock_top':
                variable = variable.replace('soil_bedrock_top','bedrock_top_from-soil_surface')

            if object == 'sea_water_bottom':
                variable = variable.replace('sea_water_bottom','sea_water_to-sea_bottom')
            
            if object == 'water_channel-network_source':
                variable = variable.replace('water_channel-network_source', \
                                            'channel-network_source')
                
            if object.endswith('_basin'):
                variable = 'basin_' + variable.replace('_basin','')

            # separate out linked terms or link separated terms
            # make terminology uniform
            variable = variable.replace('helium-plume','helium_plume')\
                        .replace('wing__span','_wingspan')\
                        .replace('aceto-nitrile','acetonitrile')\
                        .replace('air-column','air_column')\
                        .replace('liquid-equivalent','leq')\
                        .replace('_leq-','_leq_')\
                        .replace('economy','distance-per-volume_efficiency')\
                        .replace('fuel_tank','fuel-tank')\
                        .replace('rear_axle','axle~rear')\
                        .replace('seat_belt','seat-belt')\
                        .replace('basin~drainage','basin')\
                        .replace('basin_','drainage-basin_')\
                        .replace('basin~','drainage-basin~')\
                        .replace('total-length','total_length')\
                        .replace('number-per-area','count-per-area')\
                        .replace('__permeability','__fluid_permeability')\
                        .replace('c_c_c__bond','bond-c-c-c_')\
                        .replace('carbon_hydrogen__bond','bond-c-h_')\
                        .replace('hydrogen_oxygen__bond','bond-h-o_')\
                        .replace('h-h__bond','bond-h-h_')\
                        .replace('n-n__bond','bond-n-n_')\
                        .replace('o-o__bond','bond-o-o_')\
                        .replace('h-o__bond','bond-h-o_')\
                        .replace('__neutron','_neutron__neutron')\
                        .replace('__proton','_proton__atomic')\
                        .replace('electron__affinity','electron__electron_affinity')\
                        .replace('per-unit','per')\
                        .replace('initial_mean','mean_initial')\
                        .replace('parabola__coefficient','parabola__leading_coefficient')\
                        .replace('__metabolizable-','~metabolizable__')\
                        .replace('consumer__price_index','market-basket__consumer_price_index')\
                        .replace('__top_width','_top__width')\
                        .replace('mass-to-volume_density','mass-per-volume_density')\
                        .replace('crust-mantle_boundary','crust-mantle-boundary')\
                        .replace('core-mantle_boundary','core-mantle-boundary')\
                        .replace('lithosphere-asthenosphere_boundary','lithosphere-asthenosphere-boundary')\
                        .replace('_slip_','_seismic_slip_')\
                        .replace('slip-vector','seismic_slip')\
                        .replace('slip-rake','seismic_slip-rake')\
                        .replace('moment_tensor','seismic_moment')\
                        .replace('earthquake__rupture','earthquake_fault_plane_rupture_')\
                        .replace('wave~p','seismic-wave~p')\
                        .replace('wave~s_','seismic-wave~s_')\
                        .replace('__p_wave','_seismic-wave~p_')\
                        .replace('__aphelion','_aphelion_')\
                        .replace('__perihelion','_perihelion_')\
                        .replace('charge-to-mass','electric-charge-to-mass')\
                        .replace('mass-to-charge','mass-to-electric-charge')\
                        .replace('gm_hummer','automobile~gm~hummer')\
                        .replace('toyota_corolla','automobile~toyota~corolla')\
                        .replace('energy~net~total__','_net_')\
                        .replace('__vacuum','_vacuum_')\
                        .replace('__light','_light_')\
                        .replace('mrsp','msrp')\
                        .replace('projectile_origin','projectile_trajectory_origin')\
                        .replace('projectile_target','projectile_trajectory_target')\
                        .replace('land~grassland','grassland')\
                        .replace('land~parkland','parkland')\
                        .replace('degrees-per-hour_speed','angular_speed')\
                        .replace('wave~breaking','breaking-wave')\
                        .replace('wave__breaking','breaking-wave_')\
                        .replace('wave~internal_','internal-gravity-wave_')\
                        .replace('wave~internal~gravity','internal-gravity-wave')\
                        .replace('wave~incoming~deepwater','deepwater-wave~incoming')\
                        .replace('refraction_index','refractive_index')\
                        .replace('zone~aphotic','aphotic-zone')\
                        .replace('zone~photic','photic-zone')\
                        .replace('zone~surf','surf-zone')\
                        .replace('root-zone','rhizosphere')\
                        .replace('__void_ratio','_void__volume_ratio')\
                        .replace('axis~semi-major','semi-major-axis')\
                        .replace('axis~semi-minor','semi-minor-axis')\
                        .replace('appliance~electric','electric-appliance')\
                        .replace('solar_irradiation_constant','solar_constant')\
                        .replace('curve~enclosing','enclosing-curve')\
                        .replace('delta_front_toe','delta-front-toe')\
                        .replace('plain~lower-and-upper','plain~lower-and-plain~upper')\
                        .replace('aerosol_dust', 'dust~aerosol')
            
            variable = variable.replace('soil_horizon~','soil-horizon-')\
                        .replace('__atterberg_liquid_limit','_atterberg-liquid-limit_')\
                        .replace('__atterberg_plastic_limit','_atterberg-plastic-limit_')\
                        .replace('__atterberg_shrinkage_limit','_atterberg-shrinkage-limit_')\
                        .replace('kelly','kelley')\
                        .replace('power_law_viscosity','power_law_viscosity_law')\
                        .replace('value','viscosity')\
                        .replace('_upward_','_upward_component_of_')\
                        .replace('_downward_','_downward_component_of_')\
                        .replace('van_genuchten','van-genuchten')\
                        .replace('hydraulic_geometry','hydraulic-geometry')\
                        .replace('channel-bank','river-bank')\
                        .replace('channel_bank','river-bank')\
                        .replace('_bank~','_river-bank~')\
                        .replace('bear~alaskan~black','black-bear~alaskan')\
                        .replace('star~neutron','neutron-star')\
                        .replace('star~white-dwarf','white-dwarf')\
                        .replace('beds~topset~','topset-beds~')\
                        .replace('beds~topset','topset-beds')\
                        .replace('cell~platelet','platelet')\
                        .replace('earth_core~inner','earth-inner-core')\
                        .replace('earth_core~outer','earth-outer-core')\
                        .replace('earth_crust_','earth-crust_')\
                        .replace('snowpack_crust','snowpack-crust')\
                        .replace('earth_mantle_','earth-mantle_')\
                        .replace('tide_constituent~','tide_constituent-')\
                        .replace('light-bulb~incandescent','incandescent-light-bulb')\
                        .replace('unsat-zone','vadose-zone')\
                        .replace('zone~vadose','vadose-zone')\
                        .replace('sat-zone','phreatic-zone')\
                        .replace('tank~storage','storage-tank')\
                        .replace('glacier_terminus','glacier-terminus')\
                        .replace('x_section','x-section')\
                        .replace('virus_chicken-pox','chicken-pox-virus')\
                        .replace('glacier_equilibrium','glacier-equilibrium')\
                        .replace('d_infinity','d-infinity')\
                        .replace('__cosmic_background_radiation','_cosmic-background-radiation_')\
                        .replace('__hydrogen_number','_hydrogen__mass_number')\
                        .replace('__dive_','_dive__')\
                        .replace('water~liquid~20C__vapor_pressure','water~20C__vapor_pressure')\
                        .replace('relative_molecular_mass_ratio','relative_molecular_mass')\
                        .replace('relative_electric_permittivity','relative_permittivity')\
                        .replace('electric_absolute_permittivity','absolute_permittivity')\
                        .replace('electric_relative_permittivity','relative_permittivity')\
                        .replace('magnetic_relative_permeability','relative_magnetic_permeability')\
                        .replace('specific_permeability','specific_fluid_permeability')\
                        .replace('__oxygen_fugacity','_oxygen__fugacity')\
                        .replace('__water_content','_water__mass_fraction')\
                        .replace('lame_parameters_lambda','lame_first_parameter')\
                        .replace('weight_content','weight_fraction')\
                        .replace('(en)','')\
                        .replace('__equation-of-state','_equation-of-state__name')\
                        .replace('proportion','mass_fraction')\
                        .replace('__water_solubility_in_melt','~melt_water__solubility')\
                        .replace('__water_solubility','_water__solubility')\
                        .replace('__network','_network__name')\
                        .replace('__filter_type','_filter__type')\
                        .replace('__cell_count','_cell__count')\
                        .replace('__shell_count','_shell__count')\
                        .replace('__column_count','_column__count')\
                        .replace('__row_count','_row__count')\
                        .replace('__harvest','_harvest_')\
                        .replace('__fertilization','_fertilization_')\
                        .replace('__irrigation','_irrigation_')\
                        .replace('__drainage_volume_flux','_drainage__volume_flux')\
                        .replace('~from-row-below_groundwater','_groundwater_from-row-below')\
                        .replace('daily', 'one-day')\
                        .replace('yearly', 'one-year')\
                        .replace('annual','one-year')\
                        .replace('beds~foreset','foreset-beds')\
                        .replace('beds~bottomset','bottomset-beds')\
                        .replace('wheelbase__distance','_wheelbase_length')\
                        .replace('day~solar-mean','solar-mean-day')\
                        .replace('day~stellar','stellar-day')\
                        .replace('magnetization','magnetic-m-field')\
                        .replace('successive_time_step_multiplier','successive_time_step_multiplication_factor')\
                        .replace('_cos_of_','_cosine_of_')
                        # - SEISMIC SLIP is a vector
                        # - SEISMIC MOMENT has a scalar and tensor version -- need to determine how to distinguish between these two
                        #   in such cases usually the scalar is determined by performing some sort of operation on the tensor
                        # - RUPTURE is a process that happens to create a fault, so added 'fault_plane' to terms that did not have it
                        #.replace('~upward__','__upward_component_of_')\
                        #.replace('~downward__','__downward_component_of_')

            # add process information
            variable = variable.replace('__absorptance','_absorption__absorptance')\
                            .replace('__reflectance','_reflection__reflectance')\
                            .replace('__emittance','_emission__emittance')\
                            .replace('__transmittance','_transmission__transmittance')

            # change syntax for coupled variables
            variable = variable.replace('__speed_reference_height','_at-speed__reference_height')\
                            .replace('__reference_height_speed','_at-reference-height__speed')\
                            .replace('__reference_depth_temperature','_at-reference-depth__temperature')\
                            .replace('__temperature_reference_depth','_at-temperature__reference_depth')\
                            .replace('__pressure_head_reference_depth','_at-pressure-head__reference_depth')\
                            .replace('__reference_depth_pressure_head','_at-reference-depth__pressure_head')\
                            .replace('__isothermal_compressibility_reference_temperature','_at-isothermal-process_compressibility__reference_temperature')

            # create uniform naming convention
            variable = variable.replace('acceleration_time','acceleration_duration')
            
            # adapt operation
            variable = variable.replace('top_speed','max_of_speed')\
                            .replace('channel__downstream_hydraulic','downstream_channel__hydraulic')\
                            .replace('__depth-times-bottom-surface-slope','_channel_bottom_surface__product_of_depth_and_slope')\
                            .replace('angular_frequency_times_time','product_of_angular_frequency_and_time')\
                            .replace('kinetic_energy_plus_potential_energy','summation_of_kinetic_energy_and_potential_energy')\
                            .replace('minimum','min_of')
            #.replace('downvalley','downvalley_component_of')\

            [object,quantity] = split_variable(variable)

            if '_mean_' in variable and '_mean_of_' not in variable:
                variable = variable.replace('_mean_','_mean_of_')
                [object,quantity] = split_variable(variable)

            if 'average' in variable and 'average_of' not in variable:
                variable = variable.replace('average','average_of')
                [object,quantity] = split_variable(variable)

            if '_min_' in variable and 'min_of' not in variable:
                variable = variable.replace('min','min_of')
                [object,quantity] = split_variable(variable)

            if '_max_' in variable and 'max_of' not in variable:
                variable = variable.replace('max','max_of')
                [object,quantity] = split_variable(variable)
            
            if 'vertical' in quantity:
                variable = variable.replace('vertical','vertical_component_of')
                [object,quantity] = split_variable(variable)
            
            if 'horizontal' in quantity:
                variable = variable.replace('horizontal','horizontal_component_of')
                [object,quantity] = split_variable(variable)

            if 'lateral' in quantity:
                variable = variable.replace('lateral','lateral_component_of')
                [object,quantity] = split_variable(variable)

            # move object from quantity to object
            variable = variable.replace('__above-ground','_above-ground_')\
                        .replace('__graph_diameter','_graph__diameter')\
                        .replace('ground~above','above-ground')

            [object,quantity] = split_variable(variable)

            if 'brutsaert' in quantity:
                obj = variable.split('_')[-2]
                variable = variable.replace(obj + '_','')\
                            .replace('__','_'+obj+'__')
                [object,quantity] = split_variable(variable)

            if 'cargo' in quantity:
                variable = variable.replace('cargo_','')\
                            .replace('automobile','automobile_cargo')
                [object,quantity] = split_variable(variable)

            if 'fuel' in quantity:
                variable = variable.replace('fuel_','')\
                        .replace('fuel-','')\
                        .replace('__','_fuel__')
                [object,quantity] = split_variable(variable)

            if '-wave_' in quantity:
                if '_over_' in quantity:
                    first_wave = quantity.split('-wave')[0].split('_')[-1]
                    second_wave = quantity.split('-wave')[1].split('_')[-1]
                    variable = variable.split('__')[0] + '_seismic-wave~' + \
                        first_wave + '_seismic-wave~'  + second_wave + '__' + \
                                quantity.split('-wave')[2].strip('_')
                else:
                    wave = quantity.split('-wave')[0].split('_')[-1]
                    if not 'station' in variable:
                        variable = variable.split('__')[0] + '_seismic-wave~' \
                            + wave + '__' + quantity.replace(wave + '-wave_','')
                    else:
                        variable = variable.split('__')[0].replace('surface','surface_' + \
                                'seismic-wave~' + wave) + '__' + quantity.replace(wave + '-wave_','')
                    if 'arrival' in variable:
                        variable = variable.replace('_station~seismic__arrival','_station~seismic_arrival_')
                    if 'travel' in variable:
                        variable = variable.replace('_station~seismic__travel','_station~seismic_travel_')\
                            .replace('time','duration')
                [object,quantity] = split_variable(variable)
                        
            for term in ['rainfall','snowfall','icefall']:
                if term in quantity:
                    variable = variable.replace(term + '_','')\
                                .replace('atmosphere_water','atmosphere_'+term+'_water')
                [object,quantity] = split_variable(variable)

            if 'station_hydraulic' in quantity:
                variable = 'station_' + variable.replace('station_','')
                [object,quantity] = split_variable(variable)

            if 'carbonatite' in quantity:
                variable = variable.replace('carbonatite_','')\
                            .replace('material','material_carbonatite')
                [object,quantity] = split_variable(variable)

            if 'particle' in quantity:
                variable = variable.replace('particle_','')\
                    .replace('sediment','sediment_particle')\
                    .replace('soil','soil_particle')
                [object,quantity] = split_variable(variable)


            if 'bond' in quantity and 'h-o-h' in object:
                variable = variable.replace('h-o-h','bond-h-o-h')\
                            .replace('bond_','')
                [object,quantity] = split_variable(variable)

            if 'sidereal' in variable:
                variable = variable.replace('sidereal_day','duration')\
                            .replace('earth__','earth_sidereal-day__')\
                            .replace('day~sidereal','sidereal-day')
                [object,quantity] = split_variable(variable)

            if 'earth' in object and 'angle' in quantity and 'solar' in quantity:
                variable = variable.replace('solar_','')\
                    .replace('earth','earth_surface_viewpoint_sun')

            if 'meander' in quantity:
                variable = variable.replace('meander_','')\
                    .replace('channel','channel_meander')
                [object,quantity] = split_variable(variable)

            # move abstraction from quantity to object side
            for term in ['plan','profile','sunshine','streamline']:
                if '_'+term+'_' in quantity or quantity.startswith(term+'_'):
                    variable = variable.replace(term+'_','')\
                            .replace('surface','surface_'+term)
                    [object,quantity] = split_variable(variable)

            if 'vertex' in quantity:
                variable = variable.replace('vertex_','')\
                    .replace('x-section','x-section_vertex')
                [object,quantity] = split_variable(variable)

            if 'equatorial' in variable or 'equator' in object:
                variable = variable.replace('equatorial_','')\
                    .replace('ellipsoid','ellipsoid_equator')
                [object,quantity] = split_variable(variable)

            if 'index_from' in quantity:
                variable = variable.split('_from_')[0]\
                            .replace('__','_from-grid_' + variable.split('_')[-1].strip()+'__')
                [object,quantity] = split_variable(variable)

            if 'model' in object and 'velocity' in quantity:
                if 'water' not in variable:
                    variable = variable.replace('__','_water__')
                [object,quantity] = split_variable(variable)

            if 'model' in object and 'depth' in quantity:
                if '_to_' in variable:
                    to_what = variable.split('_')[-1].strip()
                    variable = variable.split('_to_')[0]\
                                .replace('__','_to-grid_'+to_what+'__')
                elif 'water' not in variable:
                    variable = variable.replace('__','_water__')
                [object,quantity] = split_variable(variable)

            if 'model' in object and 'volume' in quantity:
                if 'water' not in variable:
                    variable = variable.replace('__','_water__')
                [object,quantity] = split_variable(variable)

            if 'node' in quantity:
                if 'average' in quantity:
                    variable = variable.replace('node_','')\
                        .replace('grid','grid_node')
                else:
                    first_attr = variable.split('__')[1].split('_')[0]
                    second_attr = variable.split('-count')[0].split('_')[-1]
                    variable = variable.split('__')[0] + '_node~' + first_attr + '~' + second_attr + '__count'
                [object,quantity] = split_variable(variable)

            # clarify object
            if 'delta' in object:
                variable = variable.replace('delta','river-delta')
                [object,quantity] = split_variable(variable)

            # move process to after object undergoing that process
            if 'simulated' in quantity:
                variable = variable.replace('simulated_','')
                variable = 'model_simulation_' + variable
                [object,quantity] = split_variable(variable)

            if 'observed' in quantity:
                variable = variable.replace('observed_','')
                variable = 'observation_' + variable
                [object,quantity] = split_variable(variable)

            if 'allocated' in quantity and 'land_crop' in object:
                variable = variable.replace('allocated_','')\
                            .replace('land_crop','land_crop_allocation')
                [object,quantity] = split_variable(variable)
            
            if 'produced' in quantity and 'crop' in object:
                variable = variable.replace('produced_','')\
                            .replace('crop','crop_production')
                [object,quantity] = split_variable(variable)
                            
            if 'applied' in quantity:
                if 'usage-cost-per-applied-mass' in variable:
                    variable = 'fertilizer~nitrogen_usage-vs-application__cost_per_mass'
                if 'applied_mass' in quantity and 'fertilizer' in object:
                    variable = variable.replace('applied_','')\
                                .replace('fertilizer_','fertilizer_application_')\
                                .replace('fertilizer~nitrogen','fertilizer~nitrogen_application')
                [object,quantity] = split_variable(variable)

            if 'applied-' in object:
                variable = variable.replace('~applied-as-nitrogen','-as-nitrogen_application')

            if 'absorbed' in quantity:
                variable = variable.replace('absorbed_','')\
                                .replace('__','~absorbed__')
                [object,quantity] = split_variable(variable)

            if 'reflected' in quantity:
                variable = variable.replace('reflected_','')\
                                .replace('__','~reflected__')
                [object,quantity] = split_variable(variable)

            if 'transmitted' in quantity:
                variable = variable.replace('transmitted_','')\
                                .replace('__','~transmitted__')
                [object,quantity] = split_variable(variable)

            if 'emitted' in quantity:
                variable = variable.replace('emitted_','')\
                                .replace('__','~emitted__')
                [object,quantity] = split_variable(variable)

            if 'diffuse' in quantity:
                variable = variable.replace('diffuse_','')\
                                .replace('__','~diffuse__')
                [object,quantity] = split_variable(variable)

            if 'direct' in quantity:
                variable = variable.replace('direct_','')\
                                .replace('__','~direct__')
                [object,quantity] = split_variable(variable)
            
            if 'application' in quantity and ('fertilizer' in object or 'nitrogen' in object):
                # applied to fertilizer, fertilizer~nitrogen, and nitrogen
                variable = variable.replace('application_','')\
                            .replace('__','_application__')
                [object,quantity] = split_variable(variable)

            if 'production' in quantity:
                # applied to crop, oxygen~photosynthetic, roots-and-rhizodeposits
                variable = variable.replace('production_','')\
                            .replace('__','_production__')
                [object,quantity] = split_variable(variable)

            if 'transpiration' in quantity:
                if not 'evapotranspiration' in quantity:
                    if 'water' not in variable:
                        variable = variable.replace('crop','crop_water')
                    variable = variable.replace('transpiration_','')\
                                .replace('water','water_transpiration')
                elif 'evapotranspiration' in quantity and 'water' in object:
                    variable = variable.replace('evapotranspiration_','')\
                                    .replace('water','water_evapotranspiration')
                [object,quantity] = split_variable(variable)

            if 'runoff' in quantity and 'water' in object:
                variable = variable.replace('runoff_','')\
                    .replace('water','water_runoff')
                [object,quantity] = split_variable(variable)

            if 'interception' in quantity and ('water' in object or 'radiation~solar' in object):
                variable = variable.replace('interception_','')\
                    .replace('water','water_interception')\
                    .replace('radiation~solar','radiation~solar_interception')
                [object,quantity] = split_variable(variable)

            if ('_melt_' in quantity or quantity.startswith('melt_')) and 'factor' not in quantity:
                variable = variable.replace('melt_','')\
                            .replace('material','material_melt')\
                            .replace('ice','ice_meltwater')\
                            .replace('snowpack','snowpack_meltwater')\
                            .replace('snow_','snow_meltwater_')\
                            .replace('factor','degree-day_factor')
                if 'partial' in variable:
                    variable = variable.replace('partial_','')\
                        .replace('melt','partial-melt')

            if '_flow_' in quantity or quantity.startswith('flow_'):
                if 'law' not in quantity:
                    variable = variable.replace('flow_','')
                if 'current' not in object:
                    variable = variable.replace('water_','water_flow_')\
                            .replace('water~incoming-and-outgoing','water~incoming-and-outgoing_flow')\
                            .replace('water~incoming_','water~incoming_flow_')\
                            .replace('water~outgoing_','water~outgoing_flow_')\
                            .replace('debris','debris_flow')
                if 'water' not in variable:
                    variable = variable.replace('__','_water_flow__')
                [object,quantity] = split_variable(variable)
            
            if 'baseflow' in quantity and 'water' in object:
                variable = variable.replace('baseflow_','')\
                    .replace('water','water_baseflow')
                [object,quantity] = split_variable(variable)

            if 'leakage' in quantity and 'water' in object:
                variable = variable.replace('leakage_','')\
                    .replace('water','water_leakage')
                [object,quantity] = split_variable(variable)

            if 'accumulation' in quantity and ('nitrogen' in object or 'ice' in object or 'snow'in object):
                variable = variable.replace('accumulation_','')\
                            .replace('nitrogen','nitrogen_accumulation')\
                            .replace('snow','snow_accumulation')\
                            .replace('ice','ice_accumulation')
                [object,quantity] = split_variable(variable)

            if ('_evaporation_' in quantity or quantity.startswith('evaporation_')) and 'water' in object:
                variable = variable.replace('evaporation_','')\
                    .replace('water_','water_evaporation_')\
                    .replace('water~intercepted','water~intercepted_evaporation')\
                    .replace('water~direct','water_evaporation~direct')
                [object,quantity] = split_variable(variable)

            if 'flight' in quantity:
                variable = variable.replace('flight_','')\
                    .replace('aircraft','aircraft_flight')\
                    .replace('projectile','projectile_flight')
                [object,quantity] = split_variable(variable)

            if '_fall_' in quantity or quantity.startswith('fall_'):
                variable = variable.replace('fall_','')\
                                .replace('__','_falling__')
                [object,quantity] = split_variable(variable)

            if 'precipitation' in quantity:
                variable = variable.replace('precipitation_','')\
                                .replace('__','_precipitation__')
                [object,quantity] = split_variable(variable)

            if 'acceleration' in quantity:
                variable = variable.replace('automobile','automobile_acceleration')\
                            .replace('acceleration_duration','duration')\
                            .replace('projectile','projectile_acceleration')\
                            .replace('motion','motion_acceleration')\
                            .replace('__0-to-60mph','~0-to-60mph_')
                [object,quantity] = split_variable(variable)

            if 'braking' in quantity:
                variable = variable.replace('braking_','')\
                    .replace('automobile','automobile_braking')
                [object,quantity] = split_variable(variable)

            if 'lifetime_travel' in quantity:
                variable = variable.replace('lifetime_travel_','')\
                    .replace('automobile','automobile_lifetime-travel')
                [object,quantity] = split_variable(variable)

            if 'manufacture' in quantity:
                variable = variable.replace('manufacture_','')\
                    .replace('automobile','automobile_manufacture')
                [object,quantity] = split_variable(variable)

            if 'stopping' in quantity:
                variable = variable.replace('stopping_','')\
                    .replace('automobile','automobile_stopping')\
                    .replace('time','duration')
                [object,quantity] = split_variable(variable)

            if 'travel' in quantity:
                variable = variable.replace('travel_','')\
                            .replace('time','duration')\
                            .replace('automobile','automobile_travel')\
                            .replace('mars','mars_travel')\
                            .replace('station','station_travel')
                [object,quantity] = split_variable(variable)

            if 'arrival' in quantity:
                variable = variable.replace('__arrival','_arrival_')
                [object,quantity] = split_variable(variable)

            if 'turning' in quantity:
                variable = variable.replace('turning_','')\
                        .replace('automobile','automobile_turning')
                [object,quantity] = split_variable(variable)

            if 'emission' in quantity:
                variable = variable.replace('emission_','')\
                        .replace('carbon-dioxide_','carbon-dioxide_emission_')\
                        .replace('nitrous-oxide-as-nitrogen','nitrous-oxide-as-nitrogen_emission')\
                        .replace('atom','atom_radiation_emission')
                [object,quantity] = split_variable(variable)

            if 'reaction' in quantity:
                variable = variable.replace('reaction_','')\
                        .replace('driver','driver_reaction')\
                        .replace('time','duration')
                [object,quantity] = split_variable(variable)

            if 'roll_rotation' in quantity:
                variable = variable.replace('roll_rotation_','')\
                        .replace('projectile','projectile_roll_rotation')
                [object,quantity] = split_variable(variable)
            
            if 'rotation_tillage' in quantity:
                variable = variable.replace('rotation_tillage_','')\
                        .replace('land','crop_rotation_land_tillage')
                [object,quantity] = split_variable(variable)

            if 'rotation_' in quantity:
                if 'angle' not in object:
                    variable = variable.replace('rotation_','')\
                        .replace('earth','earth_rotation')\
                        .replace('crankshaft','crankshaft_rotation')
                [object,quantity] = split_variable(variable)

            if 'consumption' in quantity:
                variable = variable.replace('consumption_','')\
                    .replace('alcohol','alcohol_consumption')\
                    .replace('oxygen~dissolved','oxygen~dissolved_consumption')\
                    .replace('fuel','fuel_consumption')
                [object,quantity] = split_variable(variable)

            if 'impact' in quantity:
                variable = variable.replace('impact_','')\
                            .replace('projectile','projectile_impact')\
                            .replace('baseball_','baseball_impact_')
                [object,quantity] = split_variable(variable)

            if 'uplift' in quantity:
                variable = variable.replace('uplift_','')\
                            .replace('bedrock','bedrock_uplift')
                [object,quantity] = split_variable(variable)

            if 'migration' in quantity:
                variable = variable.replace('migration_','')\
                    .replace('meander','meander_migration')
                [object,quantity] = split_variable(variable)

            if 'dissipation' in quantity:
                variable = variable.replace('dissipation_','')\
                    .replace('__','_dissipation__')
                [object,quantity] = split_variable(variable)

            # check to see if this interpretation of settling speed is correct ...
            if 'settling' in quantity:
                variable = variable.replace('settling','terminal')\
                            .replace('grain','grain_settling')
                [object,quantity] = split_variable(variable)

            if 'conching' in quantity:
                variable = variable.replace('conching_time','duration')\
                            .replace('chocolate','chocolate_conching')
                [object,quantity] = split_variable(variable)
            
            if 'tempering' in quantity:
                variable = variable.replace('tempering_time','duration')\
                            .replace('chocolate','chocolate_tempering')
                [object,quantity] = split_variable(variable)
            
            if 'subsidence' in quantity:
                variable = variable.replace('subsidence_','')\
                            .replace('ground','ground_subsidence')\
                            .replace('delta','delta_subsidence')
                [object,quantity] = split_variable(variable)
            
            if 'transport' in quantity:
                variable = variable.replace('transport_','')\
                            .replace('sediment~suspended','sediment~suspended_transport')
                [object,quantity] = split_variable(variable)

            if 'progradation' in quantity:
                variable = variable.replace('progradation_','')\
                            .replace('shoreline','shoreline_progradation')
                [object,quantity] = split_variable(variable)

            if 'reworking' in quantity:
                variable = variable.replace('reworking_','')\
                            .replace('sediment','sediment_reworking')
                [object,quantity] = split_variable(variable)
            
            if 'escape' in quantity:
                variable = variable.replace('escape_','')\
                        .replace('earth__','earth_gravity__')\
                        .replace('gravity','gravity_projectile_escape')
                [object,quantity] = split_variable(variable)

            if 'nutation' in quantity:
                variable = variable.replace('nutation_','')\
                    .replace('axis','axis_nutation')
                [object,quantity] = split_variable(variable)

            if 'precession' in quantity:
                variable = variable.replace('precession_','')\
                    .replace('axis','axis_precession')
                [object,quantity] = split_variable(variable)

            if 'rupture' in quantity:
                variable = variable.replace('rupture_','')\
                    .replace('plane','plane_rupture')
                [object,quantity] = split_variable(variable)

            if 'shaking' in quantity:
                variable = variable.replace('shaking_','')\
                    .replace('seismograph','seismograph_shaking')
                [object,quantity] = split_variable(variable)

            if 'rise' in quantity:
                variable = variable.replace('rise_','')\
                            .replace('__','_rising__')
                [object,quantity] = split_variable(variable)

            if '_set_' in quantity or quantity.startswith('set'):
                variable = variable.replace('set_','')\
                            .replace('__','_setting__')
                [object,quantity] = split_variable(variable)

            if 'sliding' in quantity:
                variable = variable.replace('__sliding','_sliding_')
                [object,quantity] = split_variable(variable)

            if 'ablation' in quantity:
                variable = variable.replace('__ablation','_ablation_')
                [object,quantity] = split_variable(variable)
            
            if 'fusion' in quantity and not 'diffusion' in quantity:
                variable = variable.replace('fusion_','')\
                    .replace('ice','ice_fusion')\
                    .replace('water','water_fusion')
                [object,quantity] = split_variable(variable)
            
            if 'sublimation' in quantity:
                if 'desublimation' in quantity:
                    variable = variable.replace('desublimation_','')\
                        .replace('ice','ice_desublimation')\
                        .replace('snowpack','snowpack_snow_desublimation')
                else:
                    variable = variable.replace('sublimation_','')\
                        .replace('water','water_sublimation')\
                        .replace('ice','ice_sublimation')\
                        .replace('snow_','snow_sublimation_')\
                        .replace('snowpack','snowpack_snow_sublimation')
                [object,quantity] = split_variable(variable)

            if 'vaporization' in quantity:
                variable = variable.replace('vaporization_','')\
                        .replace('water','water_vaporization')\
                        .replace('ice','ice_vaporization')
                [object,quantity] = split_variable(variable)

            for term in ['advance','calving','retreat']:
                if term in quantity:
                    variable = variable.replace(term+'_','')\
                        .replace('terminus','terminus_'+term)
                    [object,quantity] = split_variable(variable)

            if 'scour' in quantity:
                variable = variable.replace('scour_','')\
                        .replace('wind','wind_scour')
                [object,quantity] = split_variable(variable)

            if 'hearing' in quantity:
                variable = variable.replace('hearing_','')\
                    .replace('human','human_acoustic-wave_hearing')
                [object,quantity] = split_variable(variable)

            if 'detection' in quantity:
                variable = variable.replace('detection_','')\
                    .replace('photon','photon_detection')\
                    .replace('number','count')
                [object,quantity] = split_variable(variable)

            if 'infiltration' in quantity:
                if 'water' not in object:
                    variable = variable.replace('surface','surface_water')
                variable = variable.replace('infiltration_','')\
                            .replace('water','water_infiltration')
                if 'ponding' in variable:
                    variable = variable.replace('ponding_','')\
                        .replace('infiltration','infiltration_ponding')
                [object,quantity] = split_variable(variable)

            elif 'infiltration' in object:
                variable = variable.replace('~infiltration','_water_infiltration')
                [object,quantity] = split_variable(variable)

            if 'throughfall' in quantity:
                variable = variable.replace('throughfall_','')\
                        .replace('water','water_throughfall')
                [object,quantity] = split_variable(variable)

            if '_run_' in variable:
                variable = variable.replace('run_','')\
                    .replace('model','model_running')\
                    .replace('time','duration')
                [object,quantity] = split_variable(variable)
            
            if 'spinup' in variable:
                variable = variable.replace('spinup_','')\
                    .replace('model','model_spinup')\
                    .replace('time','duration')
                [object,quantity] = split_variable(variable)

            if 'firing' in quantity:
                variable = variable.replace('firing_','')\
                    .replace('projectile','projectile_firing')
                [object,quantity] = split_variable(variable)

            if 'deposition' in quantity:
                variable = variable.replace('deposition_','')\
                    .replace('sediment','sediment_deposition')
                [object,quantity] = split_variable(variable)

            if 'surge' in quantity:
                variable = variable.replace('surge_','')\
                    .replace('water','water_surge')
                [object,quantity] = split_variable(variable)

            if 'refraction' in quantity:
                variable = variable.replace('refraction_','')\
                    .replace('wave','wave_refraction')
                [object,quantity] = split_variable(variable)

            if 'blowing' in quantity:
                variable = variable.replace('blowing_','')\
                    .replace('snow','snow_blowing')
                [object,quantity] = split_variable(variable)

            if 'freeze' in quantity:
                variable = variable.replace('freeze_','')\
                    .replace('soil','soil_freezing')
                [object,quantity] = split_variable(variable)

            if 'thaw' in quantity:
                variable = variable.replace('thaw_','')\
                    .replace('soil','soil_thawing')
                [object,quantity] = split_variable(variable)

            if 'recharge' in quantity:
                variable = variable.replace('recharge_','')\
                    .replace('__','_recharge__')
                [object,quantity] = split_variable(variable)

            if 'decomposition' in quantity:
                if not 'respiration' in quantity and not 'mineralization' in quantity:
                    variable = variable.replace('_carbon','-as-carbon')\
                            .replace('decomposition_','').replace('carbon','carbon_decomposition')
                    [object,quantity] = split_variable(variable)

            if 'respiration' in quantity and 'decomposition' in quantity:
                variable = variable.replace('respiration_','')\
                    .replace('decomposition_','')\
                    .replace('residue','residue_decomposition')\
                    .replace('stabilized','stabilized_decomposition')\
                    .replace('soil_','soil_decomposition_')\
                    .replace('carbon','carbon_respiration')
                [object,quantity] = split_variable(variable)

            if 'leaching' in quantity:
                variable = variable.replace('leaching_','')\
                        .replace('ammonium_','ammonium_leaching_')\
                        .replace('nitrate_','nitrate_leaching_')\
                        .replace('nitrogen','nitrogen_leaching')
                if 'drainage' in quantity:
                    variable = variable.replace('drainage_','')\
                        .replace('water','water_drainage')
                [object,quantity] = split_variable(variable)

            if 'mineralization' in quantity:
                variable = variable.replace('mineralization_','')\
                        .replace('nitrogen','nitrogen_mineralization')
                if 'decomposition' in variable:
                    variable = variable.replace('decomposition_','')\
                        .replace('organic','organic_decomposition')
                [object,quantity] = split_variable(variable)

            if 'nitrification' in quantity:
                if 'denitrification' in quantity:
                    if 'nitrous' in variable:
                        variable = variable.replace('denitrification_','')\
                            .replace('soil', 'soil_as-nitrogen_denitrification')
                    else:
                        variable = variable.replace('denitrification_','')\
                            .replace('nitrogen', 'nitrogen_denitrification')\
                            .replace('soil_nitrogen','soil_as-nitrogen')
                else:
                    if 'nitrous' in variable:
                        variable = variable.replace('nitrification_','')\
                            .replace('soil', 'soil_as-nitrogen_nitrification')
                    else:
                        variable = variable.replace('nitrification_','')\
                            .replace('nitrogen', 'nitrogen_nitrification')\
                            .replace('soil_nitrogen','soil_as-nitrogen')
                [object,quantity] = split_variable(variable)
                print(object, quantity)
                            
            if 'simulation' in quantity:
                variable = variable.replace('simulation_','')\
                            .replace('model','model_simulation')
                [object,quantity] = split_variable(variable)

            if 'observation' in quantity:
                variable = variable.replace('observation_','')
                variable = 'observation_' + variable
                [object,quantity] = split_variable(variable)
                            
            if 'planting' in variable:
                if 'from-planting' in variable:
                    variable = variable.replace('from-','since-')
                elif 'planting_or_sowing' in variable:
                    variable = variable.replace('planting_or_sowing_','')\
                            .replace('crop','crop_planting-or-sowing')
                else:
                    variable = variable.replace('planting_','')\
                                .replace('crop','crop_planting')
                [object,quantity] = split_variable(variable)

            for term in ['dissociation','protection','incubation','volatilization',
                        'immobilization','addition','fixation','lowering',
                        'propelling','dilation','takeoff', 'compaction']:
                if term in quantity.split('_'):
                    variable = variable.replace(term+'_','')\
                                .replace('__','_'+term+'__')
                    [object,quantity] = split_variable(variable)

            # move attribute from quantity to object
            if 'saturated' in quantity:
                variable = variable.replace('saturated_','')\
                    .replace('air','air~saturated')\
                    .replace('soil_water','soil~saturated_water')\
                    .replace('soil_macropores','soil_macropores~saturated')\
                    .replace('soil_layer~top','soil_layer~top~saturated')\
                    .replace('soil_layer~0','soil_layer~0~saturated')\
                    .replace('soil_layer~1','soil_layer~1~saturated')\
                    .replace('soil_layer~2','soil_layer~2~saturated')\
                    .replace('soil_active-layer','soil_active-layer~saturated')\
                    .replace('soil__','soil~saturated__')\
                    .replace('sediment','sediment~saturated')\
                    .replace('atmosphere_water~vapor','atmosphere_air~saturated_water~vapor')
                [object,quantity] = split_variable(variable)

            if 'backscattered' in quantity:
                variable = variable.replace('__backscattered','~backscattered_')
                [object,quantity] = split_variable(variable)

            if 'field-capacity' in quantity:
                variable = variable.replace('__field-capacity','_at-field_capacity_')

            for term in ['isochoric','isobaric','isentropic','isothermal','adiabatic']:
                if term in quantity and ('material' in object or 'ice' in object or 'snow' in object or 'water' in object \
                    or 'air' in object or 'aluminum' in object or 'chocolate' in object or 'anvil' in object or 'tile' in object \
                    or 'soil' in object):
                    variable = variable.replace(term+'_','')\
                                .replace('air_','air_'+term+'-process_')\
                                .replace('water_','water_'+term+'-process_')\
                                .replace('ice_','ice_'+term+'-process_')\
                                .replace('air~saturated_','air~saturated_'+term+'-process_')\
                                .replace('snow_','snow_'+term+'-process_')\
                                .replace('soil_','soil_'+term+'-process_')\
                                .replace('chocolate_','chocolate_'+term+'-process_')\
                                .replace('material_','material_'+term+'-process_')\
                                .replace('snowpack_','snowpack_'+term+'-process_')\
                                .replace('tile_','tile_'+term+'-process_')\
                                .replace('anvil_','anvil_'+term+'-process_')\
                                .replace('aluminum_','aluminum_'+term+'-process_')
                [object,quantity] = split_variable(variable)

            if 'point' in quantity:
                variable = variable.replace('_point','-point')
                state = variable.split('-point')[0].split('_')[-1] + '-point'
                variable = variable.replace(state + '_', '')\
                        .replace('atmosphere_water','atmosphere_air_water')\
                        .replace('water~vapor','water~vapor~'+state)\
                        .replace('chocolate','chocolate~'+state)\
                        .replace('ice','ice~'+state)\
                        .replace('water_','water~'+state+'_')\
                        .replace('iron','iron~'+state)
                [object,quantity] = split_variable(variable)

            if 'dry' in quantity:
                variable = variable.replace('dry_','')\
                            .replace('air','air~dry')\
                            .replace('soil','soil~dry')
                [object,quantity] = split_variable(variable)

            for term in ['oven-dried','air-dried']:   
                if term in quantity:
                    variable = variable.replace(term+'_','')\
                            .replace('soil','soil~'+term)

            if 'equilibrium' in quantity:
                variable = variable.replace('equilibrium_','')\
                            .replace('carbon-dioxide','carbon-dioxide~equilibrium')\
                            .replace('water~vapor','water~vapor~equilibrium')
                [object,quantity] = split_variable(variable)

            if 'bankfull' in quantity:
                variable = variable.replace('bankfull_','')\
                        .replace('basin','basin~bankfull')
                [object,quantity] = split_variable(variable)

            if 'immersed' in quantity:
                variable = variable.replace('immersed_','')\
                            .replace('bedload','bedload~immersed')\
                            .replace('sediment_','sediment~immersed_')

            # disambiguate quantities and make uniform
            if 'lapse_rate' in quantity and 'temperature' in quantity:
                variable = variable.replace('temperature_','')\
                    .replace('lapse_rate','temperature_lapse_rate')
                [object,quantity] = split_variable(variable)

            if 'lapse_rate' in quantity and 'static_pressure' in quantity:
                variable = variable.replace('static_pressure_','')\
                    .replace('lapse_rate','static_pressure_lapse_rate')
                [object,quantity] = split_variable(variable)

            if 'viscosity' in quantity:
                variable = variable.replace('dynamic_shear','shear_dynamic')\
                            .replace('kinematic_shear','shear_kinematic')\
                            .replace('dynamic_volume','volume_dynamic')\
                            .replace('kinematic_volume','volume_kinematic')
                [object,quantity] = split_variable(variable)

            # move form from quantity to object
            if '_bulk_' in quantity or quantity.startswith('bulk'):
                if not 'modulus' in quantity:
                    variable = variable.replace('bulk_','').replace('__','_bulk__')
                [object,quantity] = split_variable(variable)

            # move quantity from object to quantity
            if 'heat' in object:
                if 'heat_flow' in object:
                    variable = variable.replace('heat_','')\
                            .replace('roughness','heat_roughness')
                elif 'heat~' in object:
                    heat_term = variable.split('__')[0].split('_')[-1]
                    variable = variable.replace(heat_term + '_','')
                    heat_unpacked = '_'.join(reversed(heat_term.split('~')))
                    if '_net_' in heat_unpacked:
                        heat_unpacked = 'net_' + heat_unpacked.replace('net_','')
                    if '_incoming_' in heat_unpacked:
                        heat_unpacked = 'incoming_' + heat_unpacked.replace('incoming_','')
                    variable = variable.replace('energy',heat_unpacked+'_energy')
                    for term in ['advection','convection','diffusion','conduction']:
                        if term in variable:
                            variable = variable.replace(term+'_','')\
                                    .replace('__','_'+term+'__')
                    for term in ['frictional','geothermal']:
                        if term in variable:
                            variable = variable.replace(term+'_','')\
                                    .replace('conduction',term+'-conduction')
                            if 'conduction' not in variable:
                                variable = variable.replace('__','_'+term+'-conduction'+'__')
                elif '_heat' in object:
                    variable = variable.replace('heat_','')\
                            .replace('diffusion','heat_diffusion')
                [object,quantity] = split_variable(variable)

            if 'energy~' in object:
                energy_term = variable.split('__')[0].split('_')[-1]
                energy_term_reverse = '_'.join(reversed(energy_term.split('~')))
                variable = variable.replace(energy_term + '_','')\
                            .replace('diffusion',energy_term_reverse+'_diffusion')
                [object,quantity] = split_variable(variable)

            if 'equation~' in object:
                variable = variable.replace('equation~','')\
                    .replace('__','-equation__')
                [object,quantity] = split_variable(variable)

            # fix post processing
            variable = variable.replace('__pressure_temperature','_at-air_pressure__temperature')\
                        .replace('fertilizer~nitrogen','nitrogen-fertilizer')\
                        .replace('sulfuric-acid_solution','sulfuric-acid-solution')\
                        .replace('land-surface','land_surface')\
                        .replace('channel~stream','stream_channel')\
                        .replace('channel~river','river_channel')\
                        .replace('~along','_along')\
                        .replace('forage-harvest','forage_harvest')\
                        .replace('graph~tree~rooted','rooted-tree-graph')\
                        .replace('ice~above-bed','ice_above-bed')\
                        .replace('pole~north~magnetic','magnetic-north-pole')\
                        .replace('pole~south~magnetic','magnetic-south-pole')\
                        .replace('_wave~incoming','_water_wave~incoming')\
                        .replace('wave~electromagnetic','electromagnetic-wave')\
                        .replace('wave~acoustic','acoustic-wave')\
                        .replace('wave~airy','airy-wave')\
                        .replace('wave~cnoidal','cnoidal-wave')\
                        .replace('wave~gravity','gravity-wave')\
                        .replace('wave~ocean','ocean_water_wave')\
                        .replace('wave~seismic','seismic-wave')\
                        .replace('wave~sine','sine-wave')\
                        .replace('wave~stokes','stokes-wave')\
                        .replace('shale~burgess','burgess-shale')\
                        .replace('building~empire-state','empire-state-building')\
                        .replace('region_state','constituent-state')

            variable = variable.replace('antoine_vapor_pressure','antoine-vapor-pressure')\
                            .replace('ashton_et_al','ashton-et-al')\
                            .replace('beer_lambert_law','beer-lambert-law')\
                            .replace('volume_flow_rate_law','volume-flow-rate-law')\
                            .replace('van-genuchten_beta','van-genuchten_alpha')\
                            .replace('power_law_viscosity_law','power-law-viscosity-law')\
                            .replace('sulphuric-acid','sulfuric-acid')\
                            .replace('modified_omori_law','modified-omori-law')\
                            .replace('herschel_bulkley','herschel-bulkley')\
                            .replace('flint_law','flint-law')\
                            .replace('gutenberg-richter_law','gutenberg-richter-law')\
                            .replace('hack_law','hack-law')\
                            .replace('hooke_law','hooke-law')\
                            .replace('glen_law','glen-law')\
                            .replace('chezy_formula','chezy-formula')\
                            .replace('log_law','log-law')\
                            .replace('tolman_oppenheimer_volkoff_limit','tolman-oppenheimer-volkoff-limit')\
                            .replace('von_karman','von-karman')\
                            .replace('volume-vs-area_law','volume-vs-area-law')\
                            .replace('twin_prime','twin-prime')\
                            .replace('planck_charge','planck_electric-charge')\
                            .replace('motor-trend-magazine-safety','motor-trend-magazine_safety')\
                            .replace('moment_magnitude','moment-magnitude_scale')\
                            .replace('mole_concentration','molar_concentration')\
                            .replace('modified_mercali_intensity', 'modified-mercalli-intensity_scale')\
                            .replace('modified_mercalli_intensity','modified-mercalli-intensity_scale')\
                            .replace('richter_magnitude','richter-magnitude_scale')\
                            .replace('apparent_magnitude','apparent-magnitude_scale')\
                            .replace('mass-per_','mass-per-')\
                            .replace('manning','manning-formula')\
                            .replace('width_vs_discharge','width-vs-discharge')\
                            .replace('length-to-area_ratio','length-per-area_density')\
                            .replace('channels','channel-network')\
                            .replace('total_contributing','contributing')\
                            .replace('total_length','length')\
                            .replace('total_distance','distance')\
                            .replace('total_duration','duration')\
                            .replace('~total','')\
                            .replace('~all','')\
                            .replace('steepness','slope')\
                            .replace('porsche~911','porsche-911')\
                            .replace('msl','mean-sea-level')\
                            .replace('stefan_boltzmann','stefan-boltzmann')\
                            .replace('shields_number','shields_parameter')\
                            .replace('brunt_vaisala','brunt-vaisala')\
                            .replace('casson_model','casson-model')\
                            .replace('chandrasekhar_limit','chandrasekhar-limit')\
                            .replace('power-per-length','power-per-length_density')\
                            .replace('magnetic-field-strength','magnetic-h-field')\
                            .replace('magnetic-field','magnetic-b-field')\
                            .replace('incompressibility','compressibility')\
                            .replace('golden_ratio','golden-ratio')\
                            .replace('tillage','tilling')\
                            .replace('impedance_constant','electrical_impedance_constant')\
                            .replace('gravitational_coupling','gravitational-coupling')\
                            .replace('thermal_expansion_coefficient','thermal_volume_expansion_coefficient')\
                            .replace('specific_energy_content','energy-per-mass_density')\
                            .replace('specific_fluid_permeability','absolute_permeability')\
                            .replace('current~rip','rip-current')\
                            .replace('current~longshore','longshore-current')\
                            .replace('relative_roughness_ratio','relative_hydraulic_roughness')\
                            .replace('relative_smoothness_ratio','relative_hydraulic_smoothness')\
                            .replace('suceptibility','susceptibility')\
                            .replace('electric-polarization','electric-p-field')\
                            .replace('electric-field-potential','electric_potential')\
                            .replace('electric-field','electric-e-field')\
                            .replace('electric-displacement','electric-d-field')\
                            .replace('elementary_charge','elementary-electric-charge')\
                            .replace('blood_cell~red','red-blood-cell')\
                            .replace('blood_cell~white','white-blood-cell')\
                            .replace('electric_permittivity','permittivity')\
                            .replace('seismic-wave~rayleigh','rayleigh-seismic-wave')\
                            .replace('seismic-wave~love','love-seismic-wave')\
                            .replace('seismic-wave~p','p-seismic-wave')\
                            .replace('seismic-wave~sh','sh-seismic-wave')\
                            .replace('seismic-wave~sv','sv-seismic-wave')\
                            .replace('seismic-wave~s','s-seismic-wave')\
                            .replace('dielectric_constant','relative_permittivity')\
                            .replace('casson-model_k_parameter','casson-model_a_parameter')\
                            .replace('thermal_quality_ratio','thermal_quality')\
                            .replace('thermal_energy_content','thermal_energy-per-volume_density')\
                            .replace('standard_gravity_constant','standard_gravitational_acceleration')\
                            .replace('universe~friedmann','friedmann-universe')\
                            .replace('watershed','drainage-basin')\
                            .replace('__factor','__spf_rating')\
                            .replace('fine_structure','fine-structure')\
                            .replace('_roll_','_rolling_')\
                            .replace('count-per-volume','count-per-volume_density')\
                            .replace('cost_per_mass','cost-per-mass')\
                            .replace('meander','meandering')\
                            .replace('alpha-hexachlorocyclohexane','alpha-hch')\
                            .replace('oak~bluejack','bluejack-oak')\
                            .replace('__cold_content','__cold_energy-per-area_density')\
                            .replace('date','time')\
                            .replace('energy-per-area_cold_content','cold_energy-per-area_density')\
                            .replace('layer~base','base-layer')\
                            .replace('layer~top_','layer~topmost_')\
                            .replace('layer~top~','layer~topmost~')\
                            .replace('skin__average_of_temperature','_average_of_skin_temperature')\
                            .replace('node~dual~x','x-dual-node')\
                            .replace('node~dual~y','y-dual-node')\
                            .replace('node~dual~z','z-dual-node')\
                            .replace('node~dual','dual-node')\
                            .replace('node~primary~x','x-primary-node')\
                            .replace('node~primary~y','y-primary-node')\
                            .replace('node~primary~z','z-primary-node')\
                            .replace('node~primary','primary-node')\
                            .replace('cell~dual','dual-cell')\
                            .replace('cell~primary','primary-cell')\
                            .replace('atmosphere_carbon-dioxide','atmosphere_air_carbon-dioxide')\
                            .replace('atmosphere_water~vapor','atmosphere_air_water~vapor')\
                            .replace('plain~subaqueous_plain','plain_plain~subaqueous')\
                            .replace('material_melt_carbonatite__fraction','material~melt_carbonatite__mass_fraction')\
                            .replace('partial-melt__fraction','partial-melt__mass_fraction')\
                            .replace('station~seismic','seismic-station')\
                            .replace('_station_','_seismic-station_')\
                            .replace('max_of_allowed','allowed_max_of')\
                            .replace('min_of_allowed','allowed_min_of')\
                            .replace('__stress_period','_stress-period_')\
                            .replace('land~flooded__max_of_depth','land~flooded_water__max_of_depth')\
                            .replace('above-bottom','above-sea_bottom')\
                            .replace('below-surface','below-sea_surface')\
                            .replace('__diffusivity','__mass_diffusivity')\
                            .replace('spring~steel','steel-spring')
            
            if '_flow' in object:
                variable = variable.replace('_flow_','_flowing_')

            if 'flowing_sediment~suspended' in variable:
                variable = variable.replace('flowing_sediment~suspended','sediment~suspended_flowing')

            if 'flowing_snow~suspended' in variable:
                variable = variable.replace('flowing_snow~suspended','snow~suspended_flowing')
            
            if 'flowing_sediment~bedload' in variable:
                variable = variable.replace('flowing_sediment~bedload','sediment~bedload_flowing')

            if 'flowing_sediment~washload' in variable:
                variable = variable.replace('flowing_sediment~washload','sediment~washload_flowing')

            if 'flowing_sediment_' in variable:
                variable = variable.replace('flowing_sediment','sediment_flowing')

            if 'flowing_grain' in variable:
                variable = variable.replace('flowing_grain','grain_flowing')
                
            if 'flowing_x-section_sediment~suspended' in variable:
                variable = variable.replace('flowing_x-section_sediment~suspended','sediment~suspended_flowing_x-section')  

            variable = variable.replace('water_flowing_debris_flowing','water_debris_flowing')     
            [object,quantity] = split_variable(variable)

            if 'incoming' in quantity:
                variable = variable.replace('incoming','incoming_component_of')
                [object,quantity] = split_variable(variable)

            if 'downstream_volume' in quantity:
                variable = variable.replace('downstream','downstream_component_of')
                [object,quantity] = split_variable(variable)
            
            if 'upstream' in quantity:
                variable = variable.replace('upstream','upstream_component_of')
                [object,quantity] = split_variable(variable)

            if 'diffusion_coefficient' in quantity:
                if 'salt' in object:
                    variable = variable.replace('diffusion_coefficient','mass_diffusivity')
                else:
                    variable = variable.replace('diffusion_coefficient','diffusivity')
                [object,quantity] = split_variable(variable)

            if 'interbed' in object:
                variable = variable.replace('interbed~no-delay','no-delay-interbed')\
                            .replace('interbed~delay','delay-interbed')\
                            .replace('interbed_system~delay','delay-interbed_system')\
                            .replace('interbed_system~no-delay','no-delay-interbed_system')
                [object,quantity] = split_variable(variable)

            if 'mineral-phase' in variable:
                variable = variable.replace('melt~partial','partial-melt')\
                        .replace('melt_carbonatite_mineral-phase','mineral-phase~melt_carbonatite')\
                        .replace('partial-melt_mineral-phase','mineral-phase_partial-melt')\
                        .replace('_mineral-phase','~mineral-phase')\
                        .replace('__fraction','__mass_fraction')\
                        .replace('material~mineral-phase__mass_fraction','material_material~mineral-phase__mass_fraction')
                [object,quantity] = split_variable(variable)

            if 'solar_constant' in quantity:
                variable = 'sun_' + variable
                [object,quantity] = split_variable(variable)

            if 'partial-melt' in variable:
                variable = variable.replace('partial-melt','material~partial-melt')
                [object,quantity] = split_variable(variable)

            if 'phreatic-zone' in variable and 'recharge' in variable:
                variable = variable.replace('soil_water_phreatic-zone_top','soil_phreatic-zone_top_water')
                [object,quantity] = split_variable(variable)

            if variable in ['automobile_carbon-dioxide_emission__rate',
                            'automobile_fuel_consumption__rate','human_alcohol_consumption__rate']:
                variable = variable.replace('rate','mass-per-length_rate')
                [object,quantity] = split_variable(variable)

            if variable in ['channel_bottom_sediment_oxygen~dissolved_consumption__rate',
                            'channel_water_oxygen~photosynthetic_production__rate']:
                variable = variable.replace('rate','mass-per-time_rate')
                [object,quantity] = split_variable(variable)

            if quantity in ['mean_of_rate','rate']:
                variable = variable.replace('rate','length-per-time_rate')
                [object,quantity] = split_variable(variable)

            if quantity == 'fraction':
                variable = variable.replace('fraction','volume_fraction')
                [object,quantity] = split_variable(variable)      
                
            # write edited variable to file
            dst_f.write(variable_original + ', ' + variable + '\n')

            if wordy:
                if variable_original != variable:
                    print(variable_original, ',', variable)
                    input("Press Enter to continue...")
