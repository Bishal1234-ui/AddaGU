#!/usr/bin/env python
"""
Test script to verify IST timezone is working correctly
"""

import os
import sys
import django
from datetime import datetime

# Add the project directory to the Python path
sys.path.append('d:\\DESKTOP_FOLDERS\\New folder\\Test\\GUBlogs')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GUBlogs.settings')
django.setup()

from django.utils import timezone
from django.conf import settings

print("Django timezone settings:")
print(f"TIME_ZONE: {settings.TIME_ZONE}")
print(f"USE_TZ: {settings.USE_TZ}")
print()

print("Current time checks:")
print(f"timezone.now(): {timezone.now()}")
print(f"timezone.now() formatted: {timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
print()

# Test IST conversion
ist_time = timezone.now()
print(f"IST time: {ist_time}")
print(f"IST time formatted for display: {ist_time.strftime('%I:%M %p')}")
