from tokenizer import TokenType, MATH_FUNCTIONS
import re

def validate_expression(tokens):
    errors = []
    stack = []

    def check_parentheses():
        for index in stack:
            errors.append(f"Відкриваюча дужка без відповідної закриваючої на позиції {tokens[index]['position']}")

    def check_ending_token():
        last_token = tokens[-1] if tokens else None
        if last_token:
            if last_token['type'] == TokenType.OPERATOR:
                errors.append(f"Вираз закінчується оператором на позиції {last_token['position']}")
            elif last_token['value'] == '(':
                errors.append(f"Вираз закінчується відкриваючою дужкою на позиції {last_token['position']}")

    def check_operator_before_closing_parenthesis(token, next_token):
        if token['type'] == TokenType.OPERATOR and next_token and next_token['value'] == ')':
            return f"Оператор '{token['value']}' перед закриваючою дужкою на позиції {token['position']}"
        return None

    def check_number_before_variable(token, next_token):
        if token['type'] == TokenType.NUMBER and next_token and next_token['type'] == TokenType.VARIABLE:
            return f"Число '{token['value']}' без оператора перед змінною '{next_token['value']}' на позиції {token['position']}"
        return None


    def check_variable_before_number(token, next_token):
        if token['type'] == TokenType.VARIABLE and next_token and next_token['type'] == TokenType.NUMBER:
            return f"Змінна '{token['value']}' без оператора перед числом '{next_token['value']}' на позиції {token['position']}"
        return None

    def check_empty_parentheses(token, next_token):
        if token['value'] == '(' and next_token and next_token['value'] == ')':
            return f"Пусті дужки на позиціях {token['position']} і {next_token['position']}"
        return None

    def check_closing_parenthesis_after_operator(token, prev_token):
        if token['value'] == ')' and prev_token and prev_token['type'] == TokenType.OPERATOR:
            return f"Закриваюча дужка після оператора '{prev_token['value']}' на позиції {prev_token['position']}"
        return None

    def check_consecutive_operators(token, prev_token):
        if token['type'] == TokenType.OPERATOR and prev_token and prev_token['type'] == TokenType.OPERATOR:
            return f"Два оператори підряд на позиціях {prev_token['position']} і {token['position']}"
        return None

    def check_operator_after_opening_parenthesis(token, prev_token):
        if prev_token and prev_token['value'] == '(' and token['type'] == TokenType.OPERATOR:
            return f"Оператор '{token['value']}' одразу після відкриваючої дужки на позиції {token['position']}"
        return None

    
    
    
    # перевірка 1 рівня, а саме дозволені переходи між різнми токенами 
    def check_token_transitions(token, index):
        next_token = tokens[index + 1] if index + 1 < len(tokens) else None
        prev_token = tokens[index - 1] if index > 0 else None

        checks = [
            check_operator_before_closing_parenthesis(token, next_token),
            check_number_before_variable(token, next_token),
            check_variable_before_number(token, next_token),
            check_empty_parentheses(token, next_token),
            check_closing_parenthesis_after_operator(token, prev_token),
            check_consecutive_operators(token, prev_token),
            check_operator_after_opening_parenthesis(token, prev_token),
        ]

        for check in checks:
            if check:
                errors.append(check)


    # перевірка 2 рівня
    def check_starting_token(token):
        if token['type'] == TokenType.OPERATOR and token['value'] not in '+-':
            errors.append(f"Недопустимий оператор '{token['value']}' на початку виразу (позиція {token['position']})")

    def check_variable_name(token, index):
        next_token = tokens[index + 1] if index + 1 < len(tokens) else None
        if token['type'] == TokenType.VARIABLE and next_token and next_token['type'] == TokenType.VARIABLE:
            errors.append(f"Некоректна комбінація змінних '{token['value']}{next_token['value']}' на позиціях {token['position']} і {next_token['position']}")

    def check_number_format(token):
        if token['type'] == TokenType.NUMBER and not re.match(r'^\d+\.\d+$|^\d+$', token['value']):
            errors.append(f"Некоректний формат числа '{token['value']}' на позиції {token['position']}")
        elif token['type'] == TokenType.UNKNOWN and token['value'] == '.':
            errors.append(f"Некоректне використання десяткової крапки на позиції {token['position']}")

    def check_function_name(token, index):
        next_token = tokens[index + 1] if index + 1 < len(tokens) else None
        if token['type'] == TokenType.FUNCTION and (not next_token or next_token['value'] != '('):
            errors.append(f"Відсутня відкрита дужка після функції '{token['value']}' на позиції {token['position']}")

    def check_division_by_zero(token, index):
        if token['type'] == TokenType.NUMBER and token['value'] == '0':
            prev_token = tokens[index - 1] if index > 0 else None
            if prev_token and prev_token['value'] == '/':
                errors.append(f"Ділення на нуль на позиції {token['position']}")

    for i, token in enumerate(tokens):
        if token['value'] == '(':
            stack.append(i)
        elif token['value'] == ')':
            if not stack:
                errors.append(f"Закриваюча дужка без відповідної відкриваючої на позиції {token['position']}")
            else:
                stack.pop()

        if i == 0:
            check_starting_token(token)
        check_token_transitions(token, i)
        check_variable_name(token, i)
        check_number_format(token)
        if token['type'] == TokenType.FUNCTION:
            check_function_name(token, i)
        check_division_by_zero(token, i)

    check_parentheses()
    check_ending_token()

    return errors
