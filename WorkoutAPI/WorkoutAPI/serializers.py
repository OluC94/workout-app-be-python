from rest_framework import serializers
from .models import Exercises, Day

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
    
    def get_exercises(self, validated_data):
        exercise_data = validated_data.pop('DayExercises')


    def create(self, validated_data):
        exercise_data = validated_data.pop('DayExercises')
        day = Day.objects.create(**validated_data)
        for data in exercise_data:
            exercise = Exercises.objects.get_or_create(**data)
            day.DayExercises.add(exercise)
        return day
    
    def update(self, instance, validated_data):
        exercise_data = validated_data.pop('DayExercises')
        exercises = (instance.DayExercises).all()
        exercises = list(exercises)
        instance.DayName = validated_data.get('DayName', instance.DayName)
        instance.save()

        for _exercise in exercise_data:
            exercise = exercises.pop(0)
            exercise['ExerciseName'] = _exercise.get('ExerciseName', exercise['ExerciseName'])
            exercise['Muscle'] = _exercise.get('Muscle', exercise['Muscle'])
            exercise['Equipment'] = _exercise.get('Equipment', exercise['Equipment'])
            exercise['Instructions'] = _exercise.get('Instructions', exercise['Instructions'])
            exercise.save()
        return instance
        
        
        
            
                