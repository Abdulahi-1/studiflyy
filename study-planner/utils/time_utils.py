from datetime import datetime

def days_until(deadline: datetime) -> int:
    return (deadline - datetime.now()).days
