from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from django.contrib.auth.models import User

from pymongo import MongoClient

# Sample data
USERS = [
    {"username": "superman", "email": "superman@dc.com", "team": "dc"},
    {"username": "batman", "email": "batman@dc.com", "team": "dc"},
    {"username": "wonderwoman", "email": "wonderwoman@dc.com", "team": "dc"},
    {"username": "ironman", "email": "ironman@marvel.com", "team": "marvel"},
    {"username": "spiderman", "email": "spiderman@marvel.com", "team": "marvel"},
    {"username": "captainamerica", "email": "captainamerica@marvel.com", "team": "marvel"},
]

TEAMS = [
    {"name": "marvel", "members": ["ironman", "spiderman", "captainamerica"]},
    {"name": "dc", "members": ["superman", "batman", "wonderwoman"]},
]

ACTIVITIES = [
    {"user": "superman", "activity": "flying", "duration": 60},
    {"user": "batman", "activity": "martial arts", "duration": 45},
    {"user": "ironman", "activity": "engineering", "duration": 50},
]

LEADERBOARD = [
    {"team": "marvel", "points": 300},
    {"team": "dc", "points": 250},
]

WORKOUTS = [
    {"name": "strength", "description": "Strength training workout"},
    {"name": "agility", "description": "Agility and speed workout"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Create unique index on email
        db.users.create_index("email", unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
