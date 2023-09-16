from flask import Flask, request, json
import pandas as pd
import os
import csv

app = Flask(__name__)

# Endpoint: /calculate
@app.route('/calculate', methods=['POST'])
def calculate():
    input_data = request.get_json()
    input_file = input_data.get('file')
    product = input_data.get('product')
    if not input_file:
        return json.dumps({'file': None, 'error': 'Invalid JSON input.'}), 400
    mounted_file = os.path.join('/Dhruv_PV_dir/', input_file)

    if not os.path.isfile(mounted_file):
        return json.dumps({"file": input_file,"error": "File not found."}), 400

    with open(mounted_file,'r',encoding='utf-8-sig') as file:
        dataframes = pd.read_csv(mounted_file)
        try:
            fileReader=csv.DictReader(file)
            column_names = fileReader.fieldnames
            print(fileReader)
            print(column_names)
            if len(column_names) != 2:
                return json.dumps({"file": input_file, "error":  "Input file not in CSV format."}), 400
            if dataframes['product'].isnull().any() or dataframes['amount'].isnull().any():
                return json.dumps({"file": input_file, "error":  "Input file not in CSV format."}), 400  
             
        except csv.Error:
            response = json.dumps({"file": input_file, "error":  "Input file not in CSV format."})
            return response, 400, {'Content-Type': 'application/json'}

        sum = 0
        for index, row in dataframes.iterrows():
            print(row['product'], product, row['product'] == product)
            if(row['product'] == product):
                sum = sum + row['amount']

        print(sum)

        return json.dumps({"file": input_file,"sum": str(sum)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
