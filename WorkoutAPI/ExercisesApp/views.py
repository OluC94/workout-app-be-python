from django.shortcuts import render
from django.http import JsonResponse
from WorkoutAPI.models import Exercises
from WorkoutAPI.serializers import ExerciseSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['GET', 'POST'])
def exercise_list(request):
    if request.method == 'GET':
        exercises = Exercises.objects.all() # get exercises
        serializer = ExerciseSerializer(exercises, many=True)    # many=True to serialize whole list
        return JsonResponse({'exercises': serializer.data})
    
    elif request.method == 'POST':
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def exercise_detail(request, id):
    # id comes from the params in the views
    try:
        exercise = Exercises.objects.get(pk=id)
    except Exercises.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExerciseSerializer(exercise)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExerciseSerializer(exercise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)