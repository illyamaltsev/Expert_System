# coding: utf8
import json
import config


def check_BRACKETS(rule_name):
    lenght = len(config.Rules[rule_name])
    for i, r in enumerate(config.Rules[rule_name]):
        # (A) -> A or (bool) -> bool
        if i + 2 < lenght and r["value"] == "(" and (
                config.Rules[rule_name][i + 1]["type"] == "fact" or config.Rules[rule_name][i + 1]["type"] == "bool") and \
                config.Rules[rule_name][i + 2]["value"] == ")":
            # !(...) -> !...
            if config.Rules[rule_name][i]["not"]:
                # !(A) -> !A
                if config.Rules[rule_name][i + 1]["type"] == "fact":
                    config.Rules[rule_name][i + 1]["not"] = not config.Rules[rule_name][i + 1]["not"]
                else:
                    config.Rules[rule_name][i + 1]["value"] = not config.Rules[rule_name][i + 1]["value"]
            del config.Rules[rule_name][i]
            del config.Rules[rule_name][i + 1]
            check_BRACKETS(rule_name)


def check_AND(rule_name):
    lenght = len(config.Rules[rule_name])
    for i, r in enumerate(config.Rules[rule_name]):
        if i + 1 < lenght and i > 0 and r["value"] == "and":
            ### A AND bool
            if config.Rules[rule_name][i - 1]["type"] == "fact" and config.Rules[rule_name][i + 1]["type"] == "bool":
                # A AND True -> A
                if config.Rules[rule_name][i + 1]["value"] == True:
                    del config.Rules[rule_name][i]
                    del config.Rules[rule_name][i]
                # A AND False -> False
                else:
                    del config.Rules[rule_name][i]
                    del config.Rules[rule_name][i]
                    config.Rules[rule_name][i - 1]["type"] = "bool"
                    config.Rules[rule_name][i - 1]["value"] = False
                check_AND(rule_name)
            ### bool AND A
            elif config.Rules[rule_name][i - 1]["type"] == "bool" and config.Rules[rule_name][i + 1]["type"] == "fact":
                # True AND A -> A
                if config.Rules[rule_name][i - 1]["value"] == True:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                # False AND A -> False
                else:
                    del config.Rules[rule_name][i]
                    del config.Rules[rule_name][i]
                check_AND(rule_name)
            ### bool AND bool
            elif config.Rules[rule_name][i - 1]["type"] == "bool" and config.Rules[rule_name][i + 1]["type"] == "bool":
                # True AND True -> True
                if config.Rules[rule_name][i - 1]["value"] == config.Rules[rule_name][i + 1]["value"] == True:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                # False AND bool -> False or bool AND False -> False
                if config.Rules[rule_name][i - 1]["value"] == False or config.Rules[rule_name][i + 1]["value"] == False:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                    config.Rules[rule_name][i - 1]["type"] = "bool"
                    config.Rules[rule_name][i - 1]["value"] = False
                check_AND(rule_name)
            ### A and A
            elif config.Rules[rule_name][i - 1]["value"] == config.Rules[rule_name][i + 1]["value"]:
                # A AND A -> A or !A AND !A -> !A
                if config.Rules[rule_name][i - 1]["not"] == config.Rules[rule_name][i + 1]["not"]:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                # A AND !A -> False or !A AND A -> False
                else:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                    config.Rules[rule_name][i - 1]["type"] = "bool"
                    config.Rules[rule_name][i - 1]["value"] = False
                check_AND(rule_name)


def check_OR(rule_name):
    lenght = len(config.Rules[rule_name])
    for i, r in enumerate(config.Rules[rule_name]):
        if i + 1 < lenght and i > 0 and r["value"] == "or":
            ### A OR bool
            if config.Rules[rule_name][i - 1]["type"] == "fact" and config.Rules[rule_name][i + 1]["type"] == "bool":
                # A OR True -> True
                if config.Rules[rule_name][i + 1]["value"] == True:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                # A OR False -> A
                else:
                    del config.Rules[rule_name][i]
                    del config.Rules[rule_name][i]
                check_OR(rule_name)
            ### bool OR A
            elif config.Rules[rule_name][i - 1]["type"] == "bool" and config.Rules[rule_name][i + 1]["type"] == "fact":
                # True OR A -> True
                if config.Rules[rule_name][i - 1]["value"] == True:
                    del config.Rules[rule_name][i]
                    del config.Rules[rule_name][i]
                # False OR A -> A
                else:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                check_OR(rule_name)
            ### bool OR bool
            elif config.Rules[rule_name][i - 1]["type"] == "bool" and config.Rules[rule_name][i + 1]["type"] == "bool":
                # True OR True -> True
                if config.Rules[rule_name][i - 1]["value"] == True or config.Rules[rule_name][i + 1]["value"] == True:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                    config.Rules[rule_name][i - 1]["type"] = "bool"
                    config.Rules[rule_name][i - 1]["value"] = True
                # False OR bool -> bool
                elif config.Rules[rule_name][i - 1]["value"] == False:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                # bool OR False -> bool
                elif config.Rules[rule_name][i + 1]["value"] == False:
                    del config.Rules[rule_name][i]
                    del config.Rules[rule_name][i]
                check_OR(rule_name)
            ### A OR A
            elif config.Rules[rule_name][i - 1]["value"] == config.Rules[rule_name][i + 1]["value"]:
                # A OR A -> A or !A OR !A -> !A
                if config.Rules[rule_name][i - 1]["not"] == config.Rules[rule_name][i + 1]["not"]:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                # A OR !A -> True or !A OR A -> True
                else:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                    config.Rules[rule_name][i - 1]["type"] = "bool"
                    config.Rules[rule_name][i - 1]["value"] = True
                check_OR(rule_name)


