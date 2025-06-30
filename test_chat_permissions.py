#!/usr/bin/env python
"""
Test script to verify the chat restriction functionality
"""
import os
import sys
import django

# Add the project root to the Python path
sys.path.append('d:\\DESKTOP_FOLDERS\\New folder\\Test\\GUBlogs')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GUBlogs.settings')
django.setup()

from users.models import CustomUser

def test_chat_permissions():
    """Test the chat permission functionality"""
    print("Testing chat permissions...")
    
    # Try to get some users for testing
    users = CustomUser.objects.all()[:3]
    
    if len(users) < 2:
        print("Need at least 2 users to test chat permissions")
        return
    
    user1, user2 = users[0], users[1]
    
    print(f"Testing chat between {user1.username} and {user2.username}")
    
    # Initially, they shouldn't be able to chat
    print(f"Can {user1.username} chat with {user2.username}? {user1.can_chat_with(user2)}")
    print(f"Can {user2.username} chat with {user1.username}? {user2.can_chat_with(user1)}")
    
    # Make user1 follow user2
    user1.following.add(user2)
    print(f"\n{user1.username} now follows {user2.username}")
    print(f"Can {user1.username} chat with {user2.username}? {user1.can_chat_with(user2)}")
    print(f"Can {user2.username} chat with {user1.username}? {user2.can_chat_with(user1)}")
    
    # Make user2 follow user1 back
    user2.following.add(user1)
    print(f"\n{user2.username} now follows {user1.username} back")
    print(f"Can {user1.username} chat with {user2.username}? {user1.can_chat_with(user2)}")
    print(f"Can {user2.username} chat with {user1.username}? {user2.can_chat_with(user1)}")
    
    print("\nTest completed!")

if __name__ == '__main__':
    test_chat_permissions()
