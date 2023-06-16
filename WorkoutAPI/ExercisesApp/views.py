from django.shortcuts import render
from django.http import JsonResponse
from WorkoutAPI.models import Exercises, Day, Routine
from WorkoutAPI.serializers import ExerciseSerializer, DaySerializer, RoutineSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['GET', 'POST'])
def exercise_list(request, format=None):
    if request.method == 'GET':
        exercises = Exercises.objects.all() # get exercises
        serializer = ExerciseSerializer(exercises, many=True)    # many=True to serialize whole list
        return JsonResponse({'exercises': serializer.data})
    
    elif request.method == 'POST':

        if not bool(request.data):
            return Response({"msg": "No content submitted"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def exercise_detail(request, id, format=None):
    # id comes from the params in the views
    if type(id) is not int:
        return Response({"msg": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def day_list(request, format=None):
    if request.method == 'GET':
        days = Day.objects.all()
        serializer = DaySerializer(days, many=True)
        return JsonResponse({'days': serializer.data})
    
    elif request.method == 'POST':
            
        if not bool(request.data):
            return Response({"msg": "No content submitted"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DaySerializer(data=request.data)
        
        # make sure the Day Exercises comes in blank when creating a new day
        if 'DayExercises' in request.data:
            return Response({"msg": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"msg": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def day_detail(request, id, format=None):

    try:
        day = Day.objects.get(pk=id)
    except Day.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DaySerializer(day)
        return Response(serializer.data)
    
    elif request.method == 'PUT':

        if 'ExerciseId' in request.data:
            if type(request.data['ExerciseId']) is not int:
                return Response({"msg": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                exercise = Exercises.objects.get(pk=request.data["ExerciseId"])
            except Exercises.DoesNotExist:
                return Response({"msg": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)
            day.DayExercises.add(exercise)
            # print('day exercise after stuff: ', day.DayExercises.all())
        
        elif 'exercise_id_to_remove' in request.data:
            if type(request.data['exercise_id_to_remove']) is not int:
                return Response({"msg": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                exercise = Exercises.objects.get(pk=request.data["exercise_id_to_remove"])
            except Exercises.DoesNotExist:
                return Response({"msg": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)
            day.DayExercises.remove(exercise)

        serializer = DaySerializer(day, data=request.data)

        if serializer.is_valid():
            # print('ser validated data: ', serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        day.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def routine_list(request, format=None):
    if request.method == 'GET':
        routines = Routine.objects.all()
        serializer = RoutineSerializer(routines, many=True)
        return JsonResponse({'routines': serializer.data})

    elif request.method == 'POST':
        if not bool(request.data):
            return Response({"msg": "No content submitted"}, status=status.HTTP_400_BAD_REQUEST)

        if 'RoutineDays' in request.data:
            return Response({"msg": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RoutineSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"msg": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def routine_detail(request, id, format=None):
    
    try:
        routine = Routine.objects.get(pk=id)
    except Routine.DoesNotExist:
        return Response({"msg": "Routine not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RoutineSerializer(routine)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if 'DayId' in request.data:
            if type(request.data['DayId']) is not int:
                return Response({"msg": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                day = Day.objects.get(pk=request.data['DayId'])
            except Day.DoesNotExist:
                return Response({"msg": "Day not found"}, status=status.HTTP_404_NOT_FOUND)
            routine.RoutineDays.add(day)
        
        elif 'day_to_remove' in request.data:
            if type(request.data['day_to_remove']) is not int:
                return Response({"msg": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                day = Day.objects.get(pk=request.data['day_to_remove'])
            except Day.DoesNotExist:
                return Response({"msg": "Day not found"}, status=status.HTTP_404_NOT_FOUND)
            routine.RoutineDays.remove(day)

        serializer = RoutineSerializer(routine, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({"msg": "/routines/<int:id>"})