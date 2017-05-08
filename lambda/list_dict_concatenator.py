def lambda_handler(event, context):
    # Expects [ { "key_a1":"value_a1", ... }, { "key_b1":"value_b1", ... } ]
    # and returns a concatenated dict containing all values
    # If b has keys in a, then the a values are overwritten by the v values
    for key in event[1].keys():
        event[0][key] = event[1][key]
    return event[0]

