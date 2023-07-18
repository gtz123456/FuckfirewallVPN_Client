import requests

def login(email, password, address):
    response = requests.post(f'{address}/api/tokens', auth=(email, password))

    if response.status_code == 200:
        token = response.json().get('token')
        return token
    else:
        return None

def getConfig(token, address):
    headers = {'Authorization': f'Bearer {token}'}
    config = requests.get(f'{address}/api/config', headers=headers)
    if config.status_code == 200:
        return config.json()
    else:
        None

def getUserConfig(email, password, address):
    token = login(email, password, address)
    if not token: return None
    data = getConfig(token, address)
    if not data: return None
    #address = '209.141.49.64' TODO
    port = data['port']
    uuid = data['uuid']
    pubkey = data['pubkey']
    shortid = data['shortid']
    return address, port, uuid, pubkey, shortid