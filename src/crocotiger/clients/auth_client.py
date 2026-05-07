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

    def reset_passphrase(self, reset_token: str, passphrase: str) -> None:
        self._rest_client.post(
            f"{self._endpoint}/reset",
            data={"reset_token": reset_token, "passphrase": passphrase},
        )

    def sign_out(self) -> None:
        self._rest_client.post(f"{self._endpoint}/sign-out", data={})
        self._rest_client.remove_authorization_token()
