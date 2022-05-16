import pytest, sys
sys.path.append('../app/')
from app import create_app, db





#test will fail if any other CLI command is executed after the CLI command "initmockdata"
#workaround: run mockdata tests separately, which will also save time as mockdata creation will take longer
#python3 -m pytest tests_pytest/ -v && python3 -m pytest mockdata_pytest/ -v


@pytest.fixture(scope ='module')
def test_client():
    flask_app = create_app()
    flask_app.config['WTF_CSRF_ENABLED'] = False # needs to be disabled, otherwise WTForms cannot be tested
    database = db


    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        yield test_client # this is where the testing happens!


