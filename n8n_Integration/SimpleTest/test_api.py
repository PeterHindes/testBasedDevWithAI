import requests          

def test_api_hello_world():
    # Replace this URL with your actual API endpoint
    url = "http://localhost:9090/hello"

    # Make a GET request to the API
    response = requests.get(url)

    # Verify the HTTP status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Parse the JSON response
    data = response.json()

    # Verify the response contains {"hello": "world"}
    assert data == {"hello": "world"}, f'Expected {{"hello": "world"}}, got {data}'

# def test_api_hello_world_should_fail():
#     # Replace this URL with your actual API endpoint
#     url = "http://localhost:5000/hello"

#     # Make a GET request to the API
#     response = requests.get(url)

#     # Verify the HTTP status code is 200 (OK)
#     assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

#     # Parse the JSON response
#     data = response.json()

#     # Intentionally check for an incorrect response
#     assert data == {"hello": "mars"}, f'Expected {{"hello": "mars"}}, got {data}'