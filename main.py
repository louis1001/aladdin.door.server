from garage_connection import GarageConnection, DoorStatus
import json
import logging
from flask import Flask, send_file
from flask_cors import CORS

def get_credentials():
    with open('config.json', 'r') as f:
        json_data = json.load(f)

        return json_data['username'], json_data['password']

app = Flask(__name__, static_folder='assets')
CORS(app)

testing = True

@app.post("/close")
def close_door():
    user, password = get_credentials()
    conn = GarageConnection(user, password)

    if conn.can_close():
        print("Closing door")
        # conn.close_door()
    else:
        return "Already closed", 409

@app.post("/open")
def open_door():
    user, password = get_credentials()
    conn = GarageConnection(user, password)

    if conn.can_open():
        print("Opening door")
        if not testing: conn.open_door()
        return "Open"
    else:
        return "Already closed", 409

@app.post("/toggle")
def toggle_door():
    user, password = get_credentials()
    conn = GarageConnection(user, password)

    try:
        status = conn.get_status()
        if status == DoorStatus.closed:
            print("Opening door")
            if not testing: conn.open_door()

            return "Opening!"
        elif status == DoorStatus.open:
            print("Closing door")
            if not testing: conn.close_door()

            return "Closing!"
        else:
            return "Busy door", 409
    except:
        print("Error :(")
        return "Failure :(", 500

@app.route("/")
def home():
    return send_file('assets/home.html')

if __name__ == "__main__":
    from waitress import serve
    logger = logging.getLogger('waitress')

    logger.setLevel(logging.INFO)
    serve(app, host='0.0.0.0', port=8000)
