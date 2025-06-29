#!/usr/bin/env python
"""
Migration script to encrypt existing chat messages.
Run this script to encrypt any existing unencrypted messages in the database.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GUBlogs.settings')
django.setup()

from users.models import ChatMessage
from users.encryption import encrypt_for_user, decrypt_for_user


def migrate_existing_messages():
    """
    Migrate existing unencrypted messages to encrypted format.
    This function checks if messages are already encrypted and only encrypts unencrypted ones.
    """
    print("Starting chat message encryption migration...")
    print("=" * 50)
    
    # Get all chat messages
    messages = ChatMessage.objects.all()
    total_messages = messages.count()
    
    if total_messages == 0:
        print("No messages found in the database.")
        return
    
    print(f"Found {total_messages} messages to process.")
    
    encrypted_count = 0
    already_encrypted_count = 0
    error_count = 0
    
    for i, message in enumerate(messages, 1):
        try:
            # Try to decrypt the message to see if it's already encrypted
            try:
                decrypted_test = decrypt_for_user(message.message, message.sender.id)
                if decrypted_test != "[Message could not be decrypted]":
                    # Message is already encrypted and decryptable
                    already_encrypted_count += 1
                    print(f"[{i}/{total_messages}] Message ID {message.id}: Already encrypted")
                    continue
            except:
                pass  # Message is likely not encrypted yet
            
            # Check if the message looks like it might be encrypted (base64-like)
            if len(message.message) > 100 and message.message.replace('=', '').replace('+', '').replace('/', '').isalnum():
                # Looks like it might be encrypted already
                already_encrypted_count += 1
                print(f"[{i}/{total_messages}] Message ID {message.id}: Appears to be encrypted")
                continue
            
            # Store the original message
            original_message = message.message
            
            # Encrypt the message
            encrypted_message = encrypt_for_user(original_message, message.sender.id)
            
            # Update the message
            message.message = encrypted_message
            message.save()
            
            encrypted_count += 1
            print(f"[{i}/{total_messages}] Message ID {message.id}: Encrypted successfully")
            
        except Exception as e:
            error_count += 1
            print(f"[{i}/{total_messages}] Message ID {message.id}: Error - {str(e)}")
    
    print("\n" + "=" * 50)
    print("Migration completed!")
    print(f"Total messages: {total_messages}")
    print(f"Newly encrypted: {encrypted_count}")
    print(f"Already encrypted: {already_encrypted_count}")
    print(f"Errors: {error_count}")
    
    if error_count > 0:
        print(f"\n⚠️  {error_count} messages had errors during migration.")
        print("Please check the error messages above and resolve any issues.")
    else:
        print("\n✅ All messages processed successfully!")


def verify_encryption():
    """
    Verify that encrypted messages can be decrypted properly.
    """
    print("\nVerifying encrypted messages...")
    print("-" * 30)
    
    messages = ChatMessage.objects.all()[:5]  # Check first 5 messages
    
    for message in messages:
        try:
            decrypted = decrypt_for_user(message.message, message.sender.id)
            if decrypted != "[Message could not be decrypted]":
                print(f"✅ Message ID {message.id}: Decryption successful")
                print(f"   Preview: {decrypted[:50]}{'...' if len(decrypted) > 50 else ''}")
            else:
                print(f"❌ Message ID {message.id}: Decryption failed")
        except Exception as e:
            print(f"❌ Message ID {message.id}: Error during verification - {str(e)}")


if __name__ == "__main__":
    migrate_existing_messages()
    verify_encryption()
