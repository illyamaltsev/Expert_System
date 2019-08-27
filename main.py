import sys
import json
import networkx as nx

from utils.reader import read_all
from utils.lexer import lex
from utils.parser import parse
from utils.drawer import draw_graph, init_pos, rule_to_str
import config
from tranformator import transform

# Global variables


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
        if config.native:
            print("============================")
        fact = facts.pop(0)
        if config.native and config.Facts[fact] != None:
            print("We know exactly that " + fact + " is " + str(config.Facts[fact]))
        if config.Facts[fact] == '?':
            return
        if config.Facts[fact] == None:
            config.Facts[fact] = False
            if config.native:
                print(fact + " is " + str(config.Facts[fact]))
        connected_rules = list(config.Graph.neighbors(fact))
        for rule in connected_rules:
            if config.visual:
                draw_graph(fact, rule)
            if config.native:
                print("-  -  -  -  -  -  -  -  -  -")
                print(fact, "is mentioned in rule:", rule_to_str(rule))

            res = transform(rule, fact)
            config.Graph.remove_edge(fact, rule)
            if res:  # if transform solved all rule
                config.Graph.remove_node(rule)
        update_none_right()
        facts = sorted(facts, key=lambda f: priority(f), reverse=True)

def check_rules(Rules):
    # is_implie = False
    # for rule in Rules:
    #     for i, r in enumerate(rule):
    #         if r["value"] == "implies" or r["value"] == "if and only if":
    #             is_implie = True
    #         if r["type"] == "fact" and i + 1 < len(rule) and (rule[i + 1]["type"] == "fact" or rule[i + 1]["value"] == "("):
    #             return False
    #         elif r["type"] == "operation" and r["value"] != "(" and i + 1 < len(rule) and rule[i + 1]["type"] == "operation":
   pass         

def main(argc, argv):
    visual = False
    native = False
    if "-v" in argv:
        visual = True
    if "-n" in argv:
        native = True
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
    check_rules(Rules)
    Facts = parsed["facts"]
    Graph = nx.Graph(parsed["graph_body"])

    config.init(Rules, Facts, Graph, visual, native)

    init_pos()
    if config.visual:
        draw_graph()
    solve()
    if config.visual:
        draw_graph()

    # Result
    for q in question_facts:
        print(q, Facts[q])


main(len(sys.argv), sys.argv)
