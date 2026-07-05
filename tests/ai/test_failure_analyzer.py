from __future__ import annotations

import json

from pyrestkit.ai.analyzer import FailureAnalyzer, parse_failure_analysis
from pyrestkit.ai.client import AIClient
from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.models import FailureContext
from pyrestkit.ai.provider import StaticAIProvider


def test_failure_analyzer_returns_structured_analysis() -> None:
    provider = StaticAIProvider(
        json.dumps({
            "summary": "Status assertion failed.",
            "likely_cause": "The endpoint returned 404 instead of 200.",
            "recommended_fix": "Check the endpoint path or expected status.",
            "suggested_patch": None,
            "confidence": 0.8,
        })
    )
    client = AIClient(
        config=AIConfig(
            provider="openai",
            model="gpt-test",
        ),
        provider=provider,
    )
    analyzer = FailureAnalyzer(client)

    analysis = analyzer.analyze(
        FailureContext(
            test_name="test_get_user",
            file_path="tests/clients/test_user_client.py",
            error_type="AssertionError",
            expected="200",
            actual="404",
        )
    )

    assert analysis.summary == "Status assertion failed."
    assert analysis.likely_cause == "The endpoint returned 404 instead of 200."
    assert analysis.recommended_fix == "Check the endpoint path or expected status."
    assert analysis.suggested_patch is None
    assert analysis.confidence == 0.8
    assert "test_get_user" in provider.calls[0].prompt


def test_parse_failure_analysis_handles_markdown_json() -> None:
    analysis = parse_failure_analysis(
        """```json
{
  "summary": "Schema drift",
  "likely_cause": "Response has a new field",
  "recommended_fix": "Update the schema fixture",
  "suggested_patch": "diff --git a/schema b/schema",
  "confidence": 2
}
```"""
    )

    assert analysis.summary == "Schema drift"
    assert analysis.confidence == 1.0
    assert analysis.suggested_patch == "diff --git a/schema b/schema"


def test_parse_failure_analysis_falls_back_to_raw_text() -> None:
    analysis = parse_failure_analysis("Could not determine the root cause.")

    assert analysis.summary == "Could not determine the root cause."
    assert analysis.likely_cause == ""
    assert analysis.recommended_fix == ""


def test_parse_failure_analysis_handles_non_object_json() -> None:
    analysis = parse_failure_analysis('["not", "an", "object"]')

    assert analysis.summary == '["not", "an", "object"]'
    assert analysis.likely_cause == ""
    assert analysis.recommended_fix == ""
