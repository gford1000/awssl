def lambda_handler(event, context):
    """
    Expects a two element list: [ Input, [...] ]
    
    Returns the second element
    """
    return event[1]

