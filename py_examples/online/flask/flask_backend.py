
# Explanation:
# API 1 (/api/greet): A GET endpoint that takes an optional name parameter and returns a greeting message.
# API 2 (/api/add): A POST endpoint that accepts two numbers in the request body and returns their sum.
# API 3 (/api/is_prime): A GET endpoint that checks whether a given number (provided as a query parameter) is prime.


from flask import Flask, jsonify, request

app = Flask(__name__)


# API 1: Greeting endpoint
@app.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'World')
    return jsonify({"message": f"Hello, {name}!"})


# API 2: Add two numbers
@app.route('/api/add', methods=['POST'])
def add():
    data = request.json
    number1 = data.get('number1')
    number2 = data.get('number2')
    if number1 is None or number2 is None:
        return jsonify({"error": "Please provide both numbers"}), 400
    result = number1 + number2
    return jsonify({"result": result})


# API 3: Check if a number is prime
@app.route('/api/is_prime', methods=['GET'])
def is_prime():
    try:
        number = int(request.args.get('number'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input. Please provide a valid integer."}), 400

    if number < 2:
        return jsonify({"result": False})

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return jsonify({"result": False})

    return jsonify({"result": True})


# run app
def run_app():
    app.run(debug=True)

if __name__ == '__main__':
    run_app()
