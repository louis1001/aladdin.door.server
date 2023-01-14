from garage_connection import GarageConnection, DoorStatus
import json
import logging
from flask import Flask

def get_credentials():
    with open('config.json', 'r') as f:
        json_data = json.load(f)

        return json_data['username'], json_data['password']

# def main():
#     username, password = get_credentials()
#     connection = GarageConnection(username, password)

#     if connection.can_close():
#         print("Can close the door")
#     else:
#         print("Cannot close door. It's closed already.")

# main()

app = Flask(__name__)

@app.post("/close")
def close_door():
    user, password = get_credentials()
    conn = GarageConnection(user, password)

    if conn.can_close():
        print("Closing door")
        # conn.close_door()
    else:
        return "Already closed"

@app.post("/open")
def open_door():
    user, password = get_credentials()
    conn = GarageConnection(user, password)

    if conn.can_open():
        print("Opening door")
        # conn.open_door()
    else:
        return "Already closed"

@app.post("/toggle")
def toggle_door():
    user, password = get_credentials()
    conn = GarageConnection(user, password)

    try:
        status = conn.get_status()
        if status == DoorStatus.closed:
            print("Opening door")
            conn.open_door()

            return "Opening!"
        elif status == DoorStatus.open:
            print("Closing door")
            conn.close_door()

            return "Closing!"
        else:
            return "Busy door"
    except:
        print("Error :(")
        return "Failure :(", 500

if __name__ == "__main__":
    from waitress import serve
    logger = logging.getLogger('waitress')

    logger.setLevel(logging.INFO)
    serve(app, host='0.0.0.0', port=8000)
