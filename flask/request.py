import requests



def get_user_data(username):
    url = f"http://127.0.0.1:5000/get-user/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get user data. Status code: {response.status_code}")
        return None

def post_new_user_data(username, user_id, password):
    url = f"http://127.0.0.1:5000/create-user"
    json_data = {
        "user_id": str(username),
        "name": str(user_id),
        "password": str(password)
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, json=json_data)#, headers=headers)
    if response.status_code == 201:
        print("POST Created")
        return response.json()
    else:
        print(f"Failed to post new user data. Status code: {response.status_code}")
        return None

def send_new_message(user_id, message, sequence_number):
    url = f"http://127.0.0.1:5000/send-message"
    json_data = {
        "user_id" : str(user_id),
        "message_text" : str(message),
        "sequence_number" : sequence_number
    }
    response = requests.post(url, json=json_data)
    if response.status_code == 201:
        print("POST Message sent")
        return response.json()
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        return None

# Example usage for existing user
username = "Bob4"
user_data = get_user_data(username)
if user_data:
    print("User data:")
    print(user_data)

username = "Bob5"
user_id = "bob5"
password = "bob123"

new_user_response = post_new_user_data(username, user_id, password)
print(new_user_response)

user_data = get_user_data("Bob5")
if user_data:
    print("User data:")
    print(user_data)

message_response = send_new_message(user_id, "Does this message show in the db?", -1)
print(message_response)