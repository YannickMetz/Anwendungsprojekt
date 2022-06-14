from pickle import FALSE
from urllib import response
import pytest, click
from flask import session
from click.testing import CliRunner
from app.mock_data import reset_db, init_mockdata


#test will fail if any other CLI command is executed after the CLI command "initmockdata"
#workaround: run testfiles individually
#python3 -m pytest tests_pytest/test_01_views.py -v && python3 -m pytest tests_pytest/test_02_auth.py -v



def test_db_reset():
    runner = CliRunner()
    result = runner.invoke(reset_db)
    assert result.exit_code == 0
    assert "Tabelle" in result.output

def test_init_mockdata():
    runner = CliRunner()
    result = runner.invoke(init_mockdata)
    assert result.exit_code == 0
    assert "Abgeschlossen" in result.output


