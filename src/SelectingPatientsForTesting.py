import random
from datetime import datetime
from functools import wraps
# A decorator for logging the date and time when selecting patients for testing.
def log_selection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Before executing the function, print the current date and time.
        print(f"Selection Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # Execute the decorated function.
        return func(*args, **kwargs)
    return wrapper

class PatientTester:
    def __init__(self, recovered_patients):
        self.recovered_patients = recovered_patients

    def split_list(self,x):
      return [self.recovered_patients[i:i+x] for i in range(0, len(self.recovered_patients), x)]
  
    # Method to let the user select patients for testing
    @log_selection
    # Method to let the user select patients for testing
    def user_select_patients_for_testing_randomly(self,slected_number_patients):   
        newlist = []
        try:
            for i in slected_number_patients:
            # print(i)
                newlist.append("Patient " + random.choice(i) +" selected on :" + str(datetime.now()))
            # return selected_patients
            return newlist
        except ValueError:
            print("Invalid input! Please enter numbers only.")
            return []
        except IndexError:
            print("One or more selected numbers are out of range.")
            return []

# The initial list of recovered patients.
recovered_patients = [
    'p1', 'p2', 'p3', 'p4', 'p5',
    'p6', 'p7', 'p8', 'p9', 'p10',
    'p11', 'p12', 'p13', 'p14', 'p15',
    'p16', 'p17', 'p18', 'p19', 'p20'
]

# Create an instance of PatientTester with the list of recovered patients.
patient_list = PatientTester(recovered_patients)

print("The patient list:",patient_list.recovered_patients)

selected_recovered_patients = int(input("Enter the numbers of the patients you want to select for testing, separated by commas (e.g., 1,2,3): "))

# Allow the user to select patients for testing.
selected_patients = patient_list.user_select_patients_for_testing_randomly(patient_list.split_list(selected_recovered_patients))

# Print the selected patients.
if selected_patients:
    for patient in selected_patients:
        print(f"Selected Patients for Testing:",patient)
else:
    print("No valid patients were selected for testing.")