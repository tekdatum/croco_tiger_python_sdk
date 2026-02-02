from models.error import ApiErrorResponse


class TestAPIErrorResponse():

    def test_to_dict(self) -> None:
        error = ApiErrorResponse(
            status="error",
            message="Not Found",
            code=404,
            details={"info": "The requested resource was not found."}
        )

        expected_dict = {
            "status": "error",
            "message": "Not Found",
            "code": 404,
            "error_type": "Not Found",
            "details": {"info": "The requested resource was not found."}
        }

        assert error.to_dict() == expected_dict
    
    def test_str_and_repr(self) -> None:
        error = ApiErrorResponse(
            status="error",
            message="Unauthorized",
            code=401
        )

        assert str(error) == "<ApiErrorResponse 401: Unauthorized>"
        assert repr(error) == "ApiErrorResponse(status='error', message='Unauthorized', code=401, details=None)"
    
    def test_exception_handling(self) -> None:
        try:
            raise ApiErrorResponse(
                status="error",
                message="Internal Server Error",
                code=500
            )
        except ApiErrorResponse as e:
            assert e.status == "error"
            assert e.message == "Internal Server Error"
            assert e.code == 500