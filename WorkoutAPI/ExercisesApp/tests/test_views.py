from django.test import TestCase, Client
from django.urls import reverse
from WorkoutAPI.models import Exercises
import json

class TestExerciseViews(TestCase):

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

    def test_exercise_detail_PUT_non_existent_id(self):
        new_info = {
            "ExerciseName": "Barbell sumo deadlift",
            "Muscle": "lower_back",
            "Equipment": "barbell",
            "Instructions": "Updated instructions for the exercise"}
        
        curr_count = Exercises.objects.count()

        response = self.client.put(reverse('exercise_detail', args=[2000]), data=json.dumps(new_info), content_type = 'application/json')

        self.assertEquals(response.status_code, 404)
        self.assertEquals(curr_count, Exercises.objects.count())

    def test_exercise_detail_PUT_invalid_data_key(self):

        Exercises.objects.create(
            ExerciseId = 2,
            ExerciseName = "Barbell sumo deadlift",
            Muscle = "lower_back",
            Equipment = "barbell",
            Instructions = "instructions for sumo deadlifts here..."
        )

        new_info = {
            "ExerciseName": "Barbell sumo deadlift",
            "Invalid_Key": "lower_back",
            "Equipment": "barbell",
            "Instructions": "Updated instructions for the exercise"}
        
        response = self.client.put(reverse('exercise_detail', args=[2]), data=json.dumps(new_info), content_type = 'application/json')

        self.assertEquals(response.status_code, 400)

        response_verify = self.client.get(reverse('exercise_detail', args=[2]))
        self.assertEquals(response_verify.data['Instructions'], 'instructions for sumo deadlifts here...')

    def test_exercise_detail_PUT_invalid_data_value(self):

        Exercises.objects.create(
            ExerciseId = 2,
            ExerciseName = "Barbell sumo deadlift",
            Muscle = "lower_back",
            Equipment = "barbell",
            Instructions = "instructions for sumo deadlifts here..."
        )

        new_info = {
            "ExerciseName": "Barbell sumo deadlift",
            "Muscle": True,
            "Equipment": "barbell",
            "Instructions": "Updated instructions for the exercise"}
        
        response = self.client.put(reverse('exercise_detail', args=[2]), data=json.dumps(new_info), content_type = 'application/json')

        self.assertEquals(response.status_code, 400)

        response_verify = self.client.get(reverse('exercise_detail', args=[2]))

        self.assertEquals(response_verify.data['Instructions'], 'instructions for sumo deadlifts here...')
        self.assertEquals(response_verify.data['Muscle'], 'lower_back')

class TestDaysViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.days_url = reverse('days')
        self.exercise_1 = Exercises.objects.create(
			ExerciseName = "Bicep Curl",
			Muscle = "biceps",
			Equipment = "barbell",
			Instructions = "Perform a curl"
        )
        self.exercise_2 = Exercises.objects.create(
			ExerciseName = "Incline Hammer Curls",
		    Muscle = "biceps",
			Equipment = "dumbbell",
			Instructions = "Seat yourself on an incline bench with a dumbbell in each hand. You should pressed firmly against he back with your feet together. Allow the dumbbells to hang straight down at your side..."
        )
    
    def test_days_POST_adds_new_day(self):

        new_day = {
            'DayName': 'Day 1',
            'DayExercises': []
        }

        response = self.client.post(self.days_url, new_day)

        print(response.data)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['DayName'], 'Day 1')
    
    

        