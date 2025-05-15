# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 05:07:50 2025

@author: lenovo
"""

import pytest
import src.capabilities.hdf5_handler as th5
import src.capabilities.compress_handler as tch

#Test HDF5 error case when the file can't be found
def testHDF5_v1():
    assert th5.findFile("e:\\target", ".hdf5") == "Error:No such file in the directory or no such directory."

#Test HDF5 successful case 1    
def testHDF5_v2():
    assert th5.findFile("e:\\mcpassign\\src", ".py") == ["e:\\mcpassign\\src\\mcp_handler.py","e:\\mcpassign\\src\\server.py","e:\\mcpassign\\src\\__init__.py"]  

#Test HDF5 successful case 2    
def testHDF5_v3():
    assert th5.findFile("e:\\mcpassign\\tests", ".txt") == ["e:\\mcpassign\\tests\\demo.txt"]

#Test compress successful case 1 Note both files are under tests directory but under src directory when testing using command prompt  
def testCompress_v1():
    assert tch.compress("demo.txt", "cdemo.gz") == "Info:Complete Compressing."   

#Test compress successful case 2    
def testCompress_v2():
    assert tch.compress("e:\\mcpassign\\demo1.txt", "e:\\mcpassign\\cdemo1.gz") == "Info:Complete Compressing." 

#Test compress error case when the original file can't be found
def testCompress_v3():
    with pytest.raises(FileNotFoundError):
        tch.compress("demo1.txt", "cdemo1.gz")