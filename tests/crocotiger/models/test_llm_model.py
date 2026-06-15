from crocotiger.models.llm_model import LLMModel, LLMModels


def test_llm_models_parses_full_payload():
    """Verifies nested model entries are coerced into LLMModel objects."""
    models = LLMModels(
        openai=[
            {
                "model": "gpt-4o",
                "label": "GPT-4o",
                "message": "best",
                "recommended": True,
            }
        ],
        gemini=[{"model": "gemini-2.0-flash", "label": "Gemini 2.0 Flash"}],
    )

    assert isinstance(models.openai[0], LLMModel)
    assert models.openai[0].recommended is True
    assert models.gemini[0].message is None
    assert models.gemini[0].recommended is False


def test_llm_model_defaults():
    """Verifies message/recommended default when omitted."""
    model = LLMModel(model="gpt-4o", label="GPT-4o")
    assert model.message is None
    assert model.recommended is False


def test_llm_models_defaults_empty_lists():
    """Verifies the catalog defaults to empty openai/gemini lists."""
    models = LLMModels()
    assert models.openai == []
    assert models.gemini == []
