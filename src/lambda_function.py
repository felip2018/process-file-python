import boto3
import csv
import sys
sys.path.append('src/models')
import Row
import Report
sys.path.append('src/utils')
import Secrets
import Postgres


s3 = boto3.client('s3')


def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    report = Report.ReportInfo()
    
    try:
        
        print('Starting FileUpload lambda')

        new_secrets = Secrets.SecretsUtils()
        secrets = new_secrets.get_secrets()
        file = s3.get_object(Bucket=bucket, Key=key)
        data = file['Body'].read().decode('utf-8').splitlines()

        lines = csv.reader(data)

        postgres = Postgres.PostgresqlUtils()
        postgres.connect(secrets)
        postgres.remove_data()
        
        index = 0
        for line in lines:
            
            if(index != 0):
                arr = line[0].split(';')
                
                if(len(arr) == 12):
                    report.update_success_lines()
                    row = Row.DataRow(arr)
                    postgres.insert_data(row)
                else:
                    report.update_wrong_lines()
                    report.update_report("- Number of columns wrong in line (" + str(index+1) + ") \n")
                    
            index += 1
            
        report.set_total_processed(index-1)
        
        print(report.get_report())

    except Exception as e:
        print('Something was wrong!')
        print(e)
        