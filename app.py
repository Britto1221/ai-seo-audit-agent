import streamlit as st
from seoextract import SEOExtract

from config import MAX_PAGES, GOOGLE_SAFE_BROWSING_API_KEY
from agent.recommender import generate_recommendations

st.set_page_config(page_title="AI SEO Audit Agent", page_icon="🖥️", layout="wide")

st.markdown("""
<style>
/* Full app */
.stApp {
    background-color: #010409;
    color: #c9d1d9;
    font-family: Consolas, monospace;
}

/* Main container */
.block-container {
    background-color: #010409;
    padding-top: 2rem;
}

/* Text */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #c9d1d9 !important;
    font-family: Consolas, monospace !important;
}

/* Input boxes */
.stTextInput input {
    background-color: #010409 !important;
    color: #58a6ff !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    font-family: Consolas, monospace !important;
}

/* Buttons */
.stButton button {
    background-color: #010409 !important;
    color: #c9d1d9 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    font-family: Consolas, monospace !important;
}

.stButton button:hover {
    border-color: #238636 !important;
    color: #58a6ff !important;
}

/* Terminal cards */
.terminal-output, .terminal-box {
    background-color: #010409;
    border: 1px solid #30363d;
    border-left: 3px solid #238636;
    border-radius: 8px;
    padding: 18px;
    font-family: Consolas, monospace;
    color: #c9d1d9;
    white-space: pre-wrap;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #010409 !important;
    color: #58a6ff !important;
    border: 1px solid #30363d !important;
}

/* JSON box */
pre {
    background-color: #010409 !important;
    color: #c9d1d9 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🖥️ AI SEO Audit Agent")
st.markdown("### Developer terminal-style SEO audit interface")

url = st.text_input("Enter website_url", placeholder="https://example.com")
business_domain = st.text_input("Enter business_domain", placeholder="AI automation agency")
target_audience = st.text_input("Enter target_audience", placeholder="small business owners")
target_keyword = st.text_input("Enter target_keyword", placeholder="AI automation services")

if st.button("▶ run audit"):
    if not url:
        st.error("ERROR: website_url is required")
    else:
        st.markdown('<div class="terminal-box">Running SEOExtract.audit()...</div>', unsafe_allow_html=True)

        audit_result = SEOExtract.audit(
            url,
            max_pages=MAX_PAGES,
            safe_browsing_api_key=GOOGLE_SAFE_BROWSING_API_KEY
        )

        st.markdown("## Audit Summary")

        summary = f"""
$ seoextract audit {url}

site_score      : {audit_result.site_score}
grade           : {audit_result.grade}
pages_crawled   : {audit_result.pages_crawled}
total_issues    : {audit_result.total_issues}
safe_browsing   : {audit_result.safe_browsing.is_safe}
"""
        st.markdown(f'<div class="terminal-output">{summary}</div>', unsafe_allow_html=True)

        st.markdown("## Detected Issues")

        issues_text = ""
        for issue in audit_result.issues:
            issues_text += (
                f"[{issue.severity.value}] {issue.issue_type.value}\n"
                f"page: {issue.page_url}\n"
                f"fix : {issue.suggestion}\n\n"
            )

        st.markdown(f'<div class="terminal-output">{issues_text}</div>', unsafe_allow_html=True)

        st.markdown("## AI Recommendations")

        recommendations = generate_recommendations(
            audit_result,
            business_domain=business_domain,
            target_audience=target_audience,
            target_keyword=target_keyword,
        )

        st.code(recommendations, language="markdown")

        with st.expander("$ show raw_json"):
            st.json(audit_result.model_dump())