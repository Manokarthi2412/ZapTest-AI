import requests
import ast

def test_api(base_url, row):
    url = f"{base_url}{row['URL']}"  # Replace with your actual API base URL
    method = row['Method']
    headers = {'Content-Type': 'application/json'}
    response = None

    # Convert the string representation of JSON to a dictionary
    payload = ast.literal_eval(row['Request Body (JSON)'])

    try:
        # Send the request based on the method
        if method == 'POST':
            response = requests.post(url, json=payload, headers=headers)
        elif method == 'GET':
            response = requests.get(url, headers=headers)

        # Construct the actual response
        actual_response = f"{response.status_code} {response.reason}"
        return actual_response

    except Exception as e:
        # Handle exceptions and return error message
        return f"Error: {str(e)}"

def test_and_update_df(base_url, df):
    # Add the actual output column to the DataFrame
    df['Actual Output'] = df.apply(lambda row: test_api(base_url, row), axis=1)
    return df
