# AddaGU (আড্ডাGU)

AddaGU (আড্ডাGU) is a social media application designed exclusively for the students of Gauhati University. This platform fosters connectivity and interaction, enabling users to create, share, and engage with content while building a vibrant university community.

---

## Features

### User Authentication
- Custom user model.
- User registration and login.
- Profile management.

### Posts
- Create, view, edit, and delete posts.
- Upload and share posts with text and images.

### Comments
- Add comments to posts.
- Real-time updates for new comments using WebSockets.
- Delete comments.

### Likes
- Like and unlike posts.
- Real-time updates for likes using WebSockets.
- View the total likes on posts.

### Chat
- Real-time chat functionality between users powered by WebSockets.

### Real-Time Features
- Powered by Django Channels for WebSocket-based real-time updates:
  - Instant updates for likes and comments.
  - Live chat functionality.

### Database
- **SQLite**: Used as the database for development purposes.

---

## Tech Stack

### Backend
- **Django**: Framework used for backend logic and REST APIs.
- **Django Channels**: Enables real-time communication via WebSockets.

### Frontend
- Built using Django templates and Bootstrap 5

### Database
- **SQLite**: Lightweight database for storing user data, posts, comments, and likes.

---

## Installation

### Prerequisites
- Python (3.x)
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Bishal1234-ui/AddaGU.git
   cd AddaGU
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server ( in asgi ) :
   ```bash
   daphne -p 8000 GUBlogs.asgi:application
   ```

6. Access the application:
   Open your web browser and navigate to `http://127.0.0.1:8000/`.





