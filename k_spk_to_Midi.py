from mido import Message, MidiFile, MidiTrack, bpm2tempo

# === Symbol → MIDI note mapping from K_Spk Rosetta ===
symbol_map = {
    '◯': 60,   # Offer / Spirit
    '↬': 62,   # Transmit / Pass
    '◇': 64,   # Concept Seed / Insight
    '▭': 65,   # Structure / Frame
    '~': 67,   # Flow / Drift
    '△': 69,   # Elevate / Propose
    '✦': 71,   # Highlight / Signal
    '∞': 72,   # Loop / Continuation
    '⧉': 74,   # Connect / Reference
    '◐': 76,   # In Process / Becoming
    '▽': 77,   # Receive / Absorb
    '●': 48    # Anchor / Ground
}

# Each stanza: (symbol lines, tempo BPM)
stanzas = [
    ([
        ['◯','↬','◇','~','▭'],
        ['△','✦','∞','⧉','◐'],
        ['▽','●','~','◯','↬']
     ], 60),
    ([
        ['✦','▭','◇','⧉','∞'],
        ['◐','↬','◯','~','▽'],
        ['●','△','✦','∞','▭']
     ], 90),
    ([
        ['◇','▭','~','◐','↬'],
        ['◯','⧉','∞','▽','✦'],
        ['△','●','~','◐','◯']
     ], 75),
    ([
        ['∞','↬','▭','✦','◇'],
        ['▽','~','◯','◐','⧉'],
        ['●','●','●','●','●']
     ], 80)
]

# Create MIDI file
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Instrument: 0 = Acoustic Grand Piano, change if you want
track.append(Message('program_change', program=0, time=0))

# Helper to add a note
def add_note(note, velocity=80, duration=480):
    track.append(Message('note_on', note=note, velocity=velocity, time=0))
    track.append(Message('note_off', note=note, velocity=64, time=duration))

# Build the track
for stanza_idx, (lines, bpm) in enumerate(stanzas, start=1):
    # Tempo
    track.append(mido.MetaMessage('set_tempo', tempo=bpm2tempo(bpm)))
    for line in lines:
        for sym in line:
            note = symbol_map[sym]
            vel = 95 if sym in ['✦'] else (100 if sym == '●' else 80)
            dur = 720 if sym in ['∞'] else 480
            add_note(note, velocity=vel, duration=dur)
        # small pause between lines
        track.append(Message('note_off', note=0, velocity=0, time=240))
    # Extra pause between stanzas
    track.append(Message('note_off', note=0, velocity=0, time=480))

# Save MIDI file
mid.save('echoes_between_light_and_ground.mid')

print("MIDI file 'echoes_between_light_and_ground.mid' created successfully!")
