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
    arr = list(range(256))
    counter = 0

    for i in range(256):
        counter = (counter + arr[i] + ord(key[i % len(key)])) % 256
        arr[i], arr[counter] = arr[counter], arr[i]

    i = 0
    counter = 0
    decrypted = []

    for j in range(len(inp)):
        i = (i + 1) % 256
        counter = (counter + arr[i]) % 256
        arr[i], arr[counter] = arr[counter], arr[i]
        k = arr[(arr[i] + arr[counter]) % 256]
        decrypted.append(chr(ord(inp[j]) ^ k))

    return ''.join(decrypted)

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

def reverse(a):
    return a[::-1]

def subst(inp):
    b64_encoded = base64.b64encode(inp.encode('latin-1')).decode('latin-1')
    url_safe_b64 = b64_encoded.replace('/', '_').replace('+', '-')
    return url_safe_b64

def subst_(inp):
    inp = inp.replace('_', '/').replace('-', '+')
    i = base64.b64decode(inp)
    i = i.decode('latin-1')
    return i

def mapp(a, b, c):
    e = {b[i]: c[i] if i < len(c) else '' for i in range(len(b))}
    return ''.join(e.get(char, char) for char in a)