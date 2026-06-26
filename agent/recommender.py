import json

from .llm.client import generate_text
from .llm.prompts import build_recommendation_prompt


def generate_recommendations(
    audit_result,
    business_domain: str = "",
    target_audience: str = "",
    target_keyword: str = "",
) -> str:
    audit_json = audit_result.model_dump_json(indent=2)

    prompt = build_recommendation_prompt(
        audit_json=audit_json,
        business_domain=business_domain,
        target_audience=target_audience,
        target_keyword=target_keyword,
    )

    return generate_text(prompt)