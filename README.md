# Nữ Giới Chung AI Demo

This Flask app uses Google Gemini AI to generate responses emulating the literary style of early 20th-century Vietnamese female writers from *Nữ Giới Chung* newspaper.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/nu-gioi-chung-demo.git
cd nu-gioi-chung-demo
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory and add the following:

```env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
```

### 5. Run the app

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

