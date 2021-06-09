import os
import boto3
import base64
from botocore.exceptions import ClientError
import json

class SecretsUtils:
    def __init__(self):
        print('Create Secrets instance')
        self.__secret_name = os.environ['secret_name']
        self.__region_name = os.environ['region_name']
        # Create a Secrets Manager client
        session = boto3.session.Session()
        self.__client = session.client(
            service_name='secretsmanager',
            region_name=self.__region_name
        )

    def get_secrets(self):

        try:
            get_secret_value_response = self.__client.get_secret_value(SecretId=self.__secret_name)
            secret_str = get_secret_value_response['SecretString']
            secrets = json.loads(secret_str)
            
            return secrets
            
        except ClientError as error:
            print('Something was wrong with getSecrets')
            print(error)
            
            
