import base64
from urllib.parse import quote, unquote

# Errors
class VidSrcError(Exception):
    '''Base Error'''
    pass

class RC4DecodeError(VidSrcError):
    '''Failed to decode RC4 data (current design choices == only ever ValueError)'''
    pass

class RC4DecodeError(VidSrcError):
    '''Failed to decode RC4 data (current design choices == only ever ValueError)'''
    pass

class NoSourcesFound(VidSrcError):
    '''Failed to find any media sources @ the provided source'''
    pass


# Encrypting & Decrypt
def rc4(key, inp):
    # Initialize the state array and variables
    arr = list(range(256))
    counter = 0
    i = 0
    decrypted = ''

    # Key Scheduling Algorithm (KSA)
    key_length = len(key)
    for i in range(256):
        counter = (counter + arr[i] + ord(key[i % key_length])) % 256
        arr[i], arr[counter] = arr[counter], arr[i]

    # Pseudo-Random Generation Algorithm (PRGA)
    i = 0
    counter = 0
    for char in inp:
        i = (i + 1) % 256
        counter = (counter + arr[i]) % 256
        arr[i], arr[counter] = arr[counter], arr[i]
        decrypted += chr(ord(char) ^ arr[(arr[i] + arr[counter]) % 256])

    return decrypted

def general_enc(key, inp):
        inp = quote(inp)
        e = rc4(key, inp)
        out = base64.b64encode(e.encode("latin-1")).decode()
        out = out.replace('/', '_').replace('+', '-')
        return out

def general_dec(key, inp):
    inp = inp.replace('_', '/').replace('-', '+')
    i = str(base64.b64decode(inp),"latin-1")
    e = rc4(key,i)
    e = unquote(e)
    return e