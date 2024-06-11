import requests
import pandas as pd


def get_rows_by_time(base_url, time_value):
    endpoint = "/rows"
    url = f"{base_url}{endpoint}"
    params = {'time': time_value}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        rows = response.json()  # Get the response as JSON
        return pd.DataFrame(rows)  # Convert the JSON to a DataFrame
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
