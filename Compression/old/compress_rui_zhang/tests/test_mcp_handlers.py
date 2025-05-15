# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 05:06:54 2025

@author: lenovo
"""

import pytest

import src.mcp_handler as mht

# Test listResource handler
def test_ListResource():
    assert mht.listResource() == "Info:The capabilities I am going to implement are HDF5 and Compression Library."

# Test callHDF5 handler when the number of parameters is incorrectly given    
def test_callHDF5_v1():
    assert mht.callHDF5(["a", "b", "c"]) == "Error:The number of parameters must be 2."   

# Test callHDF5 handler handler successful case
def test_callHDF5_v2():
    assert mht.callHDF5(["e:\\mcpassign\\src", ".py"]) == ["e:\\mcpassign\\src\\mcp_handler.py","e:\\mcpassign\\src\\server.py","e:\\mcpassign\\src\\__init__.py"]

# Test callCompress handler when the number of parameters is incorrectly given    
def test_callCompress_v1():
    assert mht.callCompress(["a", "b", "c"]) == "Error:The number of parameters must be 2."

# Test callCompress handler successful case
def test_callCompress_v2():
    assert mht.callCompress(["demo.txt", "cdemo.gz"]) == "Info:Complete Compressing."

# Test callCompress handler when the original file is not found    
def test_callCompress_v3():
    with pytest.raises(FileNotFoundError):
        mht.callCompress(["demo1.txt", "cdemo.gz"])