import csv
import random

from psychopy import gui, visual, event, core, monitors
import sys
import settings
from quest_show_instructions import show_instructions
import json

import os
from psychopy import gui

# Function to check if a file already exists
def check_file_existence(folder, file_name):
    file_path = os.path.join(folder, file_name)
    return os.path.exists(file_path)

if settings.save_results:

    # Load participant info that was saved in json file
    json_filename = settings.results_dir_all + 'current_info.json'
    with open(json_filename, 'r') as json_file:
        participant_info = json.load(json_file)

    # access participant info
    sub_id = participant_info['id']
    sub_language = participant_info['language']
    sub_condition = participant_info['condition']

    while True:
        exp_info = {u"fatigue_scale_session": u"", }
        dlg = gui.DlgFromDict(dictionary=exp_info, title="fatigue_scale")

        # Store aside values from the gui for easier manipulation
        sub_fatigue_session = int(exp_info['fatigue_scale_session'])

         # Define file name
        file_name = (settings.results_dir_question + str(sub_id) + "_" + str(sub_condition) + "_fatigue_scale_session_" +
                     str(sub_fatigue_session) + ".csv")
        # Specify your folder where the CSV files are stored
        csv_folder = settings.results_dir_question

        # check if that file already exists
        if not check_file_existence(csv_folder, file_name):
            break
        else:
            print(
                f"A file with session number {sub_fatigue_session} already exists. Please enter a different session number.")

        # Now you have a unique session number that can be used to save your data
        print(f"Selected session number: {sub_fatigue_session}")

else:
    sub_language = "English"
    sub_fatigue_session = random.randint(1, 5)

print("fatigue session", sub_fatigue_session)
##---------------------------------------------------------------------------------------------------------------------
# Initialize PsychoPy window
win = visual.Window(size=(settings.screen_width, settings.screen_height),
                    units='pix',
                    useRetina=True,
                    color=settings.bg_col,
                    colorSpace='rgb255',
                    fullscr=True)

##---------------------------------------------------------------------------------------------------------------------
# Define instructions and questions and the corresponding scale labels

