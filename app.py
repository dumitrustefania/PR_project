from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from pydantic import BaseModel
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app, origins="*")

user_data = {
        "1a143bce": {
            "firstName": "Stefania",
            "lastName": "Dumitru",
            "paidMembership": True,
            "attendances": 5
        },
        "331ec827": {
            "firstName": "Donald",
            "lastName": "Trump",
            "paidMembership": False,
            "attendances": 0
        },
        "eae482ce": {
            "firstName": "Charlie",
            "lastName": "Brown",
            "paidMembership": True,
            "attendances": 1
        }
    }

class RegistrationData(BaseModel):
    firstName: str
    lastName: str
    paidMembership: bool
    attendances: int

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/check_user", methods=["POST"])
def check_user():
    card_id = request.json.get('card_id')
    first_req = request.json.get('first_request')
    response_data = {}
    if not user_data.get(card_id):
        response_data["status"] = "not registered"
        if first_req:
            socketio.emit('new_user_detected', {'card_id': card_id})
        return jsonify(response_data)

    if user_data.get(card_id).get('paidMembership'):
        user_data.get(card_id)["attendances"] += 1
        response_data["status"] = "valid"
        response_data["first_name"] = user_data.get(card_id).get('firstName')
        response_data["attendances"] = user_data.get(card_id).get('attendances')
    else:
        response_data["status"] = "invalid"

    return jsonify(response_data)

@app.route("/api/register", methods=["POST"])
def register_user():
    card_id = request.json.get('card_id')
    data = request.json.get('data')
    if not user_data.get(card_id):
        data["attendances"] = 0
        user_data[card_id] = data
        return jsonify({"message": "User registered successfully"})
    else:
        return jsonify({"error": "User already registered"}), 400

@app.route("/api/users", methods=["GET"])
def get_all_users():
    return jsonify(user_data)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
