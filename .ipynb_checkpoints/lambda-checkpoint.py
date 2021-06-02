import boto3
import csv
from models import Row
from models import Report
from utils import Secrets
from utils import Postgres


s3 = boto3.client('s3')


def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    report = Report.ReportInfo()
    lista = []
    
    try:
        
        print('Starting FileUpload lambda')
        
        file = s3.get_object(Bucket=bucket, Key=key)
        data = file['Body'].read().decode('utf-8').splitlines()

        lines = csv.reader(data)
        index = 0
        for line in lines:
            
            if(index != 0):
                arr = line[0].split(';')
                
                if(len(arr) == 12):
                    report.updateSuccessLines()
                    
                    row = Row.DataRow(arr)
                    lista.append(row)
                else:
                    report.updateWrongLines()
                    report.updateReport("- Number of columns wrong in line (" + str(index+1) + ") \n")
                    
            index += 1
            
        report.setTotalProcessed(index-1)
        
        secrets = Secrets.SecretsUtils()
        
        postgres = Postgres.PostgresqlUtils()
        postgres.connect(secrets.getSecrets())
        postgres.removeData()
        postgres.insertData(lista)
        
        print(report.getReport())

    except Exception as e:
        print('Something was wrong!')
        print(e)
        


