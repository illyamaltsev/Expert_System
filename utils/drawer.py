import networkx as nx
import matplotlib.pyplot as plt
import re
import config


def draw_graph(fact=None, rule_name=None):
    color_map = []

    for node in config.Graph:
        if node == fact:
            color_map.append('cyan')
        elif node == rule_name:
            color_map.append('grey')
        elif re.match(r"^R\d+$", node) is not None:
            color_map.append('green')
        else:
            color_map.append('red')


    text = ""
    for k in config.Rules.keys():
        text += k + ": "
        for elem in config.Rules[k]:
            text += str(elem["value"]) + " "
        text += '\n'

    plt.figure(figsize=(15, 10))
    plt.title(text)
    plt.axis('off')
    nx.draw_networkx(config.Graph, node_color=color_map)
    plt.show()
