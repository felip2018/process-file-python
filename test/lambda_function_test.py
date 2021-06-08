import boto3
import pytest
from moto import mock_s3
import sys
sys.path.append('./')
import lambda_function

test_s3_event = {
    "Records": [{
        "s3": {
            'bucket': {'name': 'proccess-file'},
            'object': {
                'key': 'renovaciones.csv'
            }
        }
    }]}

@mock_s3
def test_lambda_handler(mocker):

    try:
        # set up test bucket
        s3_client = boto3.client('s3')
        mocker.patch(
            s3_client.get_object,
            return_value = True
        )
        

        response = lambda_function.lambda_handler(event=test_s3_event, context={})

        assert response['status'] == 'success'

    except Exception as e:
        print(e)