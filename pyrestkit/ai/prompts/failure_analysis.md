Analyze this API automation failure and identify the smallest useful fix.

Return only a JSON object with this shape:

{
  "summary": "one sentence failure summary",
  "likely_cause": "most likely root cause",
  "recommended_fix": "specific next action",
  "suggested_patch": "unified diff if a safe patch is obvious, otherwise null",
  "confidence": 0.0
}

Rules:
- Do not invent endpoint behavior that is not present in the context.
- Prefer fixing test data, assertions, schemas, or client code only when the context supports it.
- Keep suggested patches minimal and in unified diff format.
- Do not include secrets or credentials in the response.

Failure context:

$context
