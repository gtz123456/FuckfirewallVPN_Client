import requests

def login(email, password, address):
    response = requests.post(f'http://{address}/api/tokens', auth=(email, password))

    if response.status_code == 200:
        token = response.json().get('token')
        return token
    else:
        return None

def getConfig(token, address):
    headers = {'Authorization': f'Bearer {token}'}
    config = requests.get(f'http://{address}/api/config', headers=headers)
    if config.status_code == 200:
        return config.json()
    else:
        None

def getUserConfig(email, password, address):
    token = login(email, password, address)
    if not token: return None
    data = getConfig(token, address)
    if not data: return None
    port = data['port']
    uuid = data['uuid']
    pubkey = data['pubkey']
    shortid = data['shortid']
    return port, uuid, pubkey, shortid