import networkx as nx
import matplotlib.pyplot as plt
import re


def draw_graph(graph, rules):
    color_map = []

    for node in graph:
        if re.match(r"^R\d+$", node) is not None:
            color_map.append('green')
        else:
            color_map.append('red')
    text = ""
    for k in rules:
        text += k + ": "
        for elem in rules[k]:
            text += str(elem[1]) + " "
        text += '\n'

    plt.title(text)

    nx.draw_networkx(graph, node_color=color_map)
    plt.show()
