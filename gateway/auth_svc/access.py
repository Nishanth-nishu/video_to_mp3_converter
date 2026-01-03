import os
import requests as http_requests

def login(req):
    auth = req.authorization
    if not auth:
        return None, {"error": "missing credentials"}, 401

    response = http_requests.post(
        f"http://{os.getenv('AUTH_SVC_ADDRESS')}/login",
        auth=(auth.username, auth.password)
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
