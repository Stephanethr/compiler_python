from enum import Enum
from typing import List, Union

# Enumération pour les types de jetons
class TokenType(Enum):
    Number = 1
    Identifier = 2
    Var = 3
    BinaryOperator = 4
    AssignmentOperator = 5
    ConditionalOperator = 6
    OpenParen = 7
    CloseParen = 8
    OpenBrace = 9
    CloseBrace = 10
    Read = 11
    Write = 12
    While = 13
    Do = 14
    If = 15
    EOF = 16

# Classe Token
class Token:
    def __init__(self, value: str, type: TokenType):
        self.value = value
        self.type = type

# Fonction utilitaire pour créer un jeton
def token(value: str, type: TokenType) -> Token:
    return Token(value, type)


# Fonction utilitaire pour vérifier si un caractère est alphabétique
def isAlpha(src: str) -> bool:
    return src.isalpha()

# Fonction utilitaire pour vérifier si une chaîne peut être interprétée comme un entier
def isInt(str: str) -> bool:
    try:
        int(str)
        return True
    except ValueError:
        return False

# Fonction utilitaire pour vérifier si un caractère est ignoré (espace, saut de ligne, tabulation)
def isSkippable(src: str) -> bool:
    return src == " " or src == "\n" or src == "\t"

# Fonction pour découper le code source en jetons
def tokenize(sourceCode: str) -> List[Token]:
    tokens = []
    src = list(sourceCode)
    while src:
        if src[0] == "(":
            tokens.append(token(src.pop(0), TokenType.OpenParen))
        elif src[0] == ")":
            tokens.append(token(src.pop(0), TokenType.CloseParen))
        elif src[0] == "{":
            tokens.append(token(src.pop(0), TokenType.OpenBrace))
        elif src[0] == "}":
            tokens.append(token(src.pop(0), TokenType.CloseBrace))
        elif src[0] in ["+", "-", "*", "/"]:
            tokens.append(token(src.pop(0), TokenType.BinaryOperator))
        elif src[0] == "=":
            if src[1] == "=":
                tokens.append(token("==", TokenType.ConditionalOperator))
                src.pop(0)
                src.pop(0)
            else:
                tokens.append(token(src.pop(0), TokenType.AssignmentOperator))
        elif src[0] == "!":
            if src[1] == "=":
                tokens.append(token("!=", TokenType.ConditionalOperator))
                src.pop(0)
                src.pop(0)
            else:
                print("Caractère inattendu après '!':", src[1])
                exit(1)
        elif src[0] == "<":
            if src[1] == "=":
                tokens.append(token("<=", TokenType.ConditionalOperator))
                src.pop(0)
                src.pop(0)
            else:
                tokens.append(token(src.pop(0), TokenType.ConditionalOperator))
        elif src[0] == ">":
            if src[1] == "=":
                tokens.append(token(">=", TokenType.ConditionalOperator))
                src.pop(0)
                src.pop(0)
            else:
                tokens.append(token(src.pop(0), TokenType.ConditionalOperator))
        else:
            if isInt(src[0]):
                num = ""
                while src and isInt(src[0]):
                    num += src.pop(0)
                tokens.append(token(num, TokenType.Number))
            elif isAlpha(src[0]):
                ident = ""
                while src and (isAlpha(src[0]) or isInt(src[0])):
                    ident += src.pop(0)
                reserved = KEYWORDS.get(ident)
                if reserved:
                    tokens.append(token(ident, reserved))
                else:
                    tokens.append(token(ident, TokenType.Identifier))
            elif isSkippable(src[0]):
                src.pop(0)
            else:
                print("Caractère non reconnu dans la source:", ord(src[0]), src[0])
                exit(1)
    tokens.append(token("", TokenType.EOF))
    return tokens

# Dictionnaire des mots-clés
KEYWORDS = {
    "var": TokenType.Var,
    "read": TokenType.Read,
    "write": TokenType.Write,
    "while": TokenType.While,
    "do": TokenType.Do,
    "if": TokenType.If
}
