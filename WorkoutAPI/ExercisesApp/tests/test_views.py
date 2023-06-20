from django.test import TestCase, Client
from django.urls import reverse
from WorkoutAPI.models import Exercises, Day, Routine
import json

class TestExerciseViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.exercises_url = reverse('exercises')
        self.exercise_detail_url = reverse('exercise_detail', args=[1])
        self.exercise1 = Exercises.objects.create(
            ExerciseId = 1,
            ExerciseName = "Barbell shrug",
            Muscle = "traps",
            Equipment = "barbell",
            Instructions = "Stand up straight with your feet at shoulder width as you hold a barbell with both hands in front of you using a pronated grip (palms facing the thighs)..."
        )
        self.exercise2 = Exercises.objects.create(
            ExerciseId = 123,
            ExerciseName = "Reverse-grip bent-over row",
            Muscle = "middle_back",
            Equipment = "barbell",
            Instructions = "Stand erect while holding a barbell with a supinated grip (palms facing up). Bend your knees slightly and bring your torso forward, by bending..."
        )
        self.exercise3 = Exercises.objects.create(
            ExerciseId = 124,
            ExerciseName = "Kettlebell thruster",
            Muscle = "glutes",
            Equipment = "kettlebells",
            Instructions = "Clean two kettlebells to your shoulders. Clean the kettlebells to your shoulders by extending through the legs and hips as you pull the kettlebells towards your shoulders..."
        )

    def test_exercise_list_GET(self):
        response = self.client.get(self.exercises_url)

        self.assertEquals(response.status_code, 200)
    
    def test_exercise_list_GET_relevant_filter_queries(self):
        inital_count = Exercises.objects.count()

        response_1 = self.client.get(self.exercises_url, {"ExerciseName": "shrug"})
        response_2 = self.client.get(self.exercises_url, {"Muscle": "middle_back"})
        response_3 = self.client.get(self.exercises_url, {"Equipment": "barbell"})
        response_4 = self.client.get(self.exercises_url)

        self.assertEquals(response_1.status_code, 200)
        self.assertEquals(len(response_1.json()['exercises']), 1)

        self.assertEquals(response_2.status_code, 200)
        self.assertEquals(len(response_2.json()['exercises']), 1)

        self.assertEquals(response_3.status_code, 200)
        self.assertEquals(len(response_3.json()['exercises']), 2)

        self.assertEquals(response_4.status_code, 200)
        self.assertEquals(len(response_4.json()['exercises']), inital_count)

    
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

        initial_count = Exercises.objects.count()

        response = self.client.delete(self.exercise_detail_url, json.dumps({
            'id': 2
        }))

        self.assertEquals(response.status_code, 204)
        self.assertEquals(Exercises.objects.count(), initial_count - 1)

    def test_exercise_detail_DELETE_non_existent_id(self):
        
        Exercises.objects.create(
            ExerciseId = 2,
            ExerciseName = "Barbell sumo deadlift",
            Muscle = "lower_back",
            Equipment = "barbell",
            Instructions = "instructions for sumo deadlifts here..."
        )
        initial_count = Exercises.objects.count()

        response = self.client.delete(reverse('exercise_detail', args=[5300]))

        self.assertEquals(response.status_code, 404)
        self.assertEquals(Exercises.objects.count(), initial_count)
    
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
            DayId = 1,
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
    
    def test_day_detail_PUT_updates_day(self):

        Day.objects.create(
            DayId = 234,
            DayName = 'Day to update'
        )

        new_info = {'DayName': 'Updated day name'}

        response = self.client.put(reverse('day_detail', args=[234]), data=json.dumps(new_info), content_type='application/json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['DayName'], 'Updated day name')
    
    def test_day_detail_PUT_invalid_key(self):
        Day.objects.create(
            DayId = 345,
            DayName = 'Day to not update'
        )
        
        new_info = {'invalid_key': 'Updated day name'}

        response = self.client.put(reverse('day_detail', args=[345]), data=json.dumps(new_info), content_type='application/json')

        self.assertEquals(response.status_code, 400)

        response_for_validation = self.client.get(reverse('day_detail', args=[345]))

        self.assertEquals(response_for_validation.data['DayName'], 'Day to not update')
    
    def test_day_detail_PUT_updates_exercise_list(self):

        # use an existing exercise
        Exercises.objects.create(
            ExerciseId = 321,
            ExerciseName = "Standing Hammer Curls",
		    Muscle = "biceps",
			Equipment = "dumbbell",
			Instructions = "instructions for standing hammer curls"
        )

        new_data = {
            "DayName": self.day_example.DayName,
            "ExerciseId": 321
        }

        target_count = len(self.day_example.DayExercises.all()) + 1

        # send data using an existing exercise id
        response = self.client.put(reverse('day_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['DayName'], self.day_example.DayName)
        self.assertEquals(len(response.data['DayExercises']), target_count)

    def test_day_detail_PUT_non_existent_exercise_id(self):

        new_data = {
            "DayName": self.day_example.DayName,
            "ExerciseId": 942
        }

        target_count = len(self.day_example.DayExercises.all())

        response = self.client.put(reverse('day_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.data['msg'], "Exercise not found")
        self.assertEquals(target_count, len(self.day_example.DayExercises.all()))

    def test_day_detail_PUT_invalid_exercise_id(self):

        new_data = {
            "DayName": self.day_example.DayName,
            "ExerciseId": "not_an_id"
        }

        target_count = len(self.day_example.DayExercises.all())

        response = self.client.put(reverse('day_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['msg'], "Bad request")
        self.assertEquals(target_count, len(self.day_example.DayExercises.all()))
    
    def test_day_detail_PUT_removes_exercise_from_day(self):
        target_count = len(self.day_example.DayExercises.all()) - 1

        new_data = {
            "DayName": self.day_example.DayName,
            "exercise_id_to_remove": 556
        }

        response = self.client.put(reverse('day_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data['DayExercises']), target_count)

        removed_exercise = Exercises.objects.get(pk=new_data['exercise_id_to_remove'])
        self.assertEquals(removed_exercise, self.exercise_2)
    
    def test_day_detail_PUT_removes_non_existant_exercise_from_day(self):
        target_count = len(self.day_example.DayExercises.all())

        new_data = {
            "DayName": self.day_example.DayName,
            "exercise_id_to_remove": 8765
        }

        response = self.client.put(reverse('day_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')
        
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.data['msg'], "Exercise not found")
        self.assertEquals(target_count, len(self.day_example.DayExercises.all()))

    def test_day_detail_PUT_removes_invalid_exercise_id_from_day(self):
        target_count = len(self.day_example.DayExercises.all())

        new_data = {
            "DayName": self.day_example.DayName,
            "exercise_id_to_remove": "not an id"
        }

        response = self.client.put(reverse('day_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')
        
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['msg'], "Bad request")
        self.assertEquals(target_count, len(self.day_example.DayExercises.all()))



class TestRoutinesViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.routines_url = reverse('routines')
        self.routine_detail_url = reverse('routine_detail', args=[1])
        self.routine_example = Routine.objects.create(
            RoutineId = 1,
            RoutineName = 'Test routine'
        )
        self.day_example_1 = Day.objects.create(
            DayId = 444,
            DayName = 'Example Day 1'
        )
        self.day_example_2 = Day.objects.create(
            DayId = 445,
            DayName = 'Example Day 2'
        )
        self.exercise_1 = Exercises.objects.create(
            ExerciseId = 333,
			ExerciseName = "Bicep Curl",
			Muscle = "biceps",
			Equipment = "barbell",
			Instructions = "Perform a curl"
        )
        self.exercise_2 = Exercises.objects.create(
            ExerciseId = 334,
			ExerciseName = "Incline Hammer Curls",
		    Muscle = "biceps",
			Equipment = "dumbbell",
			Instructions = "Incline hammer curl instructions.."
        )
        self.day_example_1.DayExercises.add(333, 334)
        self.routine_example.RoutineDays.add(444, 445)
    
    def test_POST_adds_new_routine(self):

        current_routines = Routine.objects.all()
        assertion_length = len(current_routines) + 1
        new_routine = {
            'RoutineName': 'Routine 1',
            'RoutineDays': []
        }

        response = self.client.post(self.routines_url, new_routine)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['RoutineName'], 'Routine 1')
        self.assertEquals(len(response.data['RoutineDays']), 0)
        self.assertEquals(len(Routine.objects.all()), assertion_length)
    
    def test_POST_no_content(self):

        new_routine = {}

        current_routine_len = len(Routine.objects.all())
        response = self.client.post(self.routines_url, new_routine)
        

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['msg'], 'No content submitted')
        self.assertEquals(len(Routine.objects.all()), current_routine_len)
    
    def test_POST_invalid_key(self):
        new_routine = {
            'Invalid Key': 'test name',
            'RoutineDays': []
        }

        current_routines_len = len(Routine.objects.all())
        response = self.client.post(self.routines_url, new_routine)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['msg'], 'Bad request')
        self.assertEquals(len(Routine.objects.all()), current_routines_len)
    
    def test_POST_invalid_value(self):
        new_routine = {
            'RoutineName': 'Routine to test',
            'RoutineDays': 'Invalid key'
        }

        current_routines_len = len(Routine.objects.all())
        response = self.client.post(self.routines_url, new_routine)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['msg'], 'Bad request')
        self.assertEquals(len(Routine.objects.all()), current_routines_len)
    
    def test_GET_routines(self):

        response = self.client.get(self.routines_url)

        self.assertEquals(response.status_code, 200)
        self.assertGreater(len(response.json()['routines']), 0)

    def test_routine_detail_GET(self):
        response = self.client.get(self.routine_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['RoutineName'], 'Test routine')
    
    def test_routine_detail_GET_non_existent_id(self):
        response = self.client.get(reverse('routine_detail', args=[7500]))
        
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.data['msg'], 'Routine not found')

    def test_routine_detail_DELETE_deletes_routine(self):
        initial_routine_count = Routine.objects.count()

        Routine.objects.create(
            RoutineId = 23,
            RoutineName = 'routine to delete'
        )
        
        response = self.client.delete(self.routine_detail_url, json.dumps({
            'id': 23
        }))

        self.assertEquals(response.status_code, 204)
        self.assertEquals(Routine.objects.count(), initial_routine_count)

    def test_routine_detail_DELETE_non_existent_id(self):
        initial_routine_count = Routine.objects.count()

        response = self.client.delete(reverse('routine_detail', args=[4321]))

        self.assertEquals(response.status_code, 404)
        self.assertEquals(Routine.objects.count(), initial_routine_count)

    def test_routine_detail_PUT_updates_routine_name(self):
        Routine.objects.create(
            RoutineId = 678,
            RoutineName = 'Routine name to change'
        )

        new_info = {'RoutineName': 'Updated routine name'}

        response = self.client.put(reverse('routine_detail', args=[678]), data=json.dumps(new_info), content_type='application/json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['RoutineName'], 'Updated routine name')
    
    def test_routine_detail_PUT_invalid_key(self):
        Routine.objects.create(
            RoutineId = 679,
            RoutineName = 'Routine name to keep'
        )

        new_info = {'InvalidKey': 'Updated routine name'}

        response = self.client.put(reverse('routine_detail', args=[679]), data=json.dumps(new_info), content_type='application/json')

        self.assertEquals(response.status_code, 400)

        response_for_validation = self.client.get(reverse('routine_detail', args=[679]))

        self.assertEquals(response_for_validation.data['RoutineName'], 'Routine name to keep')

    def test_routine_detail_PUT_updates_day_list(self):
        # create a new day object
        # create a new_data dictionary using the day id from self.example_1
        # set target_count for routine_days
        Day.objects.create(
            DayId = 111,
            DayName = 'Test day for routine detail'
        )

        new_data = {
            "RoutineName": self.routine_example.RoutineName,
            "DayId": 111
        }

        target_count = len(self.routine_example.RoutineDays.all()) + 1

        response = self.client.put(reverse('routine_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['RoutineName'], self.routine_example.RoutineName)
        self.assertEquals(len(response.data['RoutineDays']), target_count)
    
    def test_routine_detail_PUT_non_existent_day_id(self):
        new_data = {
            "RoutineName": self.routine_example.RoutineName,
            "DayId": 112
        }

        target_count = len(self.routine_example.RoutineDays.all())

        response = self.client.put(reverse('routine_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.data['msg'], "Day not found")
        self.assertEquals(target_count, len(self.routine_example.RoutineDays.all()))
    
    def test_routine_detail_PUT_invalid_day_id(self):
        new_data = {
            "RoutineName": self.routine_example.RoutineName,
            "DayId": "not an id"
        }

        target_count = len(self.routine_example.RoutineDays.all())

        response = self.client.put(reverse('routine_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['msg'], "Bad request")
        self.assertEquals(target_count, len(self.routine_example.RoutineDays.all()))
    
    def test_routine_detail_PUT_removes_day_from_routine(self):
        target_count = len(self.routine_example.RoutineDays.all()) - 1

        new_data = {
            "RoutineName": self.routine_example.RoutineName,
            "day_to_remove": 445
        }

        response = self.client.put(reverse('routine_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data['RoutineDays']), target_count)

        removed_day = Day.objects.get(pk=new_data['day_to_remove'])
        self.assertEquals(removed_day, self.day_example_2)

    def test_routine_detail_PUT_removes_non_existant_day_from_routine(self):
        target_count = len(self.routine_example.RoutineDays.all())

        new_data = {
            "RoutineName": self.routine_example.RoutineName,
            "day_to_remove": 9876
        }

        response = self.client.put(reverse('routine_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')
        
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.data['msg'], "Day not found")
        self.assertEquals(target_count, len(self.routine_example.RoutineDays.all()))

    def test_routine_detail_PUT_removes_invalid_day_id_from_routine(self):
        target_count = len(self.routine_example.RoutineDays.all())

        new_data = {
            "RoutineName": self.routine_example.RoutineName,
            "day_to_remove": "not an id"
        }

        response = self.client.put(reverse('routine_detail', args=[1]), data=json.dumps(new_data), content_type='application/json')
        
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['msg'], "Bad request")
        self.assertEquals(target_count, len(self.routine_example.RoutineDays.all()))







