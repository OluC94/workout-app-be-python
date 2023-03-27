from django.db import models

class Exercises(models.Model):
    ExerciseId = models.AutoField(primary_key=True)
    ExerciseName = models.CharField(max_length=100)
    Muscle = models.CharField(max_length=100)
    Equipment = models.CharField(max_length=100)
    Instructions = models.CharField(max_length=500)


class Routines(models.Model):
    RoutineId = models.AutoField(primary_key=True)
    RoutineName = models.CharField(max_length=100)


class Workouts(models.Model):
    WorkoutId = models.AutoField(primary_key=True)
    WorkoutDate = models.DateField()
    WorkoutResults = models.CharField(max_length=1000)
