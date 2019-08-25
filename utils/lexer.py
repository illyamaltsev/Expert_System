from config import FACT_CHARS, OPERATIONS


# lexer
def lex(content: str):

    # not secured start
    content = content.replace('*', '').replace('$', '')
    content = content.replace('<=>', '$')
    content = content.replace('=>', '*')
    # not secured end

    tokens = []
    i = 0
    k = 0
    while i < len(content):
        c = content[i]
        if c is "=":
            tokens.append(("true_facts", ""))
        elif c is "?":
            tokens.append(("question_facts", ""))
        elif c is "\n":
            tokens.append(("\n", ""))
            k = i
        elif c is "#":
            index = content.find('\n', i, len(content) - 1)
            if index == -1:
                index = len(content)
            # tokens.append(("comment", content[i:index]))
            i = index - 1
        elif c in FACT_CHARS:
            tokens.append(("fact", c))
        elif c in OPERATIONS.keys():
            tokens.append(("operation", OPERATIONS[c]))
        elif c not in " \t":
            print("Syntax error near '", c, "' in string:", content[k:content.find('\n', i, len(content) - 1)])
            exit()
        i = i + 1

    return tokens
