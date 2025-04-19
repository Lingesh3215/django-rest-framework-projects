from rest_framework import serializers
from .models import DailyGoal

class GoalS(serializers.ModelSerializer):
    class Meta:
        model=DailyGoal
        fields='__all__'
        