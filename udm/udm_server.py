# udm/udm_server.py
import logging
from flask import Flask, jsonify
from shared.constants import K, SNN, SQN, AK, FC_K_AUSF, FC_K_SEAF
from shared.kdf import kdf

logging.basicConfig(level=logging.INFO, format='%(asctime)s - UDM - %(message)s')
app = Flask(__name__)

@app.route('/get-auth-data', methods=['POST'])
def get_auth_data():
    logging.info("Received request for authentication data.")

    # 1. Derive K_AUSF from the root key K
    sqn_xor_ak = bytes(a ^ b for a, b in zip(SQN, AK))
    k_ausf = kdf(K, FC_K_AUSF, SNN, len(SNN).to_bytes(2, 'big'), sqn_xor_ak, len(sqn_xor_ak).to_bytes(2, 'big'))
    logging.info(f"Derived K_AUSF: {k_ausf.hex()}")

    # 2. Derive K_SEAF from K_AUSF
    k_seaf = kdf(k_ausf, FC_K_SEAF, SNN, len(SNN).to_bytes(2, 'big'))
    logging.info(f"Derived K_SEAF: {k_seaf.hex()}")

    # Package the data to be sent to AUSF
    auth_data = {
        "k_ausf_hex": k_ausf.hex(),
        "k_seaf_hex": k_seaf.hex(),
        "sqn_xor_ak_hex": sqn_xor_ak.hex()
    }
    
    logging.info("Sending K_AUSF and K_SEAF to AUSF.")
    return jsonify(auth_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
