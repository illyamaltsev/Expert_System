

Rules = {
    'R1':[
        {
            "type": "fact",
            "value": "B"
        },
        {
            "type": "operation",
            "value": "and"
        },
        {
            "type": "fact",
            "value": "C"
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

def transform(rule_name: str, fact: dict):
    global Rules
    pass
