from rest_framework import serializers
from .models import Exercises, Day

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ['ExerciseId', 'ExerciseName', 'Muscle', 'Equipment', 'Instructions']

class DaySerializer(serializers.ModelSerializer):
    
    DayExercises = ExerciseSerializer(source='Exercises', read_only=True, many=True)

    class Meta:
        model = Day
        fields = ['DayId', 'DayName', 'DayExercises']
        depth = 1