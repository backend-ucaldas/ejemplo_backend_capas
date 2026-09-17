# models/post.py

class Post:
    """
    Entity representing a blog post.
    Each post belongs to a User.
    """
    def __init__(self, post_id: int, title: str, content: str):
        self.id = post_id
        self.title = title
        self.content = content

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }
