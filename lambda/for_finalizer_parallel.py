def lambda_handler(event, context):
    """
    Expects input of the form:
    
        [ [ Input, [ O1 ] ], ... [ Input, [On ] ] ]
        
    Returns: [ O1, ... On ]

    """
    return [ e[1][0] for e in event ]
