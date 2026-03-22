from src.llm_openai import format_case_features, build_clinical_prompt

def test_format_case_features_returns_text():
    case_features = {
        "radius_mean": 17.99,
        "texture_mean": 10.38
    }

    formatted = format_case_features(case_features)

    assert "radius_mean" in formatted
    assert "texture_mean" in formatted

def test_build_clinical_prompt_contains_sections():
    prompt = build_clinical_prompt(
        predicted_class="maligno",
        predicted_probability=0.98,
        recall=0.90,
        specificity=0.97,
        precision=0.95,
        fn=4,
        fp=2,
        case_features={"radius_mean": 17.99},
        context_note="Teste acadêmico"
    )

    assert "Classe prevista" in prompt
    assert "Características do caso analisado" in prompt
    assert "saúde da mulher" in prompt.lower()