from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)

# In-memory storage for conversation history
conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def get_response():
    from duckduckgo_search import DDGS
    prompt = request.json['prompt']
    pro = request.json['ia']
    
    # Record the current date
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Store the prompt in conversation history
    conversation_history.append(f"{current_date} - User: {prompt}")
    
    keyword = DDGS().chat(keywords=f"Make a single lined internet Query for this prompt: {prompt}")
    resultss = DDGS().text(keywords=prompt)
    with open('conversation_history.txt', 'r', encoding='utf-8') as file:
     lines = file.readlines()
     for line in lines:
        filey = line.strip()
        print(filey)

    if pro == "11":
        results = DDGS().chat(f"Todays Date is {current_date}. Use this internet data only when the user specifies to use this data or else just talk casually without explaining why you are not using the internet data. Internet Data: {resultss} Prompt: {prompt}, Also give references link at the end if the given internet data is used. AND Do not give any extra explanations like 'I won't be using the internet data you provided, as I don't have a specific need for it at the moment. Let me know if there's anything else I can assist you with'. Here's the conversation history: {filey}", model='gpt-4o-mini')
    else:
        results = DDGS().chat(f"New Prompt: {prompt} . Respond as per the so that you dont forget what the user said earlierConversation History:{filey}")
    
    # Record the response in conversation history
    full_content = ''.join(results)
    conversation_history.append(f"{current_date} - Response: {full_content}")
    
    # Save the conversation history to a text file
    with open('conversation_history.txt', 'a', encoding='utf-8') as file:
        file.write('\n'.join(conversation_history) + '\n')
        
    
    return jsonify({'response': full_content})

if __name__ == '__main__':
    app.run(debug=True, port=1101)
