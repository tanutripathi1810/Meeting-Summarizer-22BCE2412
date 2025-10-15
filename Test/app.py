import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config
from transcriber import AudioTranscriber
from summarizer import MeetingSummarizer
from storage import DataStorage

app = Flask(__name__)
CORS(app)

# Initialize configuration
Config.init_app()
app.config.from_object(Config)

# Initialize services
transcriber = AudioTranscriber()
summarizer = MeetingSummarizer()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('static', 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Meeting Summarizer API'
    })


@app.route('/api/process', methods=['POST'])
def process_audio():
    """
    Process audio file: transcribe and generate summary
    
    Expected: multipart/form-data with 'audio' file
    Returns: JSON with transcript and summary
    """
    # Validate request
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'error': f'Invalid file type. Allowed types: {", ".join(Config.ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        base_name = os.path.splitext(filename)[0]
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Step 1: Transcribe audio
        transcript = transcriber.transcribe(filepath)
        
        # Save transcript
        DataStorage.save_transcript(base_name, transcript)
        
        # Step 2: Generate summary
        summary_data = summarizer.generate_summary(transcript)
        
        # Save summary
        DataStorage.save_summary(base_name, summary_data)
        
        # Clean up uploaded file (optional)
        # os.remove(filepath)
        
        return jsonify({
            'success': True,
            'filename': base_name,
            'transcript': transcript,
            'summary': summary_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/transcripts/<filename>', methods=['GET'])
def get_transcript(filename):
    """Get a specific transcript"""
    transcript = DataStorage.load_transcript(filename)
    
    if transcript is None:
        return jsonify({'error': 'Transcript not found'}), 404
    
    return jsonify({
        'filename': filename,
        'transcript': transcript
    })


@app.route('/api/summaries/<filename>', methods=['GET'])
def get_summary(filename):
    """Get a specific summary"""
    summary = DataStorage.load_summary(filename)
    
    if summary is None:
        return jsonify({'error': 'Summary not found'}), 404
    
    return jsonify({
        'filename': filename,
        'summary': summary
    })


@app.route('/api/summaries', methods=['GET'])
def list_summaries():
    """List all available summaries"""
    summaries = DataStorage.list_summaries()
    
    # Get metadata for each summary
    summary_list = []
    for filename in summaries:
        metadata = DataStorage.get_summary_metadata(filename)
        summary_list.append({
            'filename': filename,
            'metadata': metadata
        })
    
    return jsonify({
        'summaries': summary_list
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large. Maximum size is 100MB'
    }), 413


if __name__ == '__main__':
    print("=" * 60)
    print("Meeting Summarizer")
    print("=" * 60)
    print(f"Transcription: OpenAI Whisper (~$0.006/minute)")
    print(f"Summarization: {Config.OPENAI_MODEL} (OpenAI)")
    print(f"Language: {Config.SPEECH_RECOGNITION_LANGUAGE}")
    print(f"Upload folder: {Config.UPLOAD_FOLDER}")
    print(f"Transcript folder: {Config.TRANSCRIPT_FOLDER}")
    print(f"Summary folder: {Config.SUMMARY_FOLDER}")
    print("=" * 60)
    print("\nStarting Meeting Summarizer API...")
    print("Note: Uses OpenAI API for both transcription and summarization\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

