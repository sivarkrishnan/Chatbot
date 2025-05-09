from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)
CORS(app)

model_name = "facebook/blenderbot-400M-distill"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    data = request.get_json()
    input_text = data['prompt']

    # Create input string from history
    history = "\n".join(conversation_history)
    input_str = history + "\n" + input_text if history else input_text

    # Tokenize
    inputs = tokenizer(input_str, return_tensors="pt", truncation=True, max_length=512)

    # Generate response
    outputs = model.generate(**inputs, max_new_tokens=60)

    # Decode
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Update conversation
    conversation_history.append(input_text)
    conversation_history.append(response)

    return jsonify(response=response)

if __name__ == '__main__':
    app.run()
