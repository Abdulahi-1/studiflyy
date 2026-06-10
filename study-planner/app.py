from datetime import datetime

from flask import Flask, render_template, request

from models.task import Task
from planner.scheduler import build_schedule
from planner.ai_helper import summarize_notes, generate_quiz
from planner import calendar as gcal

app = Flask(__name__)


NAV_LINKS = [
    {"href": "/summaries", "label": "Summaries"},
    {"href": "/quizzes",   "label": "Quizzes"},
    {"href": "/calendar",  "label": "Calendar"},
    {"href": "/plan",      "label": "Planner"},
]

HERO = {
    "tag": "your ai study buddy",
    "title": "Welcome to",
    "title_em": "Studifly",
    "subtitle": (
        "Upload your messy notes, get clean summaries, auto-generated quizzes, "
        "and a study plan that drops straight into your Google Calendar."
    ),
    "primary_cta": "Get Started",
    "secondary_cta": "See How",
}

STATS = [
    {"num": "1.2k", "label": "Notes Summarized"},
    {"num": "850+", "label": "Quizzes Made"},
    {"num": "∞",    "label": "Late-night saves"},
]

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

HOW_STEPS = [
    {
        "icon": "📤",
        "title": "Upload your stuff",
        "body": "Drop in notes, slides, or just paste your assignment list.",
    },
    {
        "icon": "✨",
        "title": "AI does the magic",
        "body": "Summaries, quizzes, and priorities all auto-generated.",
    },
    {
        "icon": "🦋",
        "title": "Get your plan",
        "body": "A clean dashboard + Google Calendar sessions ready to go.",
    },
]

ABOUT = (
    "Studifly is a project I'm building for class, an AI Study Buddy that "
    "combines a planner and a study helper. Canvas and Google Calendar just "
    "store stuff, they don't actually help you learn it. Studifly uses "
    "Hugging Face models to summarize notes, generate quiz questions, and "
    "slot study sessions into your real calendar so studying feels a "
    "little less like drowning."
)


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


@app.route("/plan", methods=["GET", "POST"])
def plan():
    sessions = []
    calendar_links = None
    calendar_error = None

    if request.method == "POST":
        names = request.form.getlist("name")
        deadlines = request.form.getlist("deadline")
        difficulties = request.form.getlist("difficulty")

        tasks = []
        for name, deadline, difficulty in zip(names, deadlines, difficulties):
            if not name or not deadline:
                continue
            tasks.append(Task(
                name=name,
                deadline=datetime.strptime(deadline, "%Y-%m-%d"),
                difficulty=int(difficulty),
            ))

        sessions = build_schedule(tasks)

        if request.form.get("action") == "sync" and sessions:
            try:
                calendar_links = gcal.add_sessions(sessions)
            except Exception as e:
                calendar_error = str(e)

    return render_template(
        "plan.html",
        site_name="Studifly",
        nav_links=NAV_LINKS,
        sessions=sessions,
        calendar_links=calendar_links,
        calendar_error=calendar_error,
        year=2026,
    )


@app.route("/summaries", methods=["GET", "POST"])
def summaries():
    notes = ""
    summary = None
    error = None

    if request.method == "POST":
        notes = request.form.get("notes", "")
        if notes.strip():
            try:
                summary = summarize_notes(notes)
            except Exception as e:
                error = str(e)

    return render_template(
        "summaries.html", site_name="Studifly", nav_links=NAV_LINKS, year=2026,
        notes=notes, summary=summary, error=error,
    )


@app.route("/quizzes", methods=["GET", "POST"])
def quizzes():
    topic = ""
    quiz = None
    error = None

    if request.method == "POST":
        topic = request.form.get("topic", "")
        if topic.strip():
            try:
                quiz = generate_quiz(topic)
            except Exception as e:
                error = str(e)

    return render_template(
        "quizzes.html", site_name="Studifly", nav_links=NAV_LINKS, year=2026,
        topic=topic, quiz=quiz, error=error,
    )


@app.route("/calendar")
def calendar():
    return render_template(
        "feature.html", site_name="Studifly", nav_links=NAV_LINKS, year=2026,
        icon="📅", title="Calendar Sync",
        body="Head to the Planner, build a study plan, then hit "
             "\"Build + add to Google Calendar\" to send your sessions over.",
    )


if __name__ == "__main__":
    app.run(debug=True)
