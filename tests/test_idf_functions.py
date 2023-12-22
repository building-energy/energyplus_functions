# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:18:11 2023

@author: cvskf
"""

import unittest
from energyplus_functions import idf_functions

class TestIDFFunctions(unittest.TestCase):
    ""
    
    def test_convert_idf_to_epJSON(self):
        ""
        
        idf_functions.convert_idf_to_json(
            r'C:\Users\cvskf\EnergyPlusV23-2-0',
            idf_filepath = r'input\in.idf',
            output_dirpath = 'output',
            verbose = True
            )
        
        #print(csvw_metadata_dict)
        #print(csvw_csv_string[:1000])



if __name__ == "__main__":
    
    unittest.main()
