from django.test import TestCase, Client
from django.urls import reverse
from WorkoutAPI.models import Exercises
import json

class TestViews(TestCase):

    # run before everytest
    def setUp(self):
        self.client = Client()
        self.exercises_url = reverse('exercises')
        self.exercise_detail_url = reverse('exercise_detail', args=[1])
        self.exercise1 = Exercises.objects.create(
            ExerciseName = "Barbell shrug",
            Muscle = "traps",
            Equipment = "barbell",
            Instructions = "Stand up straight with your feet at shoulder width as you hold a barbell with both hands in front of you using a pronated grip (palms facing the thighs)..."
        )

    def test_exercise_list_GET(self):

        response = self.client.get(self.exercises_url)

        self.assertEquals(response.status_code, 200)
    
    def test_exercises_list_POST_adds_new_exercise(self):
        new_exercise = { 
            "ExerciseName": "Kettlebell sumo deadlift high pull",
            "Muscle": "traps",
            "Equipment": "kettlebells",
            "Instructions": "Place a kettlebell on the ground between your feet. Position your feet in a wide stance, and grasp the kettlebell with two hands. Set your hips back as far as possible, with your knees bent..."}
                
        
        response = self.client.post(self.exercises_url, new_exercise)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['ExerciseName'], 'Kettlebell sumo deadlift high pull')

    def test_exercise_list_POST_no_data(self):
        response = self.client.post(self.exercises_url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {"msg": "No content submitted"})


    def test_exercise_detail_GET(self):
        response = self.client.get(self.exercise_detail_url)

        self.assertEquals(response.status_code, 200)

    def test_exercise_detail_DELETE_deletes_exercise(self):

        Exercises.objects.create(
            ExerciseId = 2,
            ExerciseName = "Barbell sumo deadlift",
            Muscle = "lower_back",
            Equipment = "barbell",
            Instructions = "instructions for sumo deadlifts here..."
        )

        response = self.client.delete(self.exercise_detail_url, json.dumps({
            'id': 2
        }))

        self.assertEquals(response.status_code, 204)
        self.assertEquals(Exercises.objects.count(), 1)

    def test_exercise_detail_DELETE_non_existent_id(self):

        Exercises.objects.create(
            ExerciseId = 2,
            ExerciseName = "Barbell sumo deadlift",
            Muscle = "lower_back",
            Equipment = "barbell",
            Instructions = "instructions for sumo deadlifts here..."
        )

        response = self.client.delete(reverse('exercise_detail', args=[53]))

        self.assertEquals(response.status_code, 404)
        self.assertEquals(Exercises.objects.count(), 2)
    
    def test_exercise_detail_PUT_updates_data(self):

        Exercises.objects.create(
            ExerciseId = 2,
            ExerciseName = "Barbell sumo deadlift",
            Muscle = "lower_back",
            Equipment = "barbell",
            Instructions = "instructions for sumo deadlifts here..."
        )

        new_info = {
            "ExerciseName": "Barbell sumo deadlift",
            "Muscle": "lower_back",
            "Equipment": "barbell",
            "Instructions": "Updated instructions for the exercise"}

        response = self.client.put(reverse('exercise_detail', args=[2]), data=json.dumps(new_info), content_type = 'application/json')

        self.assertEquals(response.data['ExerciseName'], "Barbell sumo deadlift")
        self.assertEquals(response.data['Instructions'], "Updated instructions for the exercise")



