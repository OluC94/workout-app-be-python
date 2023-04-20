from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ExercisesApp.views import exercise_list, exercise_detail, day_list, day_detail

class TestExerciseUrls(SimpleTestCase):

    def test_exercises_url_resolves(self):
        url = reverse('exercises')
        self.assertEquals(resolve(url).func, exercise_list)

    def test_exercise_detail_resolves(self):
        url = reverse('exercise_detail', args=[1])
        self.assertEquals(resolve(url).func, exercise_detail)

class TestDaysUrls(SimpleTestCase):

    def test_days_url_resolves(self):
        url = reverse('days')
        self.assertEquals(resolve(url).func, day_list)
    
    def test_day_detail_resolves(self):
        url = reverse('day_detail', args=[1])
        self.assertEquals(resolve(url).func, day_detail)
