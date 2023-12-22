# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:03:38 2023

@author: cvskf
"""

import sys
import os
import subprocess

def run_energyplus(
        energyplus_installation_path,  # for example r'C:\EnergyPlusV23-2-0' -- the 'r' is important here
        idf_filepath = 'in.idf',  
        epw_filepath = 'in.epw',
        output_filepath = '.'
        ):
    """
    """
    
    
    exe_path = f'{energyplus_installation_path}\\EnergyPlus'
    
    command = [
        exe_path,
        '--output-directory',
        output_filepath,
        '--weather',
        epw_filepath,
        idf_filepath
        ]
    result = subprocess.run(command, capture_output=True)
    
    try:
        result.check_returncode()
    except subprocess.CalledProcessError as err:
        message = '---run_energyplus process failed---\n'
        message += f'error message from EnergyPlus.exe... {err.stderr.decode()}'
        
        try:
            with open('eplusout.err') as f:
                message2 = f.read()
        except FileNotFoundError:
            message2 = 'No .err file found'
        print(message2)
        
        raise Exception(message)
        
        
    return
        
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
        
    
