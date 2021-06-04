import pytest
import sys
sys.path.append('./utils')
import Secrets

secrets_test = {
    'HOST': 'localhost', 
    'USER': 'postgres', 
    'PASS': 'password', 
    'DB': 'bbog_mm_general'
}

def test_secrets(mocker, monkeypatch):

    monkeypatch.setenv("secret_name", "SECRET_KEY_NAME")
    monkeypatch.setenv("region_name", "us-east-1")

    mocker.patch(
        'Secrets.SecretsUtils.getSecrets',
        return_value = secrets_test
    )

    secretsInstance = Secrets.SecretsUtils()
    secrets = secretsInstance.getSecrets()
    assert secrets == secrets_test



