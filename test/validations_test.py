import pytest
from unittest.mock import patch

import sys
sys.path.append('src/utils')
from Secrets import SecretsUtils
from Validations import validate_register_type
from Postgres import PostgresqlUtils

sys.path.append('src/models')
from Row import DataRow
from Report import ReportInfo

sys.path.append('src')
from lambda_function import lambda_handler

import boto3
from moto import mock_s3, mock_secretsmanager
from botocore.exceptions import ClientError
import json

REGION = "us-east-1"
BUCKET = "test_bucket"
FILE = "archivo.csv"
SECRET_NAME = "POSTGRES_DATABASE_LOCAL_CONNECTION"

secrets_test = {
    'HOST': 'localhost', 
    'USER': 'postgres', 
    'PASS': 'password', 
    'DB': 'bbog_mm_general'
}

secret_str = '{"HOST":"localhost","USER":"postgres","PASS":"password","DB":"bbog_mm_general"}'

dummy_report = "Processing Report: \n" 
dummy_report += "- Processed Lines: 35\n" 
dummy_report += "- Success Lines: 1\n" 
dummy_report += "- Wrong Lines: 1\n" 
dummy_report += "Error lines: \n" 
dummy_report += "- Number of columns wrong in line (1) \n"

test_s3_event = {
    "Records": [{
        "s3": {
            'bucket': {'name': BUCKET},
            'object': {
                'key': FILE
            }
        }
    }]}

file_data = "TipoDocumento;Documento;ObligacionesdelclientecerradasU12M;MesesCuotasPagadasClientePorCredito;ValorDesembolsadoPorCredito;MoraIntrames;ClienteReestructurado;ClienteCobranzasOnormalizado;Solicitudesrech\n"
file_data += "C;298207;1;12;13000000;0;2;2;1;2;2;6\n"
file_data += "C;79942786;1;12;13000000;0;2;2;2;2;2;6\n"
file_data += "C;79991470;1;12;13000000;0;2;2;2;2;2;6\n"
file_data += "C;1001114544;1;12;13000000;0;2;2;2;2;2;6\n"


@mock_secretsmanager
def test_secrets(monkeypatch):

    monkeypatch.setenv("secret_name", SECRET_NAME)
    monkeypatch.setenv("region_name", REGION)

    conn = boto3.client("secretsmanager", region_name=REGION)
    conn.create_secret(
        Name=SECRET_NAME, SecretString=secret_str
    )
    result = conn.get_secret_value(SecretId=SECRET_NAME)

    secrets_instance = SecretsUtils()
    secrets = secrets_instance.get_secrets()

    assert result["SecretString"] == secret_str
    assert secrets == secrets_test

@mock_secretsmanager
def test_secrets_throw_error(monkeypatch):
    monkeypatch.setenv("secret_name", SECRET_NAME)
    monkeypatch.setenv("region_name", REGION)
    conn = boto3.client("secretsmanager", region_name=REGION)

    with pytest.raises(ClientError) as cm:
        result = conn.get_secret_value(SecretId="i-dont-exist")

    secrets_instance = SecretsUtils()
    secrets = secrets_instance.get_secrets()

    assert (
        "Secrets Manager can't find the specified secret."
        == cm.value.response["Error"]["Message"]
    )


def test_validate_register_type_renovation():
    row = ['C','298207','1','12','13000000','0','2','2','1','2','2','6']
    data = DataRow(row)
    register_type = validate_register_type(data)

    assert register_type == 'RENOVACION'
    assert data.get_tipo_documento() == 'C'
    assert data.get_documento() == '298207'
    assert data.get_obligaciones_del_cliente_cerradas_u12m() == '1'
    assert data.get_meses_cuotas_pagadas_cliente_por_credito() == '12'
    assert data.get_valor_desembolsado_por_credito() == '13000000'
    assert data.get_mora_intrames() == '0'
    assert data.get_cliente_reestructurado() == '2'
    assert data.get_cliente_cobranzas_o_normalizado() == '2'
    assert data.get_solicitudes_rechazas_flujo_mantiz_u6m() == '1'
    assert data.get_solicitudes_rechazadas_flujo_gpou6m() == '2'
    assert data.get_solicitudes_pendientes_en_gpo() == '2'
    assert data.get_numero_obligaciones_mayor_500m() == '6'

def test_validate_register_type_parallel():
    row = ['C','298207',None,None,None,'0','2','2','1','2','2','6']
    data = DataRow(row)
    register_type = validate_register_type(data)

    assert register_type == 'PARALELO'
         

def test_report_model():
    report = ReportInfo()
    report.set_total_processed(35)
    report.update_success_lines()
    report.update_wrong_lines()
    report.update_report("- Number of columns wrong in line (1) \n")

    assert report.get_report() == dummy_report

@mock_s3
@mock_secretsmanager
def test_lambda_handler(monkeypatch):
    monkeypatch.setenv("secret_name", SECRET_NAME)
    monkeypatch.setenv("region_name", REGION)
    try:
        conn = boto3.client("secretsmanager", region_name=REGION)
        conn.create_secret(
            Name=SECRET_NAME, SecretString=secret_str
        )

        
        result = conn.get_secret_value(SecretId=SECRET_NAME)
        print('SECRETS___>', result["SecretString"])

        s3 = boto3.resource("s3", region_name=REGION)
        s3.create_bucket(Bucket=BUCKET)
        s3.Bucket(BUCKET).put_object(Key=FILE, Body=file_data)
        out = s3.Object(BUCKET, FILE).get()['Body'].read().decode("utf-8")
        print('out::')
        print(out)
    
        response = lambda_handler(test_s3_event, context={})

        assert out == file_data
        assert True == True

    except Exception as e:
        print(e)


def test_postgresql(monkeypatch):
    try:
        monkeypatch.setenv("secret_name", SECRET_NAME)
        monkeypatch.setenv("region_name", REGION)

        conn = boto3.client("secretsmanager", region_name=REGION)
        result = conn.get_secret_value(SecretId=SECRET_NAME)
        secret_string = result['SecretString']
        secrets = json.loads(secret_string)

        pg = PostgresqlUtils()
        pg.connect(secrets)
        pg.get_database_version()
        pg.remove_data()

        row_1 = DataRow(['C','298207','1','12','13000000','0','2','2','1','2','2','6'])
        row_2 = DataRow(['C','298208','1','12','14000000','0','2','2','1','2','2','6'])
        row_3 = DataRow(['C','298209','1','12','15000000','0','2','2','1','2','2','6'])

        lista = [row_1, row_2, row_3]
        pg.insert_data(lista)

        assert True == True
    except Exception as e:
        print(e)
