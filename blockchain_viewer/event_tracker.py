from flask import Flask, render_template, request, jsonify
import time
import json
import datetime
#import app


def get_temperature():
    try:
        with open("/sys/bus/w1/devices/28-d6e37d0a6461/w1_slave") as file:
            content = file.read()
            pos = content.rfind("t=") + 2
            temperature_string = content[pos:]
            sensor_temp = int(float(temperature_string) / 1000)
            print(f"🌡 Current Temperature: {sensor_temp}°C")
            return sensor_temp
    except FileNotFoundError:
        print("❌ Sensor file not found.")
        return None

def start_tracking():
    while True:
        temperature = get_temperature()
        if temperature is not None and temperature > 30:
            print("⚠️ Temperature exceeds 30°C! Uploading to blockchain...")
            #app.send_transaction(temperature)
            return temperature
        else:
            print("ℹ️ Temperature is normal. No action required.")
        time.sleep(30) 
        
         
