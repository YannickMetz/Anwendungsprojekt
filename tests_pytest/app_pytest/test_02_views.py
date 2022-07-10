from dataclasses import dataclass
from http import client
from unittest.result import failfast
from urllib import response
from flask import Response, session
from click.testing import CliRunner
from app.mock_data import create_test_service, read_image
from base64 import b64encode
from app import db
from app.models import Auftrag, Dienstleisterprofil, DienstleisterProfilGalerie
from app.views import get_services_for_provider
from werkzeug.datastructures import ImmutableMultiDict



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



def test_change_service_provider_profile_POST_add_profile_image(test_client):
    """
    WHEN the route '/change_service_provider_profile' receives a POST request for AddProfileImageForm when a service provider is logged in
    THEN check that...
    ...response data does contain "Profilbeschreibung"
    ...response returns status code '302'
    ...previously empty 'Dienstleisterprofil.profilbild' field contains data
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    assert db.session.query(Dienstleisterprofil).first().profilbild is None
    imagefile = {"profile_img": (read_image(1), '1_stock.jpeg')}
    response = test_client.post("/change_service_provider_profile", data=imagefile, buffered=True, content_type='multipart/form-data')
    assert response.status_code == 302
    assert db.session.query(Dienstleisterprofil).first().profilbild is not None



def test_change_service_provider_profile_POST_add_gallery_image(test_client):
    """
    WHEN the route '/change_service_provider_profile' receives a POST request for AddImageForm when a service provider is logged in
    THEN check that...
    ...response data does contain "Profilbeschreibung"
    ...response returns status code '302'
    ...previously empty 'DienstleisterProfilGalerie' table contains data
    ...previoulsy not appearing string '<div class="col-xl-3 col-lg-4 col-md-6">' appears twice in route profile/service_provider/2' response data (used for gallery image grid view)
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    profile_response = test_client.get("profile/service_provider/2")
    assert b'<div class="col-xl-3 col-lg-4 col-md-6">' not in profile_response.data
    imagefile1 = {"img": (read_image(2), '2_stock.jpeg')}
    response = test_client.post("/change_service_provider_profile", data=imagefile1, buffered=True, content_type='multipart/form-data')
    assert response.status_code == 302
    assert len(db.session.query(DienstleisterProfilGalerie).all()) == 1
    imagefile2 = {"img": (read_image(3), '3_stock.jpeg')}
    response = test_client.post("/change_service_provider_profile", data=imagefile2, buffered=True, content_type='multipart/form-data')
    assert response.status_code == 302
    assert len(db.session.query(DienstleisterProfilGalerie).all()) == 2
    profile_response = test_client.get("profile/service_provider/2")
    assert str(profile_response.data).count('<div class="col-xl-3 col-lg-4 col-md-6">') == 2


def test_remove_gallery_image(test_client):
    """
    WHEN the route '/remove_gallery_image/1' receives a POST request for AddImageForm when a service provider is logged in
    THEN check that...
    ...response returns status code '200'
    ...'DienstleisterProfilGalerie' table contains only 1 entry (2 entries before test)
    ...string '<div class="col-xl-3 col-lg-4 col-md-6">' appears only once in route profile/service_provider/2' response data (used for gallery image grid view)
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    assert len(db.session.query(DienstleisterProfilGalerie).all()) == 2
    response = test_client.get("/remove_gallery_image/1", follow_redirects=True)
    assert response.status_code == 200
    profile_response = test_client.get("profile/service_provider/2")
    assert str(profile_response.data).count('<div class="col-xl-3 col-lg-4 col-md-6">') == 1
    assert len(db.session.query(DienstleisterProfilGalerie).all()) == 1


def test_request_quotation_as_service_provider(test_client):
    """
    WHEN the route '/request-quotation/2' receives a GET request when a service provider is logged in
    THEN check that...
    ...response returns redirect to '/'
    ...response data contains "als Dienstleister leider keine Dienstleistungen anfragen."
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    response = test_client.get("/request-quotation/2", follow_redirects=True)
    assert b'als Dienstleister leider keine Dienstleistungen anfragen.' in response.data


