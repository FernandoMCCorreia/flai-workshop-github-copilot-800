from djongo import models

class User(models.Model):
    _id = models.ObjectIdField()
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    team_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username

class Team(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return self.name

class Activity(models.Model):
    _id = models.ObjectIdField()
    user_id = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=50)
    duration = models.IntegerField()  # in minutes
    distance = models.FloatField(blank=True, null=True)  # in km
    calories_burned = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'activities'
    
    def __str__(self):
        return f"{self.activity_type} - {self.user_id}"

class Leaderboard(models.Model):
    _id = models.ObjectIdField()
    team_id = models.CharField(max_length=100)
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
    
    def __str__(self):
        return f"Team {self.team_id} - Rank {self.rank}"

class Workout(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=20)  # Easy, Medium, Hard
    duration = models.IntegerField()  # in minutes
    category = models.CharField(max_length=50)
    exercises = models.JSONField(default=list)
    
    class Meta:
        db_table = 'workouts'
    
    def __str__(self):
        return self.name
