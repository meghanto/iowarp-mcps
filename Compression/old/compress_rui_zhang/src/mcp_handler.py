# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 23:58:48 2025

@author: lenovo
"""

#This segment of code will make you avoid import error when running the server with a command line
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
#rootPath = os.path.split(curPath)[0]
sys.path.append(curPath)

from capabilities import hdf5_handler as h5
from capabilities import compress_handler as com

#Handler for listing all the implemented resources
def listResource():
       result = "Info:The capabilities I am going to implement are HDF5 and Compression Library."
       return result

#Handler for hdf5 capability    
def callHDF5(param:list[str]):
    if len(param) != 2:
        return "Error:The number of parameters must be 2."
    else:
        return h5.findFile(param[0], param[1])
        #return "HDF5"

#Handler for compress capability    
def callCompress(param:list[str]):
    if len(param) != 2:
        return "Error:The number of parameters must be 2."
    else:
        return com.compress(param[0], param[1])
        
        
        #return "Compress"