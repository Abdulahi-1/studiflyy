# Studifly 🦋

**Your AI study buddy.** Upload your messy notes, get clean summaries, auto-generated practice quizzes, and a priority-based study plan that drops straight into your Google Calendar.

Studifly is a Flask web app built for college students who are juggling multiple classes. Tools like Canvas and Google Calendar are great at *storing* your assignments, but they don't actually help you *learn* the material. Studifly combines a smart planner with AI-powered study support — using Hugging Face models to summarize notes, generate quiz questions, and slot study sessions into your real calendar so studying feels a little less like drowning.

## Features

- **📝 Smart Note Summaries** — Paste in lecture notes and the `facebook/bart-large-cnn` model condenses them down to the key ideas, so you're not re-reading 30 pages the night before an exam.
- **🧠 AI Practice Quizzes** — Generates short quiz questions from any topic using `meta-llama/Llama-3.1-8B-Instruct`, for active recall instead of passive highlighting.
- **⭐ Priority Planner** — Sorts your assignments by deadline and workload using a transparent rule-based scoring system, then builds a study plan that doesn't pretend you have unlimited time.
- **📅 Google Calendar Sync** — Sends your generated study sessions straight to your Google Calendar via the Calendar API, so they show up next to your classes.

## Tech Stack

- **Backend / routing:** Flask
- **AI models:** Hugging Face Inference API (BART for summarization, Llama 3.1 for quizzes)
- **Calendar:** Google Calendar API (OAuth 2.0)
- **Frontend:** Server-rendered HTML templates + CSS





## Project Structure

```
study-planner/
├── app.py                  # Flask routes (home, planner, summaries, quizzes, calendar)
├── requirements.txt
├── models/
│   └── task.py             # Task data model
├── planner/
│   ├── ai_helper.py        # Hugging Face API calls (summaries, quizzes)
│   ├── scheduler.py        # Rule-based priority scheduling
│   └── calendar.py         # Google Calendar integration
├── utils/
│   └── time_utils.py       # Deadline helpers
├── static/
│   └── styles.css
└── templates/              # HTML pages
```

## Setup

### 1. Clone the repo

```bash
git clone <repo-url>
cd studifly
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows use `venv\Scripts\activate` instead.

### 3. Install dependencies

```bash
pip install -r study-planner/requirements.txt
```

### 4. Configure your Hugging Face token

The summaries and quizzes features call the Hugging Face Inference API. Grab a free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens), then create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and set your token:

```
HF_API_TOKEN=hf_your_real_token_here
```

### 5. (Optional) Set up Google Calendar sync

Calendar sync is only needed if you want study sessions pushed to your calendar — the rest of the app works without it.

1. In the [Google Cloud Console](https://console.cloud.google.com/), create a project and enable the **Google Calendar API**.
2. Create an **OAuth 2.0 Client ID** (Desktop app) and download the credentials JSON.
3. Save it as `study-planner/planner/credentials.json`.

The first time you sync, a browser window will open to authorize access. A `token.json` is then cached so you won't have to re-authorize every time. Both files are gitignored.

### 6. Run the app

```bash
cd study-planner
python3 app.py
```

The app starts on [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage

1. **Summaries** — Paste your notes and get a condensed summary.
2. **Quizzes** — Enter a topic and get practice questions.
3. **Planner** — Add your assignments with deadlines and difficulty, then build a prioritized study plan. Hit *"Build + add to Google Calendar"* to sync the sessions.

## How Scheduling Works

The planner is intentionally **rule-based, not AI-generated**, to keep results predictable. Each task gets a priority score from its difficulty and how soon it's due:

```
priority = difficulty × 10 − days_until_deadline
```

Higher-priority tasks are scheduled first, and harder tasks (higher difficulty) get more study sessions spread across upcoming days.

## Notes

- `.env`, `credentials.json`, and `token.json` hold secrets and are excluded from version control — never commit them.
