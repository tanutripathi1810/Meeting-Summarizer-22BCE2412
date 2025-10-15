# 📝 Meeting Summarizer

An AI-powered meeting summarization web app that transcribes audio recordings and generates concise summaries using OpenAI Whisper and GPT-based summarization.
Built with Flask (backend) and an optional frontend (HTML/JS) interface.

# 🚀 Features

- 🎙️ Audio Upload & Transcription — Upload meeting audio files for automatic transcription

- 🧠 AI Summarization — Generate concise meeting summaries using OpenAI models

- 💾 Storage System — Save and retrieve transcripts & summaries

- 🌐 REST API — Easily integrate with frontend or third-party tools

- 🛡️ CORS Enabled — Seamless frontend-backend integration

# ⚙️ Configurable 
Manage API keys, folders, and limits in config.py

# 🧩 Tech Stack
- Component	Technology
- Backend	Flask (Python)
- AI Models	OpenAI Whisper + GPT
- Frontend	HTML / JS (served from static/)
- Storage	Local file storage via DataStorage
- Environment	Python 3.10+, virtualenv

# 📁 Project Structure
```Meeting-Summarizer/
│
├── app.py                 # Main Flask application
├── config.py              # Configuration and constants
├── transcriber.py         # Handles audio-to-text transcription
├── summarizer.py          # Generates meeting summaries
├── storage.py             # Manages local transcript and summary storage
├── static/
│   └── index.html         # Frontend UI (optional)
└── README.md              # Project documentation
```

# ⚙️ Installation & Setup
- 1️⃣ Clone the repository
```git clone https://github.com/tanutripathi1810/Meeting-Summarizer-22BCE2412.git
cd Meeting-Summarizer-22BCE2412
```
- 2️⃣ Create a virtual environment
```
python -m venv venv
source venv/Scripts/activate    # On Windows
```
# or
```
source venv/bin/activate        # On Mac/Linux
```
- 3️⃣ Install dependencies
```
pip install -r requirements.txt
```
- 4️⃣ Add your OpenAI API key
Create a .env file or update config.py:

```
OPENAI_API_KEY=your_openai_api_key
```
5️⃣ Run the app
```
python app.py
```

- Access it at → http://localhost:5000

# 📡 API Endpoints
Method	Endpoint	Description
- GET	/api/health	Check API health
- POST	/api/process	Upload an audio file and get transcript + summary
- GET	/api/transcripts/<filename>	Get a transcript by filename
- GET	/api/summaries/<filename>	Get a summary by filename
- GET	/api/summaries	List all available summaries
# 🧾 Example cURL Request
```
curl -X POST http://localhost:5000/api/process \
  -F "audio=@meeting.mp3"

```
Response:
```
{
  "success": true,
  "filename": "meeting",
  "transcript": "Full meeting transcription text...",
  "summary": "Concise AI-generated summary..."
}
```

# ⚠️ Notes

- Allowed file types: .mp3, .wav, .m4a, .flac, etc. (configured in config.py)

- Max upload size: 100MB

- Uses OpenAI Whisper for transcription (~$0.006/min)

- Summarization model configurable via Config.OPENAI_MODEL

# 🧑‍💻 Developer Info

- Author: Tanu Tripathi
- Project: Meeting Summarizer (22BCE2412)
- Framework: Flask + OpenAI API
- GitHub: tanutripathi1810
