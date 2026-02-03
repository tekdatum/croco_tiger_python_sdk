import pytest
from pydantic import ValidationError
from models.fence_validation import FenceValidation


class TestFenceValidation:
    def test_valid_fence_validation(self):
        """Test instantiation with valid data."""
        validation = FenceValidation(
            text="This is safe text.", valid=True, reason_code="safe", duration=0.123
        )

        assert validation.text == "This is safe text."
        assert validation.valid is True
        assert validation.reason_code == "safe"
        assert validation.duration == 0.123

    def test_missing_field(self):
        """Test instantiation fails when fields are missing."""
        # "reason_code" is missing
        with pytest.raises(ValidationError):
            FenceValidation(text="This is safe text.", valid=True, duration=0.123)

    def test_invalid_type(self):
        """Test instantiation fails with invalid types."""
        with pytest.raises(ValidationError):
            FenceValidation(
                text="This is safe text.",
                valid="not a boolean",  # Invalid type
                reason_code="safe",
                duration=0.123,
            )
