# -*- coding: cp1251 -*-
# module for misc functions
import os,string,cfg,sys

def get_rel_path(path):
    """ Return relative path to file
    example: c:\ot\ie\ie.exe returns ..\..\ """
    path_=''
    if os.name=='posix':
        count=(int(string.count(path,'/'))-1)
        for count_ in range(count):
            path_=path_+'../'
        return path_
    else:
        count=(int(string.count(path,'\\'))-1)
        for count_ in range(count):
            path_=path_+'..\\'
        return path_

def strip_disk(path):
    """
    Strip disk from windows path
    example: c:\ot\test returns \ot\test """
    if (int(string.count(path,':'))==0):
        return path
    else:
        return str(string.split(path,':\\')[1])
