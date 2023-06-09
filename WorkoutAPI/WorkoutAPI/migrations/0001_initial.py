# Generated by Django 4.1.7 on 2023-03-27 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercises',
            fields=[
                ('ExerciseId', models.AutoField(primary_key=True, serialize=False)),
                ('ExerciseName', models.CharField(max_length=100)),
                ('Muscle', models.CharField(max_length=100)),
                ('Equipment', models.CharField(max_length=100)),
                ('Instructions', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Routines',
            fields=[
                ('RoutineId', models.AutoField(primary_key=True, serialize=False)),
                ('RoutineName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Workouts',
            fields=[
                ('WorkoutId', models.AutoField(primary_key=True, serialize=False)),
                ('WorkoutDate', models.DateField()),
                ('WorkoutResults', models.CharField(max_length=1000)),
            ],
        ),
    ]
