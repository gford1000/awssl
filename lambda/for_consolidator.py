def lambda_handler(event, context):
    """
    Expects event in the form:
        [ [I, [O1, O2, ... On-1], On ]
    
    Returns:
        [ I, [O1, O2, ... On ]
    
    """
    results = event[0][1]
    results.append(event[1])
    return [ event[0][0], results ]