# Depending on the language:
if sub_language == "english" or sub_language == "English" or sub_language == "Englisch" or sub_language == "englisch":
    # end text
    end_text = visual.ImageStim(win=win,
                                image=settings.resources_dir_fatigue + "english/end.png",
                                size=(settings.screen_width, settings.screen_height))
    # Dont repeat the entire instructions every time, but only for the first round
    if sub_fatigue_session == 1:
        instruction_img = [settings.resources_dir_fatigue + "english/intro_" + s + ".png" for s in ["1", "2", "3", "4", "5"]]
    else:
        instruction_img = [settings.resources_dir_fatigue + "english/intro_" + s + ".png" for s in ["5"]]

    questions = [("How tired are you?"),
                 ("How sleepy are you?"),
                 ("How drowsy are you?"),
                 ("How fatigued are you?"),
                 ("How worn out are you?"),
                 ("How energetic are you?"),
                 ("How active are you?"),
                 ("How vigorous are you?"),
                 ("How efficient are you?"),
                 ("How lively are you?"),
                 ("How bushed are you?"),
                 ("How exhausted are you?"),
                 ("How much effort is it to keep your eyes open?"),
                 ("How much effort is it to move your body?"),
                 ("How much effort is it to concentrate?"),
                 ("How much effort is it to carry on a conversation?"),
                 ("How much desire do you have to close your eyes?"),
                 ("How much desire do you have to lie down?"),
                 ]
    scale_labels_left = [("not at all"),
                         ("not at all"),
                         ("not at all"),
                         ("not at all"),
                         ("not at all"),
                         ("not at all"),
                         ("not at all"),
                         ("not at all"),
                         ("not at all"),
                         ("not at all"),
                         ("not at all"),
                         ("not at all"),
                         ("no effort \n at all"),
                         ("no effort \n at all"),
                         ("no effort \n at all"),
                         ("no effort \n at all"),
                         ("absolutely \n no desire"),
                         ("absolutely \n no desire")]

    scale_labels_right = [("extremely"),
                          ("extremely"),
                          ("extremely"),
                          ("extremely"),
                          ("extremely"),
                          ("extremely"),
                          ("extremely"),
                          ("extremely"),
                          ("extremely"),
                          ("extremely"),
                          ("extremely"),
                          ("extremely"),
                          ("a tremendous \n chore"),
                          ("a tremendous \n chore"),
                          ("a tremendous \n chore"),
                          ("a tremendous \n chore"),
                          ("tremendous \n desire"),
                          ("tremendous \n desire")]


    # Initialize text stimuli for left labels
    label_stim_left = []
    for label in scale_labels_left:
        left_label = visual.TextStim(win, text=label, color='Black', height=(settings.screen_height // 30),
                                     pos=(-(settings.screen_width // 2.5), -(settings.screen_height // 30)))
        label_stim_left.append(left_label)
    # Initialize text stimuli for right labels
    label_stim_right = []
    for label in scale_labels_right:
        right_label = visual.TextStim(win, text=label, color='Black', height=(settings.screen_height // 30),
                                      pos=((settings.screen_width // 2.5), -(settings.screen_height // 30)))
        label_stim_right.append(right_label)
else: #german
    # end text
    end_text = visual.ImageStim(win=win,
                                image=settings.resources_dir_fatigue + "german/end.png",
                                size=(settings.screen_width, settings.screen_height))
    # Dont repeat the entire instructions every time, but only for the first round
    if sub_fatigue_session == 1:
        instruction_img = [settings.resources_dir_fatigue + "german/intro_" + s + ".png" for s in ["1", "2", "3", "4", "5"]]
    else:
        instruction_img = [settings.resources_dir_fatigue + "german/intro_" + s + ".png" for s in ["5"]]
    questions = [
        ("Wie müde bist du?"),
        ("Wie verschlafen bist du?"),
        ("Wie schläfrig bist du?"),
        ("Wie antriebslos bist du?"),
        ("Wie schlapp bist du?"),
        ("Wie energiegeladen bist du?"),
        ("Wie aktiv bist du?"),
        ("Wie energisch bist du?"),
        ("Wie leistungsfähig bist du?"),
        ("Wie lebhaft bist du?"),
        ("Wie ausgelaugt bist du?"),
        ("Wie erschöpft bist du?"),
        ("Wie viel Anstrengung erfordert es, deine Augen offen zu halten?"),
        ("Wie viel Anstrengung erfordert es, deinen Körper zu bewegen?"),
        ("Wie viel Anstrengung erfordert es, dich zu konzentrieren?"),
        ("Wie viel Anstrengung erfordert es, ein Gespräch zu führen?"),
        ("Wie stark ist dein Verlangen, deine Augen zu schließen?"),
        ("Wie stark ist dein Verlangen, dich hinzulegen?")
    ]
    scale_labels_left = ["gar nicht",
                         "gar nicht",
                         "gar nicht",
                         "gar nicht",
                         "gar nicht",
                         "gar nicht",
                         "gar nicht",
                         "gar nicht",
                         "gar nicht",
                         "gar nicht",
                         "gar nicht",
                         "gar nicht",
                         "gar keine \n Anstrengung",
                         "gar keine \n Anstrengung",
                         "gar keine \n Anstrengung",
                         "gar keine \n Anstrengung",
                         "gar kein \n Verlangen",
                         "gar kein \n Verlangen"]

    scale_labels_right = [("extrem"),
                          ("extrem"),
                          ("extrem"),
                          ("extrem"),
                          ("extrem"),
                          ("extrem"),
                          ("extrem"),
                          ("extrem"),
                          ("extrem"),
                          ("extrem"),
                          ("extrem"),
                          ("extrem"),
                          ("extreme \n Anstrengung"),
                          ("extreme \n Anstrengung"),
                          ("extreme \n Anstrengung"),
                          ("extreme \n Anstrengung"),
                          ("extremes \n Verlangen"),
                          ("extremes \n Verlangen")]

    label_stim_left = []
    for label in scale_labels_left:
        left_label = visual.TextStim(win, text=label, color='Black', height=(settings.screen_height // 30),
                                     pos=(-(settings.screen_width // 2.5), -(settings.screen_height // 30)))
        label_stim_left.append(left_label)
    # Initialize text stimuli for right labels
    label_stim_right = []
    for label in scale_labels_right:
        right_label = visual.TextStim(win, text=label, color='Black', height=(settings.screen_height // 30),
                                      pos=((settings.screen_width // 2.5), -(settings.screen_height // 30)))
        label_stim_right.append(right_label)

##---------------------------------------------------------------------------------------------------------------------
## Instructions

show_instructions(instruction_img, win)

##---------------------------------------------------------------------------------------------------------------------
## Main loop of questions

continue_end = False
# Initialize an empty list to store user responses
user_responses = []
# Get input for each question
for i, question in enumerate(questions):


    left_label = label_stim_left[i]
    right_label = label_stim_right[i]

    # initialize keys to close the experiment
    # Add pause/close panic button:
    if event.getKeys('escape'):
        pause = True
        while pause:
            if event.getKeys('escape'):
                pause = False
            # both tab and space have to be pressed, which makes it less likely that the experiment is aborted by accident
            elif event.getKeys('tab'):
                print("TAB")
                if event.getKeys('space'):
                    print("SPACE")
                    sys.exit()

    # get stim text from current question
    text_stim = visual.TextStim(win, color="Black", text=question, pos=(0, (settings.screen_height // 5)),
                                height= (settings.screen_height // 23))
    scale_stim = visual.RatingScale(win, choices=range(0, 11), markerStart=5, minTime = 0.5, marker='triangle', stretch=2.2,
                                    textColor="Black", showAccept=False, tickHeight=1.2, pos=(0, -(settings.screen_height // 30)))

    while scale_stim.noResponse:

        text_stim.draw()
        left_label.draw()
        right_label.draw()
        scale_stim.draw()
        win.flip()

    response = scale_stim.getRating()
    user_responses.append(response)

# Write user responses to the CSV file:
if settings.save_results:
    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["ID", "Fatigue_Session", "Question", "Response"])  # Headers row
        for i, question in enumerate(questions):
            csv_writer.writerow([sub_id, sub_fatigue_session, question, user_responses[i]])
    print("User responses saved to", file_name)
else:
    print("No file saved.")

# Define control variable:
continue_end = True

# Display experiment end text:
while continue_end:
    end_text.setAutoDraw(True)
    win.flip()
    # When 'space' is pressed BY THE EXPERIMENTER, close the system:
    if event.getKeys("space"):  # continue with space
        end_text.setAutoDraw(False)
        continue_end = False
        win.flip()
        sys.exit()

# Close the PsychoPy window after a short delay
core.wait(1)
win.close()
core.quit()