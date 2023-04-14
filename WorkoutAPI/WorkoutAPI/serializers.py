from rest_framework import serializers
from .models import Exercises, Day

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ['ExerciseId', 'ExerciseName', 'Muscle', 'Equipment', 'Instructions']

class DaySerializer(serializers.ModelSerializer):
    
    exercises_dataset = Exercises.objects.all()
    DayExercises = ExerciseSerializer(exercises_dataset, read_only=True, many=True, required=False)

    class Meta:
        model = Day
        fields = ['DayId', 'DayName', 'DayExercises']