from flask import Flask, request, jsonify
import os
import requests
import json
import pandas as pd

app = Flask(__name__)

# Endpoint: /store-file
@app.route('/store-file', methods=['POST'])
def store_file():
    
    print("try it")
    print("try it using commit buidl")

    data = request.get_json()
    file_name = data.get('file')
    file_data = data.get('data')
    print("ssss done hhh")

    if not file_name:
        return jsonify({'file': None, 'error': 'Invalid JSON input.'}), 400

       
    mount_path = "/Dhruv_PV_dir/"

        # Create the file in the persistent storage for Volume
    file_path = os.path.join(mount_path, file_name)
    try:
        with open(file_path, "w") as file:
            file.write(file_data)    
            return jsonify({'file': file_name, 'message': 'Success.'}), 200
            # Pass the endpoint to container 2 in the calculate API
            
    except Exception as e:
        return jsonify({'file': file_name, 'error': 'Error while storing the file to the storage.'}), 502


# Endpoint: /calculate
@app.route('/calculate', methods=['POST'])
def calculate():
    print("hello there")
    try:

        data = request.get_json()
        file_name = data.get('file')
        product = data.get('product')
        if not file_name:
            return jsonify({'file': None, 'error': 'Invalid JSON input.'}), 400
        # Define the path to the persistent volume mount
        mount_path = "/kube_PV_dir/"
        container2_endpoint = "http://localhost:7000/calculate"  
        payload = {'file': file_name, 'product': 'wheat'}  
        response = requests.post(container2_endpoint, json=payload)

        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({'file': None, 'error': 'Error while processing the request.'}), 5033

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)