# util functions for gambling analyses
import os

# read api key from file
def read_api_key(api_key_file):
    if not os.path.exists(api_key_file):
        raise FileNotFoundError(f"API key file {api_key_file} does not exist.")
    with open(api_key_file, 'r') as f:
        api_key = f.read().strip()
    return api_key

