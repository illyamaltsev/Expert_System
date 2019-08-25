# coding: utf8
import json

Rules = {
    'R1':[
        {
            "type": "bool",
            "value": True,
            "not": False
        },
        {
            "type": "operation",
            "value": "implies"
        },
        {
            "type": "fact",
            "value": "B",
            "not": False
        },
        {
            "type": "operation",
            "value": "and",
            "not": False
        },
        {
            "type": "fact",
            "value": "C",
            "not": False
        }
    ]
}

Facts = {
    'B': True,
    'C': False
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
            # !(...) -> !...
            if Rules[rule_name][i]["not"]:
                # !(A) -> !A
                if Rules[rule_name][i + 1]["type"] == "fact":
                    Rules[rule_name][i + 1]["not"] = not Rules[rule_name][i + 1]["not"]
                else:
                    Rules[rule_name][i + 1]["value"] = not Rules[rule_name][i + 1]["value"]
            # раскрываем скобки удаляя их
            del Rules[rule_name][i]
            del Rules[rule_name][i + 1]
            check_BRACKETS(rule_name)

def check_AND(rule_name):
    global Rules
    lenght = len(Rules[rule_name])
    for i, r in enumerate(Rules[rule_name]):
        if i + 1 < lenght and i > 0 and r["value"] == "and":
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
        if i + 1 < lenght and i > 0 and r["value"] == "or":
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
        if i + 1 < lenght and i > 0 and r["value"] == "xor":
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

def check_right_part(rule_name):
    global Rules
    global Facts
    facts_to_change = []
    implies = False
    for rule in Rules[rule_name]:
        # ignore left side, before implies
        if rule["value"] == "implies":
            implies = True
            continue
        # check only right side
        if implies == True:
            # if operations not "and", "(", ")" -> return false
            if rule["type"] == "operation" and rule["value"] not in ["and", "(", ")"]:
                return False, facts_to_change
            # append fact and value what change to
            elif rule["type"] == "fact":
                facts_to_change.append({rule["value"]:not rule["not"]})
    # return True and facts_to_change only if it's OK
    return True, facts_to_change

def check_left_part(rulename):
    global Rules
    global Facts
    facts_to_change = []
    for rule in Rules[rule_name]:
        # ignore left side, before implies
        if rule["value"] == "implies":
            return True, facts_to_change
        # check only right side
        # if operations not "and", "(", ")" -> return false
        if rule["type"] == "operation" and rule["value"] not in ["and", "(", ")"]:
            return False, facts_to_change
        # append fact and value what change to
        elif rule["type"] == "fact":
            facts_to_change.append({rule["value"]:not rule["not"]})
    

def check_IMPLIES(rule_name):
    global Rules
    global Facts
    # ... -> ... but A -> True or False -> A then A = underfit
    if len(Rules[rule_name]) == 3 and Rules[rule_name][1]["value"] == "implies":
        # True -> A => A = True
        if Rules[rule_name][0]["type"] == "bool" and Rules[rule_name][0]["value"] == True and Rules[rule_name][2]["type"] == "fact":
            # A => True
            if not Rules[rule_name][2]["not"]:
                Facts[Rules[rule_name][2]["value"]] = True
            # !A => False
            else:
                Facts[Rules[rule_name][2]["value"]] = False
        # A -> False => A = False
        if Rules[rule_name][0]["type"] == "fact" and Rules[rule_name][2]["type"] == "bool" and Rules[rule_name][2]["value"] == False:
            # A => False
            if not Rules[rule_name][0]["not"]:
                Facts[Rules[rule_name][0]["value"]] = False
            # !A => True
            else:
                Facts[Rules[rule_name][0]["value"]] = True
    # True -> ... and ... => right part is True
    elif Rules[rule_name][0]["value"] == True and Rules[rule_name][1]["value"] == "implies":
        is_need_to_change, facts_to_change = check_right_part(rule_name)
        if is_need_to_change:
            for fact, value in facts_to_change:
                Facts[fact] = value
    # ... and ... -> False => left part if Fasle
    elif Rules[rule_name][-1]["value"] == False and Rules[rule_name][-2]["value"] == "implies":
        is_need_to_change, facts_to_change = check_left_part(rule_name)
        if is_need_to_change:
            for fact, value in facts_to_change:
                Facts[fact] = value

def check_IFANDONLYIF(rule_name):
    global Rules
    global Facts
    # ... <-> ...
    if len(Rules[rule_name]) == 3 and Rules[rule_name][1]["value"] == "if and only if":
        # bool <-> A => A = bool
        if Rules[rule_name][0]["type"] == "bool" and Rules[rule_name][2]["type"] == "fact":
            # A => bool
            if not Rules[rule_name][2]["not"]:
                Facts[Rules[rule_name][2]["value"]] = Rules[rule_name][0]["value"]
            # !A => !bool
            else:
                Facts[Rules[rule_name][2]["value"]] = not Rules[rule_name][0]["value"]
        # A <-> bool => A = bool
        if Rules[rule_name][0]["type"] == "fact" and Rules[rule_name][2]["type"] == "bool":
            # A => bool
            if not Rules[rule_name][0]["not"]:
                Facts[Rules[rule_name][0]["value"]] = Rules[rule_name][2]["value"]
            # !A => !bool
            else:
                Facts[Rules[rule_name][0]["value"]] = not Rules[rule_name][2]["value"]
    # bool <-> ... and ...
    #elif Rules[rule_name][0]["type"] = "bool" and Rules[rule_name][1]["value"] == "implies" and (len(Rules[rule_name]) - 3) / 2 == 
    # ... and ... <-> bool

def check_FINAL(rule_name):
    global Rules
    # bool -> A or A -> bool
    if len(Rules[rule_name]) == 3 and (Rules[rule_name][0]["type"] == "bool" or Rules[rule_name][2]["type"] == "bool"):
        return True
    return False

def calculate(rule_name):
    global Rules
    while True:
        cur_len = len(Rules)
        check_BRACKETS(rule_name)       #+
        check_AND(rule_name)            #+ but only in left side
        check_OR(rule_name)             #+
        check_XOR(rule_name)            #+
        check_IMPLIES(rule_name)        #+-
        check_IFANDONLYIF(rule_name)    #+-
        rez = check_FINAL(rule_name)    #+-
        if cur_len == len(Rules):
            return rez




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
    return calculate(rule_name)

if __name__ == "__main__":
    print(transform('R1', 'B'))
    print(json.dumps(Rules, indent=4))
    print(json.dumps(Facts, indent=4))