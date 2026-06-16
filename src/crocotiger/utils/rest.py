import requests

from typing import Any, Dict, Optional

from crocotiger.models.error import ApiErrorResponse


class RestClient:
    def __init__(self, base_path: str):
        self.base_path = base_path.rstrip("/")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def add_authorization_token(self, token: str) -> None:
        self.headers["Authorization"] = f"Bearer {token}"

    def remove_authorization_token(self) -> None:
        self.headers.pop("Authorization", None)

    def _handle_response(
        self, response: requests.Response, *, extract_data: bool = True
    ) -> Any:
        if 200 <= response.status_code < 300:
            json_response = response.json()

            if json_response is None:
                return None
            return (
                json_response["data"]
                if extract_data and "data" in json_response
                else json_response
            )
        try:
            raise ApiErrorResponse.from_response(response)
        except ValueError:
            response.raise_for_status()

    def _prepare_url(self, endpoint: str) -> str:
        return f"{self.base_path}/{endpoint.lstrip('/')}"

    def get_paged(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = self._prepare_url(endpoint)
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response, extract_data=False)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = self._prepare_url(endpoint)
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def get_file(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> bytes:
        url = self._prepare_url(endpoint)
        response = requests.get(url, headers=self.headers, params=params)
        if not (200 <= response.status_code < 300):
            try:
                raise ApiErrorResponse.from_response(response)
            except ValueError:
                response.raise_for_status()
        return response.content

    def post(self, endpoint: str, data: Dict[str, Any]) -> Any:
        url = self._prepare_url(endpoint)
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def upload_file(
        self, endpoint: str, file_path: str, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        url = self._prepare_url(endpoint)
        # Multipart upload: keep auth/accept but drop our default
        # "Content-Type: application/json" so requests sets the
        # "multipart/form-data; boundary=..." header itself. Sending the JSON
        # content type suppresses the boundary and the server can't parse the file.
        headers = {k: v for k, v in self.headers.items() if k.lower() != "content-type"}
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, headers=headers, files=files, params=params)
        return self._handle_response(response)

    def put(self, endpoint: str, data: Dict[str, Any]) -> Any:
        url = self._prepare_url(endpoint)
        response = requests.put(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def delete(self, endpoint: str) -> Any:
        url = self._prepare_url(endpoint)
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)
