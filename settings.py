
## This script contains global settings that refer to ALL scripts in the project a
# For file specific settings check the other settings.py script

import tkinter as tk

## TODO: Change in the beginning
save_results = True # set to True if you want to save the output (performance etc)

## Obtain actual screen size
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

## ------------- Experiment settings -------------------------------------------------------------------------------
letter_color = 'black'
letter_font = 'Open Sans'
bg_col = (140, 140, 140) #(166, 166, 166)  # (140, 140, 140)

# TODO ------ Control Variables -----------------------------------------------------------------
check_framerate = False # only for target task
# It is easier to debug the script in non-fullscreen mode
full_screen = True

## -------- Directories ---------------------------------------------------------------------------------------------

# Main directory containing all scripts:
main_dir = 'C:/Users/esthe/OneDrive/PhD/AR_Duisburg/fatigue-AR/'
print("main directory", main_dir)

# results dir all (for participant info)
results_dir_all =main_dir + 'results/'  # folder to store participant's results

# low fatigue task
resources_dir_low = main_dir + 'resources/low_resources/' # folder with instructions and fix cross png
results_dir_low =main_dir + 'results/'  # folder to store participant's results

# high fatigue task
resources_dir_high = main_dir + 'resources/high_resources/' # folder with instructions and fix cross png
results_dir_high =main_dir + 'results/'  # folder to store participant's results

# fatigue questionnaire
resources_dir_fatigue =main_dir + 'resources/fatigue_scale_resources/'  # folder to store participant's results


# questionnaires results
results_dir_question = main_dir + 'results/'

#------- Stim settings that are both for low and high fatigue task-------------------------------------------------

trial_num = 16  # trial number == number of individual stimuli
face_slide_dur = 1.2  # duration of face slide (in s)
stim_dur = 1.2  # duration, within "face_slide_dir" to present face stimulus
fix_cross_dur = 0.5  # duration of avergae fixation cross duration
fix_size = 100
fix_trigger = 100,
ITI_var = 0.15 # variation of fixation cross duration
pause_slide_dur = 30 # TODO: change to 30!
pause_slide_trigger = 10
face_size = 120 # None = default
target_stim_size = 0.1

# Numbers of Block
num_of_blocks_low = 3 # Low fatigue task
num_of_blocks_high = 7 # High fatigue task
num_of_blocks_target = 6 # Target task

# Trials per block
rep_of_list_target = 5 # TODO: 4 --> 4 x 8 = 32 stim per block
rep_of_list_high = 2 # TODO: set to 4
num_trials_per_block_high = 16 * rep_of_list_high

# Number of practice trials
num_of_practice_trials_target = 10

