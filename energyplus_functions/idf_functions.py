# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:17:48 2023

@author: cvskf
"""


import subprocess
import os
import tempfile
import shutil
import json


def convert_idf_to_json(
        energyplus_installation_dirpath,  # for example r'C:\EnergyPlusV23-2-0' -- the 'r' is important here
        idf_filepath = 'in.idf',
        output_dirpath = '.',
        output_extension = '.json',
        add_json_schema_keyword = True,
        verbose = False
        ):
    """Converts an IDF file to a JSON file.
    
    :param energyplus_installation_dirpath: The path to the local directory where EnergyPlus is installed.
        Note: If using backslashes with Windows, then make sure to use a raw string i.e. r'C:\EnergyPlusV23-2-0'.
        Note: This path should not include any space characters.
    :type energyplus_installation_dirpath: string
    
    :param idf_filepath: The local path to the IDF file.
        Note: If using backslashes with Windows, then make sure to use a raw string i.e. r'C:\mydir\in.idf'.
        This has a default value of 'in.idf'
    :type idf_filepath: string
    
    :param output_dirpath: The path to the local directory where the output file is saved to.
    :type output_dirpath: string
        
    :param output_extension: The extension to be used for the output file.
    :type output_extension: str
    
    :param add_json_schema_keyword: If True, then a "$schema" keyword is added to the output JSON file. 
        The schema URL is based on the `energyplus_installation_dirpath` and should point to the "Energy+.schema.epJSON" file.
    :type add_json_schema_keyword: bool
    
    :param verbose: If True, then prints intermediate information.
    :type verbose: bool
    
    :returns: output_filepath, the local filepath of the newly created JSON file.
    :rtype: string
    
    NOTES: 
        - This makes use of the ConvertInputFormat.exe programme in the EnergyPlus installation directory.
        - The Python module 'subprocess' is used to call this .exe file.
        - If an error occurs, then the error message from ConvertInputFormat.exe is printed and an Exception is raised.
        - The final output is a file in the format of a epJSON file.
        - The output filename is the same as the idf input filename but with an new extension given by `output_extension`.
        
    ---
    For information, the help documentation for ConvertInputFormat.exe is:
    
    ConvertInputFormat --help:
        Run input file conversion tool
        Usage: ConvertInputFormat [OPTIONS] [input_file...]
    
        Positionals:
          input_file TEXT:FILE ...    Multiple input files to be translated
    
        Options:
          -h,--help                   Print this help message and exit
          -v,--version                Display program version information and exit
          -j N                        Number of threads [Default: 8]
          -i,--input LSTFILE          Text file with list of input files to convert (newline delimited)
          -o,--output DIR             Output directory. Will use input file location by default
          -f,--format FORMAT          Output format.
                                      Default means IDF->epJSON or epJSON->IDF
                                      Select one (case insensitive):
                                      [default,IDF,epJSON,CBOR,MsgPack,UBJSON,BSON]
          -n,--noHVACTemplate         Do not convert HVACTemplate objects
    
        Example: ConvertInputFormat in.idf
    ---
        
    """
    
    if verbose:
        print('--- def convert_idf_to_epJSON() ---')
    
    exe_path = f'{energyplus_installation_dirpath}\\ConvertInputFormat'
        # The path to run the ConvertInputFormat.exe program.
    
    with tempfile.TemporaryDirectory() as temp_dirpath:
        # Sets up a temporary directory for the intial output file.
        
        if verbose: 
            print(' - created temporary directory', temp_dirpath)
    
        command = [
            exe_path,
            '--output',
            temp_dirpath,
            idf_filepath,
            ]
        
        if verbose:
            print('- command:',' '.join(command))
        
        result = subprocess.run(
            command, 
            capture_output = True
            )
    
        try:
            result.check_returncode()
        except subprocess.CalledProcessError as err:
            message = '- process failed\n'
            message += '- error message from ConvertInputFormat.exe:\n'
            message += f'"{err.stderr.decode().strip()}"'
            if verbose:
                print(message)
            raise Exception(message)
        
        # get filepath in temporary directory
        temp_output_filename = os.listdir(temp_dirpath)[0]
        temp_output_filepath = os.path.join(
            temp_dirpath,
            temp_output_filename
            )
        #print(temp_output_filepath)
        
        # get filepath of final output file
        os.path.splitext(temp_output_filename)[0]
        output_filename = (
            os.path.splitext(temp_output_filename)[0]
            +
            output_extension
            )
        output_filepath = os.path.join(
            output_dirpath,
            output_filename
            )
        #print(output_filepath)
    
        # copy from temporary directory to output directory
        shutil.copyfile(
            temp_output_filepath, 
            output_filepath)
        
        
    if add_json_schema_keyword:
        
        with open(output_filepath) as f:
            epjson = json.load(f)
            
        schema_url = str(os.path.join(
            energyplus_installation_dirpath.replace('C:','file:\\'),
            'Energy+.schema.epJSON'
            ))
            
        new_epjson = {'$schema':schema_url}
        new_epjson.update(epjson)
        
        with open(output_filepath,'w') as f:
            json.dump(new_epjson,f,indent=4)
        
    
    if verbose:
        print('- process successful')
        
    return output_filepath
        
    
    
    

    