def test_request_quotation(test_client):
    """
    WHEN the route '/request-quotation/2' receives a POST request for RequestQuotationForm when a customer is logged in
    THEN check that...
    ...response returns redirect to '/'
    ...previously empty table "Auftrag" contains 1 entry
    ...response for route '/order-details/1' returns status code '200'
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="max@testmail.com", password="123456")
    assert session["_user_id"] == "1"
    response = test_client.post("/request-quotation/2", data=dict(
        service='Testservice',
        request='Request Body',
        service_start='9999-01-01',
        img=read_image(4)
        ),buffered=True, content_type='multipart/form-data', follow_redirects=True)
    assert response.request.path == "/"
    assert len(db.session.query(Auftrag).all()) == 1
    response_order_details = test_client.get('/order-details/1')
    assert response_order_details.status_code == 200




def test_order_overview_as_customer(test_client):
    """
    WHEN the route '/orders/' receives a GET request while a customer is logged in
    THEN check that...
    ...response returns status code '200'
    ...the response data contains the correct HTML string
    """

    minified_html = b'<h1>Ihre offenen Auftr\xc3\xa4ge:</h1>\n  \n      <a class="table-order-text" href="/order-details/1" id="Testservice">\n        <div class="panel-default">\n          <table class="table-order-overview">\n            <div class="order-overview-section">\n              <tr>\n                <div>\n                  <td class="table-order-details-column-left">\n                    Auftragsnummer:\n                  </td>\n                  <td class="table-order-details-column-right">\n                    1\n                  </td>\n                </div>\n              </tr>\n              <tr>\n                <td class="table-order-details-column-left">\n                  Dienstleistung:\n                </td>\n                <td class="table-order-details-column-right">\n                  Testservice\n                </td>\n              </tr>\n              <tr>\n                <td class="table-order-details-column-left">\n                  \n                  \n                  Dienstleister: \n                </td>\n                <td class="table-order-details-column-left">\n                  \n                   \n                  Testfirma GmbH \n                </td>\n              </tr>\n              <tr>\n                <td class="table-order-details-column-left">\n                  Auftragsstatus:\n                </td>\n                <td class="table-order-details-column-right">\n                  \xc3\x9cbermittelt\n                </td>\n              </tr>\n            </div>\n          </table>\n        </div>\n      </a>\n  \n</div>\n\n<div class="container container-standard">\n  <h1>Ihre abgeschlossenen Auftr\xc3\xa4ge:</h1>\n  \n</div>\n'
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="max@testmail.com", password="123456")
    assert session["_user_id"] == "1"
    response = test_client.get('/orders/')
    assert response.status_code == 200
    assert minified_html in response.data


def test_order_overview_as_service_provider(test_client):
    """
    WHEN the route '/orders/' receives a GET request while a service provider is logged in
    THEN check that...
    ...response returns status code '200'
    ...the response data contains the correct HTML string
    """

    minified_html = b'<h1>Ihre offenen Auftr\xc3\xa4ge:</h1>\n  \n      <a class="table-order-text" href="/order-details/1" id="Testservice">\n        <div class="panel-default">\n          <table class="table-order-overview">\n            <div class="order-overview-section">\n              <tr>\n                <div>\n                  <td class="table-order-details-column-left">\n                    Auftragsnummer:\n                  </td>\n                  <td class="table-order-details-column-right">\n                    1\n                  </td>\n                </div>\n              </tr>\n              <tr>\n                <td class="table-order-details-column-left">\n                  Dienstleistung:\n                </td>\n                <td class="table-order-details-column-right">\n                  Testservice\n                </td>\n              </tr>\n              <tr>\n                <td class="table-order-details-column-left">\n                   \n                  Kunde: \n                  \n                </td>\n                <td class="table-order-details-column-left">\n                  \n                  Mustermann \n                  \n                </td>\n              </tr>\n              <tr>\n                <td class="table-order-details-column-left">\n                  Auftragsstatus:\n                </td>\n                <td class="table-order-details-column-right">\n                  \xc3\x9cbermittelt\n                </td>\n              </tr>\n            </div>\n          </table>\n        </div>\n      </a>\n  \n</div>\n\n<div class="container container-standard">\n  <h1>Ihre abgeschlossenen Auftr\xc3\xa4ge:</h1>\n  \n</div>\n'
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    response = test_client.get('/orders/')
    assert response.status_code == 200
    print(response.data)
    assert minified_html in response.data
 

def test_order_details_after_quotation_request(test_client):
    """
    WHEN the route '/order-details/1' receives a GET request after quotation was requested
    THEN check that...
    ...response data contains "Angebot erstellen" when service provider is logged in
    ...response data does not contain "Angebot erstellen" when customer is logged in
    """

    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    response = test_client.get('/order-details/1')
    assert b'Angebot erstellen' in response.data

    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="max@testmail.com", password="123456")
    assert session["_user_id"] == "1"
    response = test_client.get('/order-details/1')
    assert b'Angebot erstellen' not in response.data
  

def test_create_quotation(test_client):
    """
    WHEN the route '/quote/1' receives a POST request on form 'CreateQuotation' from service provider
    THEN check that...
    ...response returns status code '200'
    ...response redirects to route '/order-details/1'
    ...response data contains '999.95'
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    response = test_client.post('/quote/1', data=dict(quote=999.95123, service_start='9999-01-31', service_finish='9999-02-25'), follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/order-details/1'
    assert b'999.95' in response.data


def test_reject_quotation(test_client):
    """
    WHEN the route '/order-details/1' receives a POST request from customer on form 'AcceptQuotation' with value 'reject'
    THEN check that...
    ...response data contains 'Abgelehnt durch Kunde' when logged in as customer
    ...order is listed in the bottom section of route '/orders/'
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="max@testmail.com", password="123456")
    assert session["_user_id"] == "1"
    response = test_client.post('/order-details/1', data=dict(accept_selection='reject'),follow_redirects=True)
    assert b'Abgelehnt durch Kunde' in response.data
    orders_response = test_client.get('/orders/')
    print(orders_response.data)
    assert (
        b'<h1>Ihre abgeschlossenen Auftr\xc3\xa4ge:</h1>\n  \n      <a class="table-order-text" href="/order-details/1">\n        <div class="panel-default">\n          <table class="table-order-overview">\n            <div class="order-overview-section">\n              <tr>\n                <div>\n                  <td class="table-order-details-column-left">\n                    Auftragsnummer:\n                  </td>\n                  <td class="table-order-details-column-right">\n                    1'
        ) in orders_response.data


def test_confirm_quotation(test_client):
    """
    WHEN the route '/order-details/1' receives a POST request from customer on form 'AcceptQuotation' with value 'accept'
    THEN check that...
    ...response data contains '<a href="/confirm_order/1">' and 'Angebot best\xc3\xa4tigt' when logged in as customer
    ...response data contains the option to cancel the order when logged in as service provider
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="max@testmail.com", password="123456")
    assert session["_user_id"] == "1"
    response = test_client.post('/order-details/1', data=dict(accept_selection='accept'),follow_redirects=True)
    assert b'<a href="/confirm_order/1">' in response.data
    assert b'Angebot best\xc3\xa4tigt' in response.data
    assert b' <input class="btn btn-custom" id="submit_cancel_order" name="submit_cancel_order" type="submit" value="Best\xc3\xa4tigen">' not in response.data
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    response = test_client.get('order-details/1')
    assert b' <input class="btn btn-custom" id="submit_cancel_order" name="submit_cancel_order" type="submit" value="Best\xc3\xa4tigen">' in response.data


def test_confirm_order(test_client):
    """
    WHEN the route '/confirm_order/1' receives a POST request from customer on form 'RateServiceForm'
    THEN check that...
    ...response data contains 'Abgenommen' when logged in as customer
    ...response data contains the option complete the order when logged in as service provider, but not as customer
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="max@testmail.com", password="123456")
    assert session["_user_id"] == "1"
    response = test_client.post('/confirm_order/1', data=dict(rating=3, comment="testcomment", img=read_image(4)), follow_redirects=True)
    assert b'Abgenommen' in response.data
    assert b'<input id="complete_order" name="complete_order" type="checkbox" value="y">' not in response.data
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    response = test_client.get('order-details/1')
    print(response.data)
    assert b'<input id="complete_order" name="complete_order" type="checkbox" value="y">' in response.data
    


def test_complete_order(test_client):
    """
    WHEN the route '/order-details/1' receives a POST request from service provider on form 'CompleteOrder' with value 'True'
    THEN check that...
    ...response data contains 'Abgeschlossen'
    ...order is listed in the bottom section of route '/orders/'
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    response = test_client.post('/order-details/1', data=dict(complete_order=True), follow_redirects=True)
    assert b'Abgeschlossen' in response.data
    orders_response = test_client.get('/orders/')
    print(orders_response.data)
    assert (
        b'<h1>Ihre abgeschlossenen Auftr\xc3\xa4ge:</h1>\n  \n      <a class="table-order-text" href="/order-details/1">\n        <div class="panel-default">\n          <table class="table-order-overview">\n            <div class="order-overview-section">\n              <tr>\n                <div>\n                  <td class="table-order-details-column-left">\n                    Auftragsnummer:\n                  </td>\n                  <td class="table-order-details-column-right">\n                    1'
        ) in orders_response.data



def test_remove_service(test_client):
    """
    WHEN the route '/remove_service/1'' receives a GET request
    THEN check that...
    ...response returns status code '200'
    ...the number of services associated with the service provider is "0"
    """
    logout(test_client)
    assert "_user_id" not in session
    login(test_client, email="erika@testmail.com", password="123456")
    assert session["_user_id"] == "2"
    assert len(get_services_for_provider(2)) == 1
    response = test_client.get('/remove_service/1', follow_redirects=True)
    assert response.status_code == 200
    assert len(get_services_for_provider(2)) == 0
