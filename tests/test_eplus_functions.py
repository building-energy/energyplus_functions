# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:06:57 2023

@author: cvskf
"""

import unittest
from energyplus_functions import eplus_functions

class TestEPlusFunctions(unittest.TestCase):
    ""
    
    def test_run_energyplus(self):
        ""
        
        
        result = \
            eplus_functions.run_energyplus(
                r'C:\Users\cvskf\EnergyPlusV23-2-0',
                input_filepath = r'input\in.json',
                epw_filepath = r'input\in.epw',
                output_dirpath = 'output',
                output_file_extensions = ['.err','.sql'],
                verbose = True
                )
        
        print(result)
        #print(csvw_metadata_dict)
        #print(csvw_csv_string[:1000])



if __name__ == "__main__":
    
    unittest.main()
