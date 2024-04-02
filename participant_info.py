import settings
from psychopy import gui
import pandas as pd
import os
import json

# Gui and output file

# At experiment start, a gui is displayed, asking for participant's gender, age and id.
# From this information, a .csv file is created, which will also store results from all experimental trials.
# This code will also check if the current file (named after the participants id) already exists in the directory
# if yes, you have to re-enter the participants info

def file_exists(filepath):
    return os.path.isfile(filepath)

def participant_info():

    # Information to ask:
    exp_info = {
        u"gender": u"",
        u"age": u"",
        u"id": u"",
        u"handedness": u"",
        u"language": u"",
        u"condition": u"",
        u"day": u"",

    }

    # Call gui with choices parameter for the language field:
    dlg = gui.DlgFromDict(dictionary=exp_info, title="info") #, fixed=["language"], choices={"language": language_choices})

    # Store aside values from the gui for easier manipulation:
    sub_id = int(exp_info['id'])  # Participant's id
    sub_age = int(exp_info['age'])  # Participant's age
    sub_gender = str(exp_info['gender'])  # Participant's gender
    sub_handedness = str(exp_info['handedness'])
    sub_language = str(exp_info['language']) # preferred language
    sub_condition = str(exp_info['condition'])  # preferred language
    sub_day = int(exp_info['day'])  # preferred language

    # Define df and store results:
    info = pd.DataFrame({
        'id': [sub_id],
        'age': [sub_age],
        'gender': [sub_gender],
        'handedness': [sub_handedness],
        'language': [sub_language],
        'condition': [sub_condition],
        'day': [sub_day],
    })

    # Create a .csv file using participant's id as file name:
    this_filename = settings.results_dir_all + exp_info['id'] + "_" + exp_info['condition'] + "_info.csv"

    if file_exists(this_filename):
        print(f"Warning: File {this_filename} already exists in the directory")
        print("Re-enter the participant info")

        exp_info = {
            u"gender": u"",
            u"age": u"",
            u"id": u"",
            u"handedness": u"",
            u"language": u"",
            u"condition": u"",
            u"day": u"",

        }
        dlg = gui.DlgFromDict(dictionary=exp_info,
                              title="info")  # , fixed=["language"], choices={"language": language_choices})

        sub_id = int(exp_info['id'])  # Participant's id
        sub_age = int(exp_info['age'])  # Participant's age
        sub_gender = str(exp_info['gender'])  # Participant's gender
        sub_handedness = str(exp_info['handedness'])
        sub_language = str(exp_info['language'])  # preferred language
        sub_condition = str(exp_info['condition'])  # preferred language
        sub_day = int(exp_info['day'])  # preferred language

        info = pd.DataFrame({
            'id': [sub_id],
            'age': [sub_age],
            'gender': [sub_gender],
            'handedness': [sub_handedness],
            'language': [sub_language],
            'condition': [sub_condition],
            'day': [sub_day],
        })

        # Create a .csv file using participant's id as file name:
        this_filename = settings.results_dir_all + exp_info['id'] + "_" + exp_info['condition'] + "_info.csv"

    # save sub_info as csv
    info.to_csv(this_filename)
    # save also json file: access variables in other scripts
    json_filename = settings.results_dir_all + 'current_info.json'
    with open(json_filename, 'w') as json_file:
        json.dump({'id':sub_id, 'age': sub_age, 'gender': sub_gender, 'handedness': sub_handedness,
                   'language': sub_language, 'condition': sub_condition, 'day': sub_day}, json_file)


    return sub_id, sub_age, sub_gender, sub_handedness, sub_language, sub_condition, sub_day