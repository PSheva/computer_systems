import re
from enum import Enum
import numpy as np

class TokenType(Enum):
    VARIABLE = 'VAR'
    NUMBER = 'NUM'
    OPERATOR = 'OPER'
    FUNCTION = 'FUNC'
    CONSTANT = 'CONST'
    PARENTHESIS = 'PAR'
    UNKNOWN = 'UN'

MATH_FUNCTIONS = ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'pow']
MATH_CONSTANTS = {
    'pi': np.pi,
    'e': np.e
}

def get_token_type(token):
    token_checks = {
        TokenType.VARIABLE: lambda t: len(t) == 1 and t.isalpha(),
        TokenType.FUNCTION: lambda t: t in MATH_FUNCTIONS,
        TokenType.CONSTANT: lambda t: t in MATH_CONSTANTS,
        TokenType.NUMBER: lambda t: re.match(r'^\d+\.\d+$|^\d+$', t),
        TokenType.OPERATOR: lambda t: t in '+-*/^',
        TokenType.PARENTHESIS: lambda t: t in '()',
    }

    for token_type, check in token_checks.items():
        if check(token):
            return token_type

    return TokenType.UNKNOWN

def tokenize(expression):
    tokens = []
    pattern = r'\b(?:sin|cos|tan|log|sqrt|exp|pow)|\b(?:pi|e)\b|[a-zA-Z]|\d+\.\d+|\d+|\.|[+\-*/^()]'
    for match in re.finditer(pattern, expression):
        token = match.group()
        token_type = get_token_type(token)
        tokens.append({
            'position': match.start(),
            'value': token,
            'type': token_type,
        })
    return tokens