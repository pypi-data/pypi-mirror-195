import asyncio

from reach_python.http_client.factory import HTTPClientFactory


class SyncReachClient:
    def __init__(self, url):
        self.url = url
        self.client = HTTPClientFactory().build("sync")

    def send_message(self, message):
        response = self.client.post(self.url + "/messages", message)
        return response


class AsyncReachClient:
    def __init__(self, url):
        self.url = url
        self.client = HTTPClientFactory().build("async")

    async def send_messages(self, messages):
        async with self.client as http:
            await asyncio.gather(
                *[http.post(self.url + "/messages", message) for message in messages]
            )

    async def send_message(self, message):
        async with self.client as http:
            await http.post(self.url + "/messages", message)
