from django.contrib import admin
from WorkoutAPI.models import Exercises, Day, Routine
# Register your models here.

admin.site.register(Exercises)
admin.site.register(Day)
admin.site.register(Routine)