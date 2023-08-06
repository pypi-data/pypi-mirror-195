#!/usr/bin/env python3
import pandas as pd
#import os
import itertools as it
import itertools  

class Overlaps:
    """
    Instantiate a the overlap search operation.
    
    :param df: The dataframe
    :type df: The columns can be type integer or string
    """
    
    def __init__(self, df):
        self.df = df
    
    def get_the_overlaps(self,df):
    
        """
        Get the overlaps between the columns of the dataframe df.
    
        :param df: The dataframe
        :type df: The columns can be type integer or string

        """
    ## lists from the dataframe; filter for None or Na values 
        lists = [[y for y in x if pd.notna(y)] for x in df.values.T.tolist()]
    # orient as list
        master_dict = df.to_dict('list')
        combinations =[]
        for l in range(2, len(lists) + 1):
            combinations += itertools.combinations(lists, l)
        key_list    = []
        for i in range(2,len(master_dict) +1):
            for combo in it.combinations(master_dict.keys(), i):
                new_key = "".join(combo)
                if (len(combo)>1):
                    key_list.append(new_key)
        final_dict = dict()
        for key, elem in zip(key_list, combinations):
            final_dict[key] = list(elem)
        overlap_list  = []
        dfs = []
        for k,v in final_dict.items():
            overlap = list(set.intersection(*[set(x) for x in v]))
            overlap_list.append(overlap)
         #print(overlap, sep=", ")
            dct  ={ 'overlaps':overlap,'number of overlaps':len(overlap),
              'overlap columns':k}
            dfs.append(dct)
        df_final          = pd.DataFrame.from_dict(dfs)
        return df_final