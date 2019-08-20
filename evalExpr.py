#!/usr/local/bin/python3.7

def number(expr):
    nb = "0123456789.,j"
    if expr[0] == '(':
        nbr1, expr = evalExpr(expr[1:])
        if expr[0] == ')':
            expr = expr[1:]
        return nbr1, expr
    i = 0
    k = ''
    if expr[0] in "-+":
        k = expr[0]
        expr = expr[1:]
        nbr1, expr = number(expr)
        if k == '-':
            return -nbr1, expr
        else:
            return nbr1, expr
    for j in expr:
        if j not in nb:
            break
        i += 1
    try:
        return int(k + expr[0:max(i,1)]), expr[i:]
    except:
        try:
            return float(k + expr[0:max(i,1)]), expr[i:]
        except:
            try:
                return complex(k + expr[0:max(i,1)]), expr[i:]
            except:
                exit()

def factors(expr):
    nbr1, expr = number(expr)
    while len(expr):
        op = expr[0]
        if op not in '/*%^':
            return nbr1, expr
        expr = expr[1:]
        nbr2, expr = number(expr)
        if op == '/':
            nbr1 /= nbr2
        elif op == '*':
            nbr1 *= nbr2
        elif op == '%':
            nbr1 %= nbr2
        else:
            nbr1 = nbr1**nbr2
    return nbr1, expr

def evalExpr(expr):
    nbr1, expr = factors(expr)
    while len(expr):
        op = expr[0]
        if op not in '+-':
            return nbr1, expr
        expr = expr[1:]
        nbr2, expr = factors(expr)
        if op == '+':
            nbr1 += nbr2
        else:
            nbr1 -= nbr2
    return nbr1, expr

def calc(expr):
    for j in "\t\n\v\f\r ":
        expr = expr.replace(j, '')
    nb, expr = evalExpr(expr.replace('i', 'j'))
    return str(nb).replace('j', 'i')

if __name__ == "__main__":
    while True:
        inp = input("> ")
        if (inp == '\\q'):
            exit()
        nb = calc(inp)
        print('aswer:', nb)