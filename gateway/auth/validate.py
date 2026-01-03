import os, requests

def token(request):
    if not "Authorization" in request.headers:
        return None, "error : missing token, 401"
    token = request.headers["Authorization"]

    if not token:
        return None, "error :missing token", 401
    
    try:
        response = requests.post(
            f'http://{os.getenv("AUTH_SVC_ADDRESS")}/validate',
            headers={"Authorization": token},
            timeout=5
        )
    except Exception as e:
        return None, ("error: failed to validate token", 500)
   
    if response.status_code == 200:
        return response.text , None
    else:
        return None, (response.text, response.status_code )