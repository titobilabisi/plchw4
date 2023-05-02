class Parser:
    def __init__(self, token_list):
        self.tokens = token_list
        self.current_token = None
        self.index = -1
        self.advance()

    def advance(self):
        # Increment the index and set the current token to the next token
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def match(self, token_type):
        # Check if the current token matches the expected token type
        # Advance if it matches, otherwise raise an exception
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(f"Syntax error: Expected {token_type} but found {self.current_token.type}")

    def parse(self):
        self.stmt_list()

    def stmt_list(self):
        self.stmt()
        self.match(';')
        while self.current_token and self.current_token.type != '}':
            self.stmt()
            self.match(';')

    def stmt(self):
        if self.current_token.type == 'IF':
            self.if_stmt()
        elif self.current_token.type == '{':
            self.block()
        elif self.current_token.type == 'WHILE':
            self.while_loop()
        else:
            self.expr()

    def if_stmt(self):
        self.match('IF')
        self.match('(')
        self.bool_expr()
        self.match(')')
        if self.current_token.type == '{':
            self.block()
            if self.current_token and self.current_token.type == 'ELSE':
                self.match('ELSE')
                if self.current_token.type == '{':
                    self.block()
                else:
                    self.stmt()
        else:
            self.stmt()
            if self.current_token and self.current_token.type == 'ELSE':
                self.match('ELSE')
                if self.current_token.type == '{':
                    self.block()
                else:
                    self.stmt()

    def block(self):
        self.match('{')
        self.stmt_list()
        self.match('}')

    def while_loop(self):
        self.match('WHILE')
        self.match('(')
        self.bool_expr()
        self.match(')')
        if self.current_token.type == '{':
            self.block()

    def expr(self):
        self.term()
        while self.current_token and self.current_token.type in ['+', '-']:
            op = self.current_token
            self.advance()
            self.term()

    def term(self):
        self.factor()
        while self.current_token and self.current_token.type in ['*', '/', '%']:
            op = self.current_token
            self.advance()
            self.factor()

    def factor(self):
        if self.current_token.type == 'ID':
            self.match('ID')
        elif self.current_token.type in ['INT_LIT', 'FLOAT_LIT']:
            self.match(self.current_token.type)
        elif self.current_token.type == '(':
            self.match('(')
            self.expr()
            self.match(')')

    def bool_expr(self):
        self.bterm()
        while self.current_token and self.current_token.type in ['>', '<', '>=', '<=']:
            op = self.current_token
            self.advance()
            self.bterm()

    def bterm(self):
        self.band()
        while self.current_token and self.current_token.type in ['==', '!=']:
            op = self.current_token
            self.advance()
            self.band()

    def band(self):
        self.bor()
        while self.current_token and self.current_token.type == '&&':
            op = self.current_token
            self.advance()
            self.bor()

    def bor
