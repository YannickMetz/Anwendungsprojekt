from flask import session
from click.testing import CliRunner
from app.mock_data import create_test_service



#test will fail if any other CLI command is executed after the CLI command "initmockdata"
#workaround: run mockdata tests separately, which will also save time as mockdata creation will take longer
#python3 -m pytest tests_pytest/ -v && python3 -m pytest mockdata_pytest/ -v

### functions ###

def logout(test_client):
    test_client.get('/logout')

def login(test_client, email, password):
    test_client.post("/login", data=dict(email=email,password=password))


### tests ###
# all following tests require the test useres created with test_01_auth.py

def test_initialize_testservice(test_client):
    """
    adds "Testservice" required for most of the following tests
    """
    runner = CliRunner()
    result = runner.invoke(create_test_service)
    assert result.exit_code == 0


def test_home_get(test_client):
    """
    WHEN the '/' page is is posted to (GET)
    THEN check that...
    ...a '200' status code is returned
    ...the response contains a string for a test specific service category 
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Testkategorie' in response.data


def test_home_post(test_client):
    """
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405


def test_login_logout_helpers(test_client):
    """
    Test if login() and logout() helper functions for testing are working as intended
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="max@testmail.com", password="123456")
    assert session["_user_id"] == "1"
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    logout(test_client)
    assert "_user_id" not in session


def test_view_services_logged_out(test_client):
    """
    WHEN the '/search/Testkategorie' receives a GET request while session has no user logged in
    THEN check that...
    ...response data does not contain "Testservice"
    ...redirect to '/login'
    ...correct error message is returned with response data
    """
    logout(test_client)
    assert "_user_id" not in session
    response = test_client.get('/search/Testkategorie', follow_redirects=True)
    assert b'Testservice' not in response.data
    assert response.request.path == "/login"
    assert b'Please log in to access this page.' in response.data


def test_search_service_providers_logged_out(test_client):
    """
    WHEN the '/search/1' receives a GET request while session has no user logged in
    THEN check that...
    ...response data does not contain "Filter setzen"
    ...redirect to '/login'
    ...correct error message is returned with response data
    """
    logout(test_client)
    assert "_user_id" not in session
    response = test_client.get('/search/1', follow_redirects=True)
    assert b'Filter setzen'  not in response.data
    assert response.request.path == "/login"
    assert b'Please log in to access this page.' in response.data


def test_change_service_provider_profile_logged_out(test_client):
    """
    WHEN the 'change_service_provider_profile' receives a GET request while session has no user logged in
    THEN check that...
    ...response data does not contain "Profilbeschreibung"
    ...redirect to '/login'
    ...correct error message is returned with response data
    """
    logout(test_client)
    assert "_user_id" not in session
    response = test_client.get('change_service_provider_profile', follow_redirects=True)
    assert b'Profilbeschreibung'  not in response.data
    assert response.request.path == "/login"
    assert b'Please log in to access this page.' in response.data


def test_change_service_provider_profile_as_customer(test_client):
    """
    WHEN the 'change_service_provider_profile' receives a GET request when a customer is logged in
    THEN check that...
    ...response data does not contain "Profilbeschreibung"
    ...redirect to '/login'
    ...correct error message is returned with response data
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="max@testmail.com", password="123456")
    assert session["_user_id"] == "1"
    response = test_client.get('change_service_provider_profile', follow_redirects=True)
    assert b'Profilbeschreibung'  not in response.data
    assert response.request.path == "/login"
    assert b'Bitte als Dienstleister einloggen' in response.data



def test_change_service_provider_profile_GET(test_client):
    """
    WHEN the 'change_service_provider_profile' receives a GET request when a service provider is logged in
    THEN check that...
    ...response path is 'change_service_provider_profile'
    ...response data does contain "Profilbeschreibung"
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    response = test_client.get('/change_service_provider_profile')
    assert response.status_code == 200
    assert b'Profilbeschreibung' in response.data



def test_change_service_provider_profile_POST_body(test_client):
    """
    WHEN the route '/change_service_provider_profile' receives a POST request for ChangeProfileBodyForm when a service provider is logged in
    THEN check that...
    ...response data does contain "Profilbeschreibung"
    ...response data contains the profile body text "test body"
    ...the route '/profile/service_provider/2' contains the profile body text "test body" in response data
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    response = test_client.post("/change_service_provider_profile", data=dict(profilbeschreibung="test body"), follow_redirects=True)
    assert b'Profilbeschreibung' in response.data
    assert b'test body' in response.data
    profile = test_client.get("profile/service_provider/2")
    assert b'test body' in profile.data



def test_change_service_provider_profile_POST_service(test_client):
    """
    WHEN the route '/change_service_provider_profile' receives a POST request for SelectServiceForm when a service provider is logged in
    THEN check that...
    ...response data does contain "Profilbeschreibung"
    ...the route '/profile/service_provider/2' contains "Testservice" in response data
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    response = test_client.post("/change_service_provider_profile", data=dict(service="Testservice"), follow_redirects=True)
    assert b'Profilbeschreibung' in response.data
    profile = test_client.get("profile/service_provider/2")
    assert b'Testservice' in profile.data


#try view_service_provider_profile > fail

#try change > fail

#try service

#change profile