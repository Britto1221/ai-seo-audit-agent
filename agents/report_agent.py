import json
import re
from openai import OpenAI
from utils import _parse_json
from config import settings
from schemas import (
    ContentAgentOutput,
    FinalSEOReport,
    MetadataRewriteAgentOutput,
    PriorityAgentOutput,
    TechnicalAgentOutput,
)

def _to_dict(data):
    if hasattr(data, "model_dump"):
        return data.model_dump()
    return data

def _report_prompt(
    audit_data: dict,
    technical_output: dict,
    content_output: dict,
    rewrite_output: dict,
    priority_output: dict,
) -> str:
    return f"""
You are a senior SEO consultant writing the final SEO audit report.

Your job is to combine the outputs from specialist SEO agents into one clear business-friendly report.

Audit Data:
{audit_data}

Technical Agent Output:
{technical_output}

Content Agent Output:
{content_output}

Metadata Rewrite Agent Output:
{rewrite_output}

Priority Planner Agent Output:
{priority_output}

Create a final SEO report for a business owner or marketing team.

Do not invent:
- keyword volume
- traffic numbers
- backlink data
- ranking positions
- revenue numbers

Return ONLY valid JSON in this exact structure:

{{
  "website_url": "",
  "site_score": 0,
  "grade": "",
  "executive_summary": "",
  "top_problems": [
    ""
  ],
  "technical_summary": "",
  "content_summary": "",
  "priority_actions": [
    {{
      "priority": "High/Medium/Low",
      "issue": "",
      "why_it_matters": "",
      "recommended_fix": "",
      "expected_impact": ""
    }}
  ],
  "page_recommendations": [
    {{
      "page_url": "",
      "summary": "",
      "suggested_title": "",
      "suggested_meta_description": "",
      "suggested_h1": "",
      "content_suggestions": [
        ""
      ]
    }}
  ],
  "thirty_day_plan": [
    ""
  ]
}}

Rules:
- Return JSON only.
- Do not include markdown.
- Keep the language clear and business-friendly.
- Use the specialist agent outputs as the source of truth.
- Do not add unsupported claims.
"""

def run_report_agent(
    audit_data: dict,
    technical_output: TechnicalAgentOutput | dict,
    content_output: ContentAgentOutput | dict,
    rewrite_output: MetadataRewriteAgentOutput | dict,
    priority_output: PriorityAgentOutput | dict,
) -> FinalSEOReport:
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    technical_output = _to_dict(technical_output)
    content_output = _to_dict(content_output)
    rewrite_output = _to_dict(rewrite_output)
    priority_output = _to_dict(priority_output)

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a senior SEO consultant and report writer.",
            },
            {
                "role": "user",
                "content": _report_prompt(
                    audit_data,
                    technical_output,
                    content_output,
                    rewrite_output,
                    priority_output,
                ),
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    parsed = _parse_json(content)

    return FinalSEOReport(**parsed)