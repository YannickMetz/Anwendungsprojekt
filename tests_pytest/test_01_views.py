from pickle import FALSE
from urllib import response
import pytest, click
from flask import session



#test will fail if any other CLI command is executed after the CLI command "initmockdata"
#workaround: run mockdata tests separately, which will also save time as mockdata creation will take longer
#python3 -m pytest tests_pytest/ -v && python3 -m pytest mockdata_pytest/ -v



def test_home_get(test_client):
    """
    WHEN the '/' page is is posted to (GET)
    THEN check that a '200' status code is returned
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_home_post(test_client):
    """
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405
