import websocket
import json
import random
# Replace 'your_server_address' with your actual server address
socket_url = 'ws://127.0.0.1:8000/ws/vehicle_location/'

def on_open(ws):
    print("WebSocket connected")
    latitude = random.uniform(-37.7749, 37.7759)
    longitude = random.uniform(-122.4194, 122.4184)
    # Your JSON payload
    payload = {
        "driver_id": "2",
        "lat": latitude,
        "long": longitude
    }

    # Sending the JSON payload as a string
    ws.send(json.dumps(payload))

def on_message(ws, message):
    data = json.loads(message)
    print(f"Received data: {data}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket disconnected")

# Create a WebSocket instance
ws = websocket.WebSocketApp(socket_url, on_open=on_open, on_message=on_message, on_close=on_close)

# Run the WebSocket connection
ws.run_forever()
