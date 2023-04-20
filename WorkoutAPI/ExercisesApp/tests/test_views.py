from django.test import TestCase, Client
from django.urls import reverse
from WorkoutAPI.models import Exercises, Day
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
        self.day_detail_url = reverse('day_detail', args=[1])
        self.exercise_1 = Exercises.objects.create(
            ExerciseId = 555,
			ExerciseName = "Bicep Curl",
			Muscle = "biceps",
			Equipment = "barbell",
			Instructions = "Perform a curl"
        )
        self.exercise_2 = Exercises.objects.create(
            ExerciseId = 556,
			ExerciseName = "Incline Hammer Curls",
		    Muscle = "biceps",
			Equipment = "dumbbell",
			Instructions = "Seat yourself on an incline bench with a dumbbell in each hand. You should pressed firmly against he back with your feet together. Allow the dumbbells to hang straight down at your side..."
        )
        self.day_example = Day.objects.create(
            DayName = 'Test Day',
        )
        self.day_example.DayExercises.add(555, 556)
    
    def test_days_POST_adds_new_day(self):

        # since all days will initially be input, make the name the only thing thats input, have the views POST dayname + dayexercises[]

        current_days = Day.objects.all()
        assertion_length = len(current_days) + 1
        new_day = {
            'DayName': 'Day 1',
            'DayExercises': []
        }

        response = self.client.post(self.days_url, new_day)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['DayName'], 'Day 1')
        self.assertEquals(len(response.data['DayExercises']), 0)
        self.assertEquals(len(Day.objects.all()), assertion_length)
    
    def test_days_POST_no_content(self):

        new_day = {}

        current_days = Day.objects.all()
        response = self.client.post(self.days_url, new_day)
        

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['msg'], 'No content submitted')
        self.assertEquals(len(Day.objects.all()), len(current_days))
    
    def test_days_POST_invalid_key(self):

        new_day = {
            'Invalid Key': 'test name',
            'DayExercises': []
        }

        current_days = Day.objects.all()
        response = self.client.post(self.days_url, new_day)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['msg'], 'Bad request')
        self.assertEquals(len(Day.objects.all()), len(current_days))

    def test_days_POST_invalid_value(self):

        new_day = {
            'DayName': 'Day to test',
            'DayExercises': 'Invalid key'
        }

        current_days = Day.objects.all()
        response = self.client.post(self.days_url, new_day)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['msg'], 'Bad request')
        self.assertEquals(len(Day.objects.all()), len(current_days))
    
    def test_days_GET(self):

        response = self.client.get(self.days_url)

        self.assertEquals(response.status_code, 200)
        self.assertGreater(len(response.json()['days']), 0)
    
    def test_day_detail_GET(self):

        response = self.client.get(self.day_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['DayName'], 'Test Day')
    
    def test_day_detail_GET_invalid_id(self):

        test_url = reverse('day_detail', args=[6000])

        response = self.client.get(test_url)

        self.assertEquals(response.status_code, 404)
    
    def test_day_detail_DELETE_deletes_day(self):
        
        initial_day_count = Day.objects.count()
        verify_creation = initial_day_count + 1
        
        Day.objects.create(
            DayId = 222,
            DayName = "Test day to be deleted"
        )

        self.assertEquals(Day.objects.count(), verify_creation)

        response = self.client.delete(self.day_detail_url, json.dumps({
            'id': 222
        }))

        self.assertEquals(response.status_code, 204)
        self.assertEquals(Day.objects.count(), initial_day_count)

    def test_day_detail_DELETE_non_existent_id(self):

        initial_day_count = Day.objects.count()

        response = self.client.delete(reverse('day_detail', args=[5353]))

        self.assertEquals(response.status_code, 404)
        self.assertEquals(Day.objects.count(), initial_day_count)
        