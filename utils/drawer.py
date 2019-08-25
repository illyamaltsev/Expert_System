import networkx as nx
import matplotlib.pyplot as plt
import re
import config


def init_pos():
    global pos_nodes
    pos_nodes = nx.spring_layout(config.Graph)


def draw_graph(fact=None, rule_name=None):
    color_map = []
    labels = {}

    for node in config.Graph:
        try:
            labels[node] = str(config.Facts[node])
        except:
            labels[node] = ""
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

    pos_labels = {}
    for node, coords in pos_nodes.items():
        pos_labels[node] = (coords[0], coords[1] + 0.08)

    plt.figure(figsize=(15, 10))
    plt.title(text)
    plt.axis('off')
    nx.draw_networkx(config.Graph, pos=pos_nodes,  node_color=color_map)
    nx.draw_networkx_labels(config.Graph, pos_labels, labels=labels)
    plt.show()

