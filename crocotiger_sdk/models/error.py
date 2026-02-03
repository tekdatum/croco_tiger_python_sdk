from typing import Any, Dict, Optional
import requests
from http import HTTPStatus


class ApiErrorResponse(Exception):
    def __init__(
        self,
        status: str,
        message: str,
        code: int,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status = status
        self.message = message
        self.code = code
        self.details = details
        super().__init__(f"[{self.code}] {self.message}")

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.code}: {self.message}>"

    def __repr__(self) -> str:
        return (
            f"ApiErrorResponse(status='{self.status}', "
            f"message='{self.message}', code={self.code}, "
            f"details={self.details})"
        )

    @property
    def error_type(self) -> str:
        try:
            return HTTPStatus(self.code).phrase
        except ValueError:
            return "Unknown Error"

    @classmethod
    def from_response(cls, response: requests.Response) -> "ApiErrorResponse":
        try:
            payload = response.json()
            if isinstance(payload, dict):
                if "detail" in payload and isinstance(payload["detail"], dict):
                    payload = payload["detail"]
        except ValueError:
            payload = {"message": response.text or "No content"}

        message = (
            payload.get("message")
            or (
                payload.get("detail")
                if isinstance(payload.get("detail"), str)
                else None
            )
            or payload.get("code")
            or response.reason
        )

        return cls(
            status=payload.get("status", "error"),
            message=str(message),
            code=response.status_code,
            details=payload if isinstance(payload, dict) else {"raw": payload},
        )
