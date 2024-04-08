from psychopy import gui, visual, core, event, parallel
from psychopy.constants import *
import pandas as pd
import random
import settings
from low_functions import FixCrossSlide, PauseSlide, StimSlide, randomize_letters, create_stim_slide_list, check_answer, update_results
from show_instructions import show_instructions
import copy
import json

# -----------------------------------------------------------------------------------------------------------------
# Preliminary steps
screen_width = settings.screen_width
screen_height = settings.screen_height
disp_size_pix = (screen_width, screen_height)

# Load participant info that was saved in json file
json_filename = settings.results_dir_all + 'current_info.json'
with open(json_filename, 'r') as json_file:
    participant_info = json.load(json_file)

# access participant info
sub_id = participant_info['id']
sub_language = participant_info['language']

# -------------------------------------------------------------------------------------------------------------------
# Set the directory for either english or german slides:

if (sub_language == "english") or (sub_language == "English"):
    resources_dir = settings.resources_dir_low + '/english/'
    instruction_img = [resources_dir + "practice_" + s + ".png" for s in ["1", "2", "3", "4", "5", "6", "7"]]
    key_order = ['two_back_trial']
    print("english")
else:
    resources_dir = settings.resources_dir_low + '/german/'
    instruction_img = [resources_dir + "practice_" + s + ".png" for s in ["1", "2", "3", "4", "5", "6", "7"]]
    key_order = ['two_back_trial']
    print("german")

# -----------------------------------------------------------------------------------------------------------------

# Define parallel port
p_port = None

# ----------------------------------------------------------------------------------------------------------------------
# Main window object

win = visual.Window(size=disp_size_pix,
                    fullscr=True,
                    useRetina=True,
                    screen=0,
                    color=settings.bg_col,
                    colorSpace='rgb255',
                    units='pix')

# Hide mouse pointer. This is a workaround an apparent bug in Psychopy which keeps the pointer visible even when set
# to 'False' when this is specified in the 'visual.Window' parameters.
my_mouse = event.Mouse(win=win)
my_mouse.setVisible(False)

# -----------------------------------------------------------------------------------------------------------------

# Display instructions
show_instructions(instruction_img, win, port=p_port)

# -----------------------------------------------------------------------------------------------------------------
# Create slide objects with randomization etc.

# We create a list of lists with randomized objects for both numbers and letter
# In the main loop we take one list for each block

# store each list in a list:
all_lists_letters = []

block = 0
while block <= 1:
    # create different slide objects for each block (with different adresses!!)
    letter_slide_list = create_stim_slide_list(stim_size=settings.face_size,
                                               slide_duration=settings.face_slide_dur,
                                               stim_duration=settings.stim_dur,
                                               stim_color=settings.letter_color,
                                               # stim_font=settings.letter_font,
                                               win=win)
    random.shuffle(letter_slide_list)
    # randomize the current object slide list
    letter_list = randomize_letters(letter_slide_list=letter_slide_list, perc_of_two_back = 0.3)
    all_lists_letters.append(letter_list)
    print("randomization done")
    block +=1

# create a list of lists containing a 1 if the current trial is a two-back-trial and 0 if not
which_rename_all = []

for each in range(0, len(all_lists_letters)):
    current_list = all_lists_letters[each].copy()
    index_to_rename = [0, 0]
    for e in range(2, len(current_list)):
        if current_list[e].stim_trigger == current_list[e-2].stim_trigger:
            index_to_rename.append(1)
        else:
            index_to_rename.append(0)
    which_rename_all.append(index_to_rename)
    print(which_rename_all)

# In the letter list rename the elements in the "all_lists" that have 1 in "rename_all_lists" and store it in all_renamed_lists
all_renamed_lists =[]

for each in range(0, len(all_lists_letters)):
    renamed_list = []
    current_list = all_lists_letters[each].copy()
    rename_current_list = which_rename_all[each].copy()
    for name in range(len(rename_current_list)):
        print(rename_current_list[name])
        if rename_current_list[name] == 1:
            current_list[name].stim_type = "two_back_trial"
            current_list[name].stim_trigger = int(str(current_list[name].stim_trigger) + str(1))
        renamed_list.append(current_list[name])
    all_renamed_lists.append(renamed_list)


#----------------------------------------------------------------------------------------------------------------------
# Fixation Cross slide:
fixcross_slide = FixCrossSlide(stim_file='+',
                               stim_type="fix_cross",
                               stim_size=settings.fix_size,
                               stim_color=settings.letter_color,
                               stim_trigger=settings.fix_trigger,
                               stim_duration=settings.fix_cross_dur,
                               win=win)

# Pause Slide:
pause_slide = PauseSlide(win=win,
                             stim_file=resources_dir + "pause_1.png",
                             stim_trigger=settings.pause_slide_trigger,
                             stim_size=disp_size_pix,
                             slide_duration=settings.pause_slide_dur)
# -----------------------------------------------------------------------------------------------------------------
# Main loop

# Loop through trials.
# For each trial present a Fixation Cross slide followed by a Face slide
# During each face slide, check if response was given and in case record response and reaction type
# At the end of the trial, update "results" data-frame

core.wait(1)  # wait a bit before starting first trial

# to try out things:
# letter_list = ['A', 'C', 'D', 'H', 'L', 'N', 'U', 'T'] * 4
# random.shuffle(letter_list)

# set the performance limit to 85 percent
this_block = 1
all_trials = 1
stimulus_duration = settings.stim_dur

for this_block in range(1): # only 1 block in practice

    # Block trigger: (51, 52, 53, 54,...)
    print("block" + str(this_block+1+50))
    # TODO port trigger for block: port.setData(this_block + 1 + 50)

    this_letter_list = all_renamed_lists[this_block].copy()

    if this_block >= 1:


        fixcross_slide.present_slide(port=p_port)  # TODO: add "port=p_port" in the brackets

        # Display pause slide for 30 s:
        # Define pause slide image files to load:
        pause_slide.present_slide()
        pause_img_2 = [settings.resources_dir_low + "pause_2.png"]
        show_instructions(pause_img_2, win)

    for this_trial in range(20): # 20 practice trials
        print("trial loop entered")

        # Add pause/close panic button:
        # both tab and space have to be pressed, which makes it less likely that the experiment is aborted by accident
        if event.getKeys('escape'):
            pause = True
            while pause:
                if event.getKeys('escape'):
                    pause = False
                elif event.getKeys('tab'):
                    print("TAB")
                    if event.getKeys('space'):
                        print("force quit")
                        sys.exit()

        # Letter slide:

        fixcross_slide.present_slide(port=p_port)

        this_letter_slide = this_letter_list[this_trial]  # get current face slide


        print(this_letter_slide.stim_duration)

        # present face slide and update response, if any:
        key_pressed, rt = this_letter_slide.present_slide(port=p_port, win=win)

        all_trials +=1

# -----------------------------------------------------------------------------------------------------------------

# 14 Display end text

print("END")

# Display end text and account balance.
end_text = visual.ImageStim(win=win,
                            image=resources_dir + "end_1.png",
                            size=disp_size_pix)

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