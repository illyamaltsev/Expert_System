import json

Rules = {
    'R1':[
        {
            "type": "operation",
            "value": "("
        },
        {
            "type": "fact", # "type": bool
            "value": "B",   # "value": True
            "not": False
        },
        {
            "type": "operation",
            "value": ")"
        },
        {
            "type": "operation",
            "value": "and"
        },
        {
            "type": "fact",
            "value": "B",
            "not": False
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
    'B': True
    
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
         # (A) -> A or (bool) -> bool
         if i + 2 < lenght and r["value"] == "(" and (Rules[rule_name][i + 1]["type"] == "fact" or Rules[rule_name][i + 1]["type"] == "bool") and Rules[rule_name][i + 2]["value"] == ")":
             del Rules[rule_name][i]
             del Rules[rule_name][i + 1]
             check_BRACKETS(rule_name)

def check_AND(rule_name):
    global Rules
    lenght = len(Rules[rule_name])
    for i, r in enumerate(Rules[rule_name]):
        if i + 3 < lenght and i > 0 and r["value"] == "and":
            ### A AND bool
            if Rules[rule_name][i - 1]["type"] == "fact" and Rules[rule_name][i + 1]["type"] == "bool":
                # A AND True -> A
                if Rules[rule_name][i + 1]["value"] == True:
                    del Rules[rule_name][i]
                    del Rules[rule_name][i]
                # A AND False -> False
                else:
                    del Rules[rule_name][i]
                    del Rules[rule_name][i]
                    Rules[rule_name][i - 1]["type"] = "bool"
                    Rules[rule_name][i - 1]["value"] = False
                check_AND(rule_name)
            ### bool AND A
            elif Rules[rule_name][i - 1]["type"] == "bool" and Rules[rule_name][i + 1]["type"] == "fact":
                # True AND A -> A
                if Rules[rule_name][i - 1]["value"] == True:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                # False AND A -> False
                else:
                    del Rules[rule_name][i]
                    del Rules[rule_name][i]
                check_AND(rule_name)
            ### bool AND bool
            elif Rules[rule_name][i - 1]["type"] == "bool" and Rules[rule_name][i + 1]["type"] == "bool":
                # True AND True -> True
                if Rules[rule_name][i - 1]["value"] == Rules[rule_name][i + 1]["value"] == True:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                # False AND bool -> False or bool AND False -> False
                if Rules[rule_name][i - 1]["value"] == False or Rules[rule_name][i + 1]["value"] == False:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                    Rules[rule_name][i - 1]["type"] = "bool"
                    Rules[rule_name][i - 1]["value"] = False
                check_AND(rule_name)
            ### A and A
            elif Rules[rule_name][i - 1]["value"] == Rules[rule_name][i + 1]["value"]:
                # A AND A -> A or !A AND !A -> !A
                if Rules[rule_name][i - 1]["not"] == Rules[rule_name][i + 1]["not"]:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                # A AND !A -> False or !A AND A -> False
                else:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                    Rules[rule_name][i - 1]["type"] = "bool"
                    Rules[rule_name][i - 1]["value"] = False
                check_AND(rule_name)

def check_OR(rule_name):
    global Rules
    lenght = len(Rules[rule_name])
    for i, r in enumerate(Rules[rule_name]):
        if i + 3 < lenght and i > 0 and r["value"] == "or":
            ### A OR bool
            if Rules[rule_name][i - 1]["type"] == "fact" and Rules[rule_name][i + 1]["type"] == "bool":
                # A OR True -> True
                if Rules[rule_name][i + 1]["value"] == True:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                # A OR False -> A
                else:
                    del Rules[rule_name][i]
                    del Rules[rule_name][i]
                check_OR(rule_name)
            ### bool OR A
            elif Rules[rule_name][i - 1]["type"] == "bool" and Rules[rule_name][i + 1]["type"] == "fact":
                # True OR A -> True
                if Rules[rule_name][i - 1]["value"] == True:
                    del Rules[rule_name][i]
                    del Rules[rule_name][i]
                # False OR A -> A
                else:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                check_OR(rule_name)
            ### bool OR bool
            elif Rules[rule_name][i - 1]["type"] == "bool" and Rules[rule_name][i + 1]["type"] == "bool":
                # True OR True -> True
                if Rules[rule_name][i - 1]["value"] == True or Rules[rule_name][i + 1]["value"] == True:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                    Rules[rule_name][i - 1]["type"] = "bool"
                    Rules[rule_name][i - 1]["value"] = True
                # False OR bool -> bool
                elif Rules[rule_name][i - 1]["value"] == False:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                # bool OR False -> bool
                elif Rules[rule_name][i + 1]["value"] == False:
                    del Rules[rule_name][i]
                    del Rules[rule_name][i]
                check_OR(rule_name)
            ### A OR A
            elif Rules[rule_name][i - 1]["value"] == Rules[rule_name][i + 1]["value"]:
                # A OR A -> A or !A OR !A -> !A
                if Rules[rule_name][i - 1]["not"] == Rules[rule_name][i + 1]["not"]:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                # A OR !A -> True or !A OR A -> True
                else:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                    Rules[rule_name][i - 1]["type"] = "bool"
                    Rules[rule_name][i - 1]["value"] = True
                check_OR(rule_name)

def check_XOR(rule_name):
    global Rules
    lenght = len(Rules[rule_name])
    for i, r in enumerate(Rules[rule_name]):
        if i + 3 < lenght and i > 0 and r["value"] == "xor":
            ### A XOR bool
            if Rules[rule_name][i - 1]["type"] == "fact" and Rules[rule_name][i + 1]["type"] == "bool":
                # A XOR True -> !A
                if Rules[rule_name][i + 1]["value"] == True:
                    del Rules[rule_name][i]
                    del Rules[rule_name][i]
                    Rules[rule_name][i - 1]["not"] = not Rules[rule_name][i - 1]["not"]

                # A XOR False -> A
                else:
                    del Rules[rule_name][i]
                    del Rules[rule_name][i]
                check_XOR(rule_name)
            ### bool XOR A
            elif Rules[rule_name][i - 1]["type"] == "bool" and Rules[rule_name][i + 1]["type"] == "fact":
                # True XOR A -> !A
                if Rules[rule_name][i - 1]["value"] == True:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                    Rules[rule_name][i - 1]["not"] = not Rules[rule_name][i - 1]["not"]
                # False XOR A -> A
                else:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                check_XOR(rule_name)
            ### bool XOR bool
            elif Rules[rule_name][i - 1]["type"] == "bool" and Rules[rule_name][i + 1]["type"] == "bool":
                # True XOR True -> False
                if Rules[rule_name][i - 1]["value"] == True and Rules[rule_name][i + 1]["value"] == True:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                    Rules[rule_name][i - 1]["type"] = "bool"
                    Rules[rule_name][i - 1]["value"] = False
                # False XOR bool -> bool
                elif Rules[rule_name][i - 1]["value"] == False:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                # bool XOR False -> bool
                elif Rules[rule_name][i + 1]["value"] == False:
                    del Rules[rule_name][i]
                    del Rules[rule_name][i]
                check_XOR(rule_name)
            ### A XOR A
            elif Rules[rule_name][i - 1]["value"] == Rules[rule_name][i + 1]["value"]:
                # A XOR A -> False or !A XOR !A -> False
                if Rules[rule_name][i - 1]["not"] == Rules[rule_name][i + 1]["not"]:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                    Rules[rule_name][i - 1]["type"] = "bool"
                    Rules[rule_name][i - 1]["value"] = False
                # A XOR !A -> True or !A XOR A -> True
                else:
                    del Rules[rule_name][i - 1]
                    del Rules[rule_name][i - 1]
                    Rules[rule_name][i - 1]["type"] = "bool"
                    Rules[rule_name][i - 1]["value"] = True
                check_XOR(rule_name)

def check_IMPLIES(rule_name):
    # ... -> A AND True =>  A = True; A AND True -> True
    pass

def check_IFANDONLYIF(rule_name):
    pass

def check_FINAL(rule_name):
    pass

def calculate(rule_name):
    check_BRACKETS(rule_name)       #+
    check_AND(rule_name)            #+ but only in left side
    check_OR(rule_name)             #+
    check_XOR(rule_name)            #+
    check_IMPLIES(rule_name)
    check_IFANDONLYIF(rule_name)
    check_FINAL(rule_name)




def transform(rule_name: str, fact: str):
    global Rules
    global Facts
    for i, r in enumerate(Rules[rule_name]):
        if r["value"] == fact:
            Rules[rule_name][i]["type"] = "bool"
            # !A -> not bool
            if r["not"]:
                Rules[rule_name][i]["value"] = not Facts[fact]
            # A -> bool
            else:
                Rules[rule_name][i]["value"] = Facts[fact]
    calculate(rule_name)

if __name__ == "__main__":
    transform('R1', 'B')
    print(json.dumps(Rules, indent=4))