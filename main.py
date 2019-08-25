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
right_Nones = []


def priority(fact_name):
    fact_value = config.Facts[fact_name]
    if fact_value == '?':
        return -3
    elif fact_value == None and fact_name in right_Nones:
        return -2
    elif fact_value == None:
        return -1
    elif fact_value == False:
        return 0
    elif fact_value == True:
        return 1


def update_none_right():
    global right_Nones
    right_Nones = []
    for rule_name in list(config.Rules.keys()):
        rule = config.Rules[rule_name]
        for i, elem in enumerate(rule):
            print(elem)
            if elem["value"] == "implies":
                while i < len(rule):
                    if rule[i]["type"] == "fact" and rule[i]["value"] not in right_Nones:
                        right_Nones.append(rule[i]["value"])
                    i += 1


def solve():
    facts = list(config.Facts.keys())
    update_none_right()
    facts = sorted(facts, key=lambda f: priority(f), reverse=True)
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
        update_none_right()
        facts = sorted(facts, key=lambda f: priority(f), reverse=True)



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
