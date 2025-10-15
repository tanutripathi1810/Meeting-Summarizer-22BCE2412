# Meeting Summarizer

An AI-powered meeting summarizer that transcribes audio files and generates professional, action-oriented summaries with key decisions and action items.

**Powered by OpenAI:**
- ✨ Whisper API for high-accuracy transcription (80-95%)
- 🧠 GPT-4o-mini for intelligent summarization
- 💰 Cost-effective: ~$0.05 for 5-min meeting, ~$0.41 for 1-hour meeting

---

## 🚀 Quick Start

### 1. Get OpenAI API Key (2 minutes)

Visit: https://platform.openai.com/api-keys
- Sign up or log in
- Click "Create new secret key"
- Copy the key (starts with `sk-`)

### 2. Run Setup Script (1 minute)

```bash
./setup.sh
```

This automatically:
- Creates a virtual environment
- Installs all dependencies
- Creates necessary folders
- Sets up `.env` configuration file

### 3. Add Your API Key

Edit the `.env` file:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-4o-mini
SPEECH_RECOGNITION_LANGUAGE=en
```

Replace `sk-your-actual-key-here` with your real API key!

### 4. Start the Application

```bash
./run.sh
```

Then open your browser to: **http://localhost:5000**

That's it! 🎉

---

## Features

### 🎙️ Audio Transcription
- **High Accuracy**: OpenAI Whisper API (80-95% accuracy)
- **Multiple Formats**: MP3, WAV, M4A, OGG, MP4, WEBM
- **50+ Languages**: Supports English, Spanish, French, German, Chinese, Japanese, and more
- **Handles Complexity**: Works with noisy audio, music, and singing

### 📝 Smart Summarization
Professional Gemini-style meeting notes with:
- **Summary**: Comprehensive paragraph capturing the entire meeting
- **Details**: Multiple titled sections with speaker attribution and timestamps
- **Suggested Next Steps**: Clear action items with assignments and deadlines

### 🎨 Web Interface
- Modern, user-friendly UI
- Drag-and-drop file upload
- Real-time progress feedback
- Beautiful formatted results display

### 💾 Data Persistence
- Saves transcripts and summaries as JSON files
- Easy retrieval through REST API
- Local storage (your data stays on your machine)

### 🔌 RESTful API
Clean API endpoints for integration:
- `POST /api/process` - Upload and process audio
- `GET /api/transcripts/<filename>` - Retrieve transcript
- `GET /api/summaries/<filename>` - Retrieve summary
- `GET /api/summaries` - List all summaries

---

## Summary Format

The application generates professional meeting notes in a structured format:

### Example Output

**Summary**

Aayush presented enhancements to MongoDB, focusing on improved observability and rate limiting to address incidents like the April 26, 2025 outage. Aayush implemented granular Prometheus metrics, a custom usage analysis pipeline for extended data retention, an enhanced query profiler, and user-based rate limiting with an access gate and cost enforcers. The discussion centered on making MongoDB more transparent, predictable, and resilient.

**Details**

**MongoDB Enhancements Overview**
Aayush presented their work on enhancing MongoDB observability and implementing rate limiting, aiming to make MongoDB more transparent, predictable, and resilient. The motivation for this project stemmed from incidents like the April 26, 2025 outage of the dev app, which was caused by high CPU and network spikes due to a notification service with 45,000 unread notifications. They highlighted that such incidents have become more common (00:00:00).

**Challenges and Solutions**
Aayush explained that MongoDB, despite being heavily used, is difficult to debug and easy to overuse, with a lack of observability leading to delayed incident detection. To address this, they implemented granular Prometheus metrics and service collection at operation levels, allowing for plotting of latency, error rates, and throughput. They also developed a custom usage analysis pipeline that supports analysis for longer durations than MongoDB Atlas's 7-day limit (00:06:11).

**Suggested next steps**
- Test the rate limiting system in staging environment - Assigned to: Engineering team - Due: Next week
- Review the new Prometheus metrics dashboard - Assigned to: DevOps team - Due: Not specified
- Schedule follow-up meeting to discuss implementation - Assigned to: Aayush - Due: Within two weeks

---

## Technology Stack

- **Backend**: Flask (Python 3.8+)
- **Transcription**: OpenAI Whisper API
- **Summarization**: OpenAI GPT-4o-mini
- **Frontend**: HTML/CSS/JavaScript (Vanilla)
- **Storage**: File-based JSON storage

**Dependencies** (only 5 packages!):
```
flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
werkzeug==3.0.1
openai==1.12.0
```

---

## Project Structure

```
meeting-summarizer/
├── app.py              # Flask server + REST API
├── config.py           # Configuration settings
├── transcriber.py      # OpenAI Whisper integration
├── summarizer.py       # OpenAI GPT integration
├── storage.py          # Data persistence (JSON)
├── static/
│   └── index.html      # Web interface
├── setup.sh            # Automated setup script
├── run.sh              # Application launcher
├── requirements.txt    # Python dependencies
├── .env               # API keys (create this)
├── .gitignore         # Git exclusions
└── uploads/           # Uploaded audio files (runtime)
    transcripts/       # Generated transcriptions (runtime)
    summaries/         # Generated summaries (runtime)
