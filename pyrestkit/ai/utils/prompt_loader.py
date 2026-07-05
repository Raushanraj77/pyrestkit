from __future__ import annotations

from pathlib import Path
from string import Template


class PromptLoader:
    """
    Loads and renders prompt templates from a directory.
    """

    def __init__(
        self,
        base_path: str | Path,
    ) -> None:
        self._base_path = Path(base_path).resolve()

    @classmethod
    def default(cls) -> PromptLoader:
        return cls(Path(__file__).resolve().parents[1] / "prompts")

    def load(
        self,
        name: str,
    ) -> str:
        path = self._resolve(name)

        if not path.exists():
            raise FileNotFoundError(f"Prompt template '{name}' was not found.")

        return path.read_text(encoding="utf-8")

    def render(
        self,
        template_name: str,
        **values: object,
    ) -> str:
        template = Template(self.load(template_name))
        return template.substitute(values)

    def _resolve(
        self,
        name: str,
    ) -> Path:
        path = (self._base_path / name).resolve()

        try:
            path.relative_to(self._base_path)
        except ValueError as exc:
            raise ValueError("Prompt template path cannot escape base path.") from exc

        return path
