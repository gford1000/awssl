def lambda_handler(event, context):
    """
    Expecting: [ Input, [ O1, ..., On-1 ], [On, ... On+r ] ]
    
    Returns: [ Input, [ O1, ... On+r ] ]
    """
    return [ event[0], event[1] + event[2] ]

