from Crypto.Cipher import AES,ARC4
import datetime
from django.utils.encoding import smart_str, smart_unicode
import base64

"""
    Performs basic encryption services using the ARC4 algorithm.
    
    @author: bill shelton    
"""

def encrypt(key, data):
    """
    Encrypts data AND encodes it as a base64 string. The base64 encoding makes it easier to pass around in web apps.
    
    @param: key, The key used to encrypt the 2nd param, data
    @param: data, The data to encrypt
    """
    crypto = ARC4.new(key)
    cipher = crypto.encrypt(data)
    return base64.encodestring(cipher)

def decrypt(key,data):
    """
    Decrypts data.
    
    @param: key, The key used to decrypt the 2nd param, data
    @param: data, The base64 data to decrypt
    
    @requires: data is base64 encoded.
    """
    uncrypto = ARC4.new(key)
    cipher = base64.decodestring(data)
    return  uncrypto.decrypt(cipher)
