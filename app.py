import streamlit as st
from report_generator import save_docx_report, save_pdf_report
from deep_agent_runner import run_deep_ai_seo_agent


st.set_page_config(
    page_title="AI SEO Audit Agent",
    page_icon="📈",
    layout="wide",
)

st.title("AI SEO Audit Agent")
st.write(
    "Run SEOExtract, analyze the results with specialist SEO subagents, "
    "and generate a business-friendly SEO action plan."
)

url = st.text_input(
    "Website URL",
    placeholder="https://example.com",
)

business_description = st.text_area(
    "Brief business description",
    placeholder=(
        "Example: We are a school management software company helping schools "
        "manage attendance, fees, communication, and admissions."
    ),
)

max_pages = st.number_input(
    "Maximum pages to crawl",
    min_value=1,
    max_value=20,
    value=5,
)

if st.button("Run Deep AI SEO Audit"):
    if not url:
        st.error("Please enter a website URL.")
    else:
        with st.spinner("Running SEOExtract and DeepAgents workflow..."):
            result = run_deep_ai_seo_agent(
                url=url,
                max_pages=max_pages,
                business_description=business_description,
            )

        raw_audit = result["raw_audit"]
        deep_agent_result = result["deep_agent_result"]

        st.success("Deep AI SEO audit completed.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Site Score", raw_audit.site_score)
        col2.metric("Grade", raw_audit.grade)
        col3.metric("Total Issues", raw_audit.total_issues)

        st.subheader("Deep Agent Output")
        st.write(deep_agent_result)