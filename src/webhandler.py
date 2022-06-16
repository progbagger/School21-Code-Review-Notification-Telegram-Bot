# import requests_html
# from requests_html import HTMLSession
import requests

link_pre_auth = "https://auth.sberclass.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/auth"

edu_link = "https://edu.21-school.ru/"

headers = {
    # "cache-control": "no-store, must-revalidate, max-age=0",
    # "content-encoding": "gzip",
    # "content-language": "ru",
    # "content-security-policy": "frame-src 'self'; frame-ancestors 'self'; object-src 'none';",
    # "content-type": "text/html;charset=utf-8",
    # "date": "Thu, 16 Jun 2022 21:37:04 GMT",
    # "referrer-policy": "no-referrer",
    # "set-cookie": "KC_RESTART=eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzYjc5MDRhYS0wY2YzLTQ1M2QtOGE5Ni1jYWM0N2MxZmU2ZmYifQ.eyJjaWQiOiJzY2hvb2wyMSIsInB0eSI6Im9wZW5pZC1jb25uZWN0IiwicnVyaSI6Imh0dHBzOi8vZWR1LjIxLXNjaG9vbC5ydS8_ZXJyb3I9aW52YWxpZF9yZXF1ZXN0JmVycm9yX2Rlc2NyaXB0aW9uPU1pc3NpbmcrcGFyYW1ldGVyJTNBK3Jlc3BvbnNlX3R5cGUiLCJhY3QiOiJBVVRIRU5USUNBVEUiLCJub3RlcyI6eyJzY29wZSI6Im9wZW5pZCIsImlzcyI6Imh0dHBzOi8vYXV0aC5zYmVyY2xhc3MucnUvYXV0aC9yZWFsbXMvRWR1UG93ZXJLZXljbG9hayIsInJlc3BvbnNlX3R5cGUiOiJjb2RlIiwicmVkaXJlY3RfdXJpIjoiaHR0cHM6Ly9lZHUuMjEtc2Nob29sLnJ1Lz9lcnJvcj1pbnZhbGlkX3JlcXVlc3QmZXJyb3JfZGVzY3JpcHRpb249TWlzc2luZytwYXJhbWV0ZXIlM0ErcmVzcG9uc2VfdHlwZSIsInN0YXRlIjoiYjc2MDA5MTctM2NhYi00ZjY4LTg0YWYtNGZjNDMxZmEzZDIzIiwibm9uY2UiOiJjYjVhNTExYi0wMzYwLTRlNDYtOGFmMS02Yjc0OGNiNjA0MDEiLCJyZXNwb25zZV9tb2RlIjoiZnJhZ21lbnQifX0.zvykGB7AMbDjYp3_ilOqUysV29Bb5pjfRrpDQdlcNzs; Version=1; Path=/auth/realms/EduPowerKeycloak/; HttpOnly",
    # "strict-transport-security": "max-age=31536000; includeSubDomains",
    # "strict-transport-security": "max-age=31536000; includeSubDomains",
    # "vary": "Accept-Encoding",
    # "x-content-type-options": "nosniff",
    # "x-envoy-upstream-service-time": "5",
    # "x-frame-options": "SAMEORIGIN",
    # "x-robots-tag": "none",
    # "x-xss-protection": "1; mode=block",
    # ":authority": "auth.sberclass.ru",
    # ":method": "GET",
    # ":path": "/auth/realms/EduPowerKeycloak/protocol/openid-connect/auth?client_id=school21&redirect_uri=https%3A%2F%2Fedu.21-school.ru%2F%3Ferror%3Dinvalid_request%26error_description%3DMissing%2Bparameter%253A%2Bresponse_type&state=b7600917-3cab-4f68-84af-4fc431fa3d23&response_mode=fragment&response_type=code&scope=openid&nonce=cb5a511b-0360-4e46-8af1-6b748cb60401",
    # ":scheme": "https",
    # "accept-encoding": "gzip, deflate, br",
    # "accept-language": "ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7",
    # "cache-control": "no-cache",
    # "cookie": "AUTH_SESSION_ID=992510ff-1a58-45e1-978c-b671f5faba28.keycloak-754c9bd57-vjj6z; AUTH_SESSION_ID_LEGACY=992510ff-1a58-45e1-978c-b671f5faba28.keycloak-754c9bd57-vjj6z; KC_RESTART=eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzYjc5MDRhYS0wY2YzLTQ1M2QtOGE5Ni1jYWM0N2MxZmU2ZmYifQ.eyJjaWQiOiJzY2hvb2wyMSIsInB0eSI6Im9wZW5pZC1jb25uZWN0IiwicnVyaSI6Imh0dHBzOi8vZWR1LjIxLXNjaG9vbC5ydS8_ZXJyb3I9aW52YWxpZF9yZXF1ZXN0JmVycm9yX2Rlc2NyaXB0aW9uPU1pc3NpbmcrcGFyYW1ldGVyJTNBK3Jlc3BvbnNlX3R5cGUiLCJhY3QiOiJBVVRIRU5USUNBVEUiLCJub3RlcyI6eyJzY29wZSI6Im9wZW5pZCIsImlzcyI6Imh0dHBzOi8vYXV0aC5zYmVyY2xhc3MucnUvYXV0aC9yZWFsbXMvRWR1UG93ZXJLZXljbG9hayIsInJlc3BvbnNlX3R5cGUiOiJjb2RlIiwicmVkaXJlY3RfdXJpIjoiaHR0cHM6Ly9lZHUuMjEtc2Nob29sLnJ1Lz9lcnJvcj1pbnZhbGlkX3JlcXVlc3QmZXJyb3JfZGVzY3JpcHRpb249TWlzc2luZytwYXJhbWV0ZXIlM0ErcmVzcG9uc2VfdHlwZSIsInN0YXRlIjoiYjc2MDA5MTctM2NhYi00ZjY4LTg0YWYtNGZjNDMxZmEzZDIzIiwibm9uY2UiOiJjYjVhNTExYi0wMzYwLTRlNDYtOGFmMS02Yjc0OGNiNjA0MDEiLCJyZXNwb25zZV9tb2RlIjoiZnJhZ21lbnQifX0.zvykGB7AMbDjYp3_ilOqUysV29Bb5pjfRrpDQdlcNzs",
    # "dnt": "1",
    # "pragma": "no-cache",
    # "referer": "https://edu.21-school.ru/",
    # "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": '"Windows"',
    # "sec-fetch-dest": "document",
    # "sec-fetch-mode": "navigate",
    # "sec-fetch-site": "cross-site",
    # "sec-fetch-user": "?1",
    # "upgrade-insecure-requests": "1",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
}

# payload = {"client_id": "school21", "redirect_uri": edu_link}

pre_auth_page_payload = {
    "client_id": "school21",
    "redirect_uri": edu_link,
    "response_mode": "fragment",
    "response_type": "code",
    "scope": "openid",
    # "state": "c6bab195-f1a0-407a-a8c2-f593f22c1df3",
    # "nonce": "998c1001-f022-4bc5-9c15-519f6c9779ce",
}

# session = HTMLSession()

# # Pre_auth requests
# pre_auth_login_request = session.get(link_pre_auth, data=pre_auth_page_payload)
# pre_auth_login_request_js = session.get(link_pre_auth_js, data={"v": 2})

# pre_auth_login_request_js.html.render()
# js_content = pre_auth_login_request_js.html.html

r = requests.get(
    url=edu_link,
    data=pre_auth_page_payload,
    timeout=10,
    # headers=headers,
)

with open("webpage.html", "w") as file:
    file.write(r.text)
print(r)
