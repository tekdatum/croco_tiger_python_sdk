from crocotiger.utils.rest import RestClient


class AuthClient:
    def __init__(self, rest_client: RestClient):
        self._rest_client = rest_client
        self._endpoint = "/auth"

    def authenticate(self, passphrase: str) -> str:
        data = self._rest_client.post(
            f"{self._endpoint}/sign-in", data={"passphrase": passphrase}
        )
        return str(data["token"])

    def reset_passphrase(self, old_passphrase: str, new_passphrase: str) -> None:
        self._rest_client.post(
            f"{self._endpoint}/reset-passphrase",
            data={"old_passphrase": old_passphrase, "new_passphrase": new_passphrase},
        )
