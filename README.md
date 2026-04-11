# LLM for Jobs

A collection of LLM-powered agents for processing job descriptions and skills, built on OpenAI's API.

## Project Structure

```
LLM-for-Jobs/
├── job_agents/        # LLM agents for job-related tasks
│   ├── client.py      # Shared OpenAI client, prompt loader, batch utility
│   ├── classify_sentences.py
│   ├── extract_skills.py
│   ├── generate_titles.py
│   ├── identify_skills.py
│   ├── skill_descriptions.py
│   ├── standardize_locations.py
│   └── translate_titles.py
├── prompts/           # Prompt templates (one file per agent)
├── evaluation/        # Evaluation framework
│   ├── cli.py
│   ├── tasks.py
│   ├── metrics.py
│   ├── dataset.py
│   └── runner.py
├── utils/
│   └── load_data.py
└── config.py
```

## Agents

| Agent | Description |
|---|---|
| `classify_sentences` | Label job description sentences: company / tasks / requirements / benefits / others |
| `extract_skills` | Extract normalized skills with text spans from job descriptions |
| `generate_titles` | Standardize raw job titles with seniority detection |
| `identify_skills` | Verify whether a skill is present in a given context |
| `skill_descriptions` | Generate 2–3 sentence descriptions for a list of skills |
| `standardize_locations` | Parse raw location text into city / region / country |
| `translate_titles` | Translate job titles to/from English |

## Setup

**Requirements**: Python 3.10+, OpenAI API key

```bash
uv sync
export OPENAI_API_KEY=your_api_key
```

## Usage

Each agent can be run directly:

```bash
python -m job_agents.extract_skills
python -m job_agents.generate_titles
```

Or imported as a module:

```python
import asyncio
from job_agents.extract_skills import extract_skills

skills = asyncio.run(extract_skills(job_description="..."))
```

## Evaluation

Gold data goes in `data/gold/` (e.g. `salary_gold.csv`). Required columns for salary: `min_salary`, `max_salary`, `currency`, `period`.

```bash
python -m evaluation.cli --data data/gold/salary_gold.csv --task salary
```

Supported tasks: `salary`, `skills`, `title`.
