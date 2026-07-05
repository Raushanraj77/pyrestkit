from __future__ import annotations

import json
from typing import Any

from pyrestkit.ai.client import AIClient
from pyrestkit.ai.models import FailureAnalysis, FailureContext
from pyrestkit.ai.utils.prompt_loader import PromptLoader

FAILURE_ANALYZER_SYSTEM_PROMPT = (
    "You are an expert Python API automation engineer. "
    "Return concise, actionable failure analysis as JSON only."
)


class FailureAnalyzer:
    """
    Generates structured analysis and fix suggestions for test failures.
    """

    def __init__(
        self,
        client: AIClient,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        self._client = client
        self._prompt_loader = prompt_loader or PromptLoader.default()

    def build_prompt(
        self,
        context: FailureContext,
    ) -> str:
        return self._prompt_loader.render(
            "failure_analysis.md",
            context=json.dumps(
                context.to_dict(),
                indent=2,
                sort_keys=True,
            ),
        )

    def analyze(
        self,
        context: FailureContext,
    ) -> FailureAnalysis:
        raw_response = self._client.complete(
            self.build_prompt(context),
            system_prompt=FAILURE_ANALYZER_SYSTEM_PROMPT,
        )

        return parse_failure_analysis(raw_response)


def parse_failure_analysis(
    raw_response: str,
) -> FailureAnalysis:
    try:
        data = json.loads(_extract_json(raw_response))
    except (json.JSONDecodeError, ValueError):
        return FailureAnalysis(
            summary=raw_response.strip(),
            likely_cause="",
            recommended_fix="",
            raw_response=raw_response,
        )

    if not isinstance(data, dict):
        return FailureAnalysis(
            summary=str(data).strip(),
            likely_cause="",
            recommended_fix="",
            raw_response=raw_response,
        )

    return FailureAnalysis(
        summary=str(data.get("summary", "")).strip(),
        likely_cause=str(data.get("likely_cause", "")).strip(),
        recommended_fix=str(data.get("recommended_fix", "")).strip(),
        suggested_patch=_optional_text(data.get("suggested_patch")),
        confidence=_confidence(data.get("confidence", 0.0)),
        raw_response=raw_response,
    )


def _extract_json(
    value: str,
) -> str:
    text = value.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    if text.startswith("{") and text.endswith("}"):
        return text

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found.")

    return text[start : end + 1]


def _optional_text(
    value: Any,
) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    return text or None


def _confidence(
    value: Any,
) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.0

    if confidence < 0.0:
        return 0.0

    if confidence > 1.0:
        return 1.0

    return confidence
