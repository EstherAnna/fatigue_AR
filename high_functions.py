# All functions, classes etc. needed for high_fatigue_task.py

import random
from psychopy import event, visual, core, gui
import pandas as pd
import os
import settings

# Functions/Classes:
# - Create stimulus objects: stimulus (letter/number), fixation cross, pause slide
# - Create a list of stimulus objects
# - Randomize list of stimulus objects
# - Check response (letter pressed)
# - Update dataframe

# -----------------------------------------------------------------------------------------------------------------
# Create stimulus objects:
# -----------------------------------------------------------------

# Stimulus slide class: Letters and numbers
class StimSlide:

    def __init__(self, stim_file, stim_type, stim_size, stim_color, stim_trigger, slide_duration, stim_duration, win):
        self.stim_file = stim_file  # Path to the PNG with stimulus stimulus
        self.stim_type = stim_type  # Whether stimulus is "letter" or "number"
        self.stim_size = stim_size  # Stimulus size (in px)
        self.stim_trigger = stim_trigger  # Trigger associated with stim stimulus type
        self.slide_duration = slide_duration  # slide duration in s
        self.stim_duration = stim_duration  # time, within "slide_duration" to present stimulus
        self.win = win  # psychopy window on which to show slide
        self.stim_color = stim_color
        # self.stim_font = stim_font

        # Create psychopy visual object:
        self.visual_obj = visual.TextStim(win=self.win,
                                          text=self.stim_file,
                                          height=self.stim_size,
                                          color=self.stim_color) # for diode test change position: pos=(300,0)

    # Present a stimulus for fixed duration. Accept user input as answer:
    def present_slide(self, win, port=None):  # TODO: add "port" as additional input argument
        # Input:
        # - "p_port": parallel port to send trigger for stimulus presentation
        # Output:
        # - "key_pressed": either "left" or "right" if a key was pressed by participant, or "None" if no response
        # - "rt": either reaction time (time at which key is pressed) or "None" if no response

        key_pressed = None  # define variable to track key press
        rt = None  # define variable to record rt
        slide_timer = core.Clock()  # timer to keep track of slide duration
        slide_timer.reset()  # reset timer just in case
        t = slide_timer.getTime()  # get time
        event.clearEvents()  # clean events buffer
        trigger_sent = False # control variable for if the trigger has been sent already
        trigger_reset = False # control variable for if the trigger has been reset after being sent

        while t <= self.slide_duration:  # present slide until duration

            t = slide_timer.getTime()

            self.visual_obj.draw()

            # Time locked Trigger for stimulus presentation
            if port is not None: # If port is given as input argument
                if not trigger_sent:
                    self.win.callOnFlip(port.setData, self.stim_trigger) #time locked stimulus trigger
                    trigger_sent = True
                if t >= 0.1 and trigger_sent and not trigger_reset:
                    port.setData(0)
                    trigger_reset = True

            # Time locked trigger for button press
            if not key_pressed:  # check if answer is already provided
                key = event.getKeys(keyList=["y", "m"])  # get possible keys for answer
                if key:
                    rt = slide_timer.getTime()  # get reaction time
                    key_pressed = key[0]  # get key pressed
                    print("Key pressed:", key_pressed)
                    trigger_sent = False
                    trigger_reset = False
                    slide_timer.reset()  # reset timer just in case
                    t = slide_timer.getTime()  # get time

            self.win.flip()  # flip screen

        return key_pressed, rt


# -----------------------------------------------------------------------------------------------------------------
# Fixation cross slide

class FixCrossSlide:

    def __init__(self, stim_file, stim_type, stim_size, stim_color, stim_trigger, stim_duration, win):
        self.stim_file = stim_file  # Path to the PNG with stimulus stimulus
        self.stim_type = stim_type  # Whether stimulus is "letter" or "number"
        self.stim_size = stim_size  # Stimulus size (in px)
        self.stim_trigger = stim_trigger  # Trigger associated with stim stimulus type
        self.stim_duration = stim_duration  # time, within "slide_duration" to present stimulus
        self.win = win  # psychopy window on which to show slide
        self.stim_color = stim_color

        # Create psychopy visual object:
        self.visual_obj = visual.TextStim(win=self.win,
                                          text=self.stim_file,
                                          height=self.stim_size,
                                          color=self.stim_color)

    # Present fixation cross for fixed duration. No user input.
    def present_slide(self, port=None):  # method to visualize slide
        # fix cross dur: 0.5
        # ITI_var: 0.15
        ITI_var = 0.15
        fix_cross_slide_dur = 0.5

        # random INTEGER number between: ITI_var *-100 (=-15) and ITI_var * 100 (15)
        # first multiplying by 100 so the random number is an integer and then dividing again by 100
        # Any number between -0.15 and 0.15 is added on top of the fix_cross_duration

        iti_duration = fix_cross_slide_dur + (random.randint(ITI_var * -100, ITI_var * 100)) / 100 # Added

        slide_timer = core.Clock()  # timer to keep track of slide duration
        slide_timer.reset()  # reset timer just in case
        t = slide_timer.getTime()  # get time

        while t <= iti_duration:  # present slide until duration
            t = slide_timer.getTime()

            self.visual_obj.draw()
            self.win.flip()  # flip screen


