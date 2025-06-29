"""
Encryption utilities for chat messages.
Uses Fernet symmetric encryption from the cryptography library.
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings


class ChatEncryption:
    """
    Handles encryption and decryption of chat messages using Fernet symmetric encryption.
    Each user has their own encryption key derived from their user ID and a master key.
    """
    
    @staticmethod
    def _get_master_key():
        """Get or create the master encryption key."""
        master_key = getattr(settings, 'CHAT_MASTER_KEY', None)
        if not master_key:
            # Generate a new master key if it doesn't exist
            master_key = Fernet.generate_key().decode()
            # In production, store this securely in environment variables
            settings.CHAT_MASTER_KEY = master_key
        return master_key.encode()
    
    @staticmethod
    def _derive_user_key(user_id):
        """Derive a unique encryption key for each user based on their ID."""
        master_key = ChatEncryption._get_master_key()
        
        # Use user ID as salt (convert to bytes and pad to 16 bytes)
        salt = str(user_id).encode().ljust(16, b'0')[:16]
        
        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key))
        return key
    
    @staticmethod
    def encrypt_message(message, user_id):
        """
        Encrypt a message for a specific user.
        
        Args:
            message (str): The message to encrypt
            user_id (int): The user ID to derive the key from
        
        Returns:
            str: Base64 encoded encrypted message
        """
        try:
            key = ChatEncryption._derive_user_key(user_id)
            fernet = Fernet(key)
            encrypted_message = fernet.encrypt(message.encode())
            return base64.b64encode(encrypted_message).decode()
        except Exception as e:
            # Log the error in production
            print(f"Encryption error: {e}")
            return message  # Return original message if encryption fails
    
    @staticmethod
    def decrypt_message(encrypted_message, user_id):
        """
        Decrypt a message for a specific user.
        
        Args:
            encrypted_message (str): Base64 encoded encrypted message
            user_id (int): The user ID to derive the key from
        
        Returns:
            str: Decrypted message
        """
        try:
            key = ChatEncryption._derive_user_key(user_id)
            fernet = Fernet(key)
            encrypted_bytes = base64.b64decode(encrypted_message.encode())
            decrypted_message = fernet.decrypt(encrypted_bytes).decode()
            return decrypted_message
        except Exception as e:
            # Log the error in production
            print(f"Decryption error: {e}")
            return "[Message could not be decrypted]"
    
    @staticmethod
    def can_decrypt_message(encrypted_message, user_id):
        """
        Check if a user can decrypt a message (useful for validation).
        
        Args:
            encrypted_message (str): Base64 encoded encrypted message
            user_id (int): The user ID to check
        
        Returns:
            bool: True if user can decrypt the message
        """
        try:
            decrypted = ChatEncryption.decrypt_message(encrypted_message, user_id)
            return decrypted != "[Message could not be decrypted]"
        except:
            return False


# Convenience functions for easier usage
def encrypt_for_user(message, user_id):
    """Encrypt a message for a specific user."""
    return ChatEncryption.encrypt_message(message, user_id)


def decrypt_for_user(encrypted_message, user_id):
    """Decrypt a message for a specific user."""
    return ChatEncryption.decrypt_message(encrypted_message, user_id)
