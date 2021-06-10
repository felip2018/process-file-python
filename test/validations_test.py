import pytest
import sys
sys.path.append('utils')
from Secrets import SecretsUtils
from Validations import validate_register_type

sys.path.append('models')
from Row import DataRow
from Report import ReportInfo

secrets_test = {
    'HOST': 'localhost', 
    'USER': 'postgres', 
    'PASS': 'password', 
    'DB': 'bbog_mm_general'
}

dummy_report = "Processing Report: \n" 
dummy_report += "- Processed Lines: 35\n" 
dummy_report += "- Success Lines: 1\n" 
dummy_report += "- Wrong Lines: 1\n" 
dummy_report += "Error lines: \n" 
dummy_report += "- Number of columns wrong in line (1) \n"

#def test_modules():
    #print('modules: ', sys.modules)

def test_secrets(mocker, monkeypatch):

    monkeypatch.setenv("secret_name", "SECRET_KEY_NAME")
    monkeypatch.setenv("region_name", "us-east-1")

    mocker.patch(
        'Secrets.SecretsUtils.get_secrets',
        return_value = secrets_test
    )

    secrets_instance = SecretsUtils()
    secrets = secrets_instance.get_secrets()
    assert secrets == secrets_test


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

