import json

def load_dropdown_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {}

# Usage
dropdown_data = load_dropdown_data('indiaandother.txt')