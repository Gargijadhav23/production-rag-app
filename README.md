# 🔍 NewsBot: AI News Research Tool

NewsBot is an AI-powered news research tool built with Google Gemini and LangChain. Users can input any news article URLs and ask natural language questions to get accurate, AI-generated answers.

## 🚀 Live Demo
[https://newsbot-gargi.streamlit.app](https://newsbot-gargi.streamlit.app)

## ✨ Features
- Input up to 3 news article URLs
- Automatically loads and processes article content
- Uses Google Gemini for AI-powered answers
- FAISS vector database for fast semantic search
- Clean, professional dark-themed UI built with Streamlit

## 🛠️ Tech Stack
- Python
- LangChain
- Google Gemini API
- FAISS Vector Database
- Streamlit

## ⚙️ Installation

1. Clone this repository:
```bash
git clone https://github.com/Gargijadhav23/production-rag-app.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your Google API key:
```bash
GOOGLE_API_KEY=your_api_key_here
```

4. Run the app:
```bash
streamlit run main.py
```

## 📁 Project Structure
- `main.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `.env` - API key configuration (not pushed to GitHub)

## 👩‍💻 Built By
Gargi Jadhav - [GitHub](https://github.com/Gargijadhav23)