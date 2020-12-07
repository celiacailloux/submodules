#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 02:18:15 2017

@author: celiacailloux
"""

#Functions that remove things

#Strips a string that is entangled in with " on both sides
def stripping(s):
    while not s.endswith("'"): 
        s = s[:-1]
        while not s.startswith("'"): 
            s = s[1:]
    if s.startswith("'"):
        s = s[:-1]
        s = s[1:]
        
    return s