import re


class MachInterpreter:

    # Définition des couleurs pour le terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Définition des instructions
    def __init__(self):
        self.MEM = []
        self.SP = 0
        self.PC = 0
        self.PCODE = []
        self.INST = None
        print("Interpréteur initialisé")

    def run(self):
        print("Début de l'exécution")
        while self.PC < len(self.PCODE):
            print(f"Avant exécution: PC = {self.PC}, SP = {self.SP}, MEM = {self.MEM}")
            self.INST, *args = self.PCODE[self.PC]
            print(f"Exécution de {self.INST} avec les arguments {args}")
            self.PC += 1
            if hasattr(self, f"do_{self.INST}"):
                getattr(self, f"do_{self.INST}")(*args)
            else:
                print(f"Instruction {self.INST} not implemented")
                break
            print(f"Après exécution: PC = {self.PC}, SP = {self.SP}, MEM = {self.MEM}")
        print("Fin de l'exécution")

    def do_ADD(self, _):
        print(f"{self.OKGREEN}DEBUG - Avant ADD: SP = {self.SP}, MEM = {self.MEM}{self.ENDC}")
        if self.SP < 1:
            print("Erreur : pas assez d'éléments dans la pile pour ADD")
            return
        print("Dernier élément de la pile {0}".format(self.MEM[self.SP-1]))
        print("Avant dernier élément de la pile {0}" .format(self.MEM[self.SP]))
        self.MEM[self.SP-1] += self.MEM[self.SP]
        print(self.MEM)
        self.MEM.pop()
        self.SP -= 1
        print(f"{self.OKGREEN}DEBUG - Après ADD: SP = {self.SP}, MEM = {self.MEM}{self.ENDC}")


    def do_SUB(self, _):
        print(f"{self.OKCYAN}DEBUG - Avant SUB: SP = {self.SP}, MEM = {self.MEM}{self.ENDC}")
        if self.SP < 1:
            print("Erreur : pas assez d'éléments dans la pile pour SUB")
            return
        print("Dernier élément de la pile : {0}".format(self.MEM[-1]))
        print("Avant dernier élément de la pile : {0}" .format(self.MEM[self.SP]))
        self.MEM[self.SP - 1] -= self.MEM[self.SP]
        self.MEM.pop()
        self.SP -= 1
        print(f"{self.OKCYAN}DEBUG - Après SUB: SP = {self.SP}, MEM = {self.MEM}{self.ENDC}")


    def do_MUL(self, _):
        print(f"{self.OKBLUE}DEBUG - Avant MUL: SP = {self.SP}, MEM = {self.MEM}{self.ENDC}")
        if self.SP < 1:
            print("Erreur : pas assez d'éléments dans la pile pour MUL")
            return
        self.MEM[self.SP-1] *= self.MEM[self.SP]
        self.MEM.pop()
        self.SP -= 1
        print(f"{self.OKBLUE}DEBUG - Après MUL: SP = {self.SP}, MEM = {self.MEM}{self.ENDC}")


    def do_DIV(self, _):
        print(f"{self.WARNING}DEBUG - Avant DIV: SP = {self.SP}, MEM = {self.MEM}{self.ENDC}")
        if self.SP < 1:
            print("Erreur : pas assez d'éléments dans la pile pour DIV")
            return
        if self.MEM[self.SP] == 0:
            print("Erreur : division par zéro")
            return
        self.MEM[self.SP-1] //= self.MEM[self.SP]
        self.MEM.pop()
        self.SP -= 1
        print(f"{self.WARNING}DEBUG - Après DIV: SP = {self.SP}, MEM = {self.MEM}{self.ENDC}")

    def do_EQL(self, _):
        self.MEM[self.SP-1] = int(self.MEM[self.SP-1] == self.MEM[self.SP])
        self.SP -= 1

    def do_NEQ(self, _):
        self.MEM[self.SP-1] = int(self.MEM[self.SP-1] != self.MEM[self.SP])
        self.SP -= 1

    def do_GTR(self, _):
        self.MEM[self.SP-1] = int(self.MEM[self.SP-1] > self.MEM[self.SP])
        self.SP -= 1

    def do_LSS(self, _):
        self.MEM[self.SP-1] = int(self.MEM[self.SP-1] < self.MEM[self.SP])
        self.SP -= 1

    def do_GEQ(self, _):
        self.MEM[self.SP-1] = int(self.MEM[self.SP-1] >= self.MEM[self.SP])
        self.SP -= 1

    def do_LEQ(self, _):
        self.MEM[self.SP-1] = int(self.MEM[self.SP-1] <= self.MEM[self.SP])
        self.SP -= 1

    def do_PRN(self, _):
        if self.SP < 0:
            print("Erreur : pile vide, rien à imprimer")
            return
        print(self.MEM[self.SP])

    def do_INN(self, _):
        self.MEM[self.MEM[self.SP]] = int(input())
        self.SP -= 1    

    def do_INT(self, args):
        if not args or len(args) != 1:
            raise ValueError("Argument manquant ou incorrect pour INT")
        c = args[0]
        self.MEM.extend([0] * c)
        self.SP = len(self.MEM) - 1
        
    def do_LDI(self, args):
        if not args or len(args) != 1:
            raise ValueError("Argument manquant ou incorrect pour LDI")
        value = args[0]
        self.MEM.append(value)
        self.SP += 1

    def do_LDA(self, args):
        if not args or len(args) != 1:
            raise ValueError("Argument manquant ou incorrect pour LDA")
        self.SP += 1
        self.MEM.append(self.MEM[args[0]])

    def do_LDV(self, _):
        if self.SP < 0:
            raise ValueError("Pile vide, impossible de charger la valeur")
        self.MEM[self.SP] = self.MEM[self.MEM[self.SP]]

    def do_BRN(self, args):
        if not args or len(args) != 1:
            raise ValueError("Argument manquant ou incorrect pour BRN")
        self.PC = args[0]

    def do_BZE(self, args):
        if not args or len(args) != 1:
            raise ValueError("Argument manquant ou incorrect pour BZE")
        if self.MEM[self.SP] == 0:
            self.PC = args[0]
        self.SP -= 1

    def do_HLT(self, _):
        self.PC = len(self.PCODE)


