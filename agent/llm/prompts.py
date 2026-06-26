def build_recommendation_prompt(
    audit_json: str,
    business_domain: str = "",
    target_audience: str = "",
    target_keyword: str = "",
) -> str:
    return f"""
You are an expert SEO consultant.

Analyze the technical SEO audit and create practical SEO improvements.

Business/domain:
{business_domain}

Target audience:
{target_audience}

Primary target keyword:
{target_keyword}

SEO audit data:
{audit_json}

Generate:

1. Overall SEO Summary
2. Recommended Page Titles
3. Recommended Meta Descriptions
4. Recommended H1 and H2 Headings
5. Internal Linking Suggestions
6. Content Improvement Suggestions
7. Priority Action Plan

Rules:
- Use the audit data.
- Use the business/domain context.
- Do not invent pages that were not crawled.
- Keep title suggestions around 50–60 characters.
- Keep meta descriptions around 120–160 characters.
- Make suggestions practical and beginner-friendly.
"""