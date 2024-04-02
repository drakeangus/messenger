import requests

def get_user_data(username):
    url = f"http://127.0.0.1:5000/get-user/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get user data. Status code: {response.status_code}")
        return None

# Example usage
username = "Bob4"
user_data = get_user_data(username)
if user_data:
    print("User data:")
    print(user_data)
