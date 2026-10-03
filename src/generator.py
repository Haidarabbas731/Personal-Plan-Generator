from dataclasses import dataclass

from langchain_core.output_parsers import StrOutputParser

from .models import build_llm
from .prompts import plan_prompt


@dataclass(frozen=True)
class PlanRequest:
    provider: str
    model: str
    category: str
    skill: str
    days_available: int
    daily_time: int
    milestone_interval: int


def generate_plan(req: PlanRequest) -> str:
    chain = plan_prompt | build_llm(req.provider, req.model) | StrOutputParser()
    return chain.invoke(
        {
            "skill": req.skill,
            "category": req.category,
            "days_available": req.days_available,
            "daily_time": req.daily_time,
            "milestone_interval": req.milestone_interval,
        }
    ).strip()
