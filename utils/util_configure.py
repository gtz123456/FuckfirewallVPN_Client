import subprocess
import os

from random import randint, choice
from utils.util_sys import XRAY_PATH

def addUser(clientNum=1):
    uuid = generateUUID()
    shortids = [generateShortID() for i in range(clientNum)]
    #TODO add user to db

def generatePort():
    port = randint(10000, 30000) #TODO:check repeated
    return port

def generateUUID():
    output, error = subprocess.Popen([XRAY_PATH, 'uuid'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if error:
        print("Error: unable to generate uuid")
    uuid = output.decode()
    return uuid

def generateKey():
    output, error = subprocess.Popen([XRAY_PATH, 'x25519'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if error:
        print("Error: unable to generate reality key")

    key = output.decode()
    pubkey, prikey = key[13:56], key[69:]
    return pubkey, prikey

def generateShortID():
    shortid = ''.join(choice('0123456789abcdef') for _ in range(16))
    return shortid
