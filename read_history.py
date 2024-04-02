import json
import os

# Define the filename
file_name = "message_history.json"

# Form the full file path
file_path = os.path.join(os.getcwd(), file_name)

# Check if the file exists in the current directory
if os.path.exists(file_path):
    # Open the file and read its contents line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Load JSON data from each line
            data = json.loads(line)
            
            print(data)

            # Process the JSON data
            print("SequenceNumber:", data["SequenceNumber"])
            print("Sender:", data["Sender"])
            print("Message:", data["Message"])
            print()  # Add a newline for clarity
else:
    print(f"File '{file_name}' does not exist in the current directory.")
