import requests

class User():
    def __init__(self, email, token, balance) -> None:
        self.email = email
        self.token = token
        self.balance = balance

def register(email, password, refer, address):
    userData = {
        'email': email,
        'password': password,
        'refer': refer
    }
    response = requests.post(f'http://{address}:8000/api/register', data=userData, verify=False)
    if response.status_code == 200:
        return response.json()['result']
        
    return "Failed to register user. Status code:" + str(response.status_code)


def getToken(email, password, address):
    response = requests.post(f'http://{address}:8000/api/tokens', auth=(email, password), verify=False)
    print(response.content)
    if response.status_code == 200:
        token = response.json().get('token')
        return token
    
    return None

def getConfig(token, address):
    headers = {'Authorization': f'Bearer {token}'}
    config = requests.get(f'http://{address}:8000/api/config', headers=headers, verify=False)
    if config.status_code == 200:
        return config.json()
    else:
        None

def login(email, password, address):
    # TODO try catch
    token = getToken(email, password, address)
    if not token: return None
    config = getConfig(token, address)
    return config if config else None
