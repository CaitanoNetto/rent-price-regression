from src.regressao_alugueis.config import settings


def test_config_has_expected_attributes():
    assert hasattr(settings, "RAW_DIR")
    assert hasattr(settings, "PROCESSED_DIR")
    assert hasattr(settings, "MODELS_DIR")
    assert hasattr(settings, "TARGET")
