import websocket
import json
import random
import time
import threading

# Replace 'your_server_address' with your actual server address
socket_url = 'ws://127.0.0.1:8000/ws/vehicle_location/'

def on_open(ws):
    def run(*args):
        while True:
            print("WebSocket connected")
            latitude = random.uniform(-37.7749, 37.7759)
            longitude = random.uniform(-122.4194, 122.4184)
            # Your JSON payload
            payload = {
                "driver_id": 3,
                "lat": latitude,
                "long": longitude,
                "user_id": 8  # Add this line to include user_id
            }
            # Sending the JSON payload as a string
            ws.send(json.dumps(payload))
            time.sleep(5)  # Send data every 5 seconds

    # Start a new thread for the run function
    thread = threading.Thread(target=run)
    thread.start()

def on_message(ws, message):
    data = json.loads(message)
    print(f"Received data: {data}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket disconnected")

# Create a WebSocket instance
ws = websocket.WebSocketApp(socket_url, on_open=on_open, on_message=on_message, on_close=on_close)

# Run the WebSocket connection
ws.run_forever()