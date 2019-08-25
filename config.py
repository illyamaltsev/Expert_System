import string


def init(r, f, g):
    global Rules
    global Facts
    global Graph
    Rules = r
    Facts = f
    Graph = g


FACT_CHARS = string.ascii_uppercase

OPERATIONS = {
    '+': 'and',
    '|': 'or',
    '^': 'xor',
    '!': 'not',
    '*': 'implies',
    '$': 'if and only if',
    '(': '(',
    ')': ')'
}

