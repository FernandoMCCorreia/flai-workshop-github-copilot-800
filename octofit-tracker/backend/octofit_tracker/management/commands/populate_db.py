from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Delete existing data
        self.stdout.write('Deleting existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes united for fitness excellence'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League champions committed to peak performance'
        )
        
        # Create Users (Superheroes)
        self.stdout.write('Creating users...')
        users_data = [
            # Team Marvel
            {'email': 'ironman@avengers.com', 'username': 'Iron Man', 'password': 'stark123', 'team': team_marvel},
            {'email': 'captainamerica@avengers.com', 'username': 'Captain America', 'password': 'shield123', 'team': team_marvel},
            {'email': 'thor@asgard.com', 'username': 'Thor', 'password': 'mjolnir123', 'team': team_marvel},
            {'email': 'blackwidow@shield.com', 'username': 'Black Widow', 'password': 'natasha123', 'team': team_marvel},
            {'email': 'hulk@gamma.com', 'username': 'Hulk', 'password': 'smash123', 'team': team_marvel},
            {'email': 'spiderman@daily.com', 'username': 'Spider-Man', 'password': 'parker123', 'team': team_marvel},
            # Team DC
            {'email': 'superman@dailyplanet.com', 'username': 'Superman', 'password': 'krypton123', 'team': team_dc},
            {'email': 'batman@wayne.com', 'username': 'Batman', 'password': 'gotham123', 'team': team_dc},
            {'email': 'wonderwoman@themyscira.com', 'username': 'Wonder Woman', 'password': 'diana123', 'team': team_dc},
            {'email': 'flash@central.com', 'username': 'Flash', 'password': 'speedforce123', 'team': team_dc},
            {'email': 'aquaman@atlantis.com', 'username': 'Aquaman', 'password': 'arthur123', 'team': team_dc},
            {'email': 'greenlantern@oa.com', 'username': 'Green Lantern', 'password': 'willpower123', 'team': team_dc},
        ]
        
        users = []
        for user_data in users_data:
            user = User.objects.create(
                email=user_data['email'],
                username=user_data['username'],
                password=user_data['password'],
                team_id=str(user_data['team']._id)
            )
            users.append(user)
        
        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'Boxing']
        base_date = datetime.now() - timedelta(days=30)
        
        for user in users:
            for i in range(10):  # 10 activities per user
                activity_type = activity_types[i % len(activity_types)]
                duration = 30 + (i * 5)
                distance = round(duration * 0.15, 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                calories = duration * 8
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories_burned=calories,
                    date=base_date + timedelta(days=i * 3),
                    notes=f'{activity_type} session {i+1} for {user.username}'
                )
        
        # Create Workouts
        self.stdout.write('Creating workouts...')
        workouts_data = [
            {
                'name': 'Superhero Strength',
                'description': 'Build strength like the mightiest heroes',
                'difficulty': 'Hard',
                'duration': 60,
                'category': 'Strength',
                'exercises': [
                    {'name': 'Deadlifts', 'sets': 4, 'reps': 8},
                    {'name': 'Bench Press', 'sets': 4, 'reps': 10},
                    {'name': 'Squats', 'sets': 4, 'reps': 12},
                    {'name': 'Pull-ups', 'sets': 3, 'reps': 15}
                ]
            },
            {
                'name': 'Speed Force Cardio',
                'description': 'Run at super speed with this cardio blast',
                'difficulty': 'Medium',
                'duration': 45,
                'category': 'Cardio',
                'exercises': [
                    {'name': 'Sprint Intervals', 'duration': '20 minutes'},
                    {'name': 'Jump Rope', 'duration': '10 minutes'},
                    {'name': 'Burpees', 'sets': 3, 'reps': 20},
                    {'name': 'Mountain Climbers', 'sets': 3, 'reps': 30}
                ]
            },
            {
                'name': 'Warrior Flexibility',
                'description': 'Stretch and flow like an Amazonian warrior',
                'difficulty': 'Easy',
                'duration': 30,
                'category': 'Flexibility',
                'exercises': [
                    {'name': 'Sun Salutations', 'reps': 5},
                    {'name': 'Warrior Poses', 'duration': '10 minutes'},
                    {'name': 'Deep Stretches', 'duration': '15 minutes'},
                    {'name': 'Meditation', 'duration': '5 minutes'}
                ]
            },
            {
                'name': 'Web-Slinger Agility',
                'description': 'Train agility like your friendly neighborhood Spider-Man',
                'difficulty': 'Medium',
                'duration': 40,
                'category': 'Agility',
                'exercises': [
                    {'name': 'Ladder Drills', 'duration': '10 minutes'},
                    {'name': 'Box Jumps', 'sets': 3, 'reps': 15},
                    {'name': 'Cone Drills', 'duration': '10 minutes'},
                    {'name': 'Plyometric Push-ups', 'sets': 3, 'reps': 12}
                ]
            },
            {
                'name': 'Atlantean Swim Workout',
                'description': 'Master the waters with this aquatic training',
                'difficulty': 'Hard',
                'duration': 50,
                'category': 'Swimming',
                'exercises': [
                    {'name': 'Freestyle', 'distance': '1000m'},
                    {'name': 'Backstroke', 'distance': '500m'},
                    {'name': 'Breaststroke', 'distance': '500m'},
                    {'name': 'Butterfly', 'distance': '200m'}
                ]
            },
            {
                'name': 'Arc Reactor Core',
                'description': 'Build a powerful core like Tony Stark\'s arc reactor',
                'difficulty': 'Medium',
                'duration': 35,
                'category': 'Core',
                'exercises': [
                    {'name': 'Plank', 'duration': '3 minutes'},
                    {'name': 'Russian Twists', 'sets': 3, 'reps': 30},
                    {'name': 'Leg Raises', 'sets': 3, 'reps': 20},
                    {'name': 'Bicycle Crunches', 'sets': 3, 'reps': 40}
                ]
            }
        ]
        
        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)
        
        # Calculate team points and create leaderboard
        self.stdout.write('Creating leaderboard...')
        
        # Calculate Team Marvel points
        marvel_users = User.objects.filter(team_id=str(team_marvel._id))
        marvel_points = 0
        for user in marvel_users:
            user_activities = Activity.objects.filter(user_id=str(user._id))
            marvel_points += sum(activity.calories_burned for activity in user_activities)
        
        # Calculate Team DC points
        dc_users = User.objects.filter(team_id=str(team_dc._id))
        dc_points = 0
        for user in dc_users:
            user_activities = Activity.objects.filter(user_id=str(user._id))
            dc_points += sum(activity.calories_burned for activity in user_activities)
        
        # Determine ranks
        if marvel_points > dc_points:
            Leaderboard.objects.create(
                team_id=str(team_marvel._id),
                total_points=marvel_points,
                rank=1
            )
            Leaderboard.objects.create(
                team_id=str(team_dc._id),
                total_points=dc_points,
                rank=2
            )
        else:
            Leaderboard.objects.create(
                team_id=str(team_dc._id),
                total_points=dc_points,
                rank=1
            )
            Leaderboard.objects.create(
                team_id=str(team_marvel._id),
                total_points=marvel_points,
                rank=2
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully populated database!'))
        self.stdout.write(self.style.SUCCESS(f'Created {Team.objects.count()} teams'))
        self.stdout.write(self.style.SUCCESS(f'Created {User.objects.count()} users'))
        self.stdout.write(self.style.SUCCESS(f'Created {Activity.objects.count()} activities'))
        self.stdout.write(self.style.SUCCESS(f'Created {Workout.objects.count()} workouts'))
        self.stdout.write(self.style.SUCCESS(f'Created {Leaderboard.objects.count()} leaderboard entries'))
