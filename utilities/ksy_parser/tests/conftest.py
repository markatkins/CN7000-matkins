"""Pytest fixtures for ksy_parser tests."""
import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir() -> Path:
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def cf_update_ksy(fixtures_dir: Path) -> Path:
    """Return path to cf_update.ksy fixture."""
    return fixtures_dir / "cf_update.ksy"


@pytest.fixture
def vc_state_machine_ksy(fixtures_dir: Path) -> Path:
    """Return path to vc_state_machine.ksy fixture."""
    return fixtures_dir / "vc_state_machine.ksy"


@pytest.fixture
def cf_update_data(cf_update_ksy: Path) -> dict:
    """Load and return cf_update.ksy as dict."""
    import yaml
    with open(cf_update_ksy) as f:
        return yaml.safe_load(f)


@pytest.fixture
def vc_state_machine_data(vc_state_machine_ksy: Path) -> dict:
    """Load and return vc_state_machine.ksy as dict."""
    import yaml
    with open(vc_state_machine_ksy) as f:
        return yaml.safe_load(f)
