#!/usr/bin/env python
"""
Test script for chat encryption functionality.
This script tests the encryption and decryption of chat messages.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GUBlogs.settings')
django.setup()

from users.encryption import ChatEncryption, encrypt_for_user, decrypt_for_user


def test_encryption():
    """Test the encryption and decryption functionality."""
    print("Testing Chat Encryption System")
    print("=" * 40)
    
    # Test data
    test_messages = [
        "Hello, how are you doing today?",
        "This is a secret message! 🔒",
        "Let's meet at the library at 3 PM.",
        "Can you help me with the assignment?",
        "Great job on your presentation! 👏"
    ]
    
    test_user_ids = [1, 2, 3]
    
    print("1. Testing basic encryption/decryption:")
    for user_id in test_user_ids:
        for message in test_messages[:2]:  # Test first 2 messages
            print(f"\nUser ID: {user_id}")
            print(f"Original: {message}")
            
            # Encrypt message
            encrypted = encrypt_for_user(message, user_id)
            print(f"Encrypted: {encrypted[:50]}..." if len(encrypted) > 50 else f"Encrypted: {encrypted}")
            
            # Decrypt message
            decrypted = decrypt_for_user(encrypted, user_id)
            print(f"Decrypted: {decrypted}")
            
            # Verify integrity
            if message == decrypted:
                print("✅ Encryption/Decryption successful!")
            else:
                print("❌ Encryption/Decryption failed!")
            print("-" * 30)
    
    print("\n2. Testing cross-user decryption (should fail):")
    message = "This is a private message"
    user1_id = 1
    user2_id = 2
    
    # Encrypt for user 1
    encrypted_for_user1 = encrypt_for_user(message, user1_id)
    print(f"Message encrypted for User {user1_id}: {message}")
    
    # Try to decrypt with user 2's key (should fail)
    try:
        decrypted_by_user2 = decrypt_for_user(encrypted_for_user1, user2_id)
        print(f"User {user2_id} decryption result: {decrypted_by_user2}")
        if decrypted_by_user2 == "[Message could not be decrypted]":
            print("✅ Cross-user decryption properly blocked!")
        else:
            print("❌ Security breach: Cross-user decryption succeeded!")
    except Exception as e:
        print(f"✅ Cross-user decryption properly blocked with exception: {e}")
    
    print("\n3. Testing ChatEncryption class methods:")
    chat_encryption = ChatEncryption()
    
    test_message = "Testing class methods"
    user_id = 1
    
    encrypted = chat_encryption.encrypt_message(test_message, user_id)
    decrypted = chat_encryption.decrypt_message(encrypted, user_id)
    can_decrypt = chat_encryption.can_decrypt_message(encrypted, user_id)
    
    print(f"Original: {test_message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Can decrypt: {can_decrypt}")
    
    if test_message == decrypted and can_decrypt:
        print("✅ ChatEncryption class methods working correctly!")
    else:
        print("❌ ChatEncryption class methods failed!")
    
    print("\n" + "=" * 40)
    print("Encryption system test completed!")


if __name__ == "__main__":
    test_encryption()
