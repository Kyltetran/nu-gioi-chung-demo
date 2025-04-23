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
def load_csv(file_path):
    data = []
    try:
        with open(file_path, "r", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=";")
            next(csvreader)  # Skip header if it exists
            for row in csvreader:
                data.append({"subject": row[0], "content": row[1]})
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return data


# Load the CSV data
csv_data = load_csv("data.csv")


# Route for index page
@app.route("/")
def index():
    session.clear()  # Clear the session when starting a new conversation
    return render_template("index.html")


# Function to generate content using the Gemini API
def generate_content(prompt):
    print("Prompt: " + prompt)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

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


    excerpt_block = "\n\n".join(
        [f"Chủ đề: {row['subject']}\nNội dung: {row['content']}" for row in csv_data[:20]]
    )

    # Build the prompt using the previous conversation and CSV content
    if not conversation_history:  # First interaction
        prompt = f"""
        Below are excerpts from the *Nữ Giới Chung* newspaper written by Vietnamese women in the early 20th century. Analyze and learn the writing style, tone, and themes they focus on:

        {excerpt_block}

        Now, based on the style you've just learned, respond to the following user question in Vietnamese. Keep your response short and emotional (under 150 words), reflecting the values and writing manner of *Nữ Giới Chung* writers.

        User question:
        {user_input}
        """
    else:  # Continuing conversation
        prompt = f"""
        You are a helpful assistant participating in the ongoing conversation below.

        Your personality and writing style are inspired by female authors from the early 20th-century Vietnamese newspaper *Nữ Giới Chung*. Keep your responses thoughtful, emotional, and concise — no more than 150 words.

        Always answer in Vietnamese.

        Conversation history:
        {conversation_history}

        User: {user_input}
        Bot:"""

    # Generate a response
    generated_response = generate_content(prompt)

    # Update conversation history
    conversation_history += f"\nUser: {user_input}\nBot: {generated_response}"
    session["conversation_history"] = conversation_history

    return jsonify({"response": generated_response})  # Return the text response


if __name__ == "__main__":
    app.run(debug=True)
