import string
import json


def init(r, f, g, v, n):
    global Rules
    global Facts
    global Graph
    global visual
    global native
    Rules = r
    Facts = f
    Graph = g
    visual = v
    native = n


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
