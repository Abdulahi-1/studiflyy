# planner/scheduler.py
# Rule-based scheduler (NOT AI - the spec says scheduling stays rule-based).
# Takes a list of Task objects and turns them into suggested study sessions.

from datetime import datetime, timedelta

from utils.time_utils import days_until


def priority_score(task):
    """How urgent is this task? Higher number = study it sooner.

    Combines the two signals from the spec:
      - difficulty (workload): bigger = more important
      - deadline (urgency):    closer = more important
    A hard task due soon scores high; an easy task far away scores low.
    """
    return task.difficulty * 10 - days_until(task.deadline)


def build_schedule(tasks):
    """Turn a list of Tasks into a list of study sessions.

    Each session is a dict: {"task", "date", "hours"}.
    Harder tasks get MORE sessions (one session per difficulty point),
    which is the "more frequent study sessions" part of the spec.
    """
    # 1. Sort tasks so the highest-priority ones come first.
    ordered = sorted(tasks, key=priority_score, reverse=True)

    sessions = []
    for task in ordered:
        # 2. Harder task -> more sessions. Difficulty 3 -> 3 sessions.
        num_sessions = task.difficulty

        for i in range(num_sessions):
            # 3. Spread sessions out: one per day starting today.
            session_date = datetime.now() + timedelta(days=i)

            sessions.append({
                "task": task.name,
                "date": session_date.date(),
                "hours": 1,  # placeholder - 1 hour per session for now
            })

    return sessions


def optimize_schedule(schedule):
    """Adjust an existing schedule to fit real-life limits.

    Stub for later: e.g. cap total hours per day, avoid overlaps, etc.
    Returning it unchanged for now so the rest of the app keeps working.
    """
    return schedule
