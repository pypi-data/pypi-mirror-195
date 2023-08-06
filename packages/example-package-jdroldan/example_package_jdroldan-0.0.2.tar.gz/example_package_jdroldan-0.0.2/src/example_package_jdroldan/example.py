# test function
ssm_parameters = {
    "mongo_test_uri": "mongo_test_uri@uri"
}

def get_parameter():
    param = ssm_parameters.get('mongo_test_uri', '')
    return f"this is the param: {param}"