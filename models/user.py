# models/user.py
from models.post import Post


class User:
    """
    Entity representing a User.
    A user can have multiple posts.
    """
    def __init__(self, user_id: int, name: str, email: str, posts=None):
        self.id = user_id
        self.name = name
        self.email = email
        self.posts = posts if posts else []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "posts": [p.to_dict() for p in self.posts]
        }
