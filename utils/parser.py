
def push_facts(facts, true_facts, question_facts):
    facts_dict = {}
    for f in facts:
        if f in true_facts:
            facts_dict[f] = True
        elif f in question_facts:
            facts_dict[f] = '?'
        else:
            facts_dict[f] = None
    return facts_dict


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
        elif k is "fact" or k is "operation":
            rules_counter += 1
            rule_name = 'R' + str(rules_counter)
            facts_in_rule = []
            rule = []
            while k is not "\n" and i < len(tokens):
                elem = {
                    "type": k,
                    "value": v
                }
                if v != "not":
                    rule.append(elem)
                if k is "fact" or (k is "operation" and v is "("):
                    if i != 0 and tokens[i-1][1] == "not":
                        elem["not"] = True
                    else:
                        elem["not"] = False
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
        "facts": push_facts(all_facts, true_facts, question_facts),
        "question_facts": question_facts,
        "rules": rules,
        "graph_body": graph_body
    }

    return response
