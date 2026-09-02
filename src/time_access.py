from datetime import datetime, time
from zoneinfo import ZoneInfo

IST = ZoneInfo('Asia/Kolkata')

def now_ist():
    return datetime.now(IST)

def is_within_window(start_hour, start_minute, end_hour, end_minute, dt=None):
    dt = dt or now_ist()
    current = dt.time()
    return time(start_hour, start_minute) <= current <= time(end_hour, end_minute)
