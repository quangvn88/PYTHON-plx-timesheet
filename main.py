from flask import Flask, request, jsonify
import timesheet

PORT = 3001
app = Flask(__name__)

@app.route("/")
def home():
    return "Test"

#http://localhost:3001/get-user/123?extra="Hello"
@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "user name",
        "email": "email@fpt.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra
    
    return jsonify(user_data), 200

#http://localhost:3001/create-ts/
@app.route("/create-ts", methods=["POST"])
def create_ts():
    data = request.get_json()    
    print("create_ts")
    timesheet.run_ts(data["fdate"], data["tdate"], data["month"], data["year"], data["user"], data["pass"])
    return jsonify("done"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)    