from flask import Flask, render_template, request, jsonify
import requests
from web3 import Web3
import datetime

# Flask App
app = Flask(__name__)


# Etherscan API Constants
ETHERSCAN_API_KEY = "DMR9TJXC5GWGQWNMQKJMRZ1ZCZPHPU86P4"  # Replace with your API Key
SEPOLIA_API_URL = "https://api-sepolia.etherscan.io/api"

# Test Var 
# wallet_address = "0x116446b40F59c09D29186d600114d614ffE39691"

# Function to fetch transactions from a wallet
def fetch_wallet_transactions(wallet_address):
    url = f"{SEPOLIA_API_URL}?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}"

    response = requests.get(url)

    try:
        data = response.json()
    except ValueError:
        return {"error": "Invalid JSON response"}

    if "result" in data and isinstance(data["result"], list):
        return data["result"]
    else:
        return {"error": "No transactions found"}

# Function to decode transaction data (Machine ID + Temperature)
def decode_transaction_data(hex_data):
    if hex_data.startswith("0x"):
        hex_data = hex_data[2:]  # Remove "0x" prefix

    if len(hex_data) < 6:
        return None, None

    machine_id = int(hex_data[:4], 16)  # First 4 characters = Machine ID
    temperature = int(hex_data[4:], 16)  # Remaining 2 characters = Temperature

    return machine_id, temperature

# Route for the website
@app.route("/index")

def index():
    return render_template("index.html")
    
@app.route("/temperatur", methods= ["GET", "POST"])
# get temperature
def get_temperature():
    if request.method == "POST":
        file =  open('~/sys/bus/w1/devices/28-d6e37d0a6461/w1_slave')
        content = file.read()
        file.close()
        pos = content.rfind('t=') + 2
        temperature_string = content[pos:]
        sensor_temp = float(temperature_string) / 1000
        return sensor_temp
    return render_template ("index.html")
    

# API Route to get transactions
@app.route("/get_transactions", methods=["POST"])
def get_transactions():
    wallet_address = request.json.get("wallet_address")
    transactions = fetch_wallet_transactions(wallet_address)

    if "error" in transactions:
        return jsonify({"error": transactions["error"]})

    result = []

    for tx in transactions:
        tx_hash = tx["hash"]
        timestamp = int(tx["timeStamp"])
        readable_time = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        hex_data = tx.get("input", "")

        if hex_data and hex_data != "0x":
            machine_id, temperature = decode_transaction_data(hex_data)
            if machine_id and temperature:
                result.append({
                    "tx_hash": tx_hash,
                    "timestamp": readable_time,
                    "machine_id": machine_id,
                    "temperature": temperature,
                    "etherscan_link": f"https://sepolia.etherscan.io/tx/{tx_hash}"
                })

    return jsonify(result)

# Run Flask App
# if __name__ == "__main__":
    # app.run(debug=True)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")
