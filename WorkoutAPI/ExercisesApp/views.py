from django.shortcuts import render
from django.http import JsonResponse
from WorkoutAPI.models import Exercises
from WorkoutAPI.serializers import ExerciseSerializer

# Create your views here.
def exercise_list(request):
    exercises = Exercises.objects.all() # get exercises
    serializer = ExerciseSerializer(exercises, many=True)    # many=True to serialize whole list
    return JsonResponse({"exercises": serializer.data}, safe=False)
