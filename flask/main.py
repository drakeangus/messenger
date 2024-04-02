from flask import Flask, request, jsonify

app = Flask(__name__)


user_dict={}

user_dict["Angus123"] = ("Angus Drake", "angus.drake@pretend.com")
user_dict["Bob4"] = ("Bob the Builder", "cowboy.builder@phony.com")


@app.route("/")
def myFunct():
    return "this is my function"

@app.route("/get-user/<user_id>")#, methods=["GET"])
def get_user(user_id):
    user_data = {
        "user_id" : user_id,
        "name" : "Unknown",
        "email" : "unknown@example.com"
    }

    if user_id in user_dict:
        user_data["name"] = user_dict[user_id][0]
        user_data["email"]= user_dict[user_id][1]

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra
    else:
        user_data["extra"] = "No extra data"
        
    return jsonify(user_data), 200


@app.route("/create-user", methods=["POST"])
def create_user():
    if not request.method == "POST":
        return
    
    data = request.get_json()
    


    if data["user_id"]:
        if data["name"] and data["email"]:
            user_dict[data["user_id"]] = (data["name"], data["email"])
        else:
            return jsonify(data), 400
        return jsonify(data), 201
    return jsonify(data), 400

if __name__ == "__main__":
    app.run(debug=True)