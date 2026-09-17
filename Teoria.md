## Arquitectura por capas

La **arquitectura por capas** es un estilo de diseño de software que organiza una aplicación en diferentes **niveles (capas)**, cada uno con responsabilidades bien definidas.
Su objetivo es **separar preocupaciones**, mejorar la **mantenibilidad**, **escalabilidad** y permitir que los cambios en una capa no afecten directamente a las demás.

---

### 🔹 Capas principales

1. **Capa de Presentación (Presentation Layer)**

   * Es la **interfaz de usuario** o la **API** que interactúa con el mundo externo.
   * Se encarga de recibir peticiones, validarlas y devolver respuestas.
   * Ejemplo: Un sitio web, una aplicación móvil, o un servicio **Flask** que expone endpoints REST.

2. **Capa de Negocio (Business Layer o Domain Layer)**

   * Contiene la **lógica de negocio** y las **reglas** que definen el comportamiento de la aplicación / **lógica de los casos de uso**.
   * Procesa la información recibida, aplica validaciones, reglas o cálculos.
   * Ejemplo: creación de un usuario, validación de un correo, asignación de un ID, manejo de posts asociados.

3. **Capa de Acceso a Datos (Data Access Layer)**

   * Se encarga de la **persistencia de los datos**, ya sea en archivos, bases de datos SQL/NoSQL, APIs externas, etc.
   * Proporciona métodos para **guardar, leer, actualizar o eliminar** la información.
   * Ejemplo: un repositorio que guarda usuarios en un archivo JSON o en una base de datos MySQL.

4. **Capa de Modelos o Entidades (Models Layer)**

   * Define las **estructuras de datos** con las que trabaja la aplicación.
   * Representa los objetos principales (ejemplo: `User`, `Post`).
   * Generalmente esta capa se usa como soporte en las demás.

---

### 🔹 Ventajas de la arquitectura por capas

* ✅ **Separación de responsabilidades** → cada capa tiene una función clara.
* ✅ **Mantenibilidad** → facilita modificaciones sin romper todo el sistema.
* ✅ **Reusabilidad** → la lógica de negocio puede ser usada por diferentes interfaces (web, móvil, API).
* ✅ **Escalabilidad** → permite crecer el sistema organizadamente.

---

👉 En el caso de ejemplo encontraremos:

* **Presentation**: carpeta `presentation` con Flask (`app.py`).
* **Business**: carpeta `business` con `user_service.py`.
* **Data Access**: carpeta `dataaccess` con `user_repository.py`.
* **Models**: carpeta `models` con `user.py` y `post.py`.

---

```
app/
│
├── presentation/
│   └── app.py                  # Flask routes (capa de presentación)
│
├── business/
│   └── user_service.py         # Lógica de negocio
│
├── dataaccess/
│   └── user_repository.py      # Acceso a datos (JSON)
│
├── models/
│   ├── user.py                 # Clase User
│   └── post.py                 # Clase Post
│
└── data.json                   # Persistencia
```

---

### 🔹 `models/user.py`

```python
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
```

---

### 🔹 `models/post.py`

```python
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
```

---

### 🔹 `dataaccess/user_repository.py`

```python
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
```

---

### 🔹 `business/user_service.py`

```python
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
```

---

### 🔹 `presentation/app.py`

```python
# presentation/app.py
from flask import Flask, request, jsonify
from business.user_service import UserService

app = Flask(__name__)

# --- User endpoints ---

@app.route("/users", methods=["GET"])
def get_users():
    users = UserService.get_all_users()
    return jsonify([u.to_dict() for u in users]), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"message": "Name and email are required"}), 400
    user = UserService.create_user(data["name"], data["email"])
    return jsonify(user.to_dict()), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = UserService.update_user(user_id, data.get("name"), data.get("email"))
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = UserService.delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404


# --- Post endpoints ---

@app.route("/users/<int:user_id>/posts", methods=["POST"])
def add_post(user_id):
    data = request.get_json()
    if not data.get("title") or not data.get("content"):
        return jsonify({"message": "Title and content are required"}), 400
    post = UserService.add_post(user_id, data["title"], data["content"])
    if post:
        return jsonify(post.to_dict()), 201
    return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
```
