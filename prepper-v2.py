import os
from os import listdir

from simple_term_menu import TerminalMenu
import mido
from midi_instruments import instruments, percussion

mid = mido.MidiFile('songs/Wii_Sports_Theme.mid', clip=True)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def find_last_program_change(track):
    program = mido.Message('program_change')
    for message in track:
        if message.type == 'program_change':
            program = message

    return program


# Choose input file
midi_files = [file for file in os.listdir("songs") if file.endswith(".midi") or file.endswith(".mid")]

# Show Tracks
tracks = []
pre_select = []
for i, track in enumerate(mid.tracks):
    program = find_last_program_change(track)
    if program.channel == 9:
        tracks.append(f"{i}: {percussion[program.program]} TRUMMOR")  # Take values from other list (https://en.wikipedia.org/wiki/General_MIDI)
        pre_select.append(i)
    else:
        tracks.append(f"{i}: {instruments[program.program][1]}")

clear_console()
terminal_menu = TerminalMenu(tracks, title="Välj spår att ta bort", multi_select=True, preselected_entries=pre_select)
menu_entry_indexes = terminal_menu.show()
print(menu_entry_indexes)

print(mid.tracks)

for index in reversed(menu_entry_indexes):
    mid.tracks.pop(index)

# Run midi conversion
