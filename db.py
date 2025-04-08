from tinydb import TinyDB, Query
from datetime import datetime, timedelta

db = TinyDB("users.json")
User = Query()

def add_user(user_id):
    if not db.contains(User.user_id == user_id):
        db.insert({
            "user_id": user_id,
            "is_premium": False,
            "downloads": 0,
            "last_reset": str(datetime.now()),
            "premium_expiry": ""
        })

def make_premium(user_id, days):
    expiry = datetime.now() + timedelta(days=days)
    db.update({
        "is_premium": True,
        "premium_expiry": str(expiry)
    }, User.user_id == user_id)

def check_premium(user_id):
    user = db.get(User.user_id == user_id)
    if user and user["is_premium"]:
        expiry = datetime.strptime(user["premium_expiry"], "%Y-%m-%d %H:%M:%S.%f")
        if datetime.now() > expiry:
            db.update({"is_premium": False, "premium_expiry": ""}, User.user_id == user_id)
            return False
        return True
    return False

def get_downloads(user_id):
    user = db.get(User.user_id == user_id)
    if user:
        return user["downloads"]
    return 0

def increase_download(user_id):
    db.update({"downloads": get_downloads(user_id) + 1}, User.user_id == user_id)

def reset_daily_limits():
    now = datetime.now().date()
    for user in db:
        last_reset = datetime.strptime(user["last_reset"], "%Y-%m-%d %H:%M:%S.%f").date()
        if now != last_reset:
            db.update({"downloads": 0, "last_reset": str(datetime.now())}, User.user_id == user["user_id"])
