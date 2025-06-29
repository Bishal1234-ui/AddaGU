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
- **🔐 End-to-end encryption** for secure messaging.

### 🛡️ Security Features

#### **Message Encryption**
- **Algorithm**: Fernet symmetric encryption (AES-128 + HMAC-SHA256)
- **All chat messages** are encrypted before being stored in the database
- **User-specific encryption keys** derived from user IDs using PBKDF2 (100,000 iterations)
- **Access control**: Only sender and receiver can decrypt and read messages
- **Message authentication**: Built-in protection against tampering
- **Transparent to users**: Chat interface works exactly as before with enhanced security

#### **Key Management**
- Master key configurable via environment variables for production
- Secure key derivation using PBKDF2 with SHA256
- Each user gets a unique encryption key
- Cross-user message access completely blocked

### Real-Time Features
- Powered by Django Channels for WebSocket-based real-time updates:
  - Instant updates for likes and comments.
  - Live chat functionality with encryption.

### Database
- **SQLite**: Used as the database for development purposes.
- **Encrypted storage**: All chat messages stored encrypted at rest.

---

## Tech Stack

### Backend
- **Django**: Framework used for backend logic and REST APIs.
- **Django Channels**: Enables real-time communication via WebSockets.
- **Cryptography**: Provides Fernet encryption for secure messaging.

### Frontend
- Built using Django templates and Bootstrap 5

### Database
- **SQLite**: Lightweight database for storing user data, posts, comments, and encrypted messages.

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

5. **Configure encryption (Optional for development):**
   ```bash
   # For production, set environment variable:
   export CHAT_MASTER_KEY="your-super-secure-key-here"
   ```

6. Run the development server ( in asgi ) :
   ```bash
   daphne -p 8001 GUBlogs.asgi:application
   ```

7. Access the application:
   Open your web browser and navigate to `http://127.0.0.1:8001/`.

---

## 🔐 Security Implementation

### Chat Encryption Details
- **Encryption at Rest**: All messages are encrypted in the database using Fernet symmetric encryption
- **Key Derivation**: PBKDF2 with SHA256, 100,000 iterations for computational hardening
- **Access Control**: Messages can only be decrypted by sender and receiver
- **Algorithm**: AES-128 in CBC mode with HMAC-SHA256 for authentication
- **Zero User Impact**: Encryption is completely transparent to end users

### Verification
To verify encryption is working:
1. Send a message in chat
2. Check database - messages will appear as encrypted base64 strings
3. View in chat interface - messages appear normally (auto-decrypted)

### Production Deployment
- Set `CHAT_MASTER_KEY` as environment variable
- Ensure HTTPS is enabled for secure transport
- All chat messages are automatically encrypted/decrypted

---

## 🚀 What Makes AddaGU Secure?

- **Privacy-First**: Messages are encrypted with industry-standard algorithms
- **University-Focused**: Designed specifically for Gauhati University students
- **Real-Time & Secure**: Live chat with end-to-end encryption
- **Transparent Security**: Enhanced protection without compromising user experience
- **Production-Ready**: Thoroughly tested encryption implementation

Your conversations are protected with the same level of encryption used by major messaging platforms! 🔐✨