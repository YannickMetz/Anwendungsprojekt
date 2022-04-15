import pytest
from app import create_app
from click.testing import CliRunner
from functools import partial

@pytest.fixture(scope ='module')
def test_client():
    flask_app = create_app()
    flask_app.config['WTF_CSRF_ENABLED'] = False # needs to be disabled, otherwise WTForms cannot be tested
    # Create a test client using the Flask application configured for testing
    
    with flask_app.test_client() as test_client:
        yield test_client # this is where the testing happens!

