import requests

API = "http://pyminer.com/"
LOGIN_URL = 'api/v1/user/login/'


def client(url, method, data):
    conn = requests.session()
    if method == "post":
        headers = {
            "Content-type": "application/json; charset=utf-8;"
        }
        resp = conn.post(url, data, headers)
    elif method == "get":
        pass
    return resp
