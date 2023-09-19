import socketio

sio = socketio.Client()


@sio.on("market_trades")
def on_market_trades(data):
    print("Received event:", data)


# Connect to the server
sio.connect("http://52.63.8.207:5001")  # Adjust the hostname and port as needed

try:
    sio.wait()
except KeyboardInterrupt:
    print("Disconnecting...")
    sio.disconnect()
