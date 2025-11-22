import subprocess
import json

# ID of the publisher to update (replace this with the actual ID you want to update)
id_editore = "692162cbb298f74270f6504b"

# Prepare the JSON payload as a dictionary
data = {
    "publisher_id": id_editore,
    "title": "Sample Book Title",  # Add a valid title
    "author": "Prova",
    "genre": "Fantascienza",
    "year": 2008
}

# Convert the dictionary to a JSON string
data_json = json.dumps(data)

# Construct the curl command for the PUT request
curl_command = [
    "curl",
    "-X", "POST",  # Use PUT method
    f"http://localhost:8888/publishers/{id_editore}/books",  # Target endpoint
    "-H", "Content-Type: application/json",  # Content-Type header
    "-d", data_json  # Pass the properly formatted JSON string
]

# Run the curl command and capture the result
result = subprocess.run(curl_command, capture_output=True, text=True)

# Print the result (response from the server)
print(result.stdout)
print(result.stderr)
