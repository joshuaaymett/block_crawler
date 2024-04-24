import json

JSON_RPC_VERSION = "2.0"


class QuickNodeRequest:
    """
    Base class for quick node requests. Current implementation only allows for Etherium calls;
    however, this class can be used as a parent to support expansion for other blockchains
    """


class QuickNodeEtheriumRequest(QuickNodeRequest):
    """
    Class for storing QuickNode etherium request headers, payload, etc.
    """

    def __init__(
        self, call_name: str, url: str, req_id: str = None, parameters: list = []
    ) -> None:
        self.url = url
        self.headers = {"Content-Type": "application/json"}
        self.payload = {
            "method": call_name,
            "params": parameters,
            "id": req_id,
            "jsonrpc": JSON_RPC_VERSION,
        }

    def get_request_params(self) -> dict:
        """
        Returns parameters for request as a dictionary
        """
        return {
            "url": self.url,
            "headers": self.headers,
            "data": json.dumps(self.payload),
            "timeout": 5,
        }
