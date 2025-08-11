## How to Run This Streamlit Project

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set environment variables
Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_API_KEY=""
YOU_TUBE_LINKS_TO_PULL=""
```

> ⚠️ Replace `your_openai_api_key` with your actual key. Keep this file **out** of version control (add `.env` to `.gitignore`).

### Step 3: Run the Streamlit app
```bash
streamlit run main.py
```

This will start a local web server and give you a URL like:
```
Local URL: http://localhost:8501
```
Open that URL in your browser to access the app.
