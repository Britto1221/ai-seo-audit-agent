from datetime import datetime

from .crawler import crawl
from .parser  import parse
from .rules   import detect_issues
from .scorer  import score_site
from .models  import AuditResult, Severity


class SEOExtract:

    @staticmethod
    def audit(url: str, max_pages: int = 20) -> AuditResult:
        """
        Main entry point.

        Usage:
            from seoextracthf import SEOExtract
            result = SEOExtract.audit("https://example.com")

        Returns an AuditResult object with:
            result.site_score
            result.grade
            result.pages        → list of PageData
            result.issues       → list of SEOIssue
        """

        # 1. Crawl
        raw_pages = crawl(url, max_pages=max_pages)

        # 2. Parse each page
        pages = [parse(r) for r in raw_pages]

        # 3. Detect issues
        issues = detect_issues(pages)

        # 4. Score
        site_score, grade = score_site(pages, issues)

        # 5. Count by severity
        critical = sum(1 for i in issues if i.severity == Severity.CRITICAL)
        warning  = sum(1 for i in issues if i.severity == Severity.WARNING)
        info     = sum(1 for i in issues if i.severity == Severity.INFO)

        return AuditResult(
            url           = url,
            audit_date    = datetime.now().strftime("%Y-%m-%d %H:%M"),
            pages_crawled = len(pages),
            site_score    = site_score,
            grade         = grade,
            total_issues  = len(issues),
            critical_count= critical,
            warning_count = warning,
            info_count    = info,
            pages         = pages,
            issues        = issues,
        )
    

if __name__ == "__main__":
    result = SEOExtract.audit("https://books.toscrape.com")
    for i in result:
        print(i)