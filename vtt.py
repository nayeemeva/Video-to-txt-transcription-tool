import os
from pydub import AudioSegment
from google.cloud import speech
import io
import ffmpeg

def extract_audio(video_path):
    """Extracts audio from video and saves it as a .wav file."""
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    ffmpeg.input(video_path).output(audio_path).run()
    return audio_path

def transcribe_audio(audio_path, language="bn-BD"):
    """Transcribes the audio file using Google Speech-to-Text API."""
    client = speech.SpeechClient()

    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language
    )

    response = client.recognize(config=config, audio=audio)

    # Collect transcription results
    transcript = "\n".join([result.alternatives[0].transcript for result in response.results])
    return transcript

def process_videos(video_paths):
    """Processes each video file and transcribes its audio."""
    transcripts = {}
    for video_path in video_paths:
        print(f"Processing {video_path}...")
        audio_path = extract_audio(video_path)
        transcript = transcribe_audio(audio_path)
        transcripts[video_path] = transcript
        os.remove(audio_path)  # Clean up audio file
    return transcripts

# Specify your list of video file paths here
video_paths = ["path/to/video1.mp4", "path/to/video2.mp4", ...]  # Add all video paths here

# Run transcription
transcripts = process_videos(video_paths)

# Save results to a text file
with open("transcripts.txt", "w", encoding="utf-8") as f:
    for video_path, transcript in transcripts.items():
        f.write(f"{video_path}:\n{transcript}\n\n")

print("Transcription complete! Check the 'transcripts.txt' file.")
