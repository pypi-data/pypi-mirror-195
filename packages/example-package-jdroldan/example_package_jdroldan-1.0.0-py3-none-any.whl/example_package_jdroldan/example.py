import boto3

client = boto3.client('ssm')

def get_parameter():
    response = client.get_parameter(
        Name='mongo_ephemeral_uri',
        WithDecryption=True|False
    )
    return response