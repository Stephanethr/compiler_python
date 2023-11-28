# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 15:02:52 2023

@author: fredt
"""
from parser.py import Parser
from lexer.py import tokenize

# Créez une instance du parseur
parser = Parser()

# Lisez le contenu du fichier source
with open("./test.src", "r") as file:
    source_code = file.read()

# Tokenisez le code source
tokens = tokenize(source_code)
print(tokens)

# Produisez l'AST en utilisant le parseur
ast = parser.produce_ast(source_code)
import json
# Affichez l'AST au format JSON
print(json.dumps(ast, indent=3))

