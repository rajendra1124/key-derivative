# gnb/gnb_server.py
import logging
from flask import Flask, jsonify, request
from shared.constants import RRC_ENC_ALG_ID, RRC_INT_ALG_ID, UP_ENC_ALG_ID, UP_INT_ALG_ID
from shared.constants import FC_RRC_ENC, FC_RRC_INT, FC_UP_ENC, FC_UP_INT
from shared.kdf import kdf

logging.basicConfig(level=logging.INFO, format='%(asctime)s - gNB - %(message)s')
app = Flask(__name__)

@app.route('/setup-security', methods=['POST'])
def setup_security():
    data = request.json
    k_gnb = bytes.fromhex(data['k_gnb_hex'])
    logging.info(f"Received K_gNB from AMF: {k_gnb.hex()}")

    # Derive RRC and UP keys from K_gNB
    k_rrc_enc = kdf(k_gnb, FC_RRC_ENC, RRC_ENC_ALG_ID, len(RRC_ENC_ALG_ID).to_bytes(2, 'big'))
    k_rrc_int = kdf(k_gnb, FC_RRC_INT, RRC_INT_ALG_ID, len(RRC_INT_ALG_ID).to_bytes(2, 'big'))
    k_up_enc = kdf(k_gnb, FC_UP_ENC, UP_ENC_ALG_ID, len(UP_ENC_ALG_ID).to_bytes(2, 'big'))
    k_up_int = kdf(k_gnb, FC_UP_INT, UP_INT_ALG_ID, len(UP_INT_ALG_ID).to_bytes(2, 'big'))
    
    logging.info(f"Derived K_RRC_ENC: {k_rrc_enc.hex()[-32:]}")
    logging.info(f"Derived K_RRC_INT: {k_rrc_int.hex()[-32:]}")
    logging.info(f"Derived K_UP_ENC: {k_up_enc.hex()[-32:]}")
    logging.info(f"Derived K_UP_INT: {k_up_int.hex()[-32:]}")
    
    return jsonify({"status": "security_context_established"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
