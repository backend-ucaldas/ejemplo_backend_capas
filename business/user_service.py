# business/user_service.py
from models.user import User
from models.post import Post
from dataaccess.user_repository import UserRepository


class UserService:
    """
    Business layer: rules and operations for Users and Posts.
    """

    @staticmethod
    def get_all_users():
        return UserRepository.load_data()

    @staticmethod
    def get_user_by_id(user_id: int):
        users = UserRepository.load_data()
        return next((u for u in users if u.id == user_id), None)

    @staticmethod
    def create_user(name: str, email: str):
        users = UserRepository.load_data()
        new_id = max([u.id for u in users], default=0) + 1
        new_user = User(new_id, name, email)
        users.append(new_user)
        UserRepository.save_data(users)
        return new_user

    @staticmethod
    def update_user(user_id: int, name: str = None, email: str = None):
        users = UserRepository.load_data()
        user = next((u for u in users if u.id == user_id), None)
        if not user:
            return None
        if name:
            user.name = name
        if email:
            user.email = email
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
