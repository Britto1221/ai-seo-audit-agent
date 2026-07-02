from openai import OpenAI
from utils import _parse_json
from config import settings
from schemas import MetadataRewriteAgentOutput

def _metadata_rewrite_prompt(audit_data: dict, content_output: dict) -> str:
    return f"""
You are an SEO metadata rewriting specialist.

Your job is to rewrite page titles, meta descriptions, and H1 headings.

Audit Data:
{audit_data}

Content Agent Output:
{content_output}

Use the business description if provided.

Focus only on:
- suggested page titles
- suggested meta descriptions
- suggested H1 headings

Do not analyze technical SEO.
Do not create a final report.
Do not invent keyword volume, ranking data, or backlink data.

Return ONLY valid JSON in this exact structure:

{{
  "rewrite_summary": "Short summary of metadata improvements.",
  "page_rewrites": [
    {{
      "page_url": "https://example.com/page",
      "current_title": "",
      "suggested_title": "",
      "current_meta_description": "",
      "suggested_meta_description": "",
      "current_h1": "",
      "suggested_h1": ""
    }}
  ]
}}

Rules:
- Return JSON only.
- Do not include markdown.
- Keep suggested titles clear, specific, and under 60 characters where possible.
- Keep suggested meta descriptions clear and roughly 50–160 characters.
- Do not rewrite pages that do not need metadata improvements.
"""


def run_metadata_rewrite_agent(
    audit_data: dict,
    content_output: MetadataRewriteAgentOutput | dict,
) -> MetadataRewriteAgentOutput:
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    if hasattr(content_output, "model_dump"):
        content_output = content_output.model_dump()

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a precise SEO metadata rewriting specialist.",
            },
            {
                "role": "user",
                "content": _metadata_rewrite_prompt(audit_data, content_output),
            },
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content
    parsed = _parse_json(content)

    return MetadataRewriteAgentOutput(**parsed)