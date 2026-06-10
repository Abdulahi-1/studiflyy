from datetime import datetime, timedelta

from utils.time_utils import days_until


def priority_score(task):
    return task.difficulty * 10 - days_until(task.deadline)


def build_schedule(tasks):
    ordered = sorted(tasks, key=priority_score, reverse=True)

    sessions = []
    for task in ordered:
        num_sessions = task.difficulty

        for i in range(num_sessions):
            session_date = datetime.now() + timedelta(days=i)

            sessions.append({
                "task": task.name,
                "date": session_date.date(),
                "hours": 1,
            })

    return sessions


def optimize_schedule(schedule):
    return schedule
