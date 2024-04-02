# Display instructions a
from psychopy import gui, visual, core, event
import settings

screen_width = settings.screen_width
screen_height = settings.screen_height
disp_size_pix = (screen_width, screen_height)
# -----------------------------------------------------------------------------------------------------------------
# Function to show instruction text images
def show_instructions(img_list, win):

    my_mouse = event.Mouse(win=win)
    my_mouse.setVisible(False)

    # Display one after the other the images in input list

    # Create blank image stimulus:
    this_instruction = visual.ImageStim(win, size=disp_size_pix)
    # this_instruction = visual.TextStim(win, size=settings.disp_size_pix) # text=self.stim_file,

    # Loop through instruction files and display them:
    for i in range(len(img_list)):
        this_instruction.image = img_list[i]

        # Draw image:
        this_instruction.setAutoDraw(True)
        win.flip()
        # Wait until 'space' key is pressed:
        event.waitKeys(keyList=['space'])

        # If key is pressed, stop drawing current instruction and move to next one:
        this_instruction.setAutoDraw(False)
        win.flip()
