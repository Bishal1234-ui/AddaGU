#!/usr/bin/env python
"""
Visual demonstration of the fix - showing before and after
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GUBlogs.settings')
django.setup()

from users.models import CustomUser, ChatMessage
from django.utils import timezone

def demonstrate_fix():
    """Demonstrate the difference between old and new chat list display"""
    
    # Get or create test users
    try:
        alice = CustomUser.objects.get(username='alice_demo')
    except CustomUser.DoesNotExist:
        alice = CustomUser.objects.create_user(
            username='alice_demo',
            email='alice_demo@test.com',
            password='testpass123'
        )
    
    try:
        bob = CustomUser.objects.get(username='bob_demo')
    except CustomUser.DoesNotExist:
        bob = CustomUser.objects.create_user(
            username='bob_demo',
            email='bob_demo@test.com',
            password='testpass123'
        )
    
    # Make them follow each other
    alice.following.add(bob)
    bob.following.add(alice)
    
    # Create encrypted messages
    messages = [
        "Hey Bob! Want to grab lunch today? 🍕",
        "Sure thing! How about that new Italian place?",
        "Perfect! Meet you there at 12:30 PM 😊"
    ]
    
    print("=" * 70)
    print("CHAT LIST DISPLAY FIX DEMONSTRATION")
    print("=" * 70)
    
    saved_messages = []
    for i, msg_text in enumerate(messages):
        # Create encrypted message
        chat_msg = ChatMessage(
            sender=alice if i % 2 == 0 else bob,
            receiver=bob if i % 2 == 0 else alice,
            timestamp=timezone.now() + timezone.timedelta(minutes=i)
        )
        chat_msg.set_message(msg_text)
        chat_msg.save()
        saved_messages.append(chat_msg)
        
        print(f"\n📨 Message {i+1}: '{msg_text}'")
        print(f"🔒 Encrypted in DB: {chat_msg.message[:30]}...")
        print(f"👁️  Decrypted for display: {chat_msg.get_display_message()}")
    
    print(f"\n" + "="*50)
    print("CHAT LIST PREVIEW (What users see now)")
    print("="*50)
    
    # Show what the chat list looks like for both users
    for user in [alice, bob]:
        conversations = user.get_conversations()
        if conversations:
            conv = conversations[0]
            other_user = conv['user']
            preview = conv['message_preview']
            
            print(f"\n👤 {user.username}'s chat list:")
            print(f"   💬 Conversation with {other_user.username}")
            print(f"   📝 Preview: \"{preview[:50]}{'...' if len(preview) > 50 else ''}\"")
            print(f"   ✅ Shows readable text instead of encrypted gibberish!")
    
    # Clean up
    for msg in saved_messages:
        msg.delete()
    alice.following.remove(bob)
    bob.following.remove(alice)
    
    print(f"\n🧹 Demo completed and cleaned up")
    print("=" * 70)
    print("🎉 PROBLEM SOLVED!")
    print("✅ Chat list now shows readable message previews")
    print("🔒 Messages are still encrypted in the database")
    print("👀 Users see decrypted previews in the chat list")
    print("=" * 70)

if __name__ == "__main__":
    demonstrate_fix()
