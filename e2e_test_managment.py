import requests
import pytest

# Base URL of the Flask app when running
BASE_URL = 'http://localhost:5001'

def test_get_management():
    # Add a management and a house to the database first, if not already done

    # Test retrieving management information
    response = requests.get(f"{BASE_URL}/house/1")
    data = response.json()

    assert response.status_code == 200
    assert 'management_name' in data
    assert 'contact_info' in data
    assert 'average_rating' in data

def test_rate_management():
    # Rate a management
    response = requests.post(f"{BASE_URL}/rate_management/1", json={'score': 4})

    assert response.status_code == 201
    assert response.json().get('message') == 'Rating added successfully'

    # Verify if the rating was correctly added
    get_response = requests.get(f"{BASE_URL}/house/1")
    get_data = get_response.json()

    assert get_response.status_code == 200
    assert get_data['average_rating'] is not None

if __name__ == "__main__":
    pytest.main()
