from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load the CSV file at startup
df = None

def load_csv():
    global df
    try:
        # Replace 'yourfile.csv' with your CSV file path
        df = pd.read_csv('transactions_1.csv')
        print("CSV file loaded successfully")
    except Exception as e:
        print(f"Failed to load CSV file: {e}")

@app.route('/rows', methods=['GET'])
def get_rows():
    time_value = request.args.get('time', default=None, type=str)
    if time_value is None:
        return "No time value provided", 400

    if df is None:
        return "CSV file not loaded", 500

    try:
        matching_rows = df[df['time'] == time_value]
        if matching_rows.empty:
            return "No rows found with the given time value", 404
        rows_list = matching_rows.to_dict(orient='records')
        return jsonify(rows_list), 200
    except Exception as e:
        return str(e), 400


if __name__ == '__main__':
    load_csv()  # Load the CSV file when the application starts
    app.run(debug=True)

