import networkx as nx
import matplotlib.pyplot as plt
import re
import config


def rule_to_str(rule_name):
    s = ""
    for elem in list(config.Rules[rule_name]):
        try:
            if elem["not"]:
                s += "not "
        except:
            pass
        s += str(elem["value"]) + " "
    return s


def init_pos():
    global pos_nodes
    global step
    step = 0
    pos_nodes = nx.spring_layout(config.Graph, seed=1)


def draw_graph(fact=None, rule_name=None):

    color_map = []
    labels = {}

    for node in config.Graph:
        try:
            if config.Facts[node]==True or config.Facts[node] == False:
                labels[node] = str(config.Facts[node])
            else:
                labels[node] = ""
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
            try:
                if elem["not"]:
                    text += "not "
            except:
                pass
            text += str(elem["value"]) + " "
        text += '\n'

    text += "step: " + str(step)
    globals()["step"] += 1

    pos_labels = {}
    for node, coords in pos_nodes.items():
        pos_labels[node] = (coords[0], coords[1] + 0.05)

    plt.figure(figsize=(15, 10))
    plt.title(text, loc="center")
    nx.draw_networkx(config.Graph, pos=pos_nodes,  node_color=color_map)
    nx.draw_networkx_labels(config.Graph, pos_labels, labels=labels)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=1-(len(config.Rules.keys()) + 1) * 0.02)
    plt.show()
    plt.close()

