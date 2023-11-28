from typing import Union, List, Optional

# Définition des types de nœuds
NodeType = Union[
    "Program",
    "NumericLiteral",
    "Identifier",
    "BinaryExpr",
    "VariableDeclaration",
    "Assignment",
    "DoWhileLoop",
    "NativeFunctionCall"
]

# Interface Stmt
class Stmt:
    def __init__(self, kind: NodeType):
        self.kind = kind

# Interface Program
class Program(Stmt):
    def __init__(self, body: List[Stmt]):
        super().__init__("Program")
        self.body = body

# Interface Expr
class Expr(Stmt):
    pass

# Interface BinaryExpr
class BinaryExpr(Expr):
    def __init__(self, left: Expr, right: Expr, operator: str):
        super().__init__("BinaryExpr")
        self.left = left
        self.right = right
        self.operator = operator

# Interface Identifier
class Identifier(Expr):
    def __init__(self, symbol: str):
        super().__init__("Identifier")
        self.symbol = symbol

# Interface NumericLiteral
class NumericLiteral(Expr):
    def __init__(self, value: float):
        super().__init__("NumericLiteral")
        self.value = value

# Interface VariableDeclaration
class VariableDeclaration(Stmt):
    def __init__(self, identifier: Identifier, initializer: Optional[Expr]):
        super().__init__("VariableDeclaration")
        self.identifier = identifier
        self.initializer = initializer

# Interface Assignment
class Assignment(Stmt):
    def __init__(self, identifier: Identifier, value: Expr):
        super().__init__("Assignment")
        self.identifier = identifier
        self.value = value

# Interface DoWhileLoop
class DoWhileLoop(Stmt):
    def __init__(self, body: List[Stmt], condition: Expr):
        super().__init__("DoWhileLoop")
        self.body = body
        self.condition = condition

# Interface NativeFunctionCall
class NativeFunctionCall(Stmt):
    def __init__(self, functionName: str, arguments: List[Expr]):
        super().__init__("NativeFunctionCall")
        self.functionName = functionName
        self.arguments = arguments

# Exemple d'utilisation
identifier = Identifier("x")
numeric_literal = NumericLiteral(42)
assignment = Assignment(identifier, numeric_literal)
stmt_list = [assignment]
program = Program(stmt_list)
print(program.kind)  # Affiche "Program"
print(program.body[0].kind)  # Affiche "Assignment"
