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