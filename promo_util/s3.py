import boto3


def get_client():
    client_session = boto3.Session(profile_name='ritesh')
    return client_session.client('s3')
