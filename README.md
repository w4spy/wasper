# wasper
fast folder encryption script using aes_128_cbc in python3
using pycryptodome lib encrypting 1024 bit at a time using generators for fast stream handling
the script count how many processors  you have and use that number in a multiprocessing encryption
cross platform work on windows also freez_support library  (didnt tried it on mac)

generate.py generates RSA 4096 key pair to handle the protection of the AES key

encrypt.py generates randome  AES-128-cbc key then encrypt it with rsa public.pem
it will encrypt all files in the given dirctory/directories

decrypt.py loads private.pem and decrypt the encrypted aes key
it wil decrypt all files in the given directory/directories 
# usage

```$ python3 generate.py```

generates RSA key paire 

```$ encrypt.py -h```

handeles rsa key encryption and aes files encryption

```$ decrypt.py -h```

handeles rsa key decryption and aes files decryption

### coffee
dogecoin:DBUgLF7hziKSjjEjz8cqayXWfFiwv8fNhY
