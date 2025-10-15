import os
from openai import OpenAI
from config import Config


class AudioTranscriber:
    """Handles audio transcription using OpenAI Whisper API"""
    
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            print("⚠ Warning: OPENAI_API_KEY not set in environment")
            print("  Add your API key to .env file")
        else:
            print("✓ OpenAI API key configured")
        
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.language = Config.SPEECH_RECOGNITION_LANGUAGE
        print(f"✓ OpenAI Whisper initialized (Language: {self.language})")
    
    def transcribe(self, audio_file_path):
        """
        Transcribe audio file to text using OpenAI Whisper API
        
        Args:
            audio_file_path (str): Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        try:
            print("Transcribing audio with Whisper...")
            
            # Check file size (Whisper has 25MB limit)
            file_size = os.path.getsize(audio_file_path)
            if file_size > 25 * 1024 * 1024:
                raise Exception("Audio file too large. Whisper API has 25MB limit.")
            
            # Transcribe with Whisper
            with open(audio_file_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=self.language.split('-')[0] if self.language else None,  # Convert en-US to en
                    response_format="text"
                )
            
            if not transcript or transcript.strip() == "":
                raise Exception("Could not transcribe audio. Audio may be silent or corrupted.")
            
            print("✓ Transcription completed successfully")
            return transcript
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    

