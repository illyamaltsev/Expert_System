import sys
import json
import networkx as nx


from utils.reader import read_all
from utils.lexer import lex
from utils.parser import parse
from utils.drawer import draw_graph, init_pos
import config
from tranformator import transform

# Global variables


def priority(f):
    if f == '?':
        return -1
    return int(f)


def solve():
    facts = list(config.Facts.keys())
    facts = sorted(facts, key=lambda f: priority(config.Facts[f]), reverse=True)
    while len(facts) > 0:
        fact = facts.pop(0)
        if config.Facts[fact] == '?':
            return
        connected_rules = list(config.Graph.neighbors(fact))
        for rule in connected_rules:
            draw_graph(fact, rule)
            res = transform(rule, fact)
            if res:  # if transform solved all rule
                config.Graph.remove_node(rule)
        facts = sorted(facts, key=lambda f: priority(config.Facts[f]), reverse=True)


def main(argc, argv):
    filename = 'test.txt'
    f_content = read_all(filename)
    tokens = lex(f_content)
    parsed = parse(tokens)
    # print(json.dumps(parsed, indent=4))

    question_facts = parsed["question_facts"]
    Rules = parsed["rules"]
    Facts = parsed["facts"]
    Graph = nx.Graph(parsed["graph_body"])

    config.init(Rules, Facts, Graph)

    init_pos()
    draw_graph()
    solve()

    # Result
    for q in question_facts:
        print(q, Facts[q])


main(len(sys.argv), sys.argv)