```

---

## How It Works

1. **Upload Audio**: User uploads meeting audio through web interface or API
2. **Transcribe**: OpenAI Whisper API converts audio → text
   - Supports all audio formats
   - Handles speech, music, accents, noisy audio
   - Maximum file size: 25MB
3. **Summarize**: OpenAI GPT analyzes transcript → structured summary
   - Generates professional meeting notes
   - Extracts key discussion points
   - Identifies action items with assignments
4. **Save & Display**: Results saved locally and displayed to user

---

## API Documentation

### Process Audio
```bash
curl -X POST -F "audio=@meeting.mp3" http://localhost:5000/api/process
```

**Response:**
```json
{
  "success": true,
  "filename": "meeting",
  "transcript": "Full transcript text...",
  "summary": {
    "summary": "Comprehensive paragraph...",
    "details": "Detailed sections...",
    "next_steps": ["Action 1", "Action 2"],
    "full_summary": "Complete formatted summary..."
  }
}
```

### Get Transcript
```bash
curl http://localhost:5000/api/transcripts/meeting
```

### Get Summary
```bash
curl http://localhost:5000/api/summaries/meeting
```

### List All Summaries
```bash
curl http://localhost:5000/api/summaries
```

---

## Configuration

### Language Settings

Edit `.env` file:
```bash
SPEECH_RECOGNITION_LANGUAGE=en  # Use 2-letter codes
```

Supported languages:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `zh` - Chinese
- `ja` - Japanese
- And 50+ more!

### Model Selection

```bash
OPENAI_MODEL=gpt-4o-mini  # Cost-effective (recommended)
# OPENAI_MODEL=gpt-4o     # More powerful, higher cost
```

### Other Settings

In `config.py`:
- `MAX_CONTENT_LENGTH` - Max upload size (default: 100MB)
- `ALLOWED_EXTENSIONS` - Audio formats (mp3, wav, m4a, ogg, mp4, webm)

---

## Cost & Pricing

### Per Meeting

| Duration | Transcription | Summary | Total |
|----------|---------------|---------|-------|
| 5 minutes | $0.03 | $0.02 | **$0.05** |
| 15 minutes | $0.09 | $0.02 | **$0.11** |
| 30 minutes | $0.18 | $0.03 | **$0.21** |
| 1 hour | $0.36 | $0.05 | **$0.41** |

### Monthly Estimate

**50 meetings/month (30 min avg): ~$10.50**

**Compare to alternatives:**
- Otter.ai Pro: $20/month
- Rev.ai: ~$15/hour
- Assembly.ai: ~$25/hour

**OpenAI is the most cost-effective!** 💰

---

## Performance & Requirements

### Speed
- **Transcription**: Real-time to 2x faster (Whisper API)
- **Summarization**: 3-10 seconds (GPT-4o-mini)
- **Total**: ~1-3 minutes for typical 30-minute meeting

### Hardware
- **Minimum**: 2GB RAM + internet connection
- **No GPU needed**
- **No local models to download**
- **Works on any machine!**

### File Limits
- Maximum upload size: 100MB (configurable)
- Whisper API limit: 25MB per file
- For larger files: Compress audio or split into segments

---

## Troubleshooting

### "OpenAI API key not found"
**Solution:**
- Create `.env` file in project root
- Add: `OPENAI_API_KEY=sk-your-key-here`
- Get key from: https://platform.openai.com/api-keys
- Restart the server

### "Port 5000 already in use" (macOS)
**Solution:**
- Disable AirPlay Receiver:
  - System Settings → General → AirDrop & Handoff
  - Turn off "AirPlay Receiver"

### "Module not found" errors
**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "File too large" / "Audio file too large"
**Solution:**
- Whisper has 25MB limit per file
- Compress audio: `ffmpeg -i input.mp3 -b:a 64k output.mp3`
- Or split into smaller segments

### "Transcription failed"
**Solutions:**
- Check internet connection
- Verify OpenAI API key is valid
- Check API key has credits/billing enabled
- Ensure audio file is not corrupted

---

## Security & Privacy

- **File uploads**: Type and size validated
- **Data transmission**: Sent to OpenAI API (encrypted in transit via HTTPS)
- **OpenAI policy**: Not used for training (as per API terms)
- **Local storage**: All results saved on your machine
- **API key**: Store securely in `.env` (never commit to git)
- **CORS**: Enabled for development (disable for production)

---

## Limitations

- Requires internet connection for API calls
- OpenAI API costs apply (see pricing above)
- 25MB file size limit (Whisper API constraint)
- No authentication (add if needed for production)
- Synchronous processing (async can be added for very long files)

---

## Development

### Manual Setup (without script)

```bash
# Clone/download repository
cd meeting-summarizer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
SPEECH_RECOGNITION_LANGUAGE=en
EOF

