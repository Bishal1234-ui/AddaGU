#!/usr/bin/env python
"""
Comprehensive test script to verify chat messages are encrypted in database
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GUBlogs.settings')
django.setup()

from users.models import CustomUser, ChatMessage
from django.utils import timezone
from django.db import connection

def test_database_encryption():
    """Test that messages are actually encrypted when stored in the database"""
    
    # Get or create test users
    try:
        user1 = CustomUser.objects.get(username='alice_test')
    except CustomUser.DoesNotExist:
        user1 = CustomUser.objects.create_user(
            username='alice_test',
            email='alice@test.com',
            password='testpass123'
        )
    
    try:
        user2 = CustomUser.objects.get(username='bob_test')
    except CustomUser.DoesNotExist:
        user2 = CustomUser.objects.create_user(
            username='bob_test',
            email='bob@test.com',
            password='testpass123'
        )
    
    # Test messages
    secret_messages = [
        "This is a confidential message 🔒",
        "Password: secretkey123!",
        "Meeting at 3 PM in room 401",
        "The project deadline is next Friday"
    ]
    
    print("=" * 60)
    print("DATABASE ENCRYPTION VERIFICATION TEST")
    print("=" * 60)
    
    message_ids = []
    
    for i, test_message in enumerate(secret_messages, 1):
        print(f"\n📝 Testing message {i}: '{test_message}'")
        
        # Create and save message using proper encryption
        chat_message = ChatMessage(
            sender=user1,
            receiver=user2,
            timestamp=timezone.now()
        )
        chat_message.set_message(test_message)
        chat_message.save()
        message_ids.append(chat_message.id)
        
        # Verify in memory
        print(f"   ✓ In-memory encrypted: {chat_message.is_encrypted}")
        print(f"   ✓ Can decrypt: {chat_message.get_display_message() == test_message}")
        
        # Retrieve from database to verify persistence
        db_message = ChatMessage.objects.get(id=chat_message.id)
        is_encrypted_in_db = db_message.message != test_message
        can_decrypt_from_db = db_message.get_display_message() == test_message
        
        print(f"   ✓ Encrypted in DB: {is_encrypted_in_db}")
        print(f"   ✓ DB decryption works: {can_decrypt_from_db}")
        
        if not (is_encrypted_in_db and can_decrypt_from_db):
            print(f"   ❌ FAILED for message {i}")
            return False
        else:
            print(f"   ✅ SUCCESS for message {i}")
    
    # Now let's check the raw database content to make sure messages are actually encrypted
    print(f"\n🔍 Raw database verification:")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, message, is_encrypted 
            FROM users_chatmessage 
            WHERE id IN ({})
        """.format(','.join(map(str, message_ids))))
        
        raw_results = cursor.fetchall()
        
        for i, (msg_id, raw_message, is_encrypted) in enumerate(raw_results):
            original_message = secret_messages[i]
            print(f"Message {i+1}:")
            print(f"  Original: {original_message}")
            print(f"  Raw DB:   {raw_message[:50]}...")
            print(f"  Encrypted: {is_encrypted}")
            print(f"  Different: {raw_message != original_message}")
            print()
    
    # Clean up test messages
    ChatMessage.objects.filter(id__in=message_ids).delete()
    
    print("🧹 Cleaned up test messages")
    print("=" * 60)
    print("🎉 ALL TESTS PASSED! Messages are properly encrypted in database!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_database_encryption()
        if success:
            print("\n✅ Encryption verification completed successfully!")
            print("Your chat messages are now encrypted in the database.")
        else:
            print("\n❌ Encryption verification failed!")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()
