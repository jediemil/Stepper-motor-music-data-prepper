import mido

mid = mido.MidiFile('dreamsweet.midi', clip=True)
numSpeakers = 8

# tempo = us / beat

def noteToFreq(note):
    a = 440  # frequency of A (coomon value is 440Hz)
    return (a / 32) * (2 ** ((note - 9) / 12))

#mid.tracks.pop(8)
#mid.tracks.pop(9)

merged_midi = mido.MidiFile()
merged_midi.tracks = [mido.merge_tracks(mid.tracks)]
print(merged_midi)

noteTable = []
playedFreqs = {}  #

savedTime = 0

for i, message in enumerate(merged_midi.tracks[0]):

    if message.type == "note_on":
        freq = round(noteToFreq(message.note))
        speaker = 1

        # find speaker
        if playedFreqs.get(freq):
            speaker = playedFreqs[freq]
        else:
            if playedFreqs.__len__() < numSpeakers:
                # speaker = playedFreqs.__len__() # bad method!!!!!!
                # find empty slot
                for sp in range(1, numSpeakers + 1):  # Doesn't work when speaker start at 0, hence the 1-8 loop.
                    # print(sp)
                    if not sp in playedFreqs.values():
                        speaker = sp
                        break

            else:
                print("Too many notes at " + str(i))
                lowestTone = 10000000
                speaker = 1
                # Steal the speaker that plays the lowest note.
                for tone, sp in playedFreqs.items():
                    if tone < lowestTone:
                        lowestTone = tone
                        speaker = sp

        # figure out what frequency to write
        if message.velocity == 0:
            if playedFreqs.get(freq):
                playedFreqs.pop(freq)
                noteTable.append([speaker-1, 0, message.time])
        else:
            playedFreqs[freq] = speaker
            noteTable.append([speaker-1, freq, message.time])

    # if tempo message
    elif message.type == "set_tempo":
        noteTable.append([numSpeakers + 1, message.tempo, message.time])

    # time of other messages gets added
    else:
        if message.type == "end_of_track":
            for sp in range(0, numSpeakers):
                noteTable.append([sp, 0, 0])

            noteTable.append([0, 0, 0])
            break
        merged_midi.tracks[0][i + 1].time += message.time

print(noteTable)
noteTableStr = str(noteTable)
noteTableStr = noteTableStr.replace("[", "{")
noteTableStr = noteTableStr.replace("]", "}") + ";"
noteTableStr = "uint32_t musicTable[][3] = " + noteTableStr + "\nint musicLen = " + str(noteTable.__len__() - 2) + ";"

print(noteTableStr)
