from Crypto.Cipher import DES,AES
from Crypto import Random
import json,base64

def manual_encrypt(key,text,type,iv):
    if type == "DES":
        cipher = DES.new(key,DES.MODE_CFB,iv)
        return cipher.encrypt(text)
    elif type == "AES":
        cipher = AES.new(key,AES.MODE_CFB ,iv)
        return cipher.encrypt(text)
    else:
        raise KeyError

def manual_decrypt(key,text,type,iv):
    if type == "DES":
        cipher = DES.new(key,DES.MODE_CFB,iv)
        return cipher.decrypt(text)
    elif type == "AES":
        cipher = AES.new(key,AES.MODE_CFB,iv)
        return cipher.decrypt(text)
    else:
        raise KeyError

def convert_json_for_encryption(json_value):#return AES hashable text
    return base64.encodestring(json.dumps(json_value))

def convert_decrypted_encode_to_json(encoded_value):#return json from decrypted AES string
    return json.loads(base64.decodestring(encoded_value))