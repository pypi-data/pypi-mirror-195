import unittest
import math
import pandas as pd
from pandas.testing import assert_frame_equal
from list_overlap import Overlaps

df_fs       = Overlaps(df)
df_string   = df_fs.get_the_overlaps(df)
df_neu      = getoverlaps(df_n)
df_neumeric = df_neu.get_the_overlaps(df_n)

class TestReturnCalculations(unittest.TestCase):
    def overlap_neumeric(self):
        """
         Creating two DataFrame: df_n: neumeric dataframe
                                 df: string dataframe
         Setup: testing for both cases a dataframe of neumeric values and secound function test for a dataframe of string values
        """
        data_n = {'A':[1,2,3],'B': [1,2,3,4],'C':[5,2],'D': [2,8,9],'E': [2,11,5,9]}
        df_n = pd.DataFrame.from_dict(data_n, orient='index').T
        data = {'A':['D','KIT','SAP'],'B': ['F','G','LUFT','SAP'],'C':['I','SAP'],'D': ['SAP','LUF','KIT'],'E': ['SAP','LUF','KIT','HASS']}
        df   = pd.DataFrame.from_dict(data, orient='index').T
        # Expectation
        expected_n = df_neumeric
        # Call function
        actual_n   = df_neu.get_the_overlaps(df_n)
        # Test
        assert_frame_equal(actual, expected)

    def overlap_string(self):
        """"
        Test the overlap for the dataframe with strings
    
        """
            # Expectation
        expected_s=df_string

            # Call function
        actual_s = df_neu.get_the_overlaps(df)

            # Test
        assert_frame_equal(actual_s, expected_s)

if __name__ == "__main__":
    unittest.main()