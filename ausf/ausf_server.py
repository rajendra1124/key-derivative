# ausf/ausf_server.py
import logging
import requests
from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO, format='%(asctime)s - AUSF - %(message)s')
app = Flask(__name__)

UDM_URL = "http://udm:5001/get-auth-data"

@app.route('/authenticate', methods=['POST'])
def authenticate():
    logging.info("Received authentication request from AMF.")
    
    # 1. Request authentication data from UDM
    logging.info("Requesting auth data from UDM...")
    response = requests.post(UDM_URL)
    auth_data = response.json()
    
    k_ausf_hex = auth_data['k_ausf_hex']
    k_seaf_hex = auth_data['k_seaf_hex']
    
    logging.info(f"Received K_AUSF from UDM: {k_ausf_hex}")
    logging.info(f"Received K_SEAF from UDM: {k_seaf_hex}")
    
    # 2. Forward K_SEAF to AMF
    logging.info("Forwarding K_SEAF to AMF.")
    return jsonify({"k_seaf_hex": k_seaf_hex})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
