# shared/constants.py
import os

# --- Pre-provisioned secrets and identifiers ---
# Root Key (256-bit). Stored in UDM and USIM.
K = bytes.fromhex('c2d4e6f8a0b2d4e6f8a0b2d4e6f8a0b2c2d4e6f8a0b2d4e6f8a0b2d4e6f8')

# Subscription Permanent Identifier (SUPI)
SUPI = "imsi-208930000000001".encode('utf-8')

# Serving Network Name (SNN)
SNN = "5g:mnc093.mcc208.3gppnetwork.org".encode('utf-8')

# --- Authentication Vector Components (from UDM) ---
# Sequence Number (48-bit) and Anonymity Key (48-bit)
SQN = bytes.fromhex('000000000001')
AK = bytes.fromhex('000000000002')

# --- Other Parameters ---
# Anti-Bidding Down Between Architectures (for K_AMF derivation)
ABBA = b'\x00\x00'

# NAS Count (for K_gNB derivation)
NAS_COUNT = b'\x00\x00\x00\x01'

# --- Algorithm Identities ---
# For NAS Keys
NAS_ENC_ALG_ID = b'\x01' # e.g., NEA1
NAS_INT_ALG_ID = b'\x01' # e.g., NIA1

# For RRC/UP Keys
RRC_ENC_ALG_ID = b'\x01'
RRC_INT_ALG_ID = b'\x01'
UP_ENC_ALG_ID = b'\x01'
UP_INT_ALG_ID = b'\x01'

# --- KDF Function Codes (FC) from 3GPP TS 33.501 Annex A.4 ---
FC_K_AUSF = b'\x12'
FC_K_SEAF = b'\x13'
FC_K_AMF = b'\x14'
FC_K_GNB = b'\x15'
FC_NAS_ENC = b'\x03'
FC_NAS_INT = b'\x04'
FC_RRC_ENC = b'\x05'
FC_RRC_INT = b'\x06'
FC_UP_ENC = b'\x07'
FC_UP_INT = b'\x08'
