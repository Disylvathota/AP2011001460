from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_valid_api_links(server_link):
    response = requests.get(server_link)
    if response.status_code == 200:
        content = response.text
        api_links = [link.strip() for link in content.split('\n') if link.startswith("http://") and link.endswith(".json")]
        return api_links
    else:
        return []

def get_numbers_from_json(api_link):
    response = requests.get(api_link)
    if response.status_code == 200:
        data = response.json()
        numbers = [value for value in data.values() if isinstance(value, (int, float))]
        return numbers
    else:
        return []

@app.route('/process_server', methods=['POST'])
def process_server():
    data = request.get_json()
    server_link = data.get('server_link')
    if server_link:
        api_links = get_valid_api_links(server_link)
        merged_numbers = []
        for api_link in api_links:
            numbers = get_numbers_from_json(api_link)
            merged_numbers.extend(numbers)
        
        sorted_unique_numbers = sorted(list(set(merged_numbers)))
        return jsonify(sorted_unique_numbers)
    else:
        return jsonify({"error": "Invalid server link"}), 400

if __name__ == '__main__':
    app.run(debug=True)
