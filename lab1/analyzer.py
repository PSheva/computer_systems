
from tokenizer import tokenize
from validator import validate_expression

def analyze_expression(expression):
    tokens = tokenize(expression)
    errors = validate_expression(tokens)

    validity = len(errors) == 0
    return {
        "expression": expression,
        "validity": validity,
        "errors": errors,
        "tokens": tokens
    }


def analyze_multiple_expressions(expressions):
    results = {}
    for expr in expressions:
        results[expr] = analyze_expression(expr)
    return results

if __name__ == "__main__":
    expressions = [
    "a+b*(c-d)/e+sin(2)",
    "3+4.5*(x-y)+z/2",
    "sqrt(a+b)*log(c/d)-pi^2",
    "x*(y+z)-tan(a)/cos(b)*exp(c)",
    "a*b*c/d+e*(f+g-h)",
    
    "3..5+a-b*c",
    "a+b*(c-d))/e",
    "sin(cos(tan(a+b)))+pi)",
    "12e5+log(a+b)",
    "a+^b/(c-d))-sqrt(2.)",
    
    
    
    
    
    
    ]
    results = analyze_multiple_expressions(expressions)
    for expr, result in results.items():
        print(f"Вираз: \n {expr}")
        print(f"Чи вираз повністю правильний: {result['validity']}")
        print("Усі знайдені помилки:")
        for error in result['errors']:
            print(f"  - {error}")
        print("Токени та їх значення:")
        for token in result['tokens']:
            print(f"  {token}")
        print("---")