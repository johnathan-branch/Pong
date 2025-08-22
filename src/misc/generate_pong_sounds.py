from pydub.generators import Sine
from misc.get_parent_dir import ROOT_DIR

SOUND_EFFECTS_FOLDER = str(ROOT_DIR) + "\\resources\\sounds\\"

def pitch_sweep(start_freq, end_freq, duration_ms):
    """Generate a pitch sweep (linear interpolation between two freqs)."""
    steps = 30
    step_dur = duration_ms // steps
    freqs = [start_freq + (end_freq - start_freq) * i / steps for i in range(steps)]
    segments = [Sine(f).to_audio_segment(duration=step_dur) for f in freqs]
    return sum(segments)

def save_sound(sound, filename):
    sound.export(filename, format="wav")
    #print(f"Saved {filename}")

def generate_wav_files():
    """Generates .wav files for game sound-effects and saves them to the /resources/sounds folder."""
    # Paddle hit: descending blip (laser feel)
    paddle = pitch_sweep(900, 500, 120).fade_out(50)
    save_sound(paddle, SOUND_EFFECTS_FOLDER + "paddle_hit.wav")

    # Wall bounce: ascending ping (spacy sparkle)
    wall = pitch_sweep(500, 1000, 100).fade_out(50)
    save_sound(wall, SOUND_EFFECTS_FOLDER + "wall_bounce.wav")

    # Score point: funky double chime (two quick tones layered)
    chime1 = Sine(600).to_audio_segment(duration=120)
    chime2 = Sine(900).to_audio_segment(duration=120).apply_gain(-3)  # softer overlay
    score = chime1.overlay(chime2).fade_out(80)
    save_sound(score, SOUND_EFFECTS_FOLDER + "score_point.wav")