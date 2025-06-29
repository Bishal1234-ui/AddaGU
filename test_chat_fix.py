#!/usr/bin/env python
"""
Test script to verify chat functionality with encryption.
This script creates test users and messages to verify the complete chat flow.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GUBlogs.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import ChatMessage
from users.encryption import encrypt_for_user, decrypt_for_user

User = get_user_model()


def test_chat_with_encryption():
    """
    Test the complete chat flow with encryption.
    """
    print("Testing Chat Functionality with Encryption")
    print("=" * 45)
    
    # Get or create test users
    try:
        user1 = User.objects.get(username='testuser1')
        user2 = User.objects.get(username='testuser2')
        print("✅ Using existing test users")
    except User.DoesNotExist:
        print("Creating test users...")
        user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        user2 = User.objects.create_user(
            username='testuser2', 
            email='test2@example.com',
            password='testpass123'
        )
        print("✅ Test users created")
    
    # Test messages
    test_messages = [
        ("Hello! How are you?", user1, user2),
        ("I'm doing great, thank you! How about you?", user2, user1),
        ("Excellent! Want to study together later?", user1, user2),
        ("Sure! Let's meet at the library at 3 PM.", user2, user1),
        ("Perfect! See you there! 📚", user1, user2)
    ]
    
    print(f"\nTesting with {len(test_messages)} messages...")
    print("-" * 30)
    
    created_messages = []
    
    # Create and save encrypted messages
    for i, (message_text, sender, receiver) in enumerate(test_messages, 1):
        print(f"[{i}] Creating message from {sender.username} to {receiver.username}")
        print(f"    Original: {message_text}")
        
        # Create message using model method
        chat_message = ChatMessage(sender=sender, receiver=receiver)
        chat_message.set_message(message_text)
        chat_message.save()
        
        print(f"    Stored as: {chat_message.message[:50]}..." if len(chat_message.message) > 50 else f"    Stored as: {chat_message.message}")
        
        # Verify sender can decrypt
        decrypted_for_sender = chat_message.get_message_for_user(sender)
        print(f"    Sender sees: {decrypted_for_sender}")
        
        # Verify receiver can decrypt  
        decrypted_for_receiver = chat_message.get_message_for_user(receiver)
        print(f"    Receiver sees: {decrypted_for_receiver}")
        
        # Verify message integrity
        if message_text == decrypted_for_sender == decrypted_for_receiver:
            print("    ✅ Message encrypted and decrypted successfully!")
        else:
            print("    ❌ Message encryption/decryption failed!")
        
        created_messages.append(chat_message)
        print()
    
    # Test conversation retrieval (like in chat view)
    print("Testing conversation retrieval...")
    print("-" * 30)
    
    conversation = ChatMessage.objects.filter(
        sender__in=[user1, user2],
        receiver__in=[user1, user2]
    ).order_by('timestamp')
    
    print(f"Found {conversation.count()} messages in conversation")
    
    # Simulate what happens in the chat view
    print("\nAs seen by user1:")
    last_messages = list(conversation)[-3:]  # Convert to list first
    for msg in last_messages:
        decrypted = msg.get_message_for_user(user1)
        direction = "sent" if msg.sender == user1 else "received"
        print(f"  [{direction}] {decrypted}")
    
    print("\nAs seen by user2:")
    for msg in last_messages:
        decrypted = msg.get_message_for_user(user2)
        direction = "sent" if msg.sender == user2 else "received"
        print(f"  [{direction}] {decrypted}")
    
    # Test access control
    print("\nTesting access control...")
    print("-" * 30)
    
    try:
        # Create a third user
        user3 = User.objects.create_user(
            username='testuser3',
            email='test3@example.com', 
            password='testpass123'
        )
        
        # Try to access conversation as user3
        test_message = created_messages[0]
        decrypted_by_outsider = test_message.get_message_for_user(user3)
        
        if decrypted_by_outsider == "[Access denied]":
            print("✅ Access control working - outsider cannot read messages")
        else:
            print(f"❌ Access control failed - outsider read: {decrypted_by_outsider}")
            
    except Exception as e:
        print(f"Access control test error: {e}")
    
    # Cleanup test data
    print("\nCleaning up test data...")
    for msg in created_messages:
        msg.delete()
    
    # Only delete test users if we created them in this session
    try:
        if 'user3' in locals():
            user3.delete()
    except:
        pass
    
    print("✅ Test data cleaned up")
    print("\n" + "=" * 45)
    print("Chat encryption test completed successfully!")


if __name__ == "__main__":
    test_chat_with_encryption()