def check_XOR(rule_name):
    lenght = len(config.Rules[rule_name])
    for i, r in enumerate(config.Rules[rule_name]):
        if i + 1 < lenght and i > 0 and r["value"] == "xor":
            ### A XOR bool
            if config.Rules[rule_name][i - 1]["type"] == "fact" and config.Rules[rule_name][i + 1]["type"] == "bool":
                # A XOR True -> !A
                if config.Rules[rule_name][i + 1]["value"] == True:
                    del config.Rules[rule_name][i]
                    del config.Rules[rule_name][i]
                    config.Rules[rule_name][i - 1]["not"] = not config.Rules[rule_name][i - 1]["not"]

                # A XOR False -> A
                else:
                    del config.Rules[rule_name][i]
                    del config.Rules[rule_name][i]
                check_XOR(rule_name)
            ### bool XOR A
            elif config.Rules[rule_name][i - 1]["type"] == "bool" and config.Rules[rule_name][i + 1]["type"] == "fact":
                # True XOR A -> !A
                if config.Rules[rule_name][i - 1]["value"] == True:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                    config.Rules[rule_name][i - 1]["not"] = not config.Rules[rule_name][i - 1]["not"]
                # False XOR A -> A
                else:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                check_XOR(rule_name)
            ### bool XOR bool
            elif config.Rules[rule_name][i - 1]["type"] == "bool" and config.Rules[rule_name][i + 1]["type"] == "bool":
                # True XOR True -> False
                if config.Rules[rule_name][i - 1]["value"] == True and config.Rules[rule_name][i + 1]["value"] == True:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                    config.Rules[rule_name][i - 1]["type"] = "bool"
                    config.Rules[rule_name][i - 1]["value"] = False
                # False XOR bool -> bool
                elif config.Rules[rule_name][i - 1]["value"] == False:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                # bool XOR False -> bool
                elif config.Rules[rule_name][i + 1]["value"] == False:
                    del config.Rules[rule_name][i]
                    del config.Rules[rule_name][i]
                check_XOR(rule_name)
            ### A XOR A
            elif config.Rules[rule_name][i - 1]["value"] == config.Rules[rule_name][i + 1]["value"]:
                # A XOR A -> False or !A XOR !A -> False
                if config.Rules[rule_name][i - 1]["not"] == config.Rules[rule_name][i + 1]["not"]:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                    config.Rules[rule_name][i - 1]["type"] = "bool"
                    config.Rules[rule_name][i - 1]["value"] = False
                # A XOR !A -> True or !A XOR A -> True
                else:
                    del config.Rules[rule_name][i - 1]
                    del config.Rules[rule_name][i - 1]
                    config.Rules[rule_name][i - 1]["type"] = "bool"
                    config.Rules[rule_name][i - 1]["value"] = True
                check_XOR(rule_name)

def check_right_part(rule_name, boolean=True):
    facts_to_change = []
    implies = False
    for rule in config.Rules[rule_name]:
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
                facts_to_change.append({rule["value"]:(not rule["not"]) and boolean})
    # return True and facts_to_change only if it's OK
    return True, facts_to_change

def check_left_part(rulename, boolean=True):
    facts_to_change = []
    for rule in config.Rules[rule_name]:
        # ignore left side, before implies
        if rule["value"] == "implies":
            return True, facts_to_change
        # check only right side
        # if operations not "and", "(", ")" -> return false
        if rule["type"] == "operation" and rule["value"] not in ["and", "(", ")"]:
            return False, facts_to_change
        # append fact and value what change to
        elif rule["type"] == "fact":
            facts_to_change.append({rule["value"]:(not rule["not"]) and boolean})
    

