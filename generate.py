from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import sys

#public key for encryption and private key for decryption
#if you lost the decryption key then forget your files for ever
#this script should be run on your safe folder beware the encrypt it!!

PRIVATE_KEY = "./keys/private.pem"
PUBLIC_KEY = "./keys/public.pem"
RSA_KEY_SIZE = 4096

def check_keys():
    if not os.path.exists("keys"):
        os.mkdir("keys")
    if os.path.exists(PRIVATE_KEY) or os.path.exists(PUBLIC_KEY):
        print("found previous keys !!")
        op = input("do you want to overwrite? y/n >> ")
        if op == "n":
            sys.exit(0)
        elif op == "y":
            pass
        else:
            sys.exit("please specify one of the options")

def generate_rsa_keys(key_size=RSA_KEY_SIZE):
    # generate decryption/encryption keys
    keyPair = RSA.generate(RSA_KEY_SIZE)
    pubKey = keyPair.publickey()
    pubKeyPEM = pubKey.exportKey()
    with open(PUBLIC_KEY, 'w') as pub:
        pub.write(pubKeyPEM.decode('ascii'))
    print("encryption/public key:\n"+pubKeyPEM.decode('ascii'))

    privKeyPEM = keyPair.exportKey()
    with open(PRIVATE_KEY, 'w') as prv:
        prv.write(privKeyPEM.decode('ascii'))
    print("decryption/private key:\n"+privKeyPEM.decode('ascii'))
    print("keys has been generated, keep them safe,u will loose your files if you loose them.")
    print("keys has been saved to your disk!")

check_keys()
generate_rsa_keys()
