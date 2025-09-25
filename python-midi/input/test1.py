def generate_midi(filename):
    import mido
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    for note in [60, 62, 64, 65, 67, 69, 71, 72]:
        track.append(mido.Message('note_on', note=note, velocity=64, time=480))
        track.append(mido.Message('note_off', note=note, velocity=64, time=480))

    mid.save(filename)
