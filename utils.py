import json
import os

def get_last_entry(file_path):
    # Open the file in binary mode to ensure proper seeking
    with open(file_path, 'rb') as file:
        # Move the file pointer to the end of the file
        file.seek(0, 2)
        # Find the position of the last newline character
        pos = file.tell()
        print(f"pos check : {pos}")
        while pos > 0:
            pos -= 1
            file.seek(pos)
            # Read a single byte
            char = file.read(1)
            # Check if it's a newline character
            if char == b'\n':
                # Move the pointer to the next position after newline
                file.seek(pos + 1)
                # Read and decode the last line
                last_line = file.readline().decode('utf-8').strip()
                # Load JSON data from the last line
                last_entry = json.loads(last_line)
                return last_entry

# Define the filename
file_name = "message_history.json"

# Get the full file path
file_path = os.path.join(os.getcwd(), file_name)

# Check if the file exists
if os.path.exists(file_path):
    # Retrieve the last entry
    last_entry = get_last_entry(file_path)
    if last_entry:
        print("Last Entry:")
        print(last_entry["SequenceNumber"]+1)
    else:
        print("No valid JSON entry found in the file.")
else:
    print(f"File '{file_name}' does not exist in the current directory.")