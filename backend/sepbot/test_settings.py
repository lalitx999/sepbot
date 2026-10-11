"""Isolated test database and disabled outbound LINE/AI credentials.

Run: python backend/manage.py test accounts assessment health faq --settings=sepbot.test_settings
"""
from .settings import *  # noqa: F403

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
LINE_CHANNEL_ACCESS_TOKEN = ''
LINE_CHANNEL_SECRET = ''
GROQ_API_KEY = ''
DEEPSEEK_API_KEY = ''
