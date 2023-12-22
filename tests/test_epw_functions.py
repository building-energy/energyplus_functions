# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 20:49:07 2023

@author: cvskf
"""

import unittest
from energyplus_functions import epw_functions
from energyplus_functions import eplus_functions
import pandas as pd
import json

class TestEPCFunctions(unittest.TestCase):
    ""
    
    def test_1_convert_epw_to_csvw(self):
        ""
        
        
        csvw_metadata_dict, csvw_csv_string = \
            epw_functions.convert_epw_to_csvw(
                'USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
                csvw_csv_filename = 'test.csv'
                )
        
        #print(csvw_metadata_dict)
        #print(csvw_csv_string[:1000])



    def test_2_convert_csvw_to_epw(self):
        ""
        
        
        epw_functions.convert_csvw_to_epw(
            'test.csv-metadata.json'
            )



    def test_3_create_simple_epw(self):
        ""
        
        null_metadata_dict, null_csv = \
            epw_functions.create_null_csvw(
                'null.csv'
                )
        
        
        epw_functions.convert_epw_to_csvw(
            'USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
            csvw_csv_filename = 'simple.csv'
            )
        
        # --- modify metadata json ---
        # this changes it to match the 'null' metadata
        with open('simple.csv-metadata.json') as f:
            metadata_dict = json.load(f)
            
        metadata_dict['https://purl.org/berg/epw_vocab#location'] = \
            null_metadata_dict['https://purl.org/berg/epw_vocab#location']
            
        metadata_dict['https://purl.org/berg/epw_vocab#design_conditions'] = \
            null_metadata_dict['https://purl.org/berg/epw_vocab#design_conditions']
            
        metadata_dict['https://purl.org/berg/epw_vocab#typical_or_extreme_periods'] = \
            null_metadata_dict['https://purl.org/berg/epw_vocab#typical_or_extreme_periods']
            
        metadata_dict['https://purl.org/berg/epw_vocab#ground_temperatures'] = \
            null_metadata_dict['https://purl.org/berg/epw_vocab#ground_temperatures']
            
        metadata_dict['https://purl.org/berg/epw_vocab#holiday_and_daylight_savings'] = \
            null_metadata_dict['https://purl.org/berg/epw_vocab#holiday_and_daylight_savings']
            
        metadata_dict['https://purl.org/berg/epw_vocab#comments_1'] = \
            null_metadata_dict['https://purl.org/berg/epw_vocab#comments_1']
            
        metadata_dict['https://purl.org/berg/epw_vocab#comments_2'] = \
            null_metadata_dict['https://purl.org/berg/epw_vocab#comments_2']
            
        metadata_dict['https://purl.org/berg/epw_vocab#data_periods'] = \
            null_metadata_dict['https://purl.org/berg/epw_vocab#data_periods']
            
        with open('simple.csv-metadata.json','w') as f:
              json.dump(metadata_dict,f,indent=4)
              
        # --- modify csv file ---
        df = pd.read_csv('simple.csv')
        df_null = pd.read_csv('null.csv')
        
        
        df.year = df_null.year
        df.month = df_null.month
        df.day = df_null.day
        df.hour = df_null.hour
        df.minute = df_null.minute
        df.data_source_and_uncertainty_flags = df_null.data_source_and_uncertainty_flags
        df.dry_bulb_temperature = df_null.dry_bulb_temperature
        df.dew_point_temperature = df_null.dew_point_temperature
        df.relative_humidity = df_null.relative_humidity
        df.atmospheric_station_pressure = df_null.atmospheric_station_pressure
        df.extraterrestrial_horizontal_radiation = df_null.extraterrestrial_horizontal_radiation
        df.extraterrestrial_direct_normal_radiation = df_null.extraterrestrial_direct_normal_radiation
        df.horizontal_infrared_radiation_intensity = df_null.horizontal_infrared_radiation_intensity
        df.global_horizontal_radiation = df_null.global_horizontal_radiation
        df.direct_normal_radiation = df_null.direct_normal_radiation
        df.diffuse_horizontal_radiation = df_null.diffuse_horizontal_radiation
        df.global_horizontal_illuminance = df_null.global_horizontal_illuminance
        df.direct_normal_illuminance = df_null.direct_normal_illuminance
        df.diffuse_horizontal_illuminance = df_null.diffuse_horizontal_illuminance
        df.zentih_luminance = df_null.zentih_luminance
        df.wind_direction = df_null.wind_direction
        df.wind_speed = df_null.wind_speed
        df.total_sky_cover = df_null.total_sky_cover
        df.opaque_sky_cover = df_null.opaque_sky_cover
        df.visibility = df_null.visibility
        df.ceiling_height = df_null.ceiling_height
        df.present_weather_observation = df_null.present_weather_observation
        df.present_weather_codes = df_null.present_weather_codes
        df.precipitable_water = df_null.precipitable_water
        df.aerosol_optical_depth = df_null.aerosol_optical_depth
        df.snow_depth = df_null.snow_depth
        df.days_since_last_snowfall = df_null.days_since_last_snowfall
        df.albedo = df_null.albedo
        df.liquid_precipitation_depth = df_null.liquid_precipitation_depth
        df.liquid_precipitation_quantity = df_null.liquid_precipitation_quantity
        
        df.to_csv(
            'simple.csv', 
            index=False
            )
              
        # convert csvw to epw
        epw_functions.convert_csvw_to_epw(
            'simple.csv-metadata.json'
            )

        # run energyplus
        eplus_functions.run_energyplus(
            r'C:\Users\cvskf\EnergyPlusV23-2-0',
            idf_filepath = 'in.idf',
            epw_filepath = 'simple.epw'
            )
        
        try:
            with open('eplusout.err') as f:
                message2 = f.read()
        except FileNotFoundError:
            message2 = 'No .err file found'
        print(message2)


if __name__ == "__main__":
    
    unittest.main()
