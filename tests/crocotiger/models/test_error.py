from crocotiger.models.error import ApiErrorResponse


class TestAPIErrorResponse:
    def test_init(self) -> None:
        error = ApiErrorResponse(
            status="error",
            message="Not Found",
            code=404,
            details={"info": "The requested resource was not found."},
        )

        assert error.status == "error"
        assert error.message == "Not Found"
        assert error.code == 404
        assert error.details == {"info": "The requested resource was not found."}

    def test_str_and_repr(self) -> None:
        error = ApiErrorResponse(status="error", message="Unauthorized", code=401)
        print_str = "<ApiErrorResponse 401: Unauthorized>"
        rep_str = (
            "ApiErrorResponse("
            "status='error', message='Unauthorized', code=401, details=None)"
        )

        assert str(error) == print_str
        assert repr(error) == rep_str

    def test_exception_handling(self) -> None:
        try:
            raise ApiErrorResponse(
                status="error", message="Internal Server Error", code=500
            )
        except ApiErrorResponse as e:
            assert e.status == "error"
            assert e.message == "Internal Server Error"
            assert e.code == 500

    def test_error_type_valid_code(self) -> None:
        """Test that a standard code (200) returns the correct phrase ('OK')."""
        # Arrange
        error = ApiErrorResponse(status="OK", message="Internal Server Error", code=200)
        # Act
        phrase = error.error_type
        # Assert
        assert phrase == "OK"

    def test_error_type_unknown_code(self) -> None:
        """Test that an invalid HTTP code returns 'Unknown Error'."""
        # Arrange
        error = ApiErrorResponse(status="error", message="Invalid Error", code=999)

        error.code = 999  # 999 is not a valid HTTP status
        # Act
        error_type = error.error_type

        # Assert
        assert error_type == "Unknown Error"
