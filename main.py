import sys

from utils.reader import read_all
from utils.lexer import lex
from utils.parser import parse, build_graph
from utils.drawer import draw_graph

# Global variables
Rules = {}
Facts = {}


def solve(graph):
    queue = []
    for k, v in Facts:
        if v:
            queue.append(k)

    while True:
        try:
            fact = queue.pop(0)
        except Exception as e:
            print(e)
            break
        connected_rules = graph.neighbors(fact)
        for r in connected_rules:
            res = transform(r, fact)


def main(argc, argv):
    filename = 'test.txt'
    f_content = read_all(filename)
    tokens = lex(f_content)
    parsed = parse(tokens)

    graph = build_graph(parsed["graph_body"])
    draw_graph(graph, parsed["rules"])


main(len(sys.argv), sys.argv)
