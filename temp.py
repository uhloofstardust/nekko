import re
import sys

INTEGER, PLUS, MULTIPLY, STRING, NYA, LPAR, RPAR, LBRACE, RBRACE, EOF = (
    'INTEGER', 'PLUS', 'MULTIPLY', 'STRING', 'NYA', 'LPAR', 'RPAR', 'LBRACE', 'RBRACE', 'EOF'
)

token_regex = [
    (r'\d+', INTEGER),       
    (r'\+', PLUS),           
    (r'\*', MULTIPLY),       
    (r'"([^"]*)"', STRING),   
    (r'nya', NYA),           
    (r'\(', LPAR),           
    (r'\)', RPAR),           
    (r'{', LBRACE),           
    (r'}', RBRACE),          
    (r'\s+', None),          
]

def lex(code):
    tokens = []
    while code:
        for pattern, token_type in token_regex:
            match = re.match(pattern, code)
            if match:
                value = match.group(0)
                code = code[len(value):].strip()
                if token_type:
                    tokens.append((token_type, value))
                break
        else:
            print(f"Lexer error: Unexpected character '{code[0]}'")
            sys.exit(1)
    tokens.append((EOF, ''))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = (EOF, '')

    def parse(self):
        return self.expr()

    def expr(self):
        if self.current_token[0] == NYA:
            return self.nya()
        else:
            return self.term()

    def nya(self):
        self.advance()  
        if self.current_token[0] != LPAR:
            print("Parser error: Expected '(' after 'nya'")
            sys.exit(1)
        self.advance()  
        if self.current_token[0] != STRING:
            print("Parser error: Expected string literal after '('")
            sys.exit(1)
        nya_string = self.current_token[1].strip('"')
        self.advance()  
        if self.current_token[0] != RPAR:
            print("Parser error: Expected ')' after string literal")
            sys.exit(1)
        self.advance()  
        nya_string = re.sub(r'{(.*?)}', lambda x: str(self.evaluate_expression(x.group(1))), nya_string)
        return nya_string

    def evaluate_expression(self, expr):
        expr = expr.strip()
        try:
            return eval(expr)
        except Exception as e:
            print(f"Evaluation error: {str(e)}")
            sys.exit(1)

    def term(self):
        token_type, value = self.current_token

        if token_type == INTEGER:
            self.advance()
            return int(value)
        elif token_type == STRING:
            self.advance()
            return str(value.strip('"'))
        else:
            print(f"Parser error: Unexpected token '{value}'")
            sys.exit(1)

def interpret(code):
    tokens = lex(code)
    parser = Parser(tokens)
    result = parser.parse()
    return result

def main(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    result = interpret(line)
                    print(f"Result: {result}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    main(filename)
