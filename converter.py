import mido

NUM_SPEAKERS = 8

class Speaker:
    def __init__(self, speaker_id):
        self.speaker_id = speaker_id
        self.freq = 0
        self.playing = False


class ToneElement:
    def __init__(self, speaker_id, freq, time_until_next):
        self.speaker_id = speaker_id
        self.freq = freq
        self.time_until_next = time_until_next


class Player:
    def __init__(self, num_speakers):
        self.num_speakers = num_speakers
        self.speakers = [Speaker(i) for i in range(num_speakers)]

    def assign_freq_to_speaker(self, freq):
        if self.__is_available_speaker():
            pass


    def __is_available_speaker(self):
        for speaker in self.speakers:
            if not speaker.playing:
                return True

        return False


def note_to_freq(note):
    a = 440
    return (a / 32) * (2 ** ((note - 9) / 12))


def convert_midi(mid):
    merged_midi = mido.MidiFile()
    merged_midi.tracks = [mido.merge_tracks(mid.tracks)]

    note_sequence = []