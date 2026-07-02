from seoextract import SEOExtract

def run_seo_audit(url: str, max_pages: int = 5):
    """
    Runs SEOExtract and returns structured AuditResult.
    """
    return SEOExtract.audit(url, max_pages=max_pages)


def compress_audit_result(audit_result, business_description: str = "") -> dict:
    return {
        "website_url": audit_result.url,
        "business_description": business_description,
        "site_score": audit_result.site_score,
        "grade": audit_result.grade,
        "pages_crawled": audit_result.pages_crawled,
        "total_issues": audit_result.total_issues,
        "critical_count": audit_result.critical_count,
        "warning_count": audit_result.warning_count,
        "info_count": audit_result.info_count,
        "pages": [
            {
                "url": page.url,
                "title": page.title or "",
                "status_code": page.status_code,
                "word_count": page.word_count,
                "page_score": page.page_score,
                "page_issues_count": page.page_issues_count,
                "h1_tags": page.h1_tags[:3],
                "meta_description": page.meta_description or "",
                "internal_count": page.internal_count,
                "external_count": page.external_count,
                "schema_found": page.schema_found,
            }
            for page in audit_result.pages[:10]
        ],
        "issues": [
            {
                "page_url": issue.page_url,
                "issue_type": issue.issue_type.value,
                "severity": issue.severity.value,
                "current_value": issue.current_value,
                "suggestion": issue.suggestion,
            }
            for issue in audit_result.issues[:50]
        ],
    }