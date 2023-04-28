from flask import Flask, jsonify
import hashlib
import jwt
from flask import Flask, jsonify, request
import openai

app = Flask(__name__)

openai.api_key = "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"
app.config['SECRET_KEY'] = 'secret_key'
user_credentials = {
    "example_user": "my_password"
}


def chat(inp, message_history, role="user"):
    message_history.append({"role": role, "content": f"{inp}"})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )
    reply_content = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": f"{reply_content}"})
    return reply_content


def check(token):
    try:
        # Verify if the token is valid and decode its payload
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return True
    except jwt.exceptions.InvalidTokenError:
        # If the token is invalid, return an error message
        return False


@app.route('/api/auth/login', methods=['POST'])
def login():
    login = request.json.get('login')
    password = request.json.get('password')

    # Verify if the user credentials are correct
    if login in user_credentials and user_credentials[login] == password:
        # Generate a token for the user
        payload = {'login': login}
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    # If the credentials are incorrect, return an error message
    return jsonify({'error': 'Invalid login or password'}), 401


@app.route('/api/auth/check', methods=['POST'])
def check_api():
    token = request.json.get('token')
    if check(token):
        return jsonify({'message': f'Token is valid'})
    else:
        return jsonify({'error': 'Invalid token.'}), 401


@app.route('/api/chat', methods=['POST'])
def chat():
    token = request.json.get('token')
    if not check(token):
        return jsonify({'error': 'Invalid token.'}), 401
    message_history = []
    for i in range(10):
        user_input = input("> ")
        print("User's input was: ", user_input)
        print(chat(user_input, message_history))
        print()


# Run the app
if __name__ == '__main__':
    print('start')
    app.run(debug=True)
