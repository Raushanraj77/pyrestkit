from __future__ import annotations

from pathlib import Path

import pytest

from pyrestkit.ai.utils.prompt_loader import PromptLoader


def test_prompt_loader_renders_template(
    tmp_path: Path,
) -> None:
    template = tmp_path / "hello.md"
    template.write_text("Hello $name", encoding="utf-8")

    loader = PromptLoader(tmp_path)

    assert loader.render("hello.md", name="PyRestKit") == "Hello PyRestKit"


def test_prompt_loader_rejects_path_traversal(
    tmp_path: Path,
) -> None:
    loader = PromptLoader(tmp_path)

    with pytest.raises(ValueError, match="escape base path"):
        loader.load("../secret.md")


def test_prompt_loader_raises_for_missing_template(
    tmp_path: Path,
) -> None:
    loader = PromptLoader(tmp_path)

    with pytest.raises(FileNotFoundError, match="was not found"):
        loader.load("missing.md")
