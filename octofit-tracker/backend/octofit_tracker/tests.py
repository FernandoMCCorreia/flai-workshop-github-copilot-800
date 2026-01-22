from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime

class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='Test team description'
        )
    
    def test_team_creation(self):
        """Test that a team can be created"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'Test team description')
        self.assertIsNotNone(self.team._id)

class UserModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team', description='Test team')
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            team_id=str(self.team._id)
        )
    
    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.team_id, str(self.team._id))
        self.assertIsNotNone(self.user._id)

class ActivityModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team', description='Test team')
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            team_id=str(self.team._id)
        )
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories_burned=250,
            date=datetime.now(),
            notes='Morning run'
        )
    
    def test_activity_creation(self):
        """Test that an activity can be created"""
        self.assertEqual(self.activity.user_id, str(self.user._id))
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.distance, 5.0)
        self.assertEqual(self.activity.calories_burned, 250)

class WorkoutModelTest(TestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='Test workout description',
            difficulty='Medium',
            duration=45,
            category='Strength',
            exercises=[
                {'name': 'Push-ups', 'sets': 3, 'reps': 15},
                {'name': 'Squats', 'sets': 3, 'reps': 20}
            ]
        )
    
    def test_workout_creation(self):
        """Test that a workout can be created"""
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.difficulty, 'Medium')
        self.assertEqual(self.workout.duration, 45)
        self.assertEqual(len(self.workout.exercises), 2)

class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team', description='Test team')
        self.leaderboard = Leaderboard.objects.create(
            team_id=str(self.team._id),
            total_points=1000,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        """Test that a leaderboard entry can be created"""
        self.assertEqual(self.leaderboard.team_id, str(self.team._id))
        self.assertEqual(self.leaderboard.total_points, 1000)
        self.assertEqual(self.leaderboard.rank, 1)

class TeamAPITest(APITestCase):
    def test_get_teams(self):
        """Test retrieving teams via API"""
        Team.objects.create(name='Team A', description='Description A')
        Team.objects.create(name='Team B', description='Description B')
        
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class UserAPITest(APITestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team', description='Test team')
    
    def test_get_users(self):
        """Test retrieving users via API"""
        User.objects.create(
            email='user1@example.com',
            username='user1',
            password='pass123',
            team_id=str(self.team._id)
        )
        
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class WorkoutAPITest(APITestCase):
    def test_get_workouts(self):
        """Test retrieving workouts via API"""
        Workout.objects.create(
            name='Test Workout',
            description='Description',
            difficulty='Easy',
            duration=30,
            category='Cardio',
            exercises=[]
        )
        
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class LeaderboardAPITest(APITestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team', description='Test team')
    
    def test_get_leaderboard(self):
        """Test retrieving leaderboard via API"""
        Leaderboard.objects.create(
            team_id=str(self.team._id),
            total_points=500,
            rank=1
        )
        
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class ActivityAPITest(APITestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team', description='Test team')
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='testpass',
            team_id=str(self.team._id)
        )
    
    def test_get_activities(self):
        """Test retrieving activities via API"""
        Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='Running',
            duration=30,
            calories_burned=250,
            date=datetime.now()
        )
        
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
