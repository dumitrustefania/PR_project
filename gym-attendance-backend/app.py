from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
from datetime import datetime
from user_data import user_data  # Import user_data from user_data.py
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static", static_url_path="")
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app, origins="*")


@app.route("/api/check_user", methods=["POST"])
def check_user():
    card_id = request.json.get("card_id")
    first_req = request.json.get("first_request")
    response_data = {}
    if not user_data.get(card_id):
        response_data["status"] = "not registered"
        if first_req:
            socketio.emit("new_user_detected", {"card_id": card_id})
        return jsonify(response_data)

    user = user_data[card_id]
    if user.get("paidMembership"):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user["attendances"].append(timestamp)
        socketio.emit(
            "user_updated", {"card_id": card_id, "attendances": user["attendances"]}
        )

        response_data["status"] = "valid"
        response_data["first_name"] = user["firstName"]
        response_data["attendances"] = user["attendances"]
    else:
        response_data["status"] = "invalid"

    return jsonify(response_data)


@app.route("/api/register", methods=["POST"])
def register_user():
    card_id = request.json.get("card_id")
    data = request.json.get("data")
    if not user_data.get(card_id):
        data["attendances"] = []
        user_data[card_id] = data
        socketio.emit("user_registered", {"card_id": card_id, "user": data})
        return jsonify({"message": "User registered successfully"})
    else:
        return jsonify({"error": "User already registered"}), 400


@app.route("/api/users", methods=["GET"])
def get_all_users():
    return jsonify(user_data)


@app.route("/api/user/<card_id>", methods=["GET"])
def get_user_details(card_id):
    user = user_data.get(card_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/api/statistics", methods=["GET"])
def get_statistics():
    stats = {
        "total_users": len(user_data),
        "daily_load": {
            "Monday": 0,
            "Tuesday": 0,
            "Wednesday": 0,
            "Thursday": 0,
            "Friday": 0,
            "Saturday": 0,
            "Sunday": 0,
        },
        "hourly_load": {
            str(i): 0 for i in range(9, 24)  # Gym open between 9 and 23
        },
        "attendances1": {}, 
        "attendances2": {}, 
    }

    # Process attendance data
    for user in user_data.values():
        for attendance in user["attendances"]:
            dt = datetime.strptime(attendance, "%Y-%m-%d %H:%M:%S")
            day = dt.strftime("%A")  # Get the day name (Monday)
            date_str = dt.strftime("%Y-%m-%d")  # Get the date string (2023-01-01)
            hour = int(dt.strftime("%H"))  # Get the hour as an integer (10 for 10:20)

            # Update attendances1 for the specific hour of the specific date
            if date_str not in stats["attendances1"]:
                stats["attendances1"][date_str] = {}
            if hour not in stats["attendances1"][date_str]:
                stats["attendances1"][date_str][hour] = 0
            stats["attendances1"][date_str][hour] += 1

            # Update attendances2 for the specific date
            if date_str not in stats["attendances2"]:
                stats["attendances2"][date_str] = 0
            stats["attendances2"][date_str] += 1

    # Compute daily load (attendance per day of the week)
    for day in stats["daily_load"]:
        total_attendance = 0
        count = 0
        for date, day_data in stats["attendances2"].items():
            day_of_week = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
            if day_of_week == day:
                total_attendance += day_data
                count += 1
        stats["daily_load"][day] = total_attendance / count

    # Compute hourly load (attendance per hour 9-23)
    for hour in range(9, 24):
        total_attendance = 0
        count = 0
        for date, hour_data in stats["attendances1"].items():
            if hour in hour_data:
                total_attendance += hour_data[hour]
                count += 1
        stats["hourly_load"][str(hour)] = total_attendance / count

    return jsonify(stats)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)
