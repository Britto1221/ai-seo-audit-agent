import json
import re
from openai import OpenAI

from config import settings
from schemas import TechnicalAgentOutput
from utils import _parse_json

def _technical_prompt(audit_data: dict) -> str:
    return f"""
You are a Technical SEO specialist.

Analyze only the technical SEO problems from this SEO audit data.

Audit Data:
{audit_data}

Focus only on:
- page accessibility
- HTTP status problems
- canonical tags
- viewport tags
- schema markup
- internal linking
- technical crawlability issues

Do not analyze content quality.
Do not rewrite titles or meta descriptions.
Do not create a final report.

Return ONLY valid JSON in this exact structure:

{{
  "technical_summary": "Short technical SEO summary.",
  "technical_issues": [
    {{
      "issue": "Short issue name",
      "severity": "CRITICAL/WARNING/INFO",
      "affected_pages": ["https://example.com/page"],
      "why_it_matters": "Why this technical issue matters.",
      "recommended_fix": "How to fix this issue."
    }}
  ]
}}

Rules:
- Return JSON only.
- Do not include markdown.
- Base the analysis only on the provided audit data.
- Do not invent data.
"""


def run_technical_agent(audit_data: dict) -> TechnicalAgentOutput:
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a precise technical SEO specialist.",
            },
            {
                "role": "user",
                "content": _technical_prompt(audit_data),
            },
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content
    parsed = _parse_json(content)

    return TechnicalAgentOutput(**parsed)