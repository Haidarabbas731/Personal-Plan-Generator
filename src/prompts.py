from langchain_core.prompts import ChatPromptTemplate

plan_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a senior {category} coach with 20 years of experience teaching people "
            "to reach real competence. You write realistic, specific study plans, not "
            "motivational filler. Every task is something the learner can start immediately "
            "and know when it is finished.",
        ),
        (
            "human",
            """Build a day-by-day plan.

Skill: {skill}
Category: {category}
Days available: {days_available}
Time per day: {daily_time} hour(s)
Milestone every: {milestone_interval} day(s)

Rules:
- Output exactly {days_available} days, numbered Day 1 to Day {days_available}. Never skip, merge or summarise days.
- Group days under a `## Week N: <theme>` heading (last week may be shorter). Each week theme should build on the previous one.
- Format each day as:
  **Day N · <short title>** (~{daily_time}h)
  - Learn: <specific concept or resource type>
  - Practice: <concrete exercise with a measurable result>
  - Review: <what to recall or fix from earlier days>
- Split each day's time sensibly across Learn / Practice / Review, favouring Practice.
- Every {milestone_interval} days, add a line `🏁 Milestone: <small project or test and how to judge it>` directly after that day.
- Start with a 2-sentence overview of the path. Finish with a short "Where you'll be on Day {days_available}" paragraph.
- No intro chatter, no closing questions. Markdown only.""",
        ),
    ]
)

