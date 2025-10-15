import os
import json
from datetime import datetime
from config import Config


class DataStorage:
    """Handles storage and retrieval of transcripts and summaries"""
    
    @staticmethod
    def save_transcript(filename, transcript):
        """
        Save transcript to file
        
        Args:
            filename (str): Base filename (without extension)
            transcript (str): Transcript text
            
        Returns:
            str: Path to saved transcript file
        """
        filepath = os.path.join(Config.TRANSCRIPT_FOLDER, f"{filename}.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(transcript)
        return filepath
    
    @staticmethod
    def save_summary(filename, summary_data):
        """
        Save summary data to JSON file
        
        Args:
            filename (str): Base filename (without extension)
            summary_data (dict): Summary data dictionary
            
        Returns:
            str: Path to saved summary file
        """
        filepath = os.path.join(Config.SUMMARY_FOLDER, f"{filename}.json")
        
        # Add metadata
        summary_data['metadata'] = {
            'generated_at': datetime.now().isoformat(),
            'filename': filename
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        return filepath
    
    @staticmethod
    def load_transcript(filename):
        """
        Load transcript from file
        
        Args:
            filename (str): Base filename (without extension)
            
        Returns:
            str: Transcript text or None if not found
        """
        filepath = os.path.join(Config.TRANSCRIPT_FOLDER, f"{filename}.txt")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    @staticmethod
    def load_summary(filename):
        """
        Load summary data from file
        
        Args:
            filename (str): Base filename (without extension)
            
        Returns:
            dict: Summary data or None if not found
        """
        filepath = os.path.join(Config.SUMMARY_FOLDER, f"{filename}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    @staticmethod
    def list_summaries():
        """
        List all available summaries
        
        Returns:
            list: List of summary filenames (without extensions)
        """
        if not os.path.exists(Config.SUMMARY_FOLDER):
            return []
        
        files = os.listdir(Config.SUMMARY_FOLDER)
        return [f.replace('.json', '') for f in files if f.endswith('.json')]
    
    @staticmethod
    def get_summary_metadata(filename):
        """
        Get metadata for a summary
        
        Args:
            filename (str): Base filename (without extension)
            
        Returns:
            dict: Metadata or None if not found
        """
        summary = DataStorage.load_summary(filename)
        if summary:
            return summary.get('metadata', {})
        return None

