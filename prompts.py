def seo_agent_prompt(audit_data: dict) -> str:
    return f"""
You are an expert SEO consultant.

Analyze this structured SEO audit data and create a business-friendly SEO improvement report.

SEO Audit Data:
{audit_data}

Return ONLY valid JSON in this exact format:

{{
  "website_url": "",
  "site_score": 0,
  "grade": "",
  "executive_summary": "",
  "top_problems": [
    ""
  ],
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
- Do not invent keyword volume, traffic numbers, or backlink data.
- Base recommendations only on the audit data provided.
- Make the advice clear enough for a business owner to understand.
"""