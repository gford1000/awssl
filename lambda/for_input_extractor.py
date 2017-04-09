def lambda_handler(event, context):
    """
    Expects a list [ InputData, [...] ]
    """
    return event[0]
