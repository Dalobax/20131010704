#Importing Libraries
from flask import Flask, request, jsonify
import requests
import threading
#Creating the Flask App
app = Flask(__name__)

#Fetching Numbers from URL
def fetchNumbers(url, result_dict):
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if "numbers" in data:
            result_dict[url] = data["numbers"]
    except Exception as e:
        pass
#Defining API Endpoint

@app.route('/numbers', methods=['GET'])
def getNumbers():
    urls = request.args.getlist('url')
    result_dict = {}
    threads = []

    for url in urls:
        t = threading.Thread(target=fetchNumbers, args=(url, result_dict))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    merged_numbers = sorted(list(set(num for nums in result_dict.values() for num in nums)))

    return jsonify({"numbers": merged_numbers})
 #Running the Microservice
if __name__ == '__main__':
    app.run(host='localhost', port=8008)
