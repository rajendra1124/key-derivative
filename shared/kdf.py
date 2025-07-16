# shared/kdf.py
import hmac
from hashlib import sha256

def kdf(key: bytes, fc: bytes, p0: bytes, l0: bytes, p1: bytes = b'', l1: bytes = b''):
    """
    Implements the 3GPP KDF as specified in TS 33.501, Annex A.
    S = FC || P0 || L0 || P1 || L1 || ...
    Output = HMAC-SHA-256(Key, S)
    """
    # L0 and L1 are the lengths of P0 and P1, respectively, encoded as 2 bytes.
    l0_bytes = len(p0).to_bytes(2, 'big')
    
    s_list = [fc, p0, l0_bytes]
    
    if p1:
        l1_bytes = len(p1).to_bytes(2, 'big')
        s_list.extend([p1, l1_bytes])
        
    S = b''.join(s_list)
    
    return hmac.new(key, S, sha256).digest()
