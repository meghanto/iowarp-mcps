# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 02:59:42 2025

@author: lenovo
"""

import gzip

#Function to compress the file
def compress(originalFile:str, compressedFile:str):
    # Open the original file in binary read mode
    with open(originalFile, 'rb') as f_in:
    # Open the gzip - compressed file in binary write mode
        with gzip.open(compressedFile, 'wb') as f_out:
            f_out.writelines(f_in) 
            
    return "Info:Complete Compressing."        