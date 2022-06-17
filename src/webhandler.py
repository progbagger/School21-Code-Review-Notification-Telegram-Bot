import requests

url = "https://edu.21-school.ru"

session = requests.Session()

resp = session.get(url, allow_redirects=False)

for r in session.resolve_redirects(resp, resp.request):
    print(r)
