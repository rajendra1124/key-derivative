# 5G Key Derivation Simulation

This project simulates the 5G key derivation process, starting from a root key `K` and deriving various security keys used in the 5G system. The simulation is implemented using a set of communicating services, each representing a 5G network function (NF).

## Project Description

The simulation demonstrates the key derivation hierarchy as specified in 3GPP TS 33.501. The process starts with a pre-shared root key `K` and involves the following network functions:

- **UDM (Unified Data Management):** Derives `K_AUSF` and `K_SEAF` from the root key `K`.
- **AUSF (Authentication Server Function):** Receives the keys from the UDM and forwards `K_SEAF` to the AMF.
- **AMF (Access and Mobility Management Function):** Derives `K_AMF`, NAS (Non-Access Stratum) keys, and `K_gNB` from `K_SEAF`.
- **gNB (Next Generation NodeB):** Derives RRC (Radio Resource Control) and UP (User Plane) keys from `K_gNB`.
- **UE (User Equipment):** Represents the user device, which independently performs the same key derivation process.

The simulation uses Python with Flask for the NF services and a `ue_client.py` script to initiate the process and verify the derived keys. The services communicate with each other via HTTP requests.

## How it Works

The simulation is orchestrated using `docker-compose`. Each network function runs in its own Docker container. The `ue` container initiates the authentication process by sending a request to the `amf`. This triggers a chain of requests between the NFs, leading to the derivation of all the necessary security keys.

The `ue` client also performs the complete key derivation on its own side. The output of the `ue` client can be compared with the logs from the other containers to verify that the keys are derived correctly on both the network and the UE side.

## Commands

### Start the project

To start the simulation, run the following command from the root of the project:

```bash
docker-compose up --build
```

This will build the Docker images and start all the services. The logs from each service will be displayed on the console.

### Stop the project

To stop the simulation and remove the containers, run the following command:

```bash
docker-compose down
```
