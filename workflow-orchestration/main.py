from dotenv import load_dotenv
import os
import base64
import json

def main():
    # Load the .env file
    load_dotenv()

    # Retrieve the Base64-encoded key
    encoded_key = os.getenv("GOOGLE_CLOUD_KEY_BASE64")
    if not encoded_key:
        raise ValueError("Environment variable GOOGLE_CLOUD_KEY_BASE64 is not set.")

    # Decode the key and load it as JSON
    key_json = json.loads(base64.b64decode(encoded_key).decode("utf-8"))
    print("Decoded key:", key_json)

if __name__ == "__main__":
    print("Hello from workflow-orchestration!")
    main()