# Start application
python app.py
```

### Project Files

**Core Application:**
- `app.py` (172 lines) - Flask server and API routes
- `transcriber.py` (58 lines) - Whisper API integration
- `summarizer.py` (145 lines) - GPT API integration with prompt engineering
- `config.py` (34 lines) - Configuration management
- `storage.py` - JSON data persistence

**Frontend:**
- `static/index.html` (429 lines) - Web interface with drag-and-drop

**Automation:**
- `setup.sh` - Automated environment setup
- `run.sh` - Application launcher with validation

---

## Production Deployment

### Considerations for Production

If deploying to production, consider adding:

1. **Authentication**: User login and API key management
2. **Rate Limiting**: Prevent abuse
3. **Database**: PostgreSQL/MySQL instead of file-based storage
4. **Async Processing**: Celery/Redis for long audio files
5. **Error Monitoring**: Sentry or similar
6. **HTTPS/SSL**: Secure connections
7. **Environment Configs**: Separate dev/staging/prod settings
8. **Logging**: Comprehensive application logging
9. **Backup**: Regular data backups

### Environment Variables for Production

```bash
OPENAI_API_KEY=sk-production-key
OPENAI_MODEL=gpt-4o-mini
SPEECH_RECOGNITION_LANGUAGE=en
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=104857600
```

---

## Contributing

This project is designed to be simple and educational. Feel free to:
- Fork and modify for your needs
- Add features (speaker diarization, real-time transcription, etc.)
- Improve the UI/UX
- Add authentication and user management
- Implement async processing

---

## License

This project is provided as-is for educational and evaluation purposes.

---

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the configuration in `.env` and `config.py`
3. Check OpenAI API status: https://status.openai.com
4. Verify your API key has credits and billing enabled

---

## What Makes This Special

✅ **Simple Setup**: 3 steps to get started  
✅ **Professional Output**: Gemini-style meeting notes  
✅ **Cost-Effective**: ~$0.20-0.50 per meeting hour  
✅ **No Heavy Dependencies**: Just 5 Python packages  
✅ **High Accuracy**: 80-95% transcription accuracy  
✅ **Modern Stack**: Latest OpenAI APIs  
✅ **Clean Code**: Well-organized and documented  
✅ **Production-Ready**: Can be deployed with minimal changes  

---

**Ready to transcribe your meetings? Run `./setup.sh` and get started!** 🚀