# Définition des tokens
TOKENS = {
    'INT': r'\bINT\b',
    'ADD': r'\bADD\b',
    'SUB': r'\bSUB\b',
    'MUL': r'\bMUL\b',
    'DIV': r'\bDIV\b',
    'LDI': r'\bLDI\b',
    'LDA': r'\bLDA\b',
    'LDV': r'\bLDV\b',
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
 
}

# Fonction pour tokeniser le code source
def tokenize(code):
    tokens = []
    while code:
        match = None
        for token_type, token_regex in TOKENS.items():
            regex = re.compile(token_regex)
            match = regex.match(code)
            if match:
                tokens.append((token_type, match.group()))
                break
        if not match:
            raise SyntaxError(f"Syntaxe incorrecte : {code}")
        code = code[code.index(match.group()) + len(match.group()):].lstrip()
    return tokens

# Fonction pour lire le code source
def read_source_code():
    print("Entrez votre code L3Lang (tapez 'END' pour terminer) :")
    code = ""
    while True:
        line = input()
        if line == "END":
            break
        code += line + '\n'
    return code

# Fonction pour convertir les tokens en PCode
def convert_to_pcode(tokens):
    pcode = []
    i = 0
    while i < len(tokens):
        token_type, token_val = tokens[i]
        if token_type in ['INT', 'LDA', 'BRN', 'BZE', 'LDI']: 
            if i + 1 < len(tokens) and tokens[i + 1][0] == 'NUMBER':
                pcode.append((token_type, [int(tokens[i + 1][1])]))
                i += 1  # Incrémentez pour passer le token du nombre
            else:
                raise SyntaxError(f"Argument manquant pour l'instruction {token_type}")
        elif token_type == 'NUMBER':
            # Gérez ici si vous avez une instruction spécifique pour les nombres seuls
            pass
        else:
            pcode.append((token_type, []))
        i += 1
    return pcode

def main():
    code = read_source_code()
    tokens = tokenize(code)
    pcode = convert_to_pcode(tokens)

    interpreter = MachInterpreter()
    interpreter.PCODE = pcode
    interpreter.run()

if __name__ == "__main__":
    main()


"""
if __name__ == "__main__":
    interpreter = MachInterpreter()
    interpreter.PCODE = [
        ('INT', [10]),   # Initialise la pile avec 10 éléments
        ('LDI', [5]),    # Empile 5
        ('LDI', [3]),    # Empile 3
        ('ADD', []),     # Additionne (5 + 3)
        ('PRN', []),     # Imprime le résultat de l'addition (devrait afficher 8)
        ('LDI', [2]),    # Empile 2
        ('SUB', []),     # Soustrait (8 - 2)
        ('PRN', []),     # Imprime le résultat de la soustraction (devrait afficher 6)
        ('LDI', [3]),    # Empile 3
        ('MUL', []),     # Multiplie (6 * 3)
        ('PRN', []),     # Imprime le résultat de la multiplication (devrait afficher 18)
        ('LDI', [2]),    # Empile 2
        ('DIV', []),     # Divise (18 / 2)
        ('PRN', []),     # Imprime le résultat de la division (devrait afficher 9)
        ('LDI', [9]),    # Empile 9
        ('EQL', []),     # Égalité (9 == 9)
        ('PRN', []),     # Imprime le résultat de l'égalité (devrait afficher 1 pour vrai)
        ('LDI', [1]),    # Empile 1
        ('LDI', [1]),    # Empile 1
        ('NEQ', []),     # Non égalité (1 != 1)
        ('PRN', []),     # Imprime le résultat de la non égalité (devrait afficher 0 pour faux)
        ('LDI', [5]),    # Empile 5
        ('GTR', []),     # Plus grand que (1 > 5)
        ('PRN', []),     # Imprime le résultat (devrait afficher 0 pour faux)
        ('LDI', [4]),    # Empile 4
        ('LSS', []),     # Moins que (5 < 4)
        ('PRN', []),     # Imprime le résultat (devrait afficher 0 pour faux)
        ('HLT', [])      # Halte
    ]
    interpreter.run()
"""