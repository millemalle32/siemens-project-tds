from web3 import Web3
import time
import json
import datetime
import event_tracker


    
sepolia_url = "https://sepolia.infura.io/v3/835d10ec0e834928b10658f71faffe74"
web3 = Web3(Web3.HTTPProvider(sepolia_url))

if web3.is_connected():
    print("✅ Connected to Sepolia Testnet!")
else:
    print("❌ Connection failed!")
    exit()

sender_address = "0x116446b40F59c09D29186d600114d614ffE39691"
private_key = "366a4abde5b129175ccd4bfbdfd3e36853c9192e3cf595d94d70d64c8400f7bf"
receiver_address = "0x8152f15133648479166B17E3C75Ad1856E2C2935"

MACHINE_ID = 959293458800
CHAIN_TYPE = "Maas"
PRODUCT_ID = "Pump MPHX-E"
ERROR_NAME = "Temperature Warning"
LOCATION = "Munich, Germany"

# This should be the json file path
log_file = "/siemens-project-tds/blockchain_viewer/json-table.json"




def send_transaction(temperature):
    print("Starting with transaction process")
    data_payload = f"{MACHINE_ID:012x}{temperature:02x}"
    hex_data = "0x" + data_payload
    nonce = web3.eth.get_transaction_count(sender_address)

    tx = {
        "nonce": nonce,
        "to": receiver_address,  
        "value": web3.to_wei(0, "ether"),  
        "gas": 50000,
        "gasPrice": web3.to_wei("20", "gwei"),
        "chainId": 11155111, 
        "data": hex_data  
    }

  
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    

    print(f"✅ Transaction sent! Hash: {web3.to_hex(tx_hash)}")
    log_transaction(temperature, web3.to_hex(tx_hash))

def log_transaction(temperature, tx_hash):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        "Machine ID": MACHINE_ID,
        "Chain Type": CHAIN_TYPE,
        "Product ID": PRODUCT_ID,
        "Error Name": ERROR_NAME,
        "Temperature": temperature,
        "Location": LOCATION,
        "Timestamp": timestamp,
        "Transaction ID": tx_hash
    }

    try:
        with open(log_file, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(log_entry)

    with open(log_file, "w") as file:
        json.dump(data, file, indent=4)

    print(f"✅ Transaction logged in {log_file}")

#starts tracking
high_temp = event_tracker.start_tracking()
if high_temp is not None:
    send_transaction(high_temp)

if __name__ == "__main__":
    app.run(host="0.0.0.0") 
