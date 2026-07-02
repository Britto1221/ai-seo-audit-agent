from deep_agent import create_ai_seo_deep_agent
from seo_service import compress_audit_result, run_seo_audit


def run_deep_ai_seo_agent(
    url: str,
    max_pages: int = 5,
    business_description: str = "",
):
    audit_result = run_seo_audit(url, max_pages=max_pages)

    audit_data = compress_audit_result(
        audit_result,
        business_description=business_description,
    )

    agent = create_ai_seo_deep_agent()

    prompt = f"""
Run a concise AI SEO audit and return the final answer immediately.

Compressed SEOExtract Audit Data:
{audit_data}

Business Description:
{business_description}

Use specialist subagents only if needed.

Final output must match the FinalSEOReport schema.

Rules:
- Do not ask follow-up questions.
- Do not browse the web.
- Do not write files.
- Do not repeat analysis.
- Do not keep planning after enough information is available.
- Finish with one final structured response.
"""

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        },
        config={"recursion_limit": 10},
    )

    return {
        "raw_audit": audit_result,
        "compressed_audit": audit_data,
        "deep_agent_result": result,
    }