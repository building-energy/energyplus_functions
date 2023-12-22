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
                #idf_filepath = 'in.idf',
                #epw_filepath = 'simple.epw'
                )
        
        #print(csvw_metadata_dict)
        #print(csvw_csv_string[:1000])



if __name__ == "__main__":
    
    unittest.main()
