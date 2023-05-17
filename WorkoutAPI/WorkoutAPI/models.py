from django.db import models

class Exercises(models.Model):
    ExerciseId = models.AutoField(primary_key=True)
    ExerciseName = models.CharField(max_length=100)
    Muscle = models.CharField(max_length=100)
    Equipment = models.CharField(max_length=100)
    Instructions = models.CharField(max_length=5000)

    def __str__(self):
        return self.ExerciseName + " - " + self.Equipment

class Day(models.Model):
    DayId = models.AutoField(primary_key=True)
    DayName = models.CharField(max_length=100)
    DayExercises = models.ManyToManyField(Exercises, blank=True)

    def __str__(self):
        return self.DayName

class Routine(models.Model):
    RoutineId = models.AutoField(primary_key=True)
    RoutineName = models.CharField(max_length=100)
    RoutineDays = models.ManyToManyField(Day, blank=True)

    def __str__(self):
        return self.RoutineName


class Workouts(models.Model):
    WorkoutId = models.AutoField(primary_key=True)
    WorkoutDate = models.DateField()
    WorkoutResults = models.CharField(max_length=1000)
