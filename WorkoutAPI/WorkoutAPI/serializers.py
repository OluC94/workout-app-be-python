from rest_framework import serializers
from .models import Exercises, Day

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ['ExerciseId', 'ExerciseName', 'Muscle', 'Equipment', 'Instructions']

class DaySerializer(serializers.ModelSerializer):
    
    DayExercises = ExerciseSerializer(many=True)

    class Meta:
        model = Day
        fields = ['DayId', 'DayName', 'DayExercises']
        depth = 1

    def create(self, validated_data):
        exercise_data = validated_data.pop('DayExercises')
        print(exercise_data)
        day = Day.objects.create(**validated_data)
        for data in exercise_data:
            exercise = Exercises.objects.get_or_create(**data)
            day.DayExercises.add(exercise)
        return day