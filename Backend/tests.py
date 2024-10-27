# test.py

from app import app  # Import your Flask app
import json

def test_create_rule():
    with app.test_client() as client:
        response = client.post('/create_rule', json={
            'rule_string': "age > 30 AND department == 'Sales'",
            'rule_id': 'rule1'
        })
        assert response.status_code == 200
        assert b'Rule created' in response.data

def test_evaluate_rule():
    with app.test_client() as client:
        response = client.post('/evaluate_rule', json={
            'rule_id': 'rule1',
            'user_data': {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        })
        assert response.status_code == 200
        assert json.loads(response.data)["eligible"] is True

if __name__ == "__main__":
    test_create_rule()
    test_evaluate_rule()
    print("All tests passed!")
