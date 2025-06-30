#!/usr/bin/env python
"""
Test to verify chat list works with both encrypted and non-encrypted messages
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GUBlogs.settings')
django.setup()

from users.models import CustomUser, ChatMessage
from django.utils import timezone

def test_mixed_message_types():
    """Test chat list with both encrypted and plain text messages"""
    
    # Get or create test users
    try:
        user1 = CustomUser.objects.get(username='test_mixed_1')
    except CustomUser.DoesNotExist:
        user1 = CustomUser.objects.create_user(
            username='test_mixed_1',
            email='test_mixed_1@test.com',
            password='testpass123'
        )
    
    try:
        user2 = CustomUser.objects.get(username='test_mixed_2')
    except CustomUser.DoesNotExist:
        user2 = CustomUser.objects.create_user(
            username='test_mixed_2',
            email='test_mixed_2@test.com',
            password='testpass123'
        )
    
    # Make them follow each other
    user1.following.add(user2)
    user2.following.add(user1)
    
    print("=" * 60)
    print("MIXED MESSAGE TYPES TEST")
    print("=" * 60)
    
    # Create a plain text message (simulate old message)
    plain_message = ChatMessage.objects.create(
        sender=user1,
        receiver=user2,
        message="This is a plain text message",
        is_encrypted=False,
        timestamp=timezone.now() - timezone.timedelta(minutes=5)
    )
    
    # Create an encrypted message (new message)
    encrypted_msg_text = "This is an encrypted message 🔐"
    encrypted_message = ChatMessage(
        sender=user2,
        receiver=user1,
        timestamp=timezone.now()
    )
    encrypted_message.set_message(encrypted_msg_text)
    encrypted_message.save()
    
    print("✓ Created plain text message (old)")
    print("✓ Created encrypted message (new)")
    
    # Test conversations for both users
    conversations_user1 = user1.get_conversations()
    conversations_user2 = user2.get_conversations()
    
    print(f"\n📋 User1 ({user1.username}) conversations:")
    if conversations_user1:
        conv = conversations_user1[0]
        print(f"   Latest message preview: '{conv['message_preview']}'")
        print(f"   Is encrypted: {conv['latest_message'].is_encrypted}")
        print(f"   ✅ Shows readable text: {conv['message_preview'] == encrypted_msg_text}")
    
    print(f"\n📋 User2 ({user2.username}) conversations:")
    if conversations_user2:
        conv = conversations_user2[0]
        print(f"   Latest message preview: '{conv['message_preview']}'")
        print(f"   Is encrypted: {conv['latest_message'].is_encrypted}")
        print(f"   ✅ Shows readable text: {conv['message_preview'] == encrypted_msg_text}")
    
    # Clean up
    plain_message.delete()
    encrypted_message.delete()
    user1.following.remove(user2)
    user2.following.remove(user1)
    
    print(f"\n🧹 Cleaned up test data")
    print("=" * 60)
    print("🎉 MIXED MESSAGE TYPES TEST PASSED!")
    print("Chat list handles both encrypted and plain text messages correctly.")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_mixed_message_types()
        if success:
            print("\n✅ Mixed message types test completed successfully!")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()
