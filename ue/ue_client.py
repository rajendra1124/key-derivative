# ue/ue_client.py
import logging
import requests
import time
from shared.constants import K, SNN, SQN, AK, SUPI, ABBA, NAS_COUNT
from shared.constants import NAS_ENC_ALG_ID, NAS_INT_ALG_ID, RRC_ENC_ALG_ID, RRC_INT_ALG_ID, UP_ENC_ALG_ID, UP_INT_ALG_ID
from shared.constants import FC_K_AUSF, FC_K_SEAF, FC_K_AMF, FC_K_GNB, FC_NAS_ENC, FC_NAS_INT, FC_RRC_ENC, FC_RRC_INT, FC_UP_ENC, FC_UP_INT
from shared.kdf import kdf

logging.basicConfig(level=logging.INFO, format='%(asctime)s - UE - %(message)s')

AMF_URL = "http://amf:5003/start-authentication"

def run_ue_simulation():
    logging.info("--- UE SIMULATION START ---")
    
    # Perform the full key derivation on the UE side
    logging.info("1. Deriving K_AUSF...")
    sqn_xor_ak = bytes(a ^ b for a, b in zip(SQN, AK))
    k_ausf = kdf(K, FC_K_AUSF, SNN, len(SNN).to_bytes(2, 'big'), sqn_xor_ak, len(sqn_xor_ak).to_bytes(2, 'big'))
    logging.info(f"   => UE K_AUSF: {k_ausf.hex()}")
    
    logging.info("2. Deriving K_SEAF...")
    k_seaf = kdf(k_ausf, FC_K_SEAF, SNN, len(SNN).to_bytes(2, 'big'))
    logging.info(f"   => UE K_SEAF: {k_seaf.hex()}")

    logging.info("3. Deriving K_AMF...")
    k_amf = kdf(k_seaf, FC_K_AMF, SUPI, len(SUPI).to_bytes(2, 'big'), ABBA, len(ABBA).to_bytes(2, 'big'))
    logging.info(f"   => UE K_AMF: {k_amf.hex()}")

    logging.info("4. Deriving NAS keys...")
    k_nas_enc = kdf(k_amf, FC_NAS_ENC, NAS_ENC_ALG_ID, len(NAS_ENC_ALG_ID).to_bytes(2, 'big'))
    k_nas_int = kdf(k_amf, FC_NAS_INT, NAS_INT_ALG_ID, len(NAS_INT_ALG_ID).to_bytes(2, 'big'))
    logging.info(f"   => UE K_NAS_ENC: {k_nas_enc.hex()[-32:]}")
    logging.info(f"   => UE K_NAS_INT: {k_nas_int.hex()[-32:]}")

    logging.info("5. Deriving K_gNB...")
    k_gnb = kdf(k_amf, FC_K_GNB, NAS_COUNT, len(NAS_COUNT).to_bytes(2, 'big'))
    logging.info(f"   => UE K_gNB: {k_gnb.hex()}")
    
    logging.info("6. Deriving RRC and UP keys...")
    k_rrc_enc = kdf(k_gnb, FC_RRC_ENC, RRC_ENC_ALG_ID, len(RRC_ENC_ALG_ID).to_bytes(2, 'big'))
    k_rrc_int = kdf(k_gnb, FC_RRC_INT, RRC_INT_ALG_ID, len(RRC_INT_ALG_ID).to_bytes(2, 'big'))
    k_up_enc = kdf(k_gnb, FC_UP_ENC, UP_ENC_ALG_ID, len(UP_ENC_ALG_ID).to_bytes(2, 'big'))
    k_up_int = kdf(k_gnb, FC_UP_INT, UP_INT_ALG_ID, len(UP_INT_ALG_ID).to_bytes(2, 'big'))
    logging.info(f"   => UE K_RRC_ENC: {k_rrc_enc.hex()[-32:]}")
    logging.info(f"   => UE K_RRC_INT: {k_rrc_int.hex()[-32:]}")
    logging.info(f"   => UE K_UP_ENC: {k_up_enc.hex()[-32:]}")
    logging.info(f"   => UE K_UP_INT: {k_up_int.hex()[-32:]}")
    
    logging.info("--- UE SIMULATION COMPLETE ---")
    logging.info("Now, compare the UE's derived keys with the logs from the network function containers.")


if __name__ == '__main__':
    # Wait for network functions to be ready
    time.sleep(5) 
    
    logging.info("Initiating connection to the network...")
    try:
        response = requests.post(AMF_URL)
        if response.status_code == 200:
            logging.info("Network authentication flow triggered successfully.")
            run_ue_simulation()
        else:
            logging.error(f"Failed to start authentication. Status: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection to AMF failed: {e}")
