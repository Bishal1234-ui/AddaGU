#!/usr/bin/env python
"""
Test script to verify chat list shows decrypted messages properly
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GUBlogs.settings')
django.setup()

from users.models import CustomUser, ChatMessage
from django.utils import timezone

def test_chat_list_display():
    """Test that chat list shows decrypted messages instead of encrypted ones"""
    
    # Get or create test users and make them follow each other
    try:
        user1 = CustomUser.objects.get(username='alice_chat_list')
    except CustomUser.DoesNotExist:
        user1 = CustomUser.objects.create_user(
            username='alice_chat_list',
            email='alice_chat_list@test.com',
            password='testpass123'
        )
    
    try:
        user2 = CustomUser.objects.get(username='bob_chat_list')
    except CustomUser.DoesNotExist:
        user2 = CustomUser.objects.create_user(
            username='bob_chat_list',
            email='bob_chat_list@test.com',
            password='testpass123'
        )
    
    # Make them follow each other so they can chat
    user1.following.add(user2)
    user2.following.add(user1)
    
    # Test message
    test_message = "Hey! This is a secret message for the chat list test 🚀"
    
    print("=" * 60)
    print("CHAT LIST DISPLAY TEST")
    print("=" * 60)
    print(f"Test message: '{test_message}'")
    
    # Create and save encrypted message
    chat_message = ChatMessage(
        sender=user1,
        receiver=user2,
        timestamp=timezone.now()
    )
    chat_message.set_message(test_message)
    chat_message.save()
    
    print(f"✓ Message saved with encryption: {chat_message.is_encrypted}")
    print(f"✓ Encrypted in DB: {chat_message.message != test_message}")
    
    # Test the get_conversations method for user2 (receiver)
    conversations = user2.get_conversations()
    
    if conversations:
        conversation = conversations[0]  # Should be the conversation with user1
        
        print(f"\n📋 Chat List Results for {user2.username}:")
        print(f"   Conversation with: {conversation['user'].username}")
        print(f"   Raw message in DB: {conversation['latest_message'].message[:50]}...")
        print(f"   Message preview for list: {conversation['message_preview']}")
        print(f"   Preview matches original: {conversation['message_preview'] == test_message}")
        
        if conversation['message_preview'] == test_message:
            print("   ✅ SUCCESS: Chat list shows decrypted message!")
        else:
            print("   ❌ FAILED: Chat list still shows encrypted message!")
            return False
    else:
        print("❌ No conversations found!")
        return False
    
    # Test the get_conversations method for user1 (sender)
    conversations_sender = user1.get_conversations()
    
    if conversations_sender:
        conversation_sender = conversations_sender[0]
        
        print(f"\n📋 Chat List Results for {user1.username} (sender):")
        print(f"   Conversation with: {conversation_sender['user'].username}")
        print(f"   Message preview for list: {conversation_sender['message_preview']}")
        print(f"   Preview matches original: {conversation_sender['message_preview'] == test_message}")
        
        if conversation_sender['message_preview'] == test_message:
            print("   ✅ SUCCESS: Chat list shows decrypted message for sender too!")
        else:
            print("   ❌ FAILED: Chat list shows encrypted message for sender!")
            return False
    
    # Clean up
    chat_message.delete()
    user1.following.remove(user2)
    user2.following.remove(user1)
    
    print(f"\n🧹 Cleaned up test data")
    print("=" * 60)
    print("🎉 CHAT LIST DISPLAY TEST PASSED!")
    print("Chat list will now show readable messages instead of encrypted text.")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_chat_list_display()
        if success:
            print("\n✅ Chat list display test completed successfully!")
        else:
            print("\n❌ Chat list display test failed!")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()
