
import subprocess
import settings
from participant_info import participant_info

main_dir = settings.main_dir

# define function that executes scripts: a
def execute_script(script_path):
    try:
        # Provide the full path to the Python interpreter within the virtual environment
        python_interpreter = r'C:/Users/esthe/OneDrive/PhD/AR_Duisburg/fatigue_AR/.venv/Scripts/python.exe'
        subprocess.run([python_interpreter, script_path],
                       check=True,
                       capture_output=True, #print output from all scripts to console
                       text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}")
    except FileNotFoundError:
        print(f"Script '{script_path}' not found.")

# define function that defines scripts and order of executing and calling execute_script
def main():

    fatigue_quest = main_dir + 'fatigue_main.py'

    low_fatigue_practice = main_dir + 'low_practice_trials.py'
    low_fatigue_main = main_dir + 'low_fatigue_task.py'


    # Define the sequence of scripts to execute
    script_sequence = [

        fatigue_quest,

        low_fatigue_practice,
        low_fatigue_main,

        fatigue_quest,
    ]

    # get participant info
    sub_id, sub_age, sub_gender, sub_handedness, sub_language, sub_condition, sub_day = participant_info()

    # Execute the scripts in the defined sequence
    for script_path in script_sequence:
        print("Start of:", script_path)
        execute_script(script_path)

# we want to run the script when its called here as main and not as module
if __name__ == "__main__":
    main()


