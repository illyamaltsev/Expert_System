import networkx as nx


# parser
def parse(tokens: list):
    true_facts = []
    question_facts = []

    rules = {}

    graph_body = {}

    all_facts = []

    rules_counter = 0

    i = 0
    while i < len(tokens):
        k, v = tokens[i]
        if k is "true_facts":
            while k is not "\n" and i < len(tokens):
                k, v = tokens[i]
                if k is "fact":
                    true_facts.append(v)
                i = i + 1
        elif k is "question_facts":
            while k is not "\n" and i < len(tokens):
                k, v = tokens[i]
                if k is "fact":
                    question_facts.append(v)
                i = i + 1
        elif k is "fact":
            rules_counter += 1
            rule_name = 'R' + str(rules_counter)
            facts_in_rule = []
            rule = []
            while k is not "\n" and i < len(tokens):
                rule.append(tokens[i])
                if k is "fact":
                    facts_in_rule.append(v)
                    if v not in all_facts:
                        all_facts.append(v)
                i = i + 1
                k, v = tokens[i]
            graph_body[rule_name] = facts_in_rule  # link from rule to facts
            rules[rule_name] = rule
        elif k is "\n":
            i = i + 1

    response = {
        "facts": all_facts,
        "true_facts": true_facts,
        "question_facts": question_facts,
        "rules": rules,
        "graph_body": graph_body
    }

    return response


def build_graph(graph_body: dict):
    graph = nx.Graph(graph_body)
    return graph