# -----------------------------------------------------------------------------------------------------------------
# Pause slide

class PauseSlide:

    def __init__(self, win, stim_file, stim_trigger, stim_size, slide_duration):
        self.win = win  # psychopy window on which to show slide
        self.stim_file = stim_file  # Path to the PNG with fix cross
        self.stim_trigger = stim_trigger
        self.stim_size = stim_size  # Stimulus size (in px)
        self.slide_duration = slide_duration  # slide duration in s

        # Create psychopy visual object:
        self.visual_obj = visual.ImageStim(win=self.win,
                                           image=self.stim_file,
                                           size=self.stim_size)

    # Present pause slide for fixed duration. No user input.
    def present_slide(self, port=None):  # method to visualize slide

        slide_timer = core.Clock()  # timer to keep track of slide duration
        slide_timer.reset()  # reset timer just in case
        t = slide_timer.getTime()  # get time

        while t <= self.slide_duration:  # present slide until duration
            t = slide_timer.getTime()

            self.visual_obj.draw()
            self.win.flip()  # flip screen

# -----------------------------------------------------------------------------------------------------------------
# Object list
# -----------------------------------------------------------------------------------------------------------------
# This functions uses the stimulus objects and creates a list
def create_stim_slide_list(stim_size, slide_duration, stim_duration, stim_color, win):
    # Input:
    # - "file_path": path to directory containing PGN files
    # - "stim_size": size of the stimulus in px
    # - "slide_duration": duration of slide in s
    # - "stim_duration": duration, within "slide_duration", to present image
    # - "win": the psychopy "visual.Window" object defining the screen where stimulus is presented
    # Output:
    # - "StimSlide_list": list containing slide objects
    stim_list = ['2', '3', '4', '5', '6', '7', '8', '9', 'A', 'C', 'D', 'H', 'L', 'N', 'U', 'T']
    #stim_type = ["even_number", "odd_number", "even_number", "odd_number", "even_number", "odd_number", "even_number", "odd_number",
    #"letter", "letter", "letter", "letter" "letter", "letter", "letter", "letter"]
    #stim_trigger = ['22', '23', '24', '25', '26', '27', '28', '29', '11', '12', '13', '14', '15', '16', '17', '18']
    number_slide_list = []
    letter_slide_list = []

    for ii in range(settings.rep_of_list_high): # 4 times 16 stimuli = 64
        for i in range(0, len(stim_list)):
            if ("2" in stim_list[i]) or ("4" in stim_list[i]) or ("6" in stim_list[i]) or ("8" in stim_list[i]):
                stim_type = "even_number"
                if "2" in stim_list[i]:
                    stim_trigger = 202
                elif "4" in stim_list[i]:
                    stim_trigger = 204
                elif "6" in stim_list[i]:
                    stim_trigger = 206
                else: #8
                    stim_trigger = 208
            elif ("3" in stim_list[i]) or ("5" in stim_list[i]) or ("7" in stim_list[i]) or ("9" in stim_list[i]):
                stim_type = "odd_number"
                if "3" in stim_list[i]:
                    stim_trigger = 203
                elif "5" in stim_list[i]:
                    stim_trigger = 205
                elif "7" in stim_list[i]:
                    stim_trigger = 207
                else: #9
                    stim_trigger = 209
            else:
                stim_type = "letter"
                if "A" in stim_list[i]:
                    stim_trigger = 211
                elif "C" in stim_list[i]:
                    stim_trigger = 212
                elif "D" in stim_list[i]:
                    stim_trigger = 213
                elif "H" in stim_list[i]:
                    stim_trigger = 214
                elif "L" in stim_list[i]:
                    stim_trigger = 215
                elif "N" in stim_list[i]:
                    stim_trigger = 216
                elif "T" in stim_list[i]:
                    stim_trigger = 217
                else: #U
                    stim_trigger = 218

            # Create StimSlide object:
            this_stimulus = StimSlide(stim_file=stim_list[i],
                                      stim_type=stim_type,
                                      stim_size=stim_size,
                                      stim_color=stim_color,
                                      # stim_font=stim_fonts,
                                      stim_trigger=stim_trigger,
                                      slide_duration=slide_duration,
                                      stim_duration=stim_duration,
                                      win=win)
            # If the stimulus type from this_stimulus is number put it in the number slide list
            if (this_stimulus.stim_type == "odd_number") or (this_stimulus.stim_type=="even_number"):
                # Append this object to stimuli list:
                number_slide_list.append(this_stimulus)
            # otherwise its a letter so put it in the letter slide list
            else:
                # Append this object to stimuli list:
                letter_slide_list.append(this_stimulus)

    return number_slide_list, letter_slide_list


