# Studifly - main Flask app
# this is what runs the website (renders the homepage template)

from flask import Flask, render_template

app = Flask(__name__)


# nav bar links. just anchors to the sections for now
NAV_LINKS = [
    {"href": "#home",     "label": "Home"},
    {"href": "#features", "label": "Features"},
    {"href": "#how",      "label": "How it works"},
    {"href": "#about",    "label": "About"},
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


# run the app (debug=True so it reloads when i save changes)
if __name__ == "__main__":
    app.run(debug=True)
