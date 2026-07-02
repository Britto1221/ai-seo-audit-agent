from agents.content_agent import run_content_agent
from agents.metadata_rewrite_agent import run_metadata_rewrite_agent
from agents.priority_agent import run_priority_agent
from agents.report_agent import run_report_agent
from agents.technical_agent import run_technical_agent
from seo_service import compress_audit_result, run_seo_audit


def run_ai_seo_agent(
    url: str,
    max_pages: int = 5,
    business_description: str = "",
):
    """
    Runs the full AI SEO Audit Agent workflow.

    Workflow:
    1. Run SEOExtract
    2. Compress audit data
    3. Run Technical SEO subagent
    4. Run Content SEO subagent
    5. Run Metadata Rewrite subagent
    6. Run Priority Planner subagent
    7. Run Report Writer subagent
    """

    audit_result = run_seo_audit(url, max_pages=max_pages)

    audit_data = compress_audit_result(
        audit_result,
        business_description=business_description,
    )

    technical_output = run_technical_agent(audit_data)

    content_output = run_content_agent(audit_data)

    rewrite_output = run_metadata_rewrite_agent(
        audit_data=audit_data,
        content_output=content_output,
    )

    priority_output = run_priority_agent(
        audit_data=audit_data,
        technical_output=technical_output,
        content_output=content_output,
        rewrite_output=rewrite_output,
    )

    final_report = run_report_agent(
        audit_data=audit_data,
        technical_output=technical_output,
        content_output=content_output,
        rewrite_output=rewrite_output,
        priority_output=priority_output,
    )

    return {
        "raw_audit": audit_result,
        "compressed_audit": audit_data,
        "technical_output": technical_output,
        "content_output": content_output,
        "rewrite_output": rewrite_output,
        "priority_output": priority_output,
        "final_report": final_report,
    }