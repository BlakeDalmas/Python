import arcade
import tempvars
import os

# Some random global variables
money = 250
population = 10
max_population = 10
level_text = arcade.create_text("0", [50, 64, 200], 24)
player = None
skills_opened = False

stats_kills = 0
stats_money = 0
stats_waves = 0
stats_player_dmg = 0
stats_total_dmg = 0

up_keys = []
down_keys = []
left_keys = []
right_keys = []
slash_keys = []
spell_keys = []

# Goes through the config.txt and figures out the correct key binds
file = open("config.txt")
lines = []
for item in file:
    lines.append(item)

keys = [up_keys, down_keys, left_keys, right_keys, slash_keys, spell_keys]
start = 0
for k in range(6):
    txt = lines[k]

    selected_keys = keys[k]
    start = 0
    for v in range(len(txt)):
        if txt[v] == ".":
            selected_keys.append(txt[start:v])
            start = v + 1


library_key = ["LAlt", "RAlt", "UP", "LEFT", "RIGHT", "DOWN", "CTRL", "LSHIFT", "RSHIFT", "CAPS", "TAB"]
library_number = ["65513", "65514", "65362", "65361", "65363", "65364", "65508", "65505", "65505", "65509", "65289"]

# Sounds
"""
Storing each sound is a separate variable would get really messy if there's too many sounds in the game.
Doing arcade.play_sound(arcade.load_sound) could be laggy and it seems unnecessary to load the sound every time.
Instead, I decided to create a custom function called emit_sound() that solves both of these problems. (It's still more
laggy than storing it in a variable and playing it, however it's faster than loading it and playing it at the
same time.) Having a variable for every sound would be really cluttered and annoying to manage.
"""

# Takes the names of all the sounds in the sound directory and puts them in a sorted list.
sound_list = os.listdir("sounds")
sound_list.sort()

# Takes the names of the sounds in the sound list and creates a new list of the actual sounds.
sound_data_list = []
for sound in sound_list:
    sound_data_list.append(arcade.load_sound(str("sounds/" + sound)))

"""
Store the last sound played in a "memory" variable, if the sound being played is the same as the variable then 
play the sound in the variable. This makes it more efficient to play the same sound over and over again. If it isn't the
same then search through the sound list using a binary search to find the sound that associates with the name in the
parameter. I could have avoided the searching process by having the parameter be the index of the sound in the sound
list. However, it would get really confusing seeing stuff like this everywhere: emit_sound(6). 
By using a name instead it's much easier to tell what is going on. 
"""
def emit_sound(filename):
    if filename != tempvars.memory_name:
        lower = 0
        upper = len(sound_list) - 1
        found = False
        middle = 0

        while lower <= upper and not found:
            middle = (lower + upper) // 2
            if sound_list[middle] < filename:
                lower = middle + 1
            elif sound_list[middle] > filename:
                upper = middle - 1
            else:
                found = True

        if found:
            temp_sound = sound_data_list[middle]
            arcade.play_sound(temp_sound)
            tempvars.memory_name = filename
            tempvars.memory_sound = temp_sound
        else:
            print("Error! Sound " + str(filename) + " doesn't exist!")
    else:
        arcade.play_sound(tempvars.memory_sound)
