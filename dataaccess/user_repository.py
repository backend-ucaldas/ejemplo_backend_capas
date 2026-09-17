# dataaccess/user_repository.py
import json
import os
from models.user import User
from models.post import Post

DATA_FILE = "data.json"


class UserRepository:
    """
    Data access layer: reads and writes Users and Posts to JSON.
    """

    @staticmethod
    def load_data():
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r") as f:
            try:
                raw_data = json.load(f)
                users = []
                for u in raw_data:
                    posts = [Post(p["id"], p["title"], p["content"]) for p in u.get("posts", [])]
                    users.append(User(u["id"], u["name"], u["email"], posts))
                return users
            except json.JSONDecodeError:
                return []

    @staticmethod
    def save_data(users):
        with open(DATA_FILE, "w") as f:
            json.dump([u.to_dict() for u in users], f, indent=4)
