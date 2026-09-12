"""The documented quick start creates `.env` at the repository root, but every
backend command runs from `backend/`. A relative env_file would silently miss it.
"""

from pathlib import Path

from app.core.config import Settings


def test_settings_read_the_repo_root_env_file():
    env_file = Settings.model_config["env_file"]
    assert env_file is not None
    root = Path(str(env_file)).parent
    assert Path(str(env_file)).name == ".env"
    # The repository root is the directory holding .env.example and the Makefile.
    assert (root / ".env.example").is_file()
    assert (root / "Makefile").is_file()
