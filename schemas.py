from pydantic import BaseModel, Field


class TechnicalIssue(BaseModel):
    issue: str
    severity: str
    affected_pages: list[str] = Field(default_factory=list)
    why_it_matters: str
    recommended_fix: str


class TechnicalAgentOutput(BaseModel):
    technical_summary: str
    technical_issues: list[TechnicalIssue] = Field(default_factory=list)


class ContentIssue(BaseModel):
    page_url: str
    issue: str
    why_it_matters: str
    recommended_fix: str


class ContentAgentOutput(BaseModel):
    content_summary: str
    content_issues: list[ContentIssue] = Field(default_factory=list)


class MetadataRewrite(BaseModel):
    page_url: str
    current_title: str = ""
    suggested_title: str = ""
    current_meta_description: str = ""
    suggested_meta_description: str = ""
    current_h1: str = ""
    suggested_h1: str = ""


class MetadataRewriteAgentOutput(BaseModel):
    rewrite_summary: str
    page_rewrites: list[MetadataRewrite] = Field(default_factory=list)


class PriorityAction(BaseModel):
    priority: str
    issue: str
    why_it_matters: str
    recommended_fix: str
    expected_impact: str


class PriorityAgentOutput(BaseModel):
    priority_summary: str
    priority_actions: list[PriorityAction] = Field(default_factory=list)
    thirty_day_plan: list[str] = Field(default_factory=list)


class PageRecommendation(BaseModel):
    page_url: str
    summary: str
    suggested_title: str = ""
    suggested_meta_description: str = ""
    suggested_h1: str = ""
    content_suggestions: list[str] = Field(default_factory=list)


class FinalSEOReport(BaseModel):
    website_url: str
    site_score: float
    grade: str
    executive_summary: str
    top_problems: list[str] = Field(default_factory=list)
    technical_summary: str = ""
    content_summary: str = ""
    priority_actions: list[PriorityAction] = Field(default_factory=list)
    page_recommendations: list[PageRecommendation] = Field(default_factory=list)
    thirty_day_plan: list[str] = Field(default_factory=list)