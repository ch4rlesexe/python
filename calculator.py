import re

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b): 
    return a * b

def divide(a, b): 
    if b==0:
        raise ValueError("Cannot divide by zero")
    return a / b

def tokenize(expression):
    expression = expression.replace(" ", "").strip()
    if not expression:
        raise ValueError("Empty expression")
    parts = re.findall(r"\d+\.?\d*|[+\-*/]", expression) 
    tokens = []
    i = 0
    while i < len(parts):
        p = parts[i]
        if p == "-" and (not tokens or tokens[-1] in "+-*/") and i + 1 < len(parts):
            i += 1
            tokens.append(-float(parts[i]))

        elif p in "+-*/":
            tokens.append(p)

        else:
            tokens.append(float(p))

        i += 1


    if len(tokens) % 2 != 1:
        raise ValueError("Invalid expression.")
    return tokens

def do_ops(tokens, ops):
    out = []
    i = 0
    while i < len(tokens):
        if i + 2 < len(tokens) and isinstance(tokens[i + 1], str) and tokens[i + 1] in ops:
            a, op, b = tokens[i], tokens[i + 1], tokens[i + 2]
            if op == "*": out.append(multiply(a, b))
            elif op == "/": out.append(divide(a, b))
            elif op == "+": out.append(add(a, b))
            else: out.append(subtract(a, b))
            i += 3
        else:
            out.append(tokens[i])
            i += 1
    return out

def evaluate(tokens):
    tokens = list(tokens)
    while len(tokens) > 1:
        tokens = do_ops(tokens, "*/")
        tokens = do_ops(tokens, "+-")
    return tokens[0]


if __name__ == "__main__":
    print("-=-=-Calculator-=-=-\n")
    print("Type an expression or 'quit' to exit.")
    while True:
        user_input = input("Enter expression: ").strip()
        if user_input.lower() == "quit":
            print("Bye!")
            break

        if not user_input:
            continue

        try:
            result = evaluate(tokenize(user_input))
            print(f"  = {int(result) if result == int(result) else result}")
        except ValueError as e:
            print(f"  Error: {e}")