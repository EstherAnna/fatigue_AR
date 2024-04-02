from psychopy import gui, visual, core, event, parallel
from psychopy.constants import *
import pandas as pd
import random
import settings
from low_functions import StimSlide, FixCrossSlide, PauseSlide, randomize_letters, create_stim_slide_list, check_answer, update_results
from show_instructions import show_instructions
import json

# -----------------------------------------------------------------------------------------------------------------
# Preliminary steps a

screen_width = settings.screen_width
screen_height = settings.screen_height
disp_size_pix = (screen_width, screen_height)

# Gui and output file

# At experiment start, a gui is displayed, asking for participant's gender, age and id.
# From this information, a .csv file is created, which will also store results from all experimental trials.

if settings.save_results:

    # Load participant info that was saved in json file
    json_filename = settings.results_dir_all + 'current_info.json'
    with open(json_filename, 'r') as json_file:
        participant_info = json.load(json_file)

    # acess participant info
    sub_id = participant_info['id']
    sub_language = participant_info['language']

    # Define df to store results:
    results = pd.DataFrame(columns=["ID",
                                    "Total_trial",
                                    "Trial",  # Trial number
                                    "Block",
                                    "Stimulus",
                                    "Response",
                                    "Type",  # "letter" or "number"
                                    "Duration",
                                    "Trigger",
                                    "Result",  # "correct" or "incorrect" (for letter/number face)
                                    "RT"])  # Reaction Time

    # Create a .csv file using participant's id as file name:
    this_filename = settings.results_dir_low + str(sub_id) + "_low.csv"
else:
    sub_id = 3
    sub_language = "english"

#-------------------------------------------------------------------------------------------------------------------
# Set the directory for either english or german slides:

if (sub_language == "english") or (sub_language == "English"):
    resources_dir = settings.resources_dir_low + '/english/'
    instruction_img = [resources_dir + "reminder_" + s + ".png" for s in ["1", "2"]]
    key_order = ['two_back_trial']
    print("english")
else:
    resources_dir = settings.resources_dir_low + '/german/'
    instruction_img = [resources_dir + "reminder_" + s + ".png" for s in ["1", "2"]]
    key_order = ['two_back_trial']
    print("german")

# ------Define parallel port-------------------------------------------------------------------------------------
p_port = None

# ------Main window object-------------------------------------------------------------------------------------------
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

# -------Play instructions----------------------------------------------------------------------------------------
show_instructions(instruction_img, win, port=p_port)

# -----Create letter slides-------------------------------------------------------------------------------------
# - We create a list of lists with randomized objects for both numbers and letter
# - In the main loop we take one list for each block

# store each list in a list:
all_lists_letters = []

block = 0
while block <= settings.num_of_blocks_low:
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
            current_list[name].stim_trigger = current_list[name].stim_trigger + 10
        renamed_list.append(current_list[name])
    all_renamed_lists.append(renamed_list)


#--------Create other slides--------------------------------------------------------------------------------------
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
# Start eeg recording
print("START ")

# -----Main loop----------------------------------------------------------------------------------------------
# - Loop through blocks
# - loop through trials
# - For each trial present a Fixation Cross slide followed by a stimulus slide
# - During each stimulus slide, check if response was given and in case record response and reaction type
# - At the end of the trial, update "results" data-frame

core.wait(1)  # wait a bit before starting first trial

# Set some parameters
this_block = 1
all_trials = 1
stimulus_duration = settings.stim_dur

# ----------- Block ---------------------------------------------------------------------------------------------------
for this_block in range(0, len(all_renamed_lists)):

    # Block trigger: (151, 152, 153, 154,...)
    print("block" + str(this_block + 1 + settings.block_trigger))

    if settings.working_in_lab:
    # Block number trigger
        print("block " + str(this_block + 1 + settings.block_trigger))
        p_port.setData(this_block + 1 + settings.block_trigger)
        core.wait(0.05)
        p_port.setData(0)
    else:
        # Block trigger: (51, 52, 53, 54,...)
        print("block" + str(this_block + 1 + settings.block_trigger))

    this_letter_list = all_renamed_lists[this_block].copy()

    if this_block >= 1:

        fixcross_slide.present_slide(port=p_port)  # TODO: add "port=p_port" in the brackets

        # Display pause slide for 30 s:
        # Define pause slide image files to load:
        pause_slide.present_slide(port=p_port)
        # pause_img_1 = [settings.resources_dir + "pause_english_1.png"]
        # show_pause(pause_img_1, win)
        # Are you ready?
        pause_img_2 = [resources_dir + "pause_2.png"]
        show_instructions(pause_img_2, win, port=p_port)

    # ----------- Trial ---------------------------------------------------------------------------------------------------
    for this_trial in range(len(this_letter_list)):
        print("trial loop entered")

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
                        #p_port.setData(settings.end_trigger)
                        sys.exit()

        # Letter slide:

        fixcross_slide.present_slide(port=p_port)  # TODO: add "port=p_port" in the brackets

        this_letter_slide = this_letter_list[this_trial]  # get current face slide

        # reduce stimulus duration if previous block was good
        this_letter_slide.stim_duration = stimulus_duration
        this_letter_slide.slide_duration = stimulus_duration

        # present face slide and update response, if any:
        key_pressed, rt = this_letter_slide.present_slide(port=p_port, win=win)  # TODO: fix "port" port=p_port

        # check answer, if any:
        result = check_answer(key_pressed=key_pressed,
                              response_order=key_order, # key_order = ["two_back_trial", "odd_number"]
                              stim_type=this_letter_slide.stim_type,
                              port=p_port,
                              win=win)

        if settings.save_results:

            # update "results" data-frame:
            results = update_results(sub_id=sub_id,
                                     results_df=results,
                                     key_pressed=key_pressed,
                                     total_trial=all_trials,
                                     trial=this_trial + 1,
                                     block=this_block + 1,
                                     stimulus=this_letter_slide.stim_file,
                                     stim_type=this_letter_slide.stim_type,
                                     stim_dur=this_letter_slide.slide_duration,
                                     stim_trigger=this_letter_slide.stim_trigger,
                                     result=result,
                                     rt=rt)

            results.to_csv(this_filename)  # Save results as .csv

        all_trials += 1

# -----------------------------------------------------------------------------------------------------------------

# 14 Display end text

# Send experiment end trigger:
print("END low task")

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