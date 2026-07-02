from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from schemas import FinalSEOReport
from config import settings


def create_ai_seo_deep_agent():
    model = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0.2,
    )

    instructions = """
You are the Main AI SEO Audit Agent.

You receive compressed SEOExtract audit data and a business description.
Your job is to delegate analysis to specialist SEO subagents and produce a final SEO action report.

Use subagents for:
- technical SEO analysis
- content SEO analysis
- metadata rewrite suggestions
- priority planning
- final report writing

Do not invent keyword volume, backlinks, rankings, revenue, or traffic numbers.
Base everything only on the provided SEOExtract audit data and business description.
"""

    subagents = [
        {
            "name": "technical-seo-agent",
            "description": "Analyzes technical SEO issues such as canonical tags, viewport, schema, accessibility, HTTP status, and internal linking.",
            "system_prompt": """
You are a Technical SEO Subagent.

Analyze only technical SEO issues:
- page accessibility
- HTTP status problems
- canonical tags
- viewport tags
- schema markup
- robots meta
- internal linking
- crawlability issues

Return clear technical findings with severity, affected pages, why it matters, and recommended fixes.
Do not analyze content quality.
Do not rewrite metadata.
""",
        },
        {
            "name": "content-seo-agent",
            "description": "Analyzes content and on-page SEO issues such as thin content, H1 problems, weak titles, and weak meta descriptions.",
            "system_prompt": """
You are a Content SEO Subagent.

Analyze only content and on-page SEO issues:
- thin content
- weak titles
- missing or weak meta descriptions
- H1 problems
- content clarity
- content gaps
- user intent alignment

Use the business description if provided.
Do not analyze technical SEO.
Do not create the final report.
""",
        },
        {
            "name": "metadata-rewrite-agent",
            "description": "Creates improved page titles, meta descriptions, and H1 suggestions for pages that need metadata improvements.",
            "system_prompt": """
You are a Metadata Rewrite Subagent.

Rewrite only:
- page titles
- meta descriptions
- H1 headings

Keep titles under 60 characters where possible.
Keep meta descriptions around 50–160 characters.
Do not invent keyword volume, rankings, or traffic.
Do not create the final report.
""",
        },
        {
            "name": "priority-planner-agent",
            "description": "Ranks SEO fixes by priority and creates a realistic 30-day action plan.",
            "system_prompt": """
You are a Priority Planner Subagent.

Rank the SEO fixes by:
- impact
- urgency
- ease of implementation
- importance of affected pages

Create:
- high priority fixes
- medium priority fixes
- low priority fixes
- a realistic 30-day SEO action plan

Do not invent unsupported metrics.
""",
        },
        {
            "name": "report-writer-agent",
            "description": "Combines all specialist outputs into a final business-friendly SEO audit report.",
            "system_prompt": """
You are a Report Writer Subagent.

Create the final SEO audit report for a business owner or marketing team.

Include:
- executive summary
- top problems
- technical summary
- content summary
- priority actions
- page recommendations
- 30-day SEO plan

Use clear business-friendly language.
Do not invent unsupported claims.
""",
        },
    ]

    return create_deep_agent(
        model=model,
        tools=[],
        system_prompt=instructions,
        subagents=subagents,
        response_format=FinalSEOReport,
    )