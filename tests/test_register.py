
def test_register_new_user_success(client):
    payload = {
        "email": "newuser@example.com",
        "username": "newuser@example.com",
        "password": "strongpassword123"
    }

    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data



# def test_register_user_already_exists(client):
#     payload = {
#         "email": "duplicate@example.com",
#         "password": "strongpassword"
#     }

#     # First registration
#     response1 = client.post("/register", json=payload)
#     assert response1.status_code == 200

#     # Second registration attempt
#     response2 = client.post("/register", json=payload)
#     assert response2.status_code == 400
#     assert response2.json()["detail"] == "Email already registered"
