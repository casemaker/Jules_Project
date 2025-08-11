from ib_insync import IB
import nest_asyncio

class IBKRClient:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        nest_asyncio.apply()

    def connect(self):
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            print("Connected to IBKR.")
        except Exception as e:
            print(f"Error connecting to IBKR: {e}")

    def disconnect(self):
        self.ib.disconnect()
        print("Disconnected from IBKR.")

if __name__ == '__main__':
    # This is an example of how to use the client.
    # It will not run in the sandbox because it requires a running TWS or IB Gateway instance.
    client = IBKRClient()
    client.connect()

    # Keep the connection alive for a short time to demonstrate it works
    if client.ib.isConnected():
        print("IBKR client is connected.")
        client.ib.sleep(5) # Keep connection open for 5 seconds
        client.disconnect()
    else:
        print("IBKR client failed to connect.")
