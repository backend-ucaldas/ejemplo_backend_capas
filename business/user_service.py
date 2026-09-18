# business/user_service.py
import re
from models.user import User
from models.post import Post
from dataaccess.user_repository import UserRepository

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UserService:
    """
    Business layer: rules and operations for Users and Posts.
    """

    @staticmethod
    def _validate_name(name: str):
        if not name or not name.strip():
            raise ValueError("Name is required")
        if len(name.strip()) < 2 or len(name.strip()) > 100:
            raise ValueError("Name must be between 2 and 100 characters")

    @staticmethod
    def _validate_email(email: str):
        if not email or not email.strip():
            raise ValueError("Email is required")
        if not EMAIL_REGEX.match(email.strip()):
            raise ValueError("Email format is invalid")

    @staticmethod
    def _validate_email_unique(users, email: str, exclude_user_id: int = None):
        for u in users:
            if u.email.lower() == email.strip().lower() and u.id != exclude_user_id:
                raise ValueError("Email is already in use")

    @staticmethod
    def get_all_users():
        return UserRepository.load_data()

    @staticmethod
    def get_user_by_id(user_id: int):
        users = UserRepository.load_data()
        return next((u for u in users if u.id == user_id), None)

    @staticmethod
    def create_user(name: str, email: str):
        UserService._validate_name(name)
        UserService._validate_email(email)
        users = UserRepository.load_data()
        UserService._validate_email_unique(users, email)
        new_id = max([u.id for u in users], default=0) + 1
        new_user = User(new_id, name.strip(), email.strip())
        users.append(new_user)
        UserRepository.save_data(users)
        return new_user

    @staticmethod
    def update_user(user_id: int, name: str = None, email: str = None):
        users = UserRepository.load_data()
        user = next((u for u in users if u.id == user_id), None)
        if not user:
            return None
        if name is not None:
            UserService._validate_name(name)
            user.name = name.strip()
        if email is not None:
            UserService._validate_email(email)
            UserService._validate_email_unique(users, email, exclude_user_id=user_id)
            user.email = email.strip()
        UserRepository.save_data(users)
        return user

    @staticmethod
    def delete_user(user_id: int):
        users = UserRepository.load_data()
        user = next((u for u in users if u.id == user_id), None)
        if not user:
            return False
        users = [u for u in users if u.id != user_id]
        UserRepository.save_data(users)
        return True

    @staticmethod
    def add_post(user_id: int, title: str, content: str):
        users = UserRepository.load_data()
        user = next((u for u in users if u.id == user_id), None)
        if not user:
            return None
        new_id = max([p.id for p in user.posts], default=0) + 1
        new_post = Post(new_id, title, content)
        user.posts.append(new_post)
        UserRepository.save_data(users)
        return new_post
