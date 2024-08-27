import os

from simple_term_menu import TerminalMenu
import mido
from midi_instruments import instruments, percussion


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def find_last_program_change(midi_track):
    midi_program = mido.Message('program_change')
    for message in midi_track:
        if message.type == 'program_change':
            midi_program = message

    return midi_program


# Choose input file
midi_files = [file for file in os.listdir("songs") if file.endswith(".midi") or file.endswith(".mid")]
file_menu = TerminalMenu(midi_files, title="Välj fil att konvertera")
chosen_file_index = file_menu.show()

# Show Tracks
mid = mido.MidiFile('songs/' + midi_files[chosen_file_index], clip=True)
tracks = []
pre_select = []

for i, track in enumerate(mid.tracks):
    program = find_last_program_change(track)
    if program.channel == 9:
        tracks.append(
            f"{i}: {percussion[program.program]} TRUMMOR")  # Take values from other list (https://en.wikipedia.org/wiki/General_MIDI)
        pre_select.append(i)
    else:
        tracks.append(f"{i}: {instruments[program.program][1]}")

clear_console()
track_menu = TerminalMenu(tracks, title="Välj spår att ta bort", multi_select=True, preselected_entries=pre_select)
track_remove_indexes = track_menu.show()
print(track_remove_indexes)

print(mid.tracks)

for index in reversed(track_remove_indexes):
    mid.tracks.pop(index)

# Run midi conversion
