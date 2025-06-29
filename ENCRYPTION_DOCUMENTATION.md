# Chat Encryption Implementation

## Overview

This document describes the implementation of end-to-end encryption for the chat functionality in AddaGU (আড্ডাGU). The system uses Fernet symmetric encryption from the `cryptography` library to secure all chat messages.

## Security Features

### 1. Secure Encryption Algorithm
- **Algorithm**: Fernet symmetric encryption (AES 128 in CBC mode with HMAC SHA256 for authentication)
- **Key Derivation**: PBKDF2 with SHA256, 100,000 iterations
- **Authentication**: Built-in message authentication to prevent tampering

### 2. User-Specific Keys
- Each user has a unique encryption key derived from their user ID
- Messages are encrypted with the sender's key
- Both sender and receiver can decrypt messages using the same key derivation process

### 3. Master Key Security
- A master key is used as the base for all user key derivations
- In development: Configurable via Django settings
- In production: Should be stored in environment variables

## Implementation Details

### File Structure
```
users/
├── encryption.py          # Core encryption functionality
├── models.py             # Updated ChatMessage model with encryption methods
└── views.py              # Updated chat view with decryption

GUBlogs/
├── settings.py           # Added CHAT_MASTER_KEY setting
└── consumers.py          # Updated WebSocket consumer for encryption

tests/
├── test_encryption.py           # Encryption system tests
└── test_encryption_update.py    # Migration script for existing messages
```

### Core Components

#### 1. ChatEncryption Class (`users/encryption.py`)
```python
class ChatEncryption:
    @staticmethod
    def encrypt_message(message, user_id)
    @staticmethod  
    def decrypt_message(encrypted_message, user_id)
    @staticmethod
    def can_decrypt_message(encrypted_message, user_id)
```

#### 2. ChatMessage Model Updates (`users/models.py`)
```python
class ChatMessage(models.Model):
    def set_message(self, plain_message)        # Encrypts and stores message
    def get_message_for_user(self, user)        # Decrypts message for specific user
    def get_plain_message(self)                 # Decrypts using sender's key
```

#### 3. WebSocket Consumer Updates (`GUBlogs/consumers.py`)
- Messages are encrypted before saving to database
- Real-time messages remain unencrypted during transmission (only encrypted at rest)

## How It Works

### Message Sending Process
1. User types a message in the chat interface
2. Message is sent via WebSocket to the server
3. Server encrypts the message using sender's derived key
4. Encrypted message is stored in the database
5. Message is broadcast to chat participants (unencrypted for real-time display)

### Message Loading Process
1. When chat is loaded, encrypted messages are retrieved from database
2. Each message is decrypted using the appropriate user's key
3. Decrypted messages are displayed in the chat interface

### Key Derivation Process
1. Master key is retrieved from Django settings
2. User ID is used as salt (padded to 16 bytes)
3. PBKDF2 with SHA256 derives a unique key for each user
4. Same process is used for both encryption and decryption

## Security Considerations

### Strengths
- **At-rest encryption**: All messages are encrypted in the database
- **User isolation**: Each user has a unique encryption key
- **Authentication**: Fernet provides built-in message authentication
- **Key derivation**: Strong PBKDF2 with high iteration count

### Current Limitations
- **In-transit encryption**: Messages are sent unencrypted over WebSocket (mitigated by HTTPS)
- **Shared access**: Both sender and receiver use the same key (sender's key)
- **Key management**: Master key is stored in application settings

### Recommended Improvements for Production
1. **Environment Variables**: Store master key in environment variables
2. **Key Rotation**: Implement periodic key rotation
3. **WebSocket Encryption**: Add client-side encryption for WebSocket messages
4. **Separate Keys**: Use different keys for sender and receiver with key exchange
5. **Hardware Security**: Use HSM or key management service for master key

## Installation and Setup

### 1. Install Dependencies
```bash
pip install cryptography>=41.0.0
```

### 2. Update Settings
Add to your Django settings:
```python
CHAT_MASTER_KEY = os.environ.get('CHAT_MASTER_KEY', 'your-master-key-here')
```

### 3. Migrate Existing Messages
Run the migration script to encrypt existing messages:
```bash
python test_encryption_update.py
```

### 4. Test the System
Run the test suite to verify encryption works:
```bash
python test_encryption.py
```

## Usage Examples

### Encrypting a Message
```python
from users.encryption import encrypt_for_user

message = "Hello, this is a secret message!"
user_id = 1
encrypted = encrypt_for_user(message, user_id)
```

### Decrypting a Message
```python
from users.encryption import decrypt_for_user

decrypted = decrypt_for_user(encrypted, user_id)
```

### Using Model Methods
```python
# Create and save encrypted message
chat_message = ChatMessage(sender=sender, receiver=receiver)
chat_message.set_message("Hello there!")
chat_message.save()

# Retrieve and decrypt message
decrypted = chat_message.get_message_for_user(request.user)
```

## Testing

### Automated Tests
- `test_encryption.py`: Comprehensive encryption/decryption tests
- Tests cross-user decryption prevention
- Verifies message integrity
- Tests all encryption class methods

### Manual Testing
1. Send a message in the chat
2. Check database - message should be encrypted (base64-encoded)
3. Reload chat - message should display decrypted
4. Try accessing from different user - should show appropriate access control

## Troubleshooting

### Common Issues

#### "Message could not be decrypted"
- Check if the user has permission to view the message
- Verify the message was encrypted with the correct key
- Ensure the master key hasn't changed

#### Encryption Errors
- Verify cryptography library is installed
- Check that the master key is properly configured
- Ensure user IDs are valid integers

#### Performance Issues
- Consider caching decrypted messages for active chats  
- Monitor database performance with encryption overhead
- Implement message pagination for large chat histories

## Production Deployment Checklist

- [ ] Set `CHAT_MASTER_KEY` as environment variable
- [ ] Ensure HTTPS is enabled for all connections
- [ ] Test encryption/decryption with production data
- [ ] Monitor performance and database load
- [ ] Set up key rotation procedures
- [ ] Configure proper backup procedures for encrypted data
- [ ] Test recovery procedures

## Conclusion

This encryption implementation provides a solid foundation for secure chat messaging in AddaGU. While there are areas for improvement (especially around key management and in-transit encryption), the current system effectively protects messages at rest and provides user-specific access control.

The modular design allows for future enhancements without major architectural changes, making it a scalable solution for the application's security needs.
