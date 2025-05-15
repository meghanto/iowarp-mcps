#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import libraries:
import pandas as pd
from typing import List


# Tool1: Filter the data based on column threshold for the client shared csv file path: 
def filter_csv_data(csv_path: str, column: str, threshold: float) -> List[dict]:
    """
    Goal: load the datafile from the path and filter rows that has values > threshold in the specefied column:
    
    Input: csv_path: str, column: str, threshold: float
        
    Output: all rows the above the threshold  
        
    """
    df = pd.read_csv(csv_path)
    df_filtered = df[df[column] > threshold]
    return df_filtered.to_dict(orient="records")












