import pytest
import requests
import json

# Base URL of the Flask app when running
BASE_URL = 'http://localhost:5002'

def test_create_appeal():
    url = f"{BASE_URL}/appeal"
    data = {'house_id': 1, 'description': 'Leaky faucet'}
    response = requests.post(url, json=data)
    
    assert response.status_code == 201
    assert 'Appeal created successfully' in response.json()['message']

def test_get_appeals():
    # First, create an appeal
    create_url = f"{BASE_URL}/appeal"
    create_data = {'house_id': 2, 'description': 'Broken window'}
    requests.post(create_url, json=create_data)

    # Now, get appeals
    get_url = f"{BASE_URL}/appeals"
    response = requests.get(get_url)
    
    assert response.status_code == 200
    appeals = response.json()
    assert any(appeal['description'] == 'Broken window' for appeal in appeals)

def test_delete_appeal():
    # First, create an appeal
    create_url = f"{BASE_URL}/appeal"
    create_data = {'house_id': 3, 'description': 'Noise complaint'}
    create_response = requests.post(create_url, json=create_data)

    appeal_id = create_response.json()['appeal_id']

    # Now, delete the appeal
    delete_url = f"{BASE_URL}/appeal/{appeal_id}"
    delete_response = requests.delete(delete_url)
    
    assert delete_response.status_code == 200
    assert 'Appeal deleted successfully' in delete_response.json()['message']

if __name__ == "__main__":
    pytest.main()
