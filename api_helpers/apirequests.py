import requests

host="10.2.75.157"
port="5000"

def get_user_data(username):
    url = f"http://{host}:{port}/get-user/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get user data. Status code: {response.status_code}")
        return None

def post_new_user_data(username, user_id, password):
    url = f"http://{host}:{port}/create-user"
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

def send_new_message(user_id, message):
    url = f"http://{host}:{port}/send-message"
    json_data = {
        "user_id" : str(user_id),
        "message_text" : str(message)
    }
    response = requests.post(url, json=json_data)
    if response.status_code == 201:
        print("POST Message sent")
        return response.json()
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        return None
    
def get_all_messages():
    url = f"http://{host}:{port}/get-message/all"
    response = requests.get(url)
    if response.status_code == 201:
        print("GET All messages recieved")
        return response.json()
    else:
        print(f"Failed to get all messages. Status code: {response.status_code}")
        return None
    
def get_messages_in_range(start, end):
    url = f"http://{host}:{port}/get-message/range/{start}-{end}"
    response = requests.get(url)
    if response.status_code == 201:
        print("GET Messages in range recieved")
        return response.json()
    else:
        print(f"Failed to get all messages. Status code: {response.status_code}")
        return None
    
def get_remote_sequence_number():
    url = f"http://{host}:{port}/data/sequence_number"
    response = requests.get(url)
    return int(response.json())