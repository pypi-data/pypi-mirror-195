from http_client.factory import HTTPClientFactory


class ReachClient:
    def __init__(self, url, client_type):
        self.url = url
        self.client_type = client_type
        self.client = HTTPClientFactory().build(client_type)

    def send_message(self, message):
        self.client.post(self.url + "/messages", message)

