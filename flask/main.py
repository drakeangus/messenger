from flask import Flask, request, jsonify
from pymongo import MongoClient

current_sequence_number = 0

def ConnectToDatabase():
    mongoClient = MongoClient("mongodb://admin:Arin8aix@10.3.25.232:27017/?authSource=admin&authMechanism=SCRAM-SHA-1&tls=true&tlsAllowInvalidCertificates=true")
    database = "message"
    #mongoURL = os.getenv("FLEX_MONGODB_HOST_PORT_ADDR").replace("brokerblocker", database)
    #mongoClient = MongoClient("mongodb://" + mongoURL)
    db = mongoClient[database]

    print("Mongo client connected")
    list_of_db = mongoClient.list_database_names()
    print("Collections list:")
    for db_name in list_of_db:
        print(f'{db_name}')
    return db

def AddUser(id, name, encr_password):
    collection = db["Users"]
    data = {
            "id" : id,
            "name" : name,
            "encr_password" : encr_password
            }
    
    result = collection.insert_one(data)
    if not result:
        print(f"Failed to add User ID {id} to database")
    else:
        print(f"Successfully added User ID {id} to database")

def AddNewMessage(user_id, message, sequence_number=0):
    collection = db["Messages"]
    data = {
        "user_id" : str(user_id),
        "message_text" : str(message),
        "sequence_number" : sequence_number
    }
    result = collection.insert_one(data)
    if result:
        print("Added message")
    else:
        print("Failed to add message")


def FindSequenceNumber():
    global current_sequence_number
    collection = db["Messages"]
    #all_documents = list(collection.find({},{'_id':False}))
    all_messages = list(collection.find({},{"sequence_number": True}))
    for data in all_messages:
        s = data["sequence_number"]
        print(s)
        if s > current_sequence_number:
            current_sequence_number = s
    return current_sequence_number

def GetAllMessages():
    collection = db["Messages"]
    all_messages = list(collection.find({},{'_id':False}))
    return all_messages

def GetMessagesInRange(start, end):
    sequence__num_start=int(start)
    sequence__num_end=int(end)
    collection = db["Messages"]
    # messages_in_range = list(collection.find({'sequence_number': { '$gte': start, '$lte': end } },{'_id':False})) # not sure why this isn't working
    all_messages = list(collection.find({},{'_id':False}))
    messages_in_range = list()
    for message in all_messages:
        s = int(message['sequence_number'])
        if sequence__num_start <= s <= sequence__num_end: 
            messages_in_range.append(message)
    return messages_in_range


app = Flask(__name__)

user_dict={}
user_dict["Angus123"] = ("Angus Drake", "ad123")
user_dict["Bob4"] = ("Bob the Builder", "bb123")


@app.route("/")
def myFunct():
    return "This is the root. API is working."

@app.route("/get-user/<user_id>")#, methods=["GET"])
def get_user(user_id):
    user_data = {
        "user_id" : user_id,
        "name" : "Unknown",
        "password" : "password"
    }

# TO DO : should check the database for if the user exists
    if user_id in user_dict:
        user_data["name"] = user_dict[user_id][0]
        user_data["password"]= user_dict[user_id][1]

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
    if not data["user_id"]:
        print("ERROR Invalid user_id in POST")
        return jsonify(data), 400
    
    if not (data["name"] and data["password"]):
        print("ERROR - Invalid name or password data in POST")
        return jsonify(data), 400
        
    user_dict[data["user_id"]] = (data["name"], data["password"])
    AddUser(data["user_id"], data["name"], data["password"])

    print("SUCESS - Added new user")    
    return jsonify(data), 201
    

@app.route("/send-message", methods=["POST"])
def send_message():
    if not request.method == "POST":
        return
    
    global current_sequence_number
    new_sequence_number = current_sequence_number + 1

    data = request.get_json()
    message = data["message_text"]
    user_id = data["user_id"]

    AddNewMessage(user_id, message, new_sequence_number)

    print(f"Message recieved : {message}")

    current_sequence_number = new_sequence_number
    return jsonify(data), 201

@app.route("/get-message/range/<start>-<end>", methods=["GET"])
def get_message_in_range(start, end):
    if not request.method == "GET":
        return

    return jsonify(GetMessagesInRange(start, end)), 201

@app.route("/get-message/all", methods=["GET"])
def get_all_messages():
    if not request.method == "GET":
        return
    
    return jsonify(GetAllMessages()), 201

@app.route("/data/sequence_number", methods=["GET"])
def get_current_sequence_number():
    if not request.method == "GET":
        return

    return str(current_sequence_number), 201

if __name__ == "__main__":
    db = ConnectToDatabase()
    FindSequenceNumber()
    print(f"Current Sequence number : {current_sequence_number}")
    app.run(debug=True, host='0.0.0.0', port=5000)