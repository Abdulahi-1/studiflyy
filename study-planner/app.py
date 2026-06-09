# Studifly - main Flask app
# this is what runs the website (renders the homepage template)

from datetime import datetime

from flask import Flask, render_template, request

from models.task import Task
from planner.scheduler import build_schedule

app = Flask(__name__)


# nav bar links. just anchors to the sections for now
# nav bar = one tab per feature. keeping it simple, just the 4 things the app does.
NAV_LINKS = [
    {"href": "/summaries", "label": "Summaries"},
    {"href": "/quizzes",   "label": "Quizzes"},
    {"href": "/calendar",  "label": "Calendar"},
    {"href": "/plan",      "label": "Planner"},
]

# big welcome section at the top of the page
HERO = {
    "tag": "your ai study buddy",
    "title": "Welcome to",
    "title_em": "Studifly",  # this part shows up italic + blue
    "subtitle": (
        "Upload your messy notes, get clean summaries, auto-generated quizzes, "
        "and a study plan that drops straight into your Google Calendar."
    ),
    "primary_cta": "Get Started",
    "secondary_cta": "See How",
}

# fake stats for now - will hook up to real numbers later
STATS = [
    {"num": "1.2k", "label": "Notes Summarized"},
    {"num": "850+", "label": "Quizzes Made"},
    {"num": "∞",    "label": "Late-night saves"},
]

# the 4 feature cards (based on what the project is supposed to do, see spec.md)
FEATURES = [
    {
        "icon": "📝",
        "title": "Smart Note Summaries",
        "body": (
            "Drop in your lecture notes and the AI shrinks them down to the key "
            "ideas so you're not re-reading 30 pages the night before."
        ),
    },
    {
        "icon": "🧠",
        "title": "AI Practice Quizzes",
        "body": (
            "Auto-generates quiz questions from your own notes. Way better "
            "than just highlighting and hoping it sticks."
        ),
    },
    {
        "icon": "📅",
        "title": "Calendar Sync",
        "body": (
            "Connects to Google Calendar so your study sessions actually show "
            "up next to your classes and not just in a random list."
        ),
    },
    {
        "icon": "⭐",
        "title": "Priority Planner",
        "body": (
            "Sorts your assignments by deadline + workload, then builds you a "
            "study plan that doesn't pretend you have unlimited time."
        ),
    },
]

# 3-step "how it works" section. mirrors the workflow described in spec.md
HOW_STEPS = [
    {
        "icon": "📤",
        "title": "Upload your stuff",
        "body": "Drop in notes, slides, or just paste your assignment list.",
    },
    {
        "icon": "✨",
        "title": "AI does the magic",
        "body": "Summaries, quizzes, and priorities — all auto-generated.",
    },
    {
        "icon": "🦋",
        "title": "Get your plan",
        "body": "A clean dashboard + Google Calendar sessions ready to go.",
    },
]

# short blurb for the about section
ABOUT = (
    "Studifly is a project I'm building for class — an AI Study Buddy that "
    "combines a planner and a study helper. Canvas and Google Calendar just "
    "store stuff, they don't actually help you learn it. Studifly uses "
    "Hugging Face models to summarize notes, generate quiz questions, and "
    "slot study sessions into your real calendar — so studying feels a "
    "little less like drowning."
)


# homepage route - just renders the template with all the data above
@app.route("/")
def index():
    return render_template(
        "index.html",
        site_name="Studifly",
        nav_links=NAV_LINKS,
        hero=HERO,
        stats=STATS,
        features=FEATURES,
        how_steps=HOW_STEPS,
        about=ABOUT,
        year=2026,
    )


# the planner page. GET shows the form, POST builds the schedule.
@app.route("/plan", methods=["GET", "POST"])
def plan():
    sessions = []

    if request.method == "POST":
        # the form sends one list per field (name[], deadline[], difficulty[])
        names = request.form.getlist("name")
        deadlines = request.form.getlist("deadline")
        difficulties = request.form.getlist("difficulty")

        # build a Task for each filled-in row
        tasks = []
        for name, deadline, difficulty in zip(names, deadlines, difficulties):
            if not name or not deadline:
                continue  # skip empty rows
            tasks.append(Task(
                name=name,
                deadline=datetime.strptime(deadline, "%Y-%m-%d"),
                difficulty=int(difficulty),
            ))

        # this is the scheduler we wrote in planner/scheduler.py
        sessions = build_schedule(tasks)

    return render_template(
        "plan.html",
        site_name="Studifly",
        nav_links=NAV_LINKS,
        sessions=sessions,
        year=2026,
    )


# the other 3 feature tabs. these aren't built yet, so they just show a
# simple "coming soon" page for now (same layout, different text).
@app.route("/summaries")
def summaries():
    return render_template(
        "feature.html", site_name="Studifly", nav_links=NAV_LINKS, year=2026,
        icon="📝", title="Smart Note Summaries",
        body="Upload your notes and get a clean summary. Coming soon!",
    )


@app.route("/quizzes")
def quizzes():
    return render_template(
        "feature.html", site_name="Studifly", nav_links=NAV_LINKS, year=2026,
        icon="🧠", title="AI Practice Quizzes",
        body="Auto-generate quiz questions from your notes. Coming soon!",
    )


@app.route("/calendar")
def calendar():
    return render_template(
        "feature.html", site_name="Studifly", nav_links=NAV_LINKS, year=2026,
        icon="📅", title="Calendar Sync",
        body="Send your study sessions to Google Calendar. Coming soon!",
    )


# run the app (debug=True so it reloads when i save changes)
if __name__ == "__main__":
    app.run(debug=True)
