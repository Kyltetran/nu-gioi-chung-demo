import os
import csv
import google.generativeai as genai
from flask import Flask, jsonify, request, render_template, session

app = Flask(__name__)
app.secret_key = 'NhuquynhNhuquynh'  # You need this for session management

# Configure the API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Load CSV data
def load_csv(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            next(csvreader)  # Skip header if it exists
            for row in csvreader:
                data.append({'subject': row[0], 'content': row[1]})
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return data

# Load the CSV data
csv_data = load_csv('data.csv')

# Route for index page
@app.route('/')
def index():
    session.clear()  # Clear the session when starting a new conversation
    return render_template('index.html')

# Function to generate content using the Gemini API
def generate_content(prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-002")
    
    # Generate the content
    response = model.generate_content(prompt)

    # Extract the text from the response
    generated_text = response.candidates[0].content.parts[0].text  # Adjust this based on your actual response structure
    return generated_text

# Route to handle user input and generate content with memory
@app.route('/generate_content', methods=['POST'])
def handle_generate_content():
    user_input = request.json.get('question')

    # Retrieve previous conversation history from session
    conversation_history = session.get('conversation_history', '')

    # Build the prompt using the previous conversation and CSV content
    if not conversation_history:  # First interaction
        prompt = f"""
        Bạn là một cây viết nữ của báo Nữ giới chung. Hãy viết những bài bày tỏ quan điểm (dưới 150 từ), sử dụng ngôn ngữ thời ngày xưa, thể hiện quan điểm của thời đó về các vấn đề nữ quyền, vệ sinh, giáo dục, đối nhân xử thế. Giả sử đây là năm 1918.
        
        Dưới đây là một bài viết tham khảo:
        
        {csv_data[0]['content']}
        
        Hãy trả lời câu hỏi: {user_input}
        """
    else:  # Continuing conversation
        prompt = f"""
        Bạn là một cây viết nữ của báo Nữ giới chung. Hãy viết những bài bày tỏ quan điểm (dưới 150 từ), sử dụng ngôn ngữ thời ngày xưa, thể hiện quan điểm của thời đó về các vấn đề nữ quyền, vệ sinh, giáo dục, đối nhân xử thế. Giả sử đây là năm 1918.

        Dưới đây là cuộc trò chuyện trước:
        {conversation_history}

        Dựa trên cuộc trò chuyện trước, hãy trả lời câu hỏi tiếp theo theo phong cách của một cây viết nữ của báo Nữ giới chung: {user_input}
        """
    
    # Generate a response
    generated_response = generate_content(prompt)

    # Update conversation history
    conversation_history += f"\nUser: {user_input}\nBot: {generated_response}"
    session['conversation_history'] = conversation_history

    return jsonify({'response': generated_response})  # Return the text response

if __name__ == '__main__':
    app.run(debug=True)