# ----------------------------------------------------------------------------------------------------------------
# (Pseudo-) Randomization
# -------------------------------------------------------------------------------------------------------
# Random shuffle the letter slide list BUT:
#  - still include around 30% of the trials to be 2-back trials
#    = 30% of the stimuli correspond to the stimulus two stimuli before
#  - not 4 times the same letter
# As input: letter_slide list created in "create_stim_slide_list"

def randomize_letters(letter_slide_list, perc_of_two_back):

    # make a copy of the original list
    list_of_letters = letter_slide_list.copy()

    # calculate how many elements of the list should be two-back trials (e.g. 30 %)
    percentage = int(len(list_of_letters) * perc_of_two_back)
    # set looping to true (as long as condition is not ful
    find_random = True

    while find_random:
        # set counter for counting the number of two-back trials
        count_2_back = 0
        # set counter for counting the number of 4x same stimulus in a row
        count_seq_4 = 0
        # count how many two-back trials in a row, we do not want more than 3
        count_two_back_reps = 0
        # shuffle the list
        random.shuffle(list_of_letters)

        # we loop through each element but start with the 2nd one because 0 and 1 cannot be 2-back trials
        for i in range(2, len(list_of_letters)):
            # compare current letter with the one two letters before
            if list_of_letters[i].stim_trigger == list_of_letters[i-2].stim_trigger:
                # if its the same count 1 two-back trial
                count_2_back += 1
            # compare four elements in a row
            if (
                list_of_letters[i].stim_trigger == list_of_letters[i-1].stim_trigger
                and list_of_letters[i-1].stim_trigger == list_of_letters[i-2].stim_trigger
                and list_of_letters[i-2].stim_trigger == list_of_letters[i-3].stim_trigger
            ):
                # if they are all the same count 1 case of 4 repetitions
                count_seq_4 += 1
            if (
                list_of_letters[i].stim_trigger == list_of_letters[i-2].stim_trigger
                and list_of_letters[i].stim_trigger == list_of_letters[i-4].stim_trigger
            ):
                count_two_back_reps +=1
            # if the two-back counter is the same as the desired percentage and there are no cases of four repetitions:
            if (count_2_back == percentage) and (count_seq_4 == 0) and (count_two_back_reps == 0):
                # set find_random to false, so the loop stops
                find_random = False
                letter_list = list_of_letters.copy()
                #print(letter_list)


    return letter_list

# -----------------------------------------------------------------------------------------------------------------
# Response
# -----------------------------------------------------------------------------------------------------------------

# Function to check for correct/incorrect answer

def check_answer(key_pressed, response_order, stim_type, port, win):
    # Inputs:
    # - "key_pressed": either "left" or "right" if a key was pressed by participant, or "None" if no response was given
    # - "response_order": ["odd", "two_back_trial"], ["even", "two_back_trial"], ["even", "two_back_trial"], ["two_back_trial", "even"]
    # - "stim_type": the .stim_type attribute of the StimSlide object of current trial
    #
    # Output:
    # - "result": either "correct", "incorrect", or "None"

    result = None  # default result
    slide_timer = core.Clock()  # timer to keep track of slide duration
    slide_timer.reset()  # reset timer just in case
    t = slide_timer.getTime()  # get time

    if key_pressed:  # check if response was given
        if key_pressed == "y":  # check which response was given
            if response_order[0] == stim_type:  # check if coincides with current stimulus type
                result = "correct"
                print("correct")
            else:
                result = "incorrect"
                print("incorrect")

        elif key_pressed == "m":
            if response_order[1] == stim_type:
                result = "correct"
                print("correct")
            else:
                result = "incorrect"
                print("incorrect")
    if not key_pressed:  # if no key was pressed
        if (response_order[0] == stim_type) or (response_order[1] == stim_type):  # check if should have pressed
            result = "miss"
            print("miss")
        else:
            result = "correct"
            print("correct")

    print("Response:", result)

    return result
# -----------------------------------------------------------------------------------------------------------------
# Output dataframe
# -----------------------------------------------------------------------------------------------------------------

# Function to update "results" data-frame
def update_results(results_df, key_pressed, sub_id, trial, total_trial, block, stimulus, stim_type, stim_dur, stim_trigger, result, rt):
    # Input:
    #   - "results_df": data-frame with results to update
    #   - "trial": current trial number
    #   - "stim_type": the .stim_type attribute of current trial's StimSlide object
    #   - "result": result of the current trial
    #   - "rt": reaction time of current trial response
    # Output:
    #   - "results_df": input data-frame updated with results of current trial

    # Add new line to "results_df":
    results_df = pd.concat([results_df,
                            pd.DataFrame([{"ID": sub_id,
                                           "Total_trial": total_trial,
                                           "Trial": trial,
                                           "Block": block,
                                           "Stimulus": stimulus,
                                           "Response": key_pressed,
                                           "Type": stim_type,
                                           "Duration": stim_dur,
                                           "Trigger": stim_trigger,
                                           "Result": result,
                                           "RT": rt}])])

    return results_df
