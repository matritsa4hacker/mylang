import re
import tkinter as tk
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Lexer, Token, and Tokenization
class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_pos = 0

    def tokenize(self):
        patterns = {
            'NUMBER': r'\d+',
            'STRING': r'"[^"]*"',
            'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'ASSIGN': r'=',
            'OPERATOR': r'[+\-*/]',
            'LPAREN': r'\(',
            'RPAREN': r'\)',
            'LBRACE': r'{',
            'RBRACE': r'}',
            'NEWLINE': r'\n',
            'SKIP': r'[ \t]'
        }

        while self.current_pos < len(self.code):
            match = None
            for token_type, pattern in patterns.items():
                regex = re.compile(pattern)
                match = regex.match(self.code, self.current_pos)
                if match:
                    value = match.group(0)
                    if token_type != 'SKIP':
                        self.tokens.append(Token(token_type, value))
                    self.current_pos = match.end(0)
                    break

            if not match:
                raise Exception(f"Unexpected character: {self.code[self.current_pos]}")
        return self.tokens

# Parser, AST Nodes, and Parsing
class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class BinaryOperationNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
        else:
            raise Exception(f"Expected token type {token_type}, but got {self.current_token.type}")

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return NumberNode(int(token.value))

    def term(self):
        node = self.factor()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in ['*', '/']:
            token = self.current_token
            self.eat('OPERATOR')
            node = BinaryOperationNode(left=node, operator=token.value, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in ['+', '-']:
            token = self.current_token
            self.eat('OPERATOR')
            node = BinaryOperationNode(left=node, operator=token.value, right=self.term())
        return node

    def parse(self):
        return self.expr()

# Interpreter for basic math operations
class Interpreter:
    def visit(self, node):
        if isinstance(node, NumberNode):
            return self.visit_number(node)
        elif isinstance(node, BinaryOperationNode):
            return self.visit_binary_operation(node)

    def visit_number(self, node):
        return node.value

    def visit_binary_operation(self, node):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        if node.operator == '+':
            return left_value + right_value
        elif node.operator == '-':
            return left_value - right_value
        elif node.operator == '*':
            return left_value * right_value
        elif node.operator == '/':
            return left_value / right_value

    def interpret(self, node):
        return self.visit(node)

# GUI Integration (Tkinter)
class UIInterpreter:
    def __init__(self):
        self.root = tk.Tk()

    def create_window(self, title="Window", size="400x400"):
        self.root.title(title)
        self.root.geometry(size)

    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command)
        button.pack()

    def start_ui(self):
        self.root.mainloop()

# 2D Game Integration (Pygame)
class GameInterpreter:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))  # Clear screen
            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit frame rate to 60 FPS

        pygame.quit()

# 3D Game Integration (PyOpenGL)
class OpenGLInterpreter:
    def __init__(self):
        self.width = 800
        self.height = 600

    def init_window(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow("OpenGL 3D Window")

    def start_opengl_loop(self):
        glutDisplayFunc(self.display)
        glutIdleFunc(self.display)
        glutMainLoop()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # Add your 3D rendering logic here
        glutSwapBuffers()

# Basic REPL (Read-Eval-Print Loop)
def repl():
    while True:
        try:
            code = input(">>> ")
            if code.strip() == "exit":
                break

            lexer = Lexer(code)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            interpreter = Interpreter()
            result = interpreter.interpret(ast)

            print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    repl()
