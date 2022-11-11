import requests

class WebAPI:
    
    def __init__(self):
        self._token = ""
        self._authorization = ""

    def get_token(self):
        pass

    def get_request(self, url, headers, body):
        return requests.get(url, headers=headers, data=body, verify=False)

    def post_request(self, url, headers, body):
        return requests.post(url, headers=headers, data=body, verify=False)

    def patch_request(self, url, headers, body):
        return requests.patch(url, headers=headers, data=body, verify=False)

    def delete_request(self, url, headers, body):
        return requests.delete(url, headers=headers, data=body, verify=False)