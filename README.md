# AddaGU (আড্ডাGU)

> A secure social media platform exclusively for Gauhati University students

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AddaGU enables university students to connect, share content, and communicate through secure real-time messaging with end-to-end encryption.

## ✨ Key Features

- **🔐 Secure Messaging**: End-to-end encrypted chat with Fernet (AES-128 + HMAC-SHA256)
- **📱 Real-time Updates**: Live notifications for posts, comments, and messages via WebSockets
- **👤 User Management**: Custom authentication with profile management
- **📝 Social Features**: Create, share, and interact with posts, comments, and likes
- **🎨 Modern UI**: Responsive design built with Bootstrap 5

## 💻 Screennshots
<p align="center">
  <img src="https://github.com/user-attachments/assets/fb6af928-eff4-41d4-bf85-b11cdf237fe5" width="300"/>
  <img src="https://github.com/user-attachments/assets/b6b7e405-4bff-4fdb-98a3-fe8803b2b351" width="300"/>
  <br>
  <img src="https://github.com/user-attachments/assets/94909266-a1a0-4bae-98c1-b0c786737862" width="300"/>
  <img src="https://github.com/user-attachments/assets/f7a8c2e1-a6cd-483a-93d2-e8342bcede30" width="300"/>
</p>




## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 4.0+, Django Channels |
| **Frontend** | Django Templates, Bootstrap 5 |
| **Database** | SQLite3 (Development) |
| **Real-time** | WebSockets via Django Channels |
| **Security** | Fernet Encryption, PBKDF2 Key Derivation |

## 🔐 Security Architecture

- **Encryption Algorithm**: Fernet symmetric encryption (AES-128 + HMAC-SHA256)
- **Key Derivation**: PBKDF2 with SHA256, 100,000 iterations
- **Access Control**: Message-level encryption ensuring only sender/receiver access
- **Data Protection**: All chat messages encrypted at rest

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone and Setup**
   ```bash
   git clone https://github.com/Bishal1234-ui/AddaGU.git
   cd AddaGU
   python -m venv env
   env\Scripts\activate  # Windows
   # source env/bin/activate  # macOS/Linux
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   python manage.py migrate
   ```

4. **Environment Configuration** (Production)
   ```bash
   # Set encryption key for production
   set CHAT_MASTER_KEY=your-super-secure-key-here
   ```

5. **Run Application**
   ```bash
   daphne -p 8001 GUBlogs.asgi:application
   ```

6. **Access Application**
   Open http://127.0.0.1:8001/ in your browser

## � Development

### Project Structure
```
GUBlogs/
├── blogs/          # Blog post functionality
├── users/          # User management & authentication
├── GUBlogs/        # Main project settings
├── media/          # User uploaded content
└── staticfiles/    # Static assets
```

### Testing Encryption
1. Send a test message in chat
2. Check database - messages appear as encrypted base64 strings
3. Verify decryption works in chat interface

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support and questions:
- Create an [issue](https://github.com/Bishal1234-ui/AddaGU/issues)
- Contact: [Your Contact Information]

---

<div align="center">
<b>Built with ❤️ for Gauhati University students</b>
</div>
