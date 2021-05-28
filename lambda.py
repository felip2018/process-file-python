import json
import boto3
import csv

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print('Starting FileUpload lambda')
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        file = s3.get_object(Bucket=bucket, Key=key)
        data = file['Body'].read().decode('utf-8').splitlines()

        lines = csv.reader(data)
        for line in lines:
            #print complete line
            row = line[0].split(';')
            print(row[0])

    except Exception as e:
        print(e)
        print('Error obteniendo archivo ', key, ' del bucket', bucket)


