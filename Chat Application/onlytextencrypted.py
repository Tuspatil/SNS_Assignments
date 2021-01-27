from Crypto.Cipher import DES3
from Crypto import Random
import hashlib 
key = '2019201001      '
iv = Random.new().read(DES3.block_size) 
def padding(msg):
  while(len(msg)%8!=0):
    # print("Looping around...")
    msg+=" "
  return msg



def encrypt_text(msg):
  # print(iv)
  cipher_encrypt = DES3.new(key, DES3.MODE_OFB, iv)
  msg=padding(msg)
  encrypted_text = cipher_encrypt.encrypt(msg)
  return encrypted_text


def decrypt_text(msg):
  cipher_decrypt = DES3.new(key, DES3.MODE_OFB, iv) 
  dec_text=cipher_decrypt.decrypt(msg)
  return dec_text


# ----------------Toy Code to check-----------

# msg="Kuch bhi Kuch bhi"
# print(msg)
# ec=encrypt_text(msg)
# print(ec)
# dc=decrypt_text(ec)
# print(dc)