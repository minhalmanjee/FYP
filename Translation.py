from ExtractWords import extractTechwords
from googletrans import Translator
from VoiceChange import audio_pitch
import speech_recognition as sr
from pydub import AudioSegment
import moviepy.editor as mp
from gtts import gTTS
import whisper
import os


# global text_to_translate

def translate_techwords_to_urdu(tech_words, dest='ur'):
    translator = Translator()
    translated_words = {}
    for word in tech_words:
        translated = translator.translate(word, dest=dest)
        translated_words[word] = translated.text
    print(translated_words)
    return translated_words
  
def translate_to_urdu(text, tech_words, dest='ur'):
    translator = Translator()
    translated_text = translator.translate(text, dest=dest).text

    for english_word, urdu_word in tech_words.items():
        translated_text = translated_text.replace(urdu_word, english_word)
    
    return translated_text

def audio_to_text(audio_file, whisper_model="base"):
  model = whisper.load_model('base.en')
  option = whisper.DecodingOptions(language='en', fp16=False)
  result = model.transcribe(audio_file)
  return result['text']

def speed_up_audio(input_file, output_file, speed_factor):
  audio = AudioSegment.from_file(input_file)
  sped_up_audio = audio.speedup(playback_speed=speed_factor)
  sped_up_audio.export(output_file)

def process_video(video_path, chunk_size=60):
    clip = mp.VideoFileClip(video_path)
    duration = clip.duration
    total_duration = 0

    for i in range(0, int(duration), chunk_size):
        start_time = i
        end_time = min(i + chunk_size, duration)
        sub_clip = clip.subclip(start_time, end_time)

        audio_path = f"./temp_{i}.wav"
        sub_clip.audio.write_audiofile(audio_path)
        
        global text_to_translate
        
        text = audio_to_text(audio_path)
        text_to_translate=text
        # print(text)
        tech_words = extractTechwords(text) 
        translated_techwords=translate_techwords_to_urdu(tech_words)
        translated_text = translate_to_urdu(text, translated_techwords)
        print("Translated Text:", translated_text)
        tts = gTTS(text=translated_text, lang='ur')
        translated_audio_path = f"./translated_audio_{i}.mp3"
        tts.save(translated_audio_path)
        
        final_audio_path = f"./final_audio_{i}.mp3"
        speed_up_audio(f"./translated_audio_{i}.mp3", f"./final_audio_{i}.mp3", 1.1)
        
        shifted_audio_path=audio_pitch(final_audio_path)
        translated_audio_clip = mp.AudioFileClip(shifted_audio_path)
        sub_clip = sub_clip.set_audio(translated_audio_clip)

        total_duration += chunk_size
        output_video_path = f".translated_video_{total_duration}.mp4"
        sub_clip.write_videofile(output_video_path, audio_codec='aac')

        os.remove(audio_path)
        os.remove(translated_audio_path)

        yield output_video_path
        #return output_video_path
      
# process_video(video_path='C:/Users/warda/OneDrive/Desktop/FYP_history/Code1000try/1.mp4')