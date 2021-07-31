from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from collections import deque
from os import walk, path, remove
from multiprocessing import cpu_count, Pool, freeze_support
import argparse


class Decrypt:
    def __init__(self):
        self.key= None
        self.dirs = None
        self.files = deque()

    def rsa_decrypt(self,InputKey,enc_key):
        with open(InputKey, 'rb') as rsa_private_key:
            rsa_key = rsa_private_key.read()
        private_key = RSA.importKey(rsa_key)
        private_decryptor = PKCS1_OAEP.new(private_key)
        with open(enc_key, "rb") as f:     
            aes_key =  private_decryptor.decrypt(f.read())
            self.key = aes_key

    def get_files(self):
            for one in self.dirs:
                for root, dirs, files in walk(one):
                    for file in files:
                        if file.endswith(".wasp"):
                            self.files.append(path.join(root,file))

    def decrypt(self,file):    
        with open(file, "rb") as f:
            iv = f.read(16)
            cipher = AES.new(self.key,AES.MODE_CBC, iv)
            while True: 
                x = f.read(1024)
                if not x:
                    break
                yield cipher.decrypt(x)

    def output(self,file,out):
        with open(file[:-5], "wb") as o:
            while True:
                try:
                    o.write(next(out))
                except StopIteration:
                    break
    def worker(self):
        while self.files:
            file = self.files.pop()
            yield file

    def test(self,file):
        dec = self.decrypt(file)
        self.output(file,dec)
        remove(file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k','--key', help='RSA private key', required=True)
    parser.add_argument('-e','--enc', help='encrypted AES key', required=True)
    parser.add_argument('-d','--dir', nargs='+', help='Directories to decrypt', required=True)
    args = parser.parse_args()
    run = Decrypt()
    run.dirs = args.dir
    print("__START DECRYPTION__")
    print("[+] decrypting aes key..")
    run.rsa_decrypt(args.key,args.enc)
    print("[+] getting files list..")
    run.get_files()
    cpu = cpu_count()
    ok = run.worker()
    print("[+] aes decryption start.")
    while True:
        try:
            with Pool(processes=cpu) as pool:
                pool.apply_async(run.test(next(ok)))
        except Exception as e:
            error = repr(e)
            if error == "StopIteration()":
                break
            else:
                print(error)
                continue
    print("[+] aes decryption end.")
    print("__END DECRYPTION__")
if __name__ == '__main__':
    freeze_support()
    main()
