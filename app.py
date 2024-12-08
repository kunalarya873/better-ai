import os
from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Groq client
client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/analyze", methods=["POST"])
def analyze_code():
    """
    Endpoint to analyze code snippets for performance bottlenecks.
    """
    try:
        # Retrieve the code snippet from the request
        data = request.json
        code_snippet = data.get("code", "")

        if not code_snippet:
            return jsonify({"error": "No code snippet provided"}), 400

        # Prompt the AI to analyze the code
        prompt = f"""
        Analyze the following code snippet for potential performance bottlenecks.
        Provide specific suggestions for optimization:
        
        ```
        {code_snippet}
        ```
        """
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        # Extract the AI's response
        analysis = chat_completion.choices[0].message.content

        return jsonify({"analysis": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
