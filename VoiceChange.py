from pydub import AudioSegment
import soundfile as sf
import librosa
import io

def audio_pitch(file_path):
    audio_mp3 = AudioSegment.from_file(file_path, format='mp3')
    audio_wav = io.BytesIO()
    audio_mp3.export(audio_wav, format="wav")
    audio_wav.seek(0)

    audio, sr = sf.read(audio_wav)
    pitch_shift_factor = 0
    pitch_shifted_audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=pitch_shift_factor)

    new_audio='altered_audio.wav'
    sf.write(new_audio, pitch_shifted_audio, sr)
    return new_audio
