import requests_html
from requests_html import HTMLSession
import requests

link_pre_auth = 'https://auth.sberclass.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/'
link_pre_auth_js = 'https://auth.sberclass.ru/auth/resources/1eha4/login/sc21/js/login.js?v=2'

pre_auth_page_payload = {
    'client_id': 'school21',
    'redirect_uri': 'https://edu.21-school.ru/',
    'response_mode': 'fragment',
    'response_type': 'code',
    'scope': 'openid',
    'state': 'c6bab195-f1a0-407a-a8c2-f593f22c1df3',
    'nonce': '998c1001-f022-4bc5-9c15-519f6c9779ce'
}

session = HTMLSession()

# Pre_auth requests
pre_auth_login_request = session.get(link_pre_auth, data=pre_auth_page_payload)
pre_auth_login_request_js = session.get(link_pre_auth_js, data={'v': 2})

# pre_auth_login_request_js.html.render()
# js_content = pre_auth_login_request_js.html.html

pre_auth_login_request.html.render()
content = pre_auth_login_request.html.html
print(content)