def check_IMPLIES(rule_name):
    # ... -> ... but A -> True or False -> A then A = underfit
    if len(config.Rules[rule_name]) == 3 and config.Rules[rule_name][1]["value"] == "implies":
        # True -> A => A = True
        if config.Rules[rule_name][0]["type"] == "bool" and config.Rules[rule_name][0]["value"] == True and config.Rules[rule_name][2]["type"] == "fact":
            # A => True
            if not config.Rules[rule_name][2]["not"]:
                config.Facts[config.Rules[rule_name][2]["value"]] = True
            # !A => False
            else:
                config.Facts[config.Rules[rule_name][2]["value"]] = False
        # A -> False => A = False
        if config.Rules[rule_name][0]["type"] == "fact" and config.Rules[rule_name][2]["type"] == "bool" and config.Rules[rule_name][2]["value"] == False:
            # A => False
            if not config.Rules[rule_name][0]["not"]:
                config.Facts[config.Rules[rule_name][0]["value"]] = False
            # !A => True
            else:
                config.Facts[Rules[rule_name][0]["value"]] = True
    # True -> ... and ... => right part is True
    elif config.Rules[rule_name][0]["value"] == True and config.Rules[rule_name][1]["value"] == "implies":
        is_need_to_change, facts_to_change = check_right_part(rule_name)
        if is_need_to_change:
            for fact, value in facts_to_change:
                config.Facts[fact] = value
    # ... and ... -> False => left part if Fasle
    elif config.Rules[rule_name][-1]["value"] == False and config.Rules[rule_name][-2]["value"] == "implies":
        is_need_to_change, facts_to_change = check_left_part(rule_name)
        if is_need_to_change:
            for fact, value in facts_to_change:
                config.Facts[fact] = value

def check_IFANDONLYIF(rule_name):
    # ... <-> ...
    if len(config.Rules[rule_name]) == 3 and config.Rules[rule_name][1]["value"] == "if and only if":
        # bool <-> A => A = bool
        if config.Rules[rule_name][0]["type"] == "bool" and config.Rules[rule_name][2]["type"] == "fact":
            # A => bool
            if not config.Rules[rule_name][2]["not"]:
                config.Facts[config.Rules[rule_name][2]["value"]] = config.Rules[rule_name][0]["value"]
            # !A => !bool
            else:
                config.Facts[config.Rules[rule_name][2]["value"]] = not config.Rules[rule_name][0]["value"]
        # A <-> bool => A = bool
        if config.Rules[rule_name][0]["type"] == "fact" and config.Rules[rule_name][2]["type"] == "bool":
            # A => bool
            if not config.Rules[rule_name][0]["not"]:
                config.Facts[config.Rules[rule_name][0]["value"]] = config.Rules[rule_name][2]["value"]
            # !A => !bool
            else:
                config.Facts[config.Rules[rule_name][0]["value"]] = not config.Rules[rule_name][2]["value"]
    # bool <-> ... and ...
    elif config.Rules[rule_name][0]["type"] == "bool" and config.Rules[rule_name][1]["value"] == "implies":
        is_need_to_change, facts_to_change = check_right_part(rule_name, config.Rules[rule_name][0]["value"])
        if is_need_to_change:
            for fact, value in facts_to_change:
                config.Facts[fact] = value
    # ... and ... <-> bool
    elif config.Rules[rule_name][-1]["type"] == "bool" and config.Rules[rule_name][-2]["value"] == "implies":
        is_need_to_change, facts_to_change = check_left_part(rule_name, config.Rules[rule_name][-1]["value"])
        if is_need_to_change:
            for fact, value in facts_to_change:
                config.Facts[fact] = value


def check_FINAL(rule_name):
    # bool -> A or A -> bool
    if len(config.Rules[rule_name]) == 3 and (config.Rules[rule_name][0]["type"] == "bool" or config.Rules[rule_name][2]["type"] == "bool"):
        return True
    return False


def calculate(rule_name):
    while True:
        cur_len = len(config.Rules)
        check_BRACKETS(rule_name)  # +
        check_AND(rule_name)  # + but only in left side
        check_OR(rule_name)  # +
        check_XOR(rule_name)  # +
        check_IMPLIES(rule_name)  # +-
        check_IFANDONLYIF(rule_name)  # +-
        rez = check_FINAL(rule_name)  # +-
        if cur_len == len(config.Rules):
            if rez:
                del config.Rules[rule_name]
            return rez


def transform(rule_name: str, fact: str):
    print(json.dumps(config.Rules, indent=2))

    for i, r in enumerate(config.Rules[rule_name]):
        if r["value"] == fact:
            config.Rules[rule_name][i]["type"] = "bool"
            # !A -> not bool
            if r["not"]:
                config.Rules[rule_name][i]["value"] = not config.Facts[fact]
            # A -> bool
            else:
                config.Rules[rule_name][i]["value"] = config.Facts[fact]
    return calculate(rule_name)


"""
if __name__ == "__main__":
    print(transform('R1', 'B'))
    print(json.dumps(config.Rules, indent=4))
"""
