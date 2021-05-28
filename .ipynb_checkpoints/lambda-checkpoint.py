import json
import boto3
import csv
from utils import Postgres
from models import Row

s3 = boto3.client('s3')


def lambda_handler(event, context):
    print('Starting FileUpload lambda')
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    lista = []
    
    try:
        file = s3.get_object(Bucket=bucket, Key=key)
        data = file['Body'].read().decode('utf-8').splitlines()

        lines = csv.reader(data)
        index = 0
        for line in lines:
            
            if(index != 0):
                arr = line[0].split(';')
                
                if(len(arr) == 12):
                    row = Row.DataRow(arr)
                    lista.append(row)
                
            index += 1
            
        print('Elements', len(lista))
        
        postgres = Postgres.PostgresqlUtils()
        postgres.connect()
        postgres.insertData(lista)

    except Exception as e:
        print('Something was wrong!')
        print(e)
        


