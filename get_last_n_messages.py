import json
import os

def get_last_n_entries(file_path, n):
    last_n_entries = []
    # Open the file in binary mode to ensure proper seeking
    with open(file_path, 'rb') as file:
        # Move the file pointer to the end of the file
        file.seek(0, 2)
        # Find the position of the last newline character
        pos = file.tell()
        count = 0
        while pos > 0 and count < n:
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
                last_n_entries.insert(0, last_entry)  # Insert at the beginning to maintain order
                count += 1
    return last_n_entries

# Define the filename
file_name = "message_history.json"

# Get the full file path
file_path = os.path.join(os.getcwd(), file_name)

# Specify the number of last messages you want to retrieve
n = 3  # Change this number to retrieve a different number of messages

# Check if the file exists
if os.path.exists(file_path):
    # Retrieve the last n entries
    last_n_entries = get_last_n_entries(file_path, n)
    print(f"Last {n} Entries:")
    for entry in last_n_entries:
        print(entry)
else:
    print(f"File '{file_name}' does not exist in the current directory.")
