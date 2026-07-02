from utils import _parse_json
from openai import OpenAI
from config import settings
from schemas import ContentAgentOutput

def _content_prompt(audit_data: dict) -> str:
    return f"""
You are a Content SEO specialist.

Analyze only the content and on-page SEO problems from this SEO audit data.

Audit Data:
{audit_data}

Use the business description if provided to make your recommendations more relevant.

Focus only on:
- thin content
- weak titles
- missing or weak meta descriptions
- H1 problems
- page clarity
- content relevance
- content gaps
- user intent alignment

Do not analyze canonical, schema, viewport, or technical crawl issues.
Do not create the final report.

Return ONLY valid JSON in this exact structure:

{{
  "content_summary": "Short content SEO summary.",
  "content_issues": [
    {{
      "page_url": "https://example.com/page",
      "issue": "Short issue name",
      "why_it_matters": "Why this content issue matters.",
      "recommended_fix": "How to fix this issue."
    }}
  ]
}}

Rules:
- Return JSON only.
- Do not include markdown.
- Base the analysis only on the provided audit data.
- Do not invent traffic, keyword volume, backlinks, or rankings.
"""

def run_content_agent(audit_data: dict) -> ContentAgentOutput:
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a precise content SEO specialist.",
            },
            {
                "role": "user",
                "content": _content_prompt(audit_data),
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    parsed = _parse_json(content)

    return ContentAgentOutput(**parsed)