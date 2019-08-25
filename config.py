import string
import json

def init(r, f, g=None):
    global Rules
    global Facts
    global Graph
    Rules = r
    Facts = f
    Graph = g
    print(json.dumps(Rules, indent=4))
    print(json.dumps(Facts, indent=4))


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

