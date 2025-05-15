# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 02:58:30 2025

@author: lenovo
"""
import glob

#Using glob to implement the find file function under a directory, rpath must be an absolute path
def findFile(rpath:str, suffix:str):
    apath = rpath + "/*" + suffix
    data_files = glob.glob(apath)
    if not data_files:
        return "Error:No such file in the directory or no such directory."
    else:
        return data_files

