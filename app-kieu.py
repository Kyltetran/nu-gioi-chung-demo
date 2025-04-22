import os
import csv
import google.generativeai as genai
from flask import Flask, jsonify, request, render_template, session

app = Flask(__name__)
app.secret_key = "NhuquynhNhuquynh"  # You need this for session management

# Configure the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


# Load CSV data
# def load_csv(file_path):
#     data = []
#     try:
#         with open(file_path, "r", encoding="utf-8") as csvfile:
#             csvreader = csv.reader(csvfile, delimiter=";")
#             next(csvreader)  # Skip header if it exists
#             for row in csvreader:
#                 data.append({"subject": row[0], "content": row[1]})
#     except FileNotFoundError:
#         print(f"File not found: {file_path}")
#     return data

# load the txt data
def load_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")

    return ""


# Load the CSV data
csv_data = load_txt("Couplets_Table.txt")


# Route for index pageç
@app.route("/")
def index():
    session.clear()  # Clear the session when starting a new conversation
    return render_template("index.html")


# Function to generate content using the Gemini API
def generate_content(prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-002")

    # Generate the content
    response = model.generate_content(prompt)

    # Extract the text from the response
    generated_text = (
        response.candidates[0].content.parts[0].text
    )  # Adjust this based on your actual response structure
    return generated_text


# Route to handle user input and generate content with memory
@app.route("/generate_content", methods=["POST"])
def handle_generate_content():
    user_input = request.json.get("question")

    # Retrieve previous conversation history from session
    conversation_history = session.get("conversation_history", "")

    # Build the prompt using the previous conversation and CSV content
    # if not conversation_history:  # First interaction
    prompt = f"""
    
    Dưới đây là bộ Truyện Kiều:
    
    {csv_data}
    
    Hãy lặp lại chính xác câu hỏi và bói Kiều bằng cách trích dẫn một câu bất kỳ trong bộ Truyện Kiều ở trên và phân tích sự liên quan của nó với câu hỏi được nhập:
    """
    # else:  # Continuing conversation
    #     prompt = f"""

    #     Bạn là Bot trong cuộc trò chuyện dưới đây.
    #     {conversation_history}
    #     Hãy tiếp tục cuộc trò chuyện với User:{user_input}

    #     """

    # Generate a response
    generated_response = generate_content(prompt)

    # Update conversation history
    conversation_history += f"\nUser: {user_input}\nBot: {generated_response}"
    session["conversation_history"] = conversation_history

    # Return the text response
    return jsonify({"response": generated_response})


if __name__ == "__main__":
    app.run(debug=True)
