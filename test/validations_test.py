import pytest
import json
import sys
sys.path.append('./utils')
import Secrets
import Validations
sys.path.append('./models')
import Row
import Report

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

def test_secrets(mocker, monkeypatch):

    monkeypatch.setenv("secret_name", "SECRET_KEY_NAME")
    monkeypatch.setenv("region_name", "us-east-1")

    mocker.patch(
        'Secrets.SecretsUtils.getSecrets',
        return_value = secrets_test
    )

    secrets_instance = Secrets.SecretsUtils()
    secrets = secrets_instance.getSecrets()
    print(secrets)
    assert secrets == secrets_test


def test_validate_register_type_renovation():
    row = ['C','298207','1','12','13000000','0','2','2','1','2','2','6']
    data = Row.DataRow(row)
    register_type = Validations.validateRegisterType(data)

    assert register_type == 'RENOVACION'
    assert data.getTipoDocumento() == 'C'
    assert data.getDocumento() == '298207'
    assert data.getObligacionesDelClienteCerradasU12M() == '1'
    assert data.getMesesCuotasPagadasClientePorCredito() == '12'
    assert data.getValorDesembolsadoPorCredito() == '13000000'
    assert data.getMoraIntrames() == '0'
    assert data.getClienteReestructurado() == '2'
    assert data.getClienteCobranzasONormalizado() == '2'
    assert data.getSolicitudesRechazasFlujoMantizU6M() == '1'
    assert data.getSolicitudesRechazadasFlujoGPOU6M() == '2'
    assert data.getSolicitudesPendientesEnGPO() == '2'
    assert data.getNumeroObligacionesMayor500M() == '6'

def test_validate_register_type_parallel():
    row = ['C','298207',None,None,None,'0','2','2','1','2','2','6']
    data = Row.DataRow(row)
    register_type = Validations.validateRegisterType(data)

    assert register_type == 'PARALELO'

def test_report_model():
    report = Report.ReportInfo()
    report.setTotalProcessed(35)
    report.updateSuccessLines()
    report.updateWrongLines()
    report.updateReport("- Number of columns wrong in line (1) \n")

    assert report.getReport() == dummy_report


