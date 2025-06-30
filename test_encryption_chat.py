#!/usr/bin/env python
"""
Test script to verify chat message encryption is working properly
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GUBlogs.settings')
django.setup()

from users.models import CustomUser, ChatMessage
from django.utils import timezone

def test_chat_encryption():
    """Test that chat messages are properly encrypted when saved"""
    
    # Get or create test users
    try:
        user1 = CustomUser.objects.get(username='testuser1')
    except CustomUser.DoesNotExist:
        user1 = CustomUser.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
    
    try:
        user2 = CustomUser.objects.get(username='testuser2')
    except CustomUser.DoesNotExist:
        user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
    
    # Test message
    test_message = "This is a secret test message! 🔐"
    
    # Create a chat message using the model's encryption method
    chat_message = ChatMessage(
        sender=user1,
        receiver=user2,
        timestamp=timezone.now()
    )
    
    # Use the set_message method to encrypt
    chat_message.set_message(test_message)
    chat_message.save()
    
    # Retrieve the message from database
    saved_message = ChatMessage.objects.get(id=chat_message.id)
    
    print("=" * 50)
    print("ENCRYPTION TEST RESULTS")
    print("=" * 50)
    print(f"Original message: {test_message}")
    print(f"Stored in database (message field): {saved_message.message}")
    print(f"Is encrypted flag: {saved_message.is_encrypted}")
    print(f"Decrypted message (get_display_message): {saved_message.get_display_message()}")
    print(f"Decrypted message (get_message_for_user sender): {saved_message.get_message_for_user(user1)}")
    print(f"Decrypted message (get_message_for_user receiver): {saved_message.get_message_for_user(user2)}")
    
    # Check if encryption worked
    if saved_message.message != test_message:
        print("✅ SUCCESS: Message is encrypted in database!")
    else:
        print("❌ FAILED: Message is stored as plain text in database!")
    
    # Check if decryption worked
    if saved_message.get_display_message() == test_message:
        print("✅ SUCCESS: Message can be decrypted correctly!")
    else:
        print("❌ FAILED: Message decryption failed!")
    
    print("=" * 50)
    
    # Clean up test message
    saved_message.delete()
    
    return saved_message.message != test_message and saved_message.get_display_message() == test_message

if __name__ == "__main__":
    success = test_chat_encryption()
    if success:
        print("🎉 All tests passed! Encryption is working correctly.")
    else:
        print("💥 Tests failed! Check the encryption implementation.")
