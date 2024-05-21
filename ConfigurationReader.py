import json

# Define a module-level variable to store the loaded configuration
_config = {}

def loadConfig(filepath):
    global _config
    try:
        with open(filepath, 'r') as file:
            _config = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {filepath} is not a valid JSON file.")

def get(key, default=None):
    return _config.get(key, default)