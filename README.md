# Sentiment Analysis Mini Project

Simple NLP mini project using **TextBlob** with:
- Script mode (demo + interactive input)
- FastAPI service (`/predict`, `/predict/batch`)
- Basic input validation
- Built-in demo evaluation

## Project Structure

- `sentiment_mini_project.py` - core logic and CLI usage
- `api.py` - FastAPI app
- `requirements.txt` - Python dependencies
- `.gitignore` - standard Python ignores

## 1) Setup

```bash
python -m venv .venv
```

Activate virtual environment:

- Windows PowerShell:
```bash
.venv\Scripts\Activate.ps1
```

- Windows CMD:
```bash
.venv\Scripts\activate.bat
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 2) Run as Script

### Demo mode (12 predefined sentences + report)
```bash
python sentiment_mini_project.py
```

### One custom sentence
```bash
python sentiment_mini_project.py --text "I love this app"
```

### Interactive input mode
```bash
python sentiment_mini_project.py --interactive
```

### Interactive mode with analysis of 2 user inputs
```bash
python sentiment_mini_project.py --interactive --analyze
```

## 3) Run as API

Start server:

```bash
uvicorn api:app --reload
```

Open docs:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Example API calls

Health:

```bash
curl http://127.0.0.1:8000/health
```

Single prediction:

```bash
curl -X POST "http://127.0.0.1:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"The service was amazing\"}"
```

Batch prediction:

```bash
curl -X POST "http://127.0.0.1:8000/predict/batch" ^
  -H "Content-Type: application/json" ^
  -d "{\"texts\":[\"I love it\",\"This is bad\",\"The meeting is at 10 AM\"]}"
```

## 4) Input Validation Included

- Empty text -> rejected
- Non-string input -> rejected
- Empty batch list -> rejected

