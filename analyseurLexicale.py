import re

TOKENS = {
    'INT': r'\bINT\b',
    'ADD': r'\bADD\b',
    'SUB': r'\bSUB\b',
    'MUL': r'\bMUL\b',
    'DIV': r'\bDIV\b',
    'LDI': r'\bLDI\b',
    'LDA': r'\bLDA\b',
    'LDV': r'\bLDV\b',
    'STO': r'\bSTO\b',
    'BRN': r'\bBRN\b',
    'BZE': r'\bBZE\b',
    'HLT': r'\bHLT\b',
    'EQL': r'\bEQL\b',
    'NEQ': r'\bNEQ\b',
    'GTR': r'\bGTR\b',
    'LSS': r'\bLSS\b',
    'GEQ': r'\bGEQ\b',
    'LEQ': r'\bLEQ\b',
    'PRN': r'\bPRN\b',
    'INN': r'\bINN\b',
    'NUMBER': r'\b\d+\b',
    'COMMENT': r'//.*',
 
}


def tokenize(code):
    tokens = []
    code = code.split('\n')  # Diviser le code en lignes
    for line in code:
        line = line.strip()  # Enlever les espaces blancs
        if not line or line.startswith('//'):  # Ignorer les lignes vides et les commentaires
            continue
        while line:
            match = None
            for token_type, token_regex in TOKENS.items():
                regex = re.compile(token_regex)
                match = regex.match(line)
                if match:
                    if token_type != 'COMMENT':  # Ignorer les commentaires
                        tokens.append((token_type, match.group()))
                    break
            if not match:
                raise SyntaxError(f"Syntaxe incorrecte : {line}")
            line = line[match.end():].strip()
    return tokens

class AnalyseurLexicale :
    