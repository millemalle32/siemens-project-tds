from web3 import Web3

# Connect to Sepolia testnet
sepolia_url = "https://sepolia.infura.io/v3/835d10ec0e834928b10658f71faffe74"
web3 = Web3(Web3.HTTPProvider(sepolia_url))

# Check connection
if web3.is_connected():
    print("✅ Connected to Sepolia Testnet!")
else:
    print("❌ Connection failed!")
    exit()


sender_address = "0x116446b40F59c09D29186d600114d614ffE39691" 
private_key = "366a4abde5b129175ccd4bfbdfd3e36853c9192e3cf595d94d70d64c8400f7bf" 
receiver_address = "0x8152f15133648479166B17E3C75Ad1856E2C2935"  


machine_id = 12134
#temperature = 63

# Get the temperature
def get_temperature():
    file = open("/sys/bus/w1/devices/28-d6e37d0a6461/w1_slave")
    content = file.read()
    file.close()
    pos = content.rfind("t=") + 2
    temperature_string = content[pos:]
    sensor_temp = int(float(temperature_string) / 1000)
    print(sensor_temp)
    return sensor_temp

# Encode machine data into transaction data (Hex format)
temperature = get_temperature()
data_payload = f"{machine_id:04x}{temperature:02x}"
hex_data = "0x" + data_payload  # Convert to Ethereum data format

# Get nonce (transaction count for sender)
nonce = web3.eth.get_transaction_count(sender_address)

# Define transaction
tx = {
    "nonce": nonce,
    "to": receiver_address,  # You can send it to your own address
    "value": web3.to_wei(0, "ether"),  # Sending 0.01 Sepolia ETH
    "gas": 50000,
    "gasPrice": web3.to_wei("20", "gwei"),
    "chainId": 11155111,  # Sepolia Chain ID
    "data": hex_data  # Custom machine data in transaction payload
}

# Sign the transaction
signed_tx = web3.eth.account.sign_transaction(tx, private_key)

# Send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

# Print transaction hash
print(f"✅ Transaction sent! Hash: {web3.to_hex(tx_hash)}")

# Verify on Etherscan
print(f"Check transaction on Sepolia Explorer: https://sepolia.etherscan.io/tx/{web3.to_hex(tx_hash)}")
