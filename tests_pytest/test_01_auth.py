from flask import session
from click.testing import CliRunner
from app.mock_data import reset_db





def test_db_reset():
    runner = CliRunner()
    result = runner.invoke(reset_db)
    assert result.exit_code == 0
    assert "Tabelle" in result.output


def test_register(test_client):
    """
    WHEN the '/register' page is posted to (POST) with selection 'Kunde'
    THEN check that a redirect to "/register_customer" is returned
    """
    assert test_client.get('/register').status_code == 200
    response = test_client.post("/register", data=dict(role='Kunde'), follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/register_customer"

    response = test_client.post("/register", data=dict(role='Dienstleister'), follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/register_business"


def test_register_customer_pw_unequal(test_client):
    """
    WHEN the '/register_customer' page is posted to (POST) with password fields unequal'
    THEN check that 
    ...a redirect to "/register_customer" is returned
    ...warning message is flashed after the redirect
    ...no login session is active
    """
    assert test_client.get('/register_customer').status_code == 200
    response = test_client.post("/register_customer", data=dict(
        k_vorname='Max',
        k_nachname="Mustermann",
        k_straße = "Teststraße 1",
        k_plz="123456",
        k_ort="Testhausen",
        email="max@testmail.com",
        password="123456",
        password_repeated="abcdefg"
        ), follow_redirects=True)
    assert response.request.path == "/register_customer"
    assert "_user_id" not in session
    assert b"Field must be equal to password." in response.data  


def test_register_customer(test_client):
    """
    WHEN the '/register_customer' page is posted to (POST) with password fields equal'
    THEN check that 
    ...a redirect to "/" is returned
    ...an active login session is created
    """
    assert test_client.get('/register_customer').status_code == 200
    response = test_client.post("/register_customer", data=dict(
        k_vorname='Max',
        k_nachname="Mustermann",
        k_straße = "Teststraße 1",
        k_plz="123456",
        k_ort="Testhausen",
        email="max@testmail.com",
        password="123456",
        password_repeated="123456"
        ), follow_redirects=True)
    assert response.request.path == "/"
    assert session["_user_id"] == "1"


def test_logout_user(test_client):
    """
    WHEN the '/logout' page receives a GET request
    THEN check that 
    ...no user is logged in
    ...a redirect to "/" is returned
    """

    assert session["_user_id"] == "1" # still logged in?
    response = test_client.get('/logout', follow_redirects=True)
    assert response.request.path == "/"
    assert "_user_id" not in session


def test_register_customer_email_taken(test_client):
    """
    WHEN the '/register_customer' page is posted to (POST) with an email that was already used
    THEN check that 
    ...a redirect to "/login" is returned
    ...no active login session is created
    """
    assert test_client.get('/register_customer').status_code == 200
    response = test_client.post("/register_customer", data=dict(
        k_vorname='Max',
        k_nachname="Mustermann",
        k_straße = "Teststraße 1",
        k_plz="123456",
        k_ort="Testhausen",
        email="max@testmail.com",
        password="123456",
        password_repeated="123456"
        ), follow_redirects=True)
    assert response.request.path == "/login"
    assert "_user_id" not in session


def test_login_user_pw_incorrect(test_client):
    """
    WHEN the '/login' page receives a POST request with incorrect password
    THEN check that 
    ...no user is logged in
    ...a redirect to "/login" is returned
    ...the response contains the correct error message
    """

    response = test_client.post("/login", data=dict(
        email="max@testmail.com",
        password="ABCDEF"
        ), follow_redirects=True)
    assert response.request.path == "/login"
    print((session))
    assert "_user_id" not in session
    assert b'Password incorrect, please try again.' in response.data


def test_login_user_email_incorrect(test_client):
    """
    WHEN the '/login' page receives a POST request with incorrect email
    THEN check that 
    ...no user is logged in
    ...a redirect to "/login" is returned
    ...the response contains the correct error message
    """
    response = test_client.post("/login", data=dict(
        email="maxine@testmail.com",
        password="123456"
        ), follow_redirects=True)
    assert response.request.path == "/login"
    print((session))
    assert "_user_id" not in session
    assert b"That email does not exist, please try again." in response.data


def test_login_user(test_client):
    """
    WHEN the '/login' page receives a POST request with correct credentials
    THEN check that 
    ...the correct user is logged in
    ...a redirect to "/" is returned
    """

    response = test_client.post("/login", data=dict(
        email="max@testmail.com",
        password="123456"
        ), follow_redirects=True)
    assert response.request.path == "/"
    assert session["_user_id"] == "1"



def test_register_business_pw_unequal(test_client):
    """
    WHEN the '/register_customer' page is posted to (POST) with password fields unequal
    THEN check that 
    ...a redirect to "/register_customer" is returned
    ...no new user is logged in
    ...the response contains teh correct error message
    """
    assert test_client.get('/register_business').status_code == 200
    response = test_client.post("/register_business", data=dict(
        d_vorname='Erika',
        d_nachname="Mustermann",
        firmenname="Testfirma GmbH",
        d_straße = "Teststraße 2",
        d_plz="123456",
        d_ort="Testhausen",
        radius = "5",
        email="erika@testmail.com",
        password="123456",
        password_repeated="ABCDEFG"
        ), follow_redirects=True)
    assert response.request.path == "/register_business"
    assert session["_user_id"] is not "2"
    assert b"Field must be equal to password." in response.data


def test_register_business(test_client):
    """
    WHEN the '/register_customer' page is posted to (POST) with password fields equal
    THEN check that 
    ...a redirect to "/" is returned
    ...the correct user is logged in
    """
    assert test_client.get('/register_business').status_code == 200
    response = test_client.post("/register_business", data=dict(
        d_vorname='Erika',
        d_nachname="Mustermann",
        firmenname="Testfirma GmbH",
        d_straße = "Teststraße 2",
        d_plz="123456",
        d_ort="Testhausen",
        radius = "5",
        email="erika@testmail.com",
        password="123456",
        password_repeated="123456"
        ), follow_redirects=True)
    assert response.request.path == "/"
    assert session["_user_id"] is not "1"
    assert session["_user_id"] == "2"


def test_register_business_email_taken(test_client):
    """
    WHEN the '/register_customer' page is posted to (POST) with email that was already used
    THEN check that 
    ...a redirect to "/login" is returned
    ...the response contains the correct error message
    ...no new user is logged in
    """
    assert test_client.get('/register_business').status_code == 200
    response = test_client.post("/register_business", data=dict(
        d_vorname='Erika',
        d_nachname="Mustermann",
        firmenname="Testfirma GmbH",
        d_straße = "Teststraße 2",
        d_plz="123456",
        d_ort="Testhausen",
        radius = "5",
        email="erika@testmail.com",
        password="123456",
        password_repeated="123456"
        ), follow_redirects=True)
    assert response.request.path == "/login"
    assert b'Es liegt bereits eine Registrierung mit dieser Email vor. Bitte Login probieren.' in response.data
    assert session["_user_id"] is not "1"
    assert session["_user_id"] is not "3"
    assert session["_user_id"] == "2"


def test_register_business_companyname_taken(test_client):
    """
    WHEN the '/register_customer' page is posted to (POST) with company name that was already used
    THEN check that 
    ...a redirect to "/register_business" is returned
    ...the response contains the correct error message
    ...no new user is logged in
    """
    assert test_client.get('/register_business').status_code == 200
    response = test_client.post("/register_business", data=dict(
        d_vorname='John',
        d_nachname="Doe",
        firmenname="Testfirma GmbH",
        d_straße = "Teststraße 3",
        d_plz="123456",
        d_ort="Testhausen",
        radius = "5",
        email="john_d@testmail.com",
        password="123456",
        password_repeated="123456"
        ), follow_redirects=True)
    assert response.request.path == "/register_business"
    assert b'Firmenname wurde bereits registriert!' in response.data
    assert session["_user_id"] is not "1"
    assert session["_user_id"] is not "3"
    assert session["_user_id"] == "2"



def test_change_pw_old_pw_incorrect(test_client):
    """
    WHEN the '/changepw' route receives a POST request with incorrect old password
    THEN check that
    ...a redirect to '/changepw' is returned
    ...the response contains the correct error message
    """
    response = test_client.post('/changepw', data=dict(
        old_pw="ABCDEF",
        new_pw="newpassword",
        new_pw_repeated="newpassword"
        ), follow_redirects=True)
    assert response.request.path == '/changepw'
    assert b'Altes Passwort nicht korrekt!'


def test_change_pw_new_pw_unequal(test_client):
    """
    WHEN the '/changepw' route receives a POST request with new passwords unequal
    THEN check that
    ...a redirect to '/changepw' is returned
    ...the response contains the correct error message
    """
    response = test_client.post('/changepw', data=dict(
        old_pw="123456",
        new_pw="newpassword",
        new_pw_repeated="newpasswörd"
        ), follow_redirects=True)
    assert response.request.path == '/changepw'
    print(response.data)
    assert b'Neue Passw\xc3\xb6rter stimmen nicht \xc3\xbcberein!' in response.data


def test_change_pw(test_client):
    """
    WHEN the '/changepw' route receives a POST request with correct credentials
    THEN check that
    ...a redirect to '/' is returned
    ...???
    """
    response = test_client.post('/changepw', data=dict(
        old_pw="123456",
        new_pw="123456",
        new_pw_repeated="123456"
        ), follow_redirects=True)
    assert response.request.path == '/'



