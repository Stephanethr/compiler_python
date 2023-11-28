# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 15:43:15 2023

@author: fredt
"""

def read_source_code():
    print("Entrez votre code L3Lang (tapez 'END' pour terminer) :")
    code = ""
    while True:
        line = input()
        if line == "END":
            break
        code += line + '\n'
    return code
