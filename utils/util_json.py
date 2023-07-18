import json
import os

def initRealityClientConfig(address: str, port: int, uuid: str, pubkey: str, shortid: str):
    from utils.util_sys import BASE_DIR
    with open(os.path.join(BASE_DIR, 'defaultClient.json')) as file:
        data = json.load(file)

    settings = data['outbounds'][0]['settings']
    vnext = settings['vnext'][0]
    vnext['address'] = address
    vnext['port'] = port

    user = vnext['users'][0]
    user['id'] = uuid

    streamSettings = data['outbounds'][0]['streamSettings']
    realitySettings = streamSettings['realitySettings']
    realitySettings['publicKey'] = pubkey
    realitySettings['shortId'] = shortid

    with open(os.path.join(BASE_DIR, 'xray', 'config.json'), mode='w+') as file:
        json.dump(data, file)

def initRealityServerConfig(port: int, uuid: str, prikey: str, shortid: str):
    from utils.util_json import BASE_DIR
    with open(os.path.join(BASE_DIR, 'utils', 'defaultServer.json')) as file:
        data = json.load(file)

    inbound = data['inbounds'][0]
    inbound['port'] = port

    client = inbound['settings']['clients'][0]
    client['id'] = uuid

    realitySettings = data['inbounds'][0]['streamSettings']['realitySettings']
    realitySettings['privateKey'] = prikey
    realitySettings['shortIds'] = [shortid]

    with open(os.path.join(BASE_DIR, 'xray', 'config.json'), mode='w+') as file:
        json.dump(data, file)

def getUser():
    from utils.util_sys import BASE_DIR

    if not os.path.isfile(os.path.join(BASE_DIR, 'user_config.json')):
        return None, None
    
    with open(os.path.join(BASE_DIR, 'user_config.json')) as file:
        data = json.load(file)
    return data['email'], data['password']

def saveUser(email, password):
    from utils.util_sys import BASE_DIR
    with open(os.path.join(BASE_DIR, 'user_config.json'), mode='w+') as file:
        data = {'email': email, 'password': password}
        json.dump(data, file)

