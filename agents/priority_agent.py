import json
import re
from openai import OpenAI
from utils import _parse_json
from config import settings
from schemas import (
    ContentAgentOutput,
    MetadataRewriteAgentOutput,
    PriorityAgentOutput,
    TechnicalAgentOutput,
)

def _to_dict(data):
    if hasattr(data, "model_dump"):
        return data.model_dump()
    return data


def _priority_prompt(
    audit_data: dict,
    technical_output: dict,
    content_output: dict,
    rewrite_output: dict,
) -> str:
    return f"""
You are an SEO priority planning specialist.

Your job is to rank SEO fixes by business impact and implementation priority.

Audit Data:
{audit_data}

Technical Agent Output:
{technical_output}

Content Agent Output:
{content_output}

Metadata Rewrite Agent Output:
{rewrite_output}

Create a clear prioritized action plan.

Focus on:
- what should be fixed first
- what has the highest SEO impact
- what is easiest to implement
- what affects important pages
- what should be done over the next 30 days

Do not invent keyword volume, traffic numbers, backlinks, or ranking data.
Do not create the final report.

Return ONLY valid JSON in this exact structure:

{{
  "priority_summary": "Short summary of what should be prioritized.",
  "priority_actions": [
    {{
      "priority": "High/Medium/Low",
      "issue": "Short issue name",
      "why_it_matters": "Why this should be prioritized.",
      "recommended_fix": "What should be done.",
      "expected_impact": "Expected SEO/business impact without inventing numbers."
    }}
  ],
  "thirty_day_plan": [
    "Week 1: ...",
    "Week 2: ...",
    "Week 3: ...",
    "Week 4: ..."
  ]
}}

Rules:
- Return JSON only.
- Do not include markdown.
- Base the priority plan only on the provided data.
- Keep the plan realistic for a small business or small team.
"""

def run_priority_agent(
    audit_data: dict,
    technical_output: TechnicalAgentOutput | dict,
    content_output: ContentAgentOutput | dict,
    rewrite_output: MetadataRewriteAgentOutput | dict,
) -> PriorityAgentOutput:
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    technical_output = _to_dict(technical_output)
    content_output = _to_dict(content_output)
    rewrite_output = _to_dict(rewrite_output)

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a precise SEO prioritization specialist.",
            },
            {
                "role": "user",
                "content": _priority_prompt(
                    audit_data,
                    technical_output,
                    content_output,
                    rewrite_output,
                ),
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    parsed = _parse_json(content)
    return PriorityAgentOutput(**parsed)