from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'team_id', 'created_at']
    search_fields = ['username', 'email']
    list_filter = ['team_id', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'activity_type', 'duration', 'distance', 'calories_burned', 'date']
    search_fields = ['user_id', 'activity_type']
    list_filter = ['activity_type', 'date']
    ordering = ['-date']

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['team_id', 'total_points', 'rank', 'updated_at']
    ordering = ['rank']
    readonly_fields = ['updated_at']

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'difficulty', 'duration']
    search_fields = ['name', 'category']
    list_filter = ['difficulty', 'category']
