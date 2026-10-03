# Personal Plan Generator

A Streamlit app that turns a skill you want to learn into a day-by-day plan.
Pick a category, a skill, how many days you have and how long you can study each day.
It writes one plan with a task for every day and a milestone on your schedule.

## Features

- Day-by-day plan grouped into weeks, with Learn / Practice / Review for each day
- Milestone checkpoints every N days
- Choose the provider (Google Gemini or OpenRouter) and any model your key can use
- Jumps to the plan when it finishes, and keeps it on screen after you download it
- Download the plan as Markdown
- Password-protected: the app stays locked until `APP_PASSWORD` is entered, with a lockout after 5 wrong attempts

## Setup

Requires Python 3.13+.

1. Copy `.env.example` to `.env`, set `APP_PASSWORD`, and set at least one API key:
   - `GOOGLE_API_KEY` from <https://aistudio.google.com/apikey>
   - `OPENROUTER_API_KEY` from <https://openrouter.ai/keys>

   The app only lists providers whose key is set. On Streamlit Cloud, set them under Settings → Secrets.
2. Install dependencies:
   ```
   uv sync
   ```
   (or `pip install -r requirements.txt`)

## Run

```
uv run streamlit run main.py
```

Without uv: `streamlit run main.py`.

## Project structure

```
main.py                 # entrypoint
src/
  app.py                # wires the page together, handles Generate and session state
  auth.py               # password gate with lockout
  config.py             # API keys, categories, page settings
  prompts.py            # plan prompt template
  models.py             # model discovery and LLM client setup
  generator.py          # PlanRequest and generate_plan()
  ui/                   # header, model picker, inputs, result view, styles.css
```

## Stack

Streamlit, LangChain (Google Gemini and OpenRouter), python-dotenv.
