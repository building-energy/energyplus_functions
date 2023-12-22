# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 20:48:37 2023

@author: cvskf
"""

import csv
import io
import json
import importlib.resources
import energyplus_functions
import os


def create_null_csvw(
        csv_filepath
        ):
    """Creates a CSV file and CSVW metadata file with no data.
    
    """
    
    # read default metadata dict from package .json file
    file = importlib.resources.files(energyplus_functions) / 'epw.csv-metadata.json'  # see https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
    #print(file)
    with file.open() as f:
        csvw_metadata_dict = json.load(f)
        
    # update "url"
    csvw_metadata_dict['url'] = csv_filepath
        
    # save metadata dict
    fp = f'{csv_filepath}-metadata.json'
    with open(fp, 'w') as f:
        json.dump(
            csvw_metadata_dict,
            f,
            indent = 4
            )
    
    # read csv file
    file = importlib.resources.files(energyplus_functions) / 'epw.csv'
    with file.open() as f:
        csv_string = f.read()
        
    # save csv file
    with open(csv_filepath, 'w') as f:
        f.write(csv_string)
    
    return csvw_metadata_dict, csv_string



def convert_epw_to_csvw(
        epw_filename_or_string,
        csvw_csv_filename=None
        ):
    """Converts an EnergyPlus weather file to a CSVW file.
    
    :param epw_filename_or_string: Either:
        - a filepath to an EPW file
        - a string containing the text of an EPW file
    :type epw_filename_or_string: string   
    
    :returns: A 2-item tuple (
        CSVW metadata file (as a dict),
        CSV file (as a string)
        )
    
    """
    
    # get epw string
    try:  # is the argument a filepath to a local file?
        with open(epw_filename_or_string, newline='') as f:
            epw_string = f.read()
    except FileNotFoundError:  # the argument is a string containing the text of an EPW file
        epw_string = epw_filename_or_string
        
    # parse as csv.reader instance
    epw_stringio = io.StringIO(epw_string)  # StringIO instance is needed for use with csv.reader
    csvreader = csv.reader(epw_stringio)
    
    # read default metadata dict from package .json file
    file = importlib.resources.files(energyplus_functions) / 'epw.csv-metadata.json'  # see https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
    #print(file)
    with file.open() as f:
        csvw_metadata_dict = json.load(f)
    
    # setup csv writer
    csvw_csv_stringio = io.StringIO()  # StringIO instance is needed for use with csv.writer
    csvwriter = csv.writer(csvw_csv_stringio)
    
    # write header row
    headers = [x['titles'] for x in csvw_metadata_dict['tableSchema']['columns']]
    
    csvwriter.writerow(headers)
    
    for line in csvreader:
        
        #print(line)
        
        if line[0]=='LOCATION':
            
            csvw_metadata_dict['https://purl.org/berg/epw_vocab#location'] = \
                _convert_location_epw_to_csvw(
                        line
                        )
            
        elif line[0]=='DESIGN CONDITIONS':
            
            csvw_metadata_dict['https://purl.org/berg/epw_vocab#design_conditions'] = \
                _convert_design_conditions_epw_to_csvw(
                        line
                        )
                
        elif line[0]=='TYPICAL/EXTREME PERIODS':
            
            csvw_metadata_dict['https://purl.org/berg/epw_vocab#typical_or_extreme_periods'] = \
                _convert_typical_or_extreme_periods_epw_to_csvw(
                        line
                        )
                
        elif line[0]=='GROUND TEMPERATURES':
            
            csvw_metadata_dict['https://purl.org/berg/epw_vocab#ground_temperatures'] = \
                _convert_ground_temperatures_epw_to_csvw(
                        line
                        )
                
        elif line[0]=='HOLIDAYS/DAYLIGHT SAVINGS':
            
            csvw_metadata_dict['https://purl.org/berg/epw_vocab#holiday_and_daylight_savings'] = \
                _convert_holiday_and_daylight_savings_epw_to_csvw(
                        line
                        )
                
        elif line[0]=='COMMENTS 1':
            
            csvw_metadata_dict['https://purl.org/berg/epw_vocab#comments_1'] = \
                _convert_comments_1_epw_to_csvw(
                        line
                        )
                
        elif line[0]=='COMMENTS 2':
            
            csvw_metadata_dict['https://purl.org/berg/epw_vocab#comments_2'] = \
                _convert_comments_2_epw_to_csvw(
                        line
                        )
                
        elif line[0]=='DATA PERIODS':
            
            csvw_metadata_dict['https://purl.org/berg/epw_vocab#data_periods'] = \
                _convert_data_periods_epw_to_csvw(
                        line
                        )
                
        else: # it's a data row
            csvwriter.writerow(line)
            
    csvw_csv_string = csvw_csv_stringio.getvalue()
    
    if not csvw_csv_filename is None:
        
        # save metadata file
        csvw_metadata_dict['url'] = csvw_csv_filename
        with open(csvw_csv_filename+'-metadata.json','w') as f:
            json.dump(csvw_metadata_dict, f, indent = 4)
        
        
        # save csv file
        with open(csvw_csv_filename,'w',newline='') as f:
            f.write(csvw_csv_string)
    
    return (
        csvw_metadata_dict,
        csvw_csv_string
        )


def convert_csvw_to_epw(
        csvw_metadata_filepath
        ):
    """
    """
    
    epw_string = ''
    
    # load metadata
    with open(csvw_metadata_filepath) as f:
        metadata_dict = json.load(f)
        
        
    # add metadata
    epw_string += \
        _convert_location_csvw_to_epw(
                metadata_dict['https://purl.org/berg/epw_vocab#location']
                )
    epw_string += \
        _convert_design_conditions_csvw_to_epw(
                metadata_dict['https://purl.org/berg/epw_vocab#design_conditions']
                )
    epw_string += \
        _convert_typical_or_extreme_periods_csvw_to_epw(
                metadata_dict['https://purl.org/berg/epw_vocab#typical_or_extreme_periods']
                )
    epw_string += \
        _convert_ground_temperatures_csvw_to_epw(
                metadata_dict['https://purl.org/berg/epw_vocab#ground_temperatures']
                )
    epw_string += \
        _convert_holiday_and_daylight_savings_csvw_to_epw(
                metadata_dict['https://purl.org/berg/epw_vocab#holiday_and_daylight_savings']
                )
    epw_string += \
        _convert_comments_1_csvw_to_epw(
                metadata_dict['https://purl.org/berg/epw_vocab#comments_1']
                )
    epw_string += \
        _convert_comments_2_csvw_to_epw(
                metadata_dict['https://purl.org/berg/epw_vocab#comments_2']
                )
    epw_string += \
        _convert_data_periods_csvw_to_epw(
                metadata_dict['https://purl.org/berg/epw_vocab#data_periods']
                )
        
    # parse csv file
    fp_csv = metadata_dict['url']
    with open(fp_csv) as f:
        next(f)
        for line in f:
            epw_string += line
        
    # save epw
    fp_epw = os.path.splitext(fp_csv)[0] + '.epw'
    with open(fp_epw, 'w') as f:
        f.write(epw_string)
        
    
    
    
def _convert_location_epw_to_csvw(
        line
        ):
    """
    """
    city = line[1]
    state_province_region = line[2]
    country = line[3]
    source = line[4]
    WMO = line[5]
    latitude = float(line[6])
    longitude = float(line[7])
    timezone = float(line[8])
    elevation = float(line[9])
    
    d = {
        'https://purl.org/berg/epw_vocab#city': city,
        'https://purl.org/berg/epw_vocab#state_province_region': state_province_region,
        'https://purl.org/berg/epw_vocab#country': country,
        'https://purl.org/berg/epw_vocab#source': source,
        'https://purl.org/berg/epw_vocab#WMO': WMO,
        'https://purl.org/berg/epw_vocab#latitude': latitude,
        'https://purl.org/berg/epw_vocab#longitude': longitude,
        'https://purl.org/berg/epw_vocab#timezone': timezone,
        'https://purl.org/berg/epw_vocab#elevation': elevation
        }
    
    return d
    

def _convert_location_csvw_to_epw(
        metadata_dict
        ):
    """
    """
    city = metadata_dict['https://purl.org/berg/epw_vocab#city']
    state_province_region = metadata_dict['https://purl.org/berg/epw_vocab#state_province_region']
    country = metadata_dict['https://purl.org/berg/epw_vocab#country']
    source = metadata_dict['https://purl.org/berg/epw_vocab#source']
    WMO = metadata_dict['https://purl.org/berg/epw_vocab#WMO']
    latitude = metadata_dict['https://purl.org/berg/epw_vocab#latitude']
    longitude = metadata_dict['https://purl.org/berg/epw_vocab#longitude']
    timezone = metadata_dict['https://purl.org/berg/epw_vocab#timezone']
    elevation = metadata_dict['https://purl.org/berg/epw_vocab#elevation']
    
    line = [
        'LOCATION',
        city,
        state_province_region,
        country,
        source,
        WMO,
        str(latitude),
        str(longitude),
        str(timezone),
        str(elevation)
        ]
    
    line = ','.join(line) + '\n'
        
    return line
        

def _convert_design_conditions_epw_to_csvw(
        line
        ):
    """
    """
    number_of_design_conditions = int(line[1])
    design_condition_source = line[2]
    design_condition_type = line[3:]
    
    d = {
        'https://purl.org/berg/epw_vocab#number_of_design_conditions': number_of_design_conditions,
        'https://purl.org/berg/epw_vocab#design_condition_source': design_condition_source,
        'https://purl.org/berg/epw_vocab#design_condition_type': design_condition_type
        }
    
    return d


def _convert_design_conditions_csvw_to_epw(
        metadata_dict
        ):
    """
    """
    number_of_design_conditions = metadata_dict['https://purl.org/berg/epw_vocab#number_of_design_conditions']
    design_condition_source = metadata_dict['https://purl.org/berg/epw_vocab#design_condition_source']
    design_condition_type = metadata_dict['https://purl.org/berg/epw_vocab#design_condition_type']
    
    line = [
        'DESIGN CONDITIONS',
        str(number_of_design_conditions),
        design_condition_source
        ]
    
    line.extend([str(x) for x in design_condition_type])
    
    line = ','.join(line) + '\n'
        
    return line


def _convert_typical_or_extreme_periods_epw_to_csvw(
        line
        ):
    """
    """
    
    number_of_typical_or_extreme_periods = int(line[1])
    
    typical_or_extreme_periods_list = []
    
    for i in range(number_of_typical_or_extreme_periods):
        typical_or_extreme_period_name = line[i*4+2]
        typical_or_extreme_period_type = line[i*4+3]
        period_start_date = line[i*4+4]
        period_end_date = line[i*4+5]
        
        typical_or_extreme_periods_list.append(
            {
                'https://purl.org/berg/epw_vocab#typical_or_extreme_period_name': typical_or_extreme_period_name,
                'https://purl.org/berg/epw_vocab#typical_or_extreme_period_type': typical_or_extreme_period_type,
                'https://purl.org/berg/epw_vocab#period_start_date': period_start_date,
                'https://purl.org/berg/epw_vocab#period_end_date': period_end_date,
                }
            )
        
    d = {
        'https://purl.org/berg/epw_vocab#number_of_typical_or_extreme_periods': number_of_typical_or_extreme_periods,
        "https://purl.org/berg/epw_vocab#typical_or_extreme_periods_list": typical_or_extreme_periods_list
        }
    
    return d


def _convert_typical_or_extreme_periods_csvw_to_epw(
        metadata_dict
        ):
    """
    """
    
    number_of_typical_or_extreme_periods = metadata_dict['https://purl.org/berg/epw_vocab#number_of_typical_or_extreme_periods']
    typical_or_extreme_periods_list = metadata_dict['https://purl.org/berg/epw_vocab#typical_or_extreme_periods_list']
    
    line = [
        'TYPICAL/EXTREME PERIODS',
        str(number_of_typical_or_extreme_periods)
        ]
    
    for i in range(number_of_typical_or_extreme_periods):
        
        d = typical_or_extreme_periods_list[i]
        
        typical_or_extreme_period_name = d['https://purl.org/berg/epw_vocab#typical_or_extreme_period_name']
        typical_or_extreme_period_type = d['https://purl.org/berg/epw_vocab#typical_or_extreme_period_type']
        period_start_date = d['https://purl.org/berg/epw_vocab#period_start_date']
        period_end_date = d['https://purl.org/berg/epw_vocab#period_end_date']
        
        line.extend([
            typical_or_extreme_period_name,
            typical_or_extreme_period_type,
            period_start_date,
            period_end_date
            ])
    
    line = ','.join(line) + '\n'
        
    return line

    
def _convert_ground_temperatures_epw_to_csvw(
        line
        ):
    """
    """
    
    number_of_ground_temperatures = int(line[1])
    
    ground_temperatures_list = []
    
    for i in range(number_of_ground_temperatures):
        ground_temperature_depth = line[i*16+2]
        soil_conductivity = line[i*16+3]
        soil_density = line[i*16+4]
        soil_specific_heat = line[i*16+5]
        january_average_ground_temperature = line[i*16+6]
        february_average_ground_temperature = line[i*16+7]
        march_average_ground_temperature = line[i*16+8]
        april_average_ground_temperature = line[i*16+9]
        may_average_ground_temperature = line[i*16+10]
        june_average_ground_temperature = line[i*16+11]
        july_average_ground_temperature = line[i*16+12]
        august_average_ground_temperature = line[i*16+13]
        september_average_ground_temperature = line[i*16+14]
        october_average_ground_temperature = line[i*16+15]
        november_average_ground_temperature = line[i*16+16]
        december_average_ground_temperature = line[i*16+17]
        
        ground_temperatures_list.append(
            {
                'https://purl.org/berg/epw_vocab#ground_temperature_depth': ground_temperature_depth,
                'https://purl.org/berg/epw_vocab#soil_conductivity': soil_conductivity,
                'https://purl.org/berg/epw_vocab#soil_density': soil_density,
                'https://purl.org/berg/epw_vocab#soil_specific_heat': soil_specific_heat,
                'https://purl.org/berg/epw_vocab#january_average_ground_temperature': january_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#february_average_ground_temperature': february_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#march_average_ground_temperature': march_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#april_average_ground_temperature': april_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#may_average_ground_temperature': may_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#june_average_ground_temperature': june_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#july_average_ground_temperature': july_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#august_average_ground_temperature': august_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#september_average_ground_temperature': september_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#october_average_ground_temperature': october_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#november_average_ground_temperature': november_average_ground_temperature,
                'https://purl.org/berg/epw_vocab#december_average_ground_temperature': december_average_ground_temperature 
                }
            )
        
    d = {
        'https://purl.org/berg/epw_vocab#number_of_ground_temperatures': number_of_ground_temperatures,
        "https://purl.org/berg/epw_vocab#ground_temperatures_list": ground_temperatures_list
        }
    
    return d
    

def _convert_ground_temperatures_csvw_to_epw(
        metadata_dict
        ):
    """
    """
    
    number_of_ground_temperatures = metadata_dict['https://purl.org/berg/epw_vocab#number_of_ground_temperatures']
    ground_temperatures_list = metadata_dict['https://purl.org/berg/epw_vocab#ground_temperatures_list']
    
    line = [
        'GROUND TEMPERATURES',
        str(number_of_ground_temperatures)
        ]
    
    for i in range(number_of_ground_temperatures):
        
        d = ground_temperatures_list[i]
        
        ground_temperature_depth = d['https://purl.org/berg/epw_vocab#ground_temperature_depth']
        soil_conductivity = d['https://purl.org/berg/epw_vocab#soil_conductivity']
        soil_density = d['https://purl.org/berg/epw_vocab#soil_density']
        soil_specific_heat = d['https://purl.org/berg/epw_vocab#soil_specific_heat']
        january_average_ground_temperature = d['https://purl.org/berg/epw_vocab#january_average_ground_temperature']
        february_average_ground_temperature = d['https://purl.org/berg/epw_vocab#february_average_ground_temperature']
        march_average_ground_temperature = d['https://purl.org/berg/epw_vocab#march_average_ground_temperature']
        april_average_ground_temperature = d['https://purl.org/berg/epw_vocab#april_average_ground_temperature']
        may_average_ground_temperature = d['https://purl.org/berg/epw_vocab#may_average_ground_temperature']
        june_average_ground_temperature = d['https://purl.org/berg/epw_vocab#june_average_ground_temperature']
        july_average_ground_temperature = d['https://purl.org/berg/epw_vocab#july_average_ground_temperature']
        august_average_ground_temperature = d['https://purl.org/berg/epw_vocab#august_average_ground_temperature']
        september_average_ground_temperature = d['https://purl.org/berg/epw_vocab#september_average_ground_temperature']
        october_average_ground_temperature = d['https://purl.org/berg/epw_vocab#october_average_ground_temperature']
        november_average_ground_temperature = d['https://purl.org/berg/epw_vocab#november_average_ground_temperature']
        december_average_ground_temperature = d['https://purl.org/berg/epw_vocab#december_average_ground_temperature']
        
        line.extend([
            str(ground_temperature_depth),
            str(soil_conductivity),
            str(soil_density),
            str(soil_specific_heat),
            str(january_average_ground_temperature),
            str(february_average_ground_temperature),
            str(march_average_ground_temperature),
            str(april_average_ground_temperature),
            str(may_average_ground_temperature),
            str(june_average_ground_temperature),
            str(july_average_ground_temperature),
            str(august_average_ground_temperature),
            str(september_average_ground_temperature),
            str(october_average_ground_temperature),
            str(november_average_ground_temperature),
            str(december_average_ground_temperature)
            ])
    
    line = ','.join(line) + '\n'
        
    return line


def _convert_holiday_and_daylight_savings_epw_to_csvw(
        line
        ):
    """
    """
    
    leap_year_observed = line[1]
    daylight_saving_start_day = line[2]
    daylight_saving_end_day = line[3]
    number_of_holidays = int(line[4])
    
    holidays_list = []
    
    for i in range(number_of_holidays):
        holiday_name = line[i*2+5]
        hoilday_date = line[i*2+6]
        
        holidays_list.append(
            {
                'https://purl.org/berg/epw_vocab#holiday_name': holiday_name,
                'https://purl.org/berg/epw_vocab#hoilday_date': hoilday_date
                }
            )
    
    d = {
        'https://purl.org/berg/epw_vocab#leap_year_observed': leap_year_observed,
        'https://purl.org/berg/epw_vocab#daylight_saving_start_day': daylight_saving_start_day,
        'https://purl.org/berg/epw_vocab#daylight_saving_end_day': daylight_saving_end_day,
        'https://purl.org/berg/epw_vocab#number_of_holidays': number_of_holidays,
        'https://purl.org/berg/epw_vocab#holidays_list': holidays_list
        }
    
    return d


def _convert_holiday_and_daylight_savings_csvw_to_epw(
        metadata_dict
        ):
    """
    """
    leap_year_observed = metadata_dict['https://purl.org/berg/epw_vocab#leap_year_observed']
    daylight_saving_start_day = metadata_dict['https://purl.org/berg/epw_vocab#daylight_saving_start_day']
    daylight_saving_end_day = metadata_dict['https://purl.org/berg/epw_vocab#daylight_saving_end_day']
    number_of_holidays = metadata_dict['https://purl.org/berg/epw_vocab#number_of_holidays']
    holidays_list = metadata_dict['https://purl.org/berg/epw_vocab#holidays_list'] 
    
    line = [
        'HOLIDAYS/DAYLIGHT SAVINGS',
        leap_year_observed,
        daylight_saving_start_day,
        daylight_saving_end_day,
        str(number_of_holidays)
        ]
    
    for i in range(number_of_holidays):
        
        d = holidays_list[i]
        
        holiday_name = d['https://purl.org/berg/epw_vocab#holiday_name']
        hoilday_date = d['https://purl.org/berg/epw_vocab#hoilday_date']
        
        line.extend([
            holiday_name,
            hoilday_date
            ])
    
    line = ','.join(line) + '\n'
        
    return line


def _convert_comments_1_epw_to_csvw(
        line
        ):
    """
    """
    comments_1 = line[1]
    
    return comments_1
    

def _convert_comments_1_csvw_to_epw(
        metadata_dict
        ):
    """
    """
    comments_1 = metadata_dict
    
    line = [
        'COMMENTS 1',
        comments_1
        ]
    
    line = ','.join(line) + '\n'
        
    return line


def _convert_comments_2_epw_to_csvw(
        line
        ):
    """
    """
    comments_2 = line[1]
    
    return comments_2


def _convert_comments_2_csvw_to_epw(
        metadata_dict
        ):
    """
    """
    comments_2 = metadata_dict
    
    line = [
        'COMMENTS 2',
        comments_2
        ]
    
    line = ','.join(line) + '\n'
        
    return line

    
def _convert_data_periods_epw_to_csvw(
        line
        ):
    """
    """
    number_of_data_periods = int(line[1])
    number_of_records_per_hour = int(line[2])
    
    data_periods_list = []
    
    for i in range(number_of_data_periods):
        data_period_name_and_description = line[i*4+3]
        data_period_start_date_of_week = line[i*4+4]
        data_period_start_day = line[i*4+5]
        data_period_end_day = line[i*4+6]
        
        data_periods_list.append(
            {
                'https://purl.org/berg/epw_vocab#data_period_name_and_description': data_period_name_and_description,
                'https://purl.org/berg/epw_vocab#data_period_start_date_of_week': data_period_start_date_of_week,
                'https://purl.org/berg/epw_vocab#data_period_start_day': data_period_start_day,
                'https://purl.org/berg/epw_vocab#data_period_end_day': data_period_end_day
                }
            )
    
    d = {
        'https://purl.org/berg/epw_vocab#number_of_data_periods': number_of_data_periods,
        'https://purl.org/berg/epw_vocab#number_of_records_per_hour': number_of_records_per_hour,
        'https://purl.org/berg/epw_vocab#data_periods_list': data_periods_list
        }
    
    return d
    

def _convert_data_periods_csvw_to_epw(
        metadata_dict
        ):
    """
    """
    number_of_data_periods = metadata_dict['https://purl.org/berg/epw_vocab#number_of_data_periods']
    number_of_records_per_hour = metadata_dict['https://purl.org/berg/epw_vocab#number_of_records_per_hour']
    data_periods_list = metadata_dict['https://purl.org/berg/epw_vocab#data_periods_list']
    
    line = [
        'DATA PERIODS',
        str(number_of_data_periods),
        str(number_of_records_per_hour)
        ]
    
    for i in range(number_of_data_periods):
        
        d = data_periods_list[i]
        
        data_period_name_and_description = d['https://purl.org/berg/epw_vocab#data_period_name_and_description']
        data_period_start_date_of_week = d['https://purl.org/berg/epw_vocab#data_period_start_date_of_week']
        data_period_start_day = d['https://purl.org/berg/epw_vocab#data_period_start_day']
        data_period_end_day = d['https://purl.org/berg/epw_vocab#data_period_end_day']
        
        line.extend([
            data_period_name_and_description,
            data_period_start_date_of_week,
            data_period_start_day,
            data_period_end_day
            ])
    
    line = ','.join(line) + '\n'
        
    return line
    
    
    
    
    
    
    
    