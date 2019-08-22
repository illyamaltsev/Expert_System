import sys
import json
import networkx as nx

from utils.reader import read_all
from utils.lexer import lex
from utils.parser import parse
from utils.drawer import draw_graph
from tranformator import transform

# Global variables
Rules = None
Facts = None
Graph = None


def priority(f):
    if f == '?':
        return -1
    return int(f)


def solve():
    global Graph
    facts = list(Facts.keys())
    while len(facts) > 0:
        fact = facts.pop()
        assert Facts[fact] != '?'
        connected_rules = Graph.neighbors(fact)
        for rule in connected_rules:
            res = transform(rule, fact)
            if res:  # if transform solved all rule
                Graph.remove_node(rule)
        Graph.remove_node(fact)
        facts = sorted(facts, key=lambda f: priority(Facts[f]), reverse=True)


def main(argc, argv):
    global Rules
    global Facts
    global Graph
    filename = 'test.txt'
    f_content = read_all(filename)
    tokens = lex(f_content)
    parsed = parse(tokens)
    print(json.dumps(parsed, indent=4))

    question_facts = parsed["question_facts"]
    Rules = parsed["rules"]
    Facts = parsed["facts"]
    Graph = nx.Graph(parsed["graph_body"])

    # draw_graph(graph, parsed["rules"])
    # solve()

    # Result
    for q in question_facts:
        print(q, Facts[q])


main(len(sys.argv), sys.argv)
