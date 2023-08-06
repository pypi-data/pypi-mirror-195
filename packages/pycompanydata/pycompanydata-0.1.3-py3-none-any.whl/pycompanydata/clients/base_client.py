import base64


def encode_key_to_base_64(key: str) -> str:
    key_bytes = key.encode("ascii")
    base64_key = base64.b64encode(key_bytes)
    base64_key_string = base64_key.decode("ascii")
    return base64_key_string


class BaseClient:
    def __init__(
        self,
        key: str,
        env: str = "prod",
    ) -> None:
        """initialization dunder method

        :param key: Codat portal API Key or auth header value
            (in the format "Basic {encoded API key}")
        :type key: str
        :param env: name of the Codat environment used, defaults to "prod"
        :type env: str, optional
        """
        if key.startswith("Basic "):
            # Already encoded, strip off 'Basic ' and use
            self.key = key[6:]
        else:
            # Need to encode to auth header
            self.key = encode_key_to_base_64(key)

        self.env = env
