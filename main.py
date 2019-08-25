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

visual = False

def priority(f):
    if f == '?':
        return -2
    if f == None:
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
            if visual:
                draw_graph(fact, rule)
            res = transform(rule, fact)
            config.Graph.remove_edge(fact, rule)
            if res:  # if transform solved all rule
                config.Graph.remove_node(rule)
        facts = sorted(facts, key=lambda f: priority(config.Facts[f]), reverse=True)



def main(argc, argv):
    global visual
    if "-v" in argv:
        visual = True
    try:
        f_content = read_all(argv[argv.index("-f") + 1])
    except:
        print("Usage: python main.py [-v] -f file_name")
        exit()
    tokens = lex(f_content)
    parsed = parse(tokens)
    # print(json.dumps(parsed, indent=4))

    question_facts = parsed["question_facts"]
    Rules = parsed["rules"]
    Facts = parsed["facts"]
    Graph = nx.Graph(parsed["graph_body"])

    config.init(Rules, Facts, Graph)

    init_pos()
    if visual:
        draw_graph()
    solve()
    if visual:
        draw_graph()

    # Result
    for q in question_facts:
        print(q, Facts[q])


main(len(sys.argv), sys.argv)
