

Rules = {
    'R1':[
        {
            "type": "fact", # "type": bool
            "value": "B"    # "value": True
        },
        {
            "type": "operation",
            "value": "and"
        },
        {
            "type": "fact",
            "value": "C",
            "not": True
        },
        {
            "type": "operation",
            "value": "implies"
        },
        {
            "type": "bool",
            "value": True
        }
    ]
}

Facts = {
    'A': True
    
}

"""
    rule name examples:
    1)rule_name = 'R1'
    2)rule_name = 'R2'
    
    fact examples:
    1)fact = {
        "fact": "B"
        "value": True
    }
    2)fact = {
        "fact": "A"
        "value": False
    }
""" 

def check_BRACKETS(rule_name):
     global Rules
     lenght = len(Rules[rule_name])
     for i, r in enumerate(Rules[rule_name]):
         if i + 2 < lenght and r["value"] == "(" and (Rules[rule_name][i + 1]["type"] == "fact" or Rules[rule_name][i + 1]["type"] == "bool") and Rules[rule_name][i + 2]["value"] == ")":
             del Rules[rule_name][i]
             del Rules[rule_name][i + 2]
             check_BRACKETS(rule_name)


def calculate(rule_name):
    check_BRACKETS(rule_name) #+
    check_AND(rule_name)
    check_OR(rule_name)
    check_XOR(rule_name)
    check_IMPLIES(rule_name)
    check_IFANDONLYIF(rule_name)
    return check_FINAL(rule_name)




def transform(rule_name: str, fact: str):
    global Rules
    global Facts
    for i, r in enumerate(Rules[rule_name]):
        if r["value"] == fact:
            Rules[rule_name][i]["type"] = "bool"
            if r["not"]:
                Rules[rule_name][i]["value"] = not Facts[fact]
            else
                Rules[rule_name][i]["value"] = Facts[fact]
    return calculate(rule_name)