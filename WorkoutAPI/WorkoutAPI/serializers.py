from rest_framework import serializers
from .models import Exercises, Day, Routine

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ['ExerciseId', 'ExerciseName', 'Muscle', 'Equipment', 'Instructions']

class DaySerializer(serializers.ModelSerializer):
    
    DayExercises = ExerciseSerializer(many=True, default=[])

    class Meta:
        model = Day
        fields = ['DayId', 'DayName', 'DayExercises']
        depth = 1
        extra_kwargs = {'DayExercises': {'required': False}}


    def create(self, validated_data):
        exercise_data = validated_data.pop('DayExercises')
        day = Day.objects.create(**validated_data)
        for data in exercise_data:
            exercise = Exercises.objects.get_or_create(**data)
            day.DayExercises.add(exercise)
        return day
    
    def update(self, instance, validated_data):
        exercises = (instance.DayExercises).all()
        exercises = list(exercises)
        instance.DayName = validated_data.get('DayName', instance.DayName)
        instance.save()

        return instance

class RoutineSerializer(serializers.ModelSerializer):

    RoutineDays = DaySerializer(many=True, default=[])

    class Meta:
        model = Routine
        fields = ['RoutineId', 'RoutineName', 'RoutineDays']
        depth = 2
        extra_kwargs = {'RoutineDays': {'required': False}}
    
    def create(self, validated_data):
        day_data = validated_data.pop('RoutineDays')
        routine = Routine.objects.create(**validated_data)
        for data in day_data:
            day = Day.objects.get_or_create(**data)
            routine.RoutineDays.add(day)
        return routine
    
    def update(self, instance, validated_data):
        days = (instance.RoutineDays).all()
        days = list(days)
        instance.RoutineName = validated_data.get('RoutineName', instance.RoutineName)
        instance.save()

        return instance