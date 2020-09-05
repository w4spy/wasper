# wasper
folder encryption script using aes_128_cbc fernet lib python3

generate.py generates RSA 4096 key pair to handle the protection of the AES key
encrypt.py generates AES-128-cbc key then it encrypt it with rsa public.pem and log it to your disk ,yet
it will encrypt all files in the given dirctory 
decrypt.py loads private.pem and decrypt the encrypted aes key and log it to disk ,
it wil decrypt all files in the given folder and clear all unnecessary  files 

# usage

```$ python3 generate.py```

copy public.pem with the encrypt.py

```$ encrypt.py folder```

copy private.pem to decrypt

```$ decrypt.py folder```

