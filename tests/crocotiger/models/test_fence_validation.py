import pytest
from pydantic import ValidationError
from crocotiger.models.fence_validation import FenceValidation


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

    def test_category_and_extra(self):
        """Test instantiation with the category and extra fields."""
        validation = FenceValidation(
            text="This is safe text.",
            valid=True,
            reason_code="within_allowed_threshold",
            category="IN_TOPIC",
            duration=0.123,
            extra={"accept_score": 0.9, "reject_score": 0.1},
        )

        assert validation.category == "IN_TOPIC"
        assert validation.extra["accept_score"] == 0.9

    def test_category_and_extra_defaults(self):
        """Test category defaults to None and extra to an empty dict."""
        validation = FenceValidation(
            text="This is safe text.", valid=True, reason_code="safe", duration=0.123
        )

        assert validation.category is None
        assert validation.extra == {}

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
