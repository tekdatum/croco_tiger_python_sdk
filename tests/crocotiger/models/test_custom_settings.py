from datetime import datetime

from crocotiger.models.custom_settings import CustomSettings


class TestCustomSettings:
    def test_trimmed_openai_key_when_gt_4_characters(self) -> None:
        settings = CustomSettings(
            openai_key="SECRET_OPENAI_1234", gemini_key=None, created_at=datetime.now()
        )
        assert settings.trimmed_openai_key == "1234"

    def test_trimmed_openai_key_when_lt_4_characters(self) -> None:
        settings = CustomSettings(
            openai_key="234", gemini_key=None, created_at=datetime.now()
        )
        assert settings.trimmed_openai_key == "234"

    def test_trimmed_openai_key_when_not_provided(self) -> None:
        settings = CustomSettings(
            openai_key=None, gemini_key=None, created_at=datetime.now()
        )
        assert settings.trimmed_openai_key is None

    def test_trimmed_gemini_key_when_gt_4_characters(self) -> None:
        settings = CustomSettings(
            openai_key=None, gemini_key="SECRET_GEMINI_1234", created_at=datetime.now()
        )
        assert settings.trimmed_gemini_key == "1234"

    def test_trimmed_gemini_key_when_lt_4_characters(self) -> None:
        settings = CustomSettings(
            openai_key=None, gemini_key="13", created_at=datetime.now()
        )
        assert settings.trimmed_gemini_key == "13"

    def test_trimmed_gemini_key_when_not_provided(self) -> None:
        settings = CustomSettings(
            openai_key=None, gemini_key=None, created_at=datetime.now()
        )
        assert settings.trimmed_gemini_key is None

    def test_is_invalid_when_missing_openai_key_only(self) -> None:
        settings = CustomSettings(
            openai_key=None, gemini_key="1234", created_at=datetime.now()
        )
        assert not settings.is_invalid()

    def test_is_invalid_when_missing_gemini_key_only(self) -> None:
        settings = CustomSettings(
            openai_key="4321", gemini_key=None, created_at=datetime.now()
        )
        assert not settings.is_invalid()

    def test_is_invalid_when_missing_both_keys(self) -> None:
        settings = CustomSettings(
            openai_key=None, gemini_key=None, created_at=datetime.now()
        )
        assert settings.is_invalid()
