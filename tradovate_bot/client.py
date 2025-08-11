import asyncio
import websockets
import json

class TradovateClient:
    def __init__(self, environment='demo', username=None, password=None, app_id='Sample App', app_version='1.0', cid=1, device_id='Your-Device-ID'):
        self.base_url = f"wss://{environment}.tradovateapi.com/v1/websocket"
        self.username = username
        self.password = password
        self.app_id = app_id
        self.app_version = app_version
        self.cid = cid
        self.device_id = device_id
        self.access_token = None
        self.websocket = None

    async def authenticate(self):
        auth_request = {
            "url": "auth/accesstokenrequest",
            "body": {
                "name": self.username,
                "password": self.password,
                "appId": self.app_id,
                "appVersion": self.app_version,
                "cid": self.cid,
                "deviceId": self.device_id,
            }
        }
        await self.send(json.dumps(auth_request))
        response = await self.receive()
        response_data = json.loads(response)

        if 'd' in response_data and 'accessToken' in response_data['d']:
            self.access_token = response_data['d']['accessToken']
            print("Successfully authenticated with Tradovate.")
        else:
            print(f"Error authenticating with Tradovate: {response_data.get('d', {}).get('message', 'No error message')}")
            raise Exception("Authentication failed")

    async def send(self, message):
        if self.websocket:
            await self.websocket.send(message)

    async def receive(self):
        if self.websocket:
            return await self.websocket.recv()

    async def run(self, message_handler):
        async with websockets.connect(self.base_url) as websocket:
            self.websocket = websocket
            print("Connected to Tradovate WebSocket.")
            await self.authenticate()

            if self.access_token:
                # Main message loop
                while True:
                    try:
                        message = await self.receive()
                        await message_handler(message)
                    except websockets.exceptions.ConnectionClosed:
                        print("Connection with Tradovate closed.")
                        break

async def main():
    # This is an example of how to use the client.
    # It will not run in the sandbox because it requires a valid username and password.

    async def dummy_handler(message):
        print(f"Received message: {message}")

    # IMPORTANT: Replace with your actual credentials and device ID before running
    # DO NOT COMMIT YOUR CREDENTIALS TO A PUBLIC REPOSITORY
    username = "your_username"
    password = "your_password"
    device_id = "your_unique_device_id"

    client = TradovateClient(username=username, password=password, device_id=device_id)

    # To run this example, you would need to provide valid credentials.
    # try:
    #     await client.run(dummy_handler)
    # except Exception as e:
    #     print(f"An error occurred: {e}")


if __name__ == '__main__':
    # asyncio.run(main())
    pass
