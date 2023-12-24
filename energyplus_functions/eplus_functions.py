# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:03:38 2023

@author: cvskf
"""

import sys
import os
import subprocess
import tempfile
import shutil
import json


def run_energyplus(
        energyplus_installation_path,  # for example r'C:\EnergyPlusV23-2-0' -- the 'r' is important here
        input_filepath = 'in.idf',  
        epw_filepath = 'in.epw',
        output_dirpath = '.',
        output_file_extensions = None, # or list i.e. ['.err','.sql']
        verbose = False
        ):
    """Runs an EnergyPlus simulation.
    
    :param energyplus_installation_dirpath: The path to the local directory where EnergyPlus is installed.
        Note: If using backslashes with Windows, then make sure to use a raw string i.e. r'C:\EnergyPlusV23-2-0'.
        Note: This path should not include any space characters.
    :type energyplus_installation_dirpath: string
    
    :param idf_filepath: The local path to the input file.
        This can be an .idf file, an .epJSON file or a .json file.
        Note: If using backslashes with Windows, then make sure to use a raw string i.e. r'C:\mydir\in.idf'.
        This has a default value of 'in.idf'
    :type idf_filepath: string
    
    :param output_dirpath: The path to the local directory where the output file is saved to.
    :type output_dirpath: string
    
    :param output_file_extensions:
    :type output_file_extensions: None or list
        
    :param verbose: If True, then prints intermediate information.
    :type verbose: bool
    
    :returns: 
    :rtype: string
    
    """
    
    if verbose:
        print('--- def run_energyplus() ---')
    
    exe_path = f'{energyplus_installation_path}\\EnergyPlus'
    
    input_basename = os.path.basename(input_filepath)
    input_basename_no_ext, input_extension = os.path.splitext(input_basename)
    
    with tempfile.TemporaryDirectory() as temp_dirpath:
        # Sets up a temporary directory for the intial output file.
        
        if verbose: 
            print('- created temporary directory', temp_dirpath)
            
        # copy input file to temp folder
        input_filepath_temp = os.path.join(temp_dirpath, input_basename)
        shutil.copyfile(
            input_filepath, 
            input_filepath_temp
            )
        
        # remove '$schema' from JSON file if present
        if input_extension == '.json':
            with open(input_filepath_temp) as f:
                d = json.load(f)
            d.pop('$schema', None)
            with open(input_filepath_temp, 'w') as f:
                json.dump(d,f,indent=4)
            
        command = [
            exe_path,
            '--output-directory',
            temp_dirpath,
            '--weather',
            epw_filepath,
            input_filepath_temp
            ]
        
        if verbose:
            print('- command:',' '.join(command))
        
        result = subprocess.run(command, capture_output=True)
        
        # create a dictionary of output filepaths
        d={}
        for x in os.listdir(temp_dirpath):
            ext = os.path.splitext(x)[1]
            if output_file_extensions is None or ext in output_file_extensions:
                temp_filepath = os.path.join(
                    temp_dirpath,
                    x)
                output_filepath = os.path.join(
                    output_dirpath,
                    x)
                if os.path.isfile(temp_filepath):
                    d[temp_filepath] = output_filepath
        
        # copy files from temp directory to output directory
        for k, v in d.items():
            shutil.copy(
                k, 
                v
                )
        
        
    try:
        result.check_returncode()
    except subprocess.CalledProcessError as err:
        message = '- process failed---\n'
        message += f'error message from EnergyPlus.exe... {err.stderr.decode()}'
        if verbose:
            print(message)
        raise Exception(message)
           
    output_filepaths = list(d.values())
        
    return output_filepaths
        













    # --- old version below using pyenergyplus ---
    
    
    # add the EnergyPlus installation directory to sys.path, so that pyenergyplus can be imported
    sys.path.insert(
        0, 
        energyplus_installation_path
        )
    
    # import pyenergyplus
    from pyenergyplus.api import EnergyPlusAPI
    
    # remove the EnergyPlus installation directory to sys.path - just to keep things clean
    # try:
    #     sys.path.remove(energyplus_installation_path)
    # except ValueError:
    #     pass
    
    
    # get an EnergyPlusAPI instance
    api = EnergyPlusAPI()
    
    # get a state instance
    state = api.state_manager.new_state()
    
    # run Energyplus
    try:
        api.runtime.run_energyplus(
            state, [
                '--output-directory',
                energyplus_installation_path,
                '--weather',
                epw_filepath,
                idf_filepath
            ]
        )
    except OSError as err:
        print(err)
        pass
        
    try:
        with open(os.path.join(energyplus_installation_path,'eplusout.err')) as f:
            message = f.read()
    except FileNotFoundError:
        message = ''
        
    print(message)
        
    
