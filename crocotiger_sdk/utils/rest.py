import requests

from typing import Any, Dict, Optional


class RestClient:
    def __init__(self, base_path: str):
        self.base_path = base_path.rstrip("/")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _handle_response(self, response: requests.Response) -> Any:
        if 200 <= response.status_code < 300:
            json_response = response.json()
            return json_response["data"] if "data" in json_response else json_response
        try:
            error_data = response.json()
            # TODO: Consider using ApiErrorResponse model here
            raise Exception(f"API Error {response.status_code}: {error_data}")
        except ValueError:
            response.raise_for_status()

    def _prepare_url(self, endpoint: str) -> str:
        return f"{self.base_path}/{endpoint.lstrip('/')}"

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = self._prepare_url(endpoint)
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def get_file(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> bytes:
        url = self._prepare_url(endpoint)
        response = requests.get(url, headers=self.headers, params=params)
        return response.content

    def post(self, endpoint: str, data: Dict[str, Any]) -> Any:
        url = self._prepare_url(endpoint)
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def put(self, endpoint: str, data: Dict[str, Any]) -> Any:
        url = self._prepare_url(endpoint)
        response = requests.put(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def delete(self, endpoint: str) -> Any:
        url = self._prepare_url(endpoint)
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)
