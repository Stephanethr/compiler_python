# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 15:05:25 2023

@author: fredt
"""

from lexer.py import Token, tokenize, TokenType
from ast.py import BinaryExpr, Expr, Identifier, NumericLiteral, Program, Stmt, VariableDeclaration, Assignment, DoWhileLoop, NativeFunctionCall

class Parser:
    def __init__(self):
        self.tokens = []

    def not_eof(self):
        return self.tokens[0].type != TokenType.EOF

    def is_identifier(self, token):
        return token.type == TokenType.Identifier

    def available_token(self):
        return self.tokens[0]

    def previous_token(self):
        return self.tokens.pop(0)

    def previous_token_with_type(self, type, err):
        prev = self.tokens.pop(0)
        if not prev or prev.type != type:
            print("Parser Error:\n", err, prev, " - Expecting: ", type)
            exit(1)
        return prev

    def produce_ast(self, source_code):
        self.tokens = tokenize(source_code)
        program = Program("Program", [])
        
        while self.not_eof():
            program.body.append(self.parse_stmt())
        
        return program

    def parse_stmt(self):
        if self.available_token().value == "var":
            return self.parse_variable_declaration()
        elif self.available_token().type == TokenType.Identifier:
            if self.is_identifier(self.available_token()):
                identifier = self.previous_token()
                if self.available_token().value == "=":
                    return self.parse_assignment(identifier)
        elif self.available_token().value == "do":
            return self.parse_do_while_loop()
        elif self.available_token().value == "write":
            return self.parse_write()
        
        return self.parse_expr()

    def parse_do_while_loop(self):
        self.previous_token_with_type(
            TokenType.Do,
            "Expecting 'do' keyword to start do-while loop."
        )

        self.previous_token_with_type(
            TokenType.OpenBrace,
            "Expecting '{' after 'do' keyword in do-while loop."
        )

        body = []
        while self.available_token().value != "}":
            body.append(self.parse_stmt())

        self.previous_token_with_type(
            TokenType.CloseBrace,
            "Expecting '}' after do-while loop body."
        )

        self.previous_token_with_type(
            TokenType.While,
            "Expecting 'while' keyword after do-while loop body."
        )

        condition = self.parse_expr()

        return DoWhileLoop("DoWhileLoop", body, condition)

    def parse_write(self):
        self.previous_token_with_type(
            TokenType.Write,
            "Expecting 'write' keyword."
        )

        self.previous_token_with_type(
            TokenType.OpenParen,
            "Expecting '(' after 'write' keyword."
        )

        args = []
        while self.available_token().value != ")":
            args.append(self.parse_expr())

            if self.available_token().value != ")":
                self.previous_token_with_type(
                    TokenType.BinaryOperator,
                    "Expecting ',' between args in 'write' function."
                )

        self.previous_token_with_type(
            TokenType.CloseParen,
            "Expecting ')' after 'write' function args."
        )

        return NativeFunctionCall("NativeFunctionCall", "write", args)

    def parse_variable_declaration(self):
        self.previous_token_with_type(
            TokenType.Var,
            "Expecting 'var' keyword for variable declaration."
        )

        identifier = self.parse_primary_expr()

        initializer = None
        if self.available_token().value == "=":
            self.previous_token()
            initializer = self.parse_expr()

        return VariableDeclaration("VariableDeclaration", identifier, initializer)

    def parse_assignment(self, identifier):
        self.previous_token_with_type(
            TokenType.AssignmentOperator,
            "Expecting '=' for variable assignment."
        )

        value = self.parse_expr()

        return Assignment("Assignment", identifier, value)

    def parse_expr(self):
        return self.parse_additive_expr()

    def parse_additive_expr(self):
        left = self.parse_multiplicative_expr()

        while self.available_token().value in ["+", "-"]:
            operator = self.previous_token().value
            right = self.parse_multiplicative_expr()
            left = BinaryExpr("BinaryExpr", left, right, operator)

        return left

    def parse_multiplicative_expr(self):
        left = self.parse_conditional_expr()

        while self.available_token().value in ["/", "*", "%"]:
            operator = self.previous_token().value
            right = self.parse_conditional_expr()
            left = BinaryExpr("BinaryExpr", left, right, operator)

        return left

    def parse_conditional_expr(self):
        left = self.parse_primary_expr()

        while self.available_token().value in ["==", "!=", "<", ">", "<=", ">="]:
            operator = self.previous_token().value
            right = self.parse_primary_expr()
            left = BinaryExpr("BinaryExpr", left, right, operator)

        return left

    def parse_primary_expr(self):
        tk = self.available_token().type

        if tk == TokenType.Identifier:
            return Identifier("Identifier", self.previous_token().value)
        elif tk == TokenType.Number:
            return NumericLiteral("NumericLiteral", float(self.previous_token().value))
        elif tk == TokenType.OpenParen:
            self.previous_token()
            value = self.parse_expr()
            self.previous_token_with_type(
                TokenType.CloseParen,
                "Unexpected token found inside parenthesized expression. Expected closing parenthesis."
            )
            return value
        elif tk == TokenType.Read:
            self.previous_token()
            self.previous_token_with_type(
                TokenType.OpenParen,
                "Expecting '(' after 'Read' keyword."
            )
            self.previous_token_with_type(
                TokenType.CloseParen,
                "Expecting ')' after 'Read' keyword."
            )
            return NativeFunctionCall("NativeFunctionCall", "read", [])

        print("Unexpected token found during parsing!", self.available_token())
        exit(1)

# Exemple d'utilisation
parser = Parser()
source_code = """
var x = 10;
write(x);
"""
ast = parser.produce_ast(source_code)
print(ast)
