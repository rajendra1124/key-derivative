# amf/amf_server.py
import logging
import requests
from flask import Flask, jsonify
from shared.constants import SUPI, ABBA, NAS_COUNT, NAS_ENC_ALG_ID, NAS_INT_ALG_ID
from shared.constants import FC_K_AMF, FC_K_GNB, FC_NAS_ENC, FC_NAS_INT
from shared.kdf import kdf

logging.basicConfig(level=logging.INFO, format='%(asctime)s - AMF - %(message)s')
app = Flask(__name__)

AUSF_URL = "http://ausf:5002/authenticate"
GNB_URL = "http://gnb:5004/setup-security"

@app.route('/start-authentication', methods=['POST'])
def start_authentication():
    logging.info("Authentication process initiated by UE.")
    
    # 1. Contact AUSF to get K_SEAF
    logging.info("Requesting authentication from AUSF...")
    response = requests.post(AUSF_URL)
    data = response.json()
    k_seaf = bytes.fromhex(data['k_seaf_hex'])
    logging.info(f"Received K_SEAF from AUSF: {k_seaf.hex()}")

    # 2. Derive K_AMF from K_SEAF
    k_amf = kdf(k_seaf, FC_K_AMF, SUPI, len(SUPI).to_bytes(2, 'big'), ABBA, len(ABBA).to_bytes(2, 'big'))
    logging.info(f"Derived K_AMF: {k_amf.hex()}")
    
    # 3. Derive NAS keys from K_AMF
    k_nas_enc = kdf(k_amf, FC_NAS_ENC, NAS_ENC_ALG_ID, len(NAS_ENC_ALG_ID).to_bytes(2, 'big'))
    k_nas_int = kdf(k_amf, FC_NAS_INT, NAS_INT_ALG_ID, len(NAS_INT_ALG_ID).to_bytes(2, 'big'))
    logging.info(f"Derived K_NAS_ENC: {k_nas_enc.hex()[-32:]}") # 128 bits
    logging.info(f"Derived K_NAS_INT: {k_nas_int.hex()[-32:]}") # 128 bits

    # 4. Derive K_gNB from K_AMF
    k_gnb = kdf(k_amf, FC_K_GNB, NAS_COUNT, len(NAS_COUNT).to_bytes(2, 'big'))
    logging.info(f"Derived K_gNB: {k_gnb.hex()}")
    
    # 5. Send K_gNB to gNB to set up security
    logging.info("Sending K_gNB to gNB...")
    requests.post(GNB_URL, json={"k_gnb_hex": k_gnb.hex()})
    
    return jsonify({"status": "authentication_successful"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
