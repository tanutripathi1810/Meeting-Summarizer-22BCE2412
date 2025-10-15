import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')  # Cost-effective model
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    TRANSCRIPT_FOLDER = 'transcripts'
    SUMMARY_FOLDER = 'summaries'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'mp4', 'webm'}
    
    # Whisper Configuration
    SPEECH_RECOGNITION_LANGUAGE = os.getenv('SPEECH_RECOGNITION_LANGUAGE', 'en')  # Language code for Whisper
    
    # Audio processing
    AUDIO_CHUNK_LENGTH_MS = 60000  # Process audio in 60-second chunks
    
    @staticmethod
    def init_app():
        """Initialize application directories"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.TRANSCRIPT_FOLDER, exist_ok=True)
        os.makedirs(Config.SUMMARY_FOLDER, exist_ok=True)

