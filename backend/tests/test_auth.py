import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuthentication:
    """Test authentication endpoints"""

    async def test_user_registration_success(self, client: AsyncClient, test_user_data, setup_test_data):
        """Test successful user registration"""
        response = await client.post("/api/v1/auth/register", json=test_user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "Registration successful"
        assert "user_id" in data["data"]

    async def test_registration_duplicate_username(self, client: AsyncClient, test_user_data, setup_test_data):
        """Test registration with duplicate username"""
        await client.post("/api/v1/auth/register", json=test_user_data)

        response = await client.post("/api/v1/auth/register", json=test_user_data)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    async def test_registration_missing_required_fields(self, client: AsyncClient, setup_test_data):
        """Test registration with missing required fields"""
        incomplete_data = {
            "uname": "testuser",
            "ctype": "ID Card",
            "idno": "110101199001011234",
            "bname": "Test User"
        }

        response = await client.post("/api/v1/auth/register", json=incomplete_data)

        assert response.status_code == 422

    async def test_registration_short_username(self, client: AsyncClient, setup_test_data):
        """Test registration with username too short"""
        data = {
            "uname": "ab",
            "ctype": "ID Card",
            "idno": "110101199001011234",
            "bname": "Test User",
            "bpwd": "Password123",
            "phoneNo": "13800138000",
        }

        response = await client.post("/api/v1/auth/register", json=data)

        assert response.status_code == 422

    async def test_registration_invalid_phone_number(self, client: AsyncClient, setup_test_data):
        """Test registration with invalid phone number"""
        data = {
            "uname": "testuser",
            "ctype": "ID Card",
            "idno": "110101199001011234",
            "bname": "Test User",
            "bpwd": "Password123",
            "phoneNo": "12345678901",
        }

        response = await client.post("/api/v1/auth/register", json=data)

        assert response.status_code == 422

    @pytest.mark.parametrize("invalid_password,reason", [
        ("Pass1", "too short"),
        ("Password", "insufficient digits"),
        ("Password1", "insufficient digits"),
        ("password12", "all lowercase"),
        ("PASSWORD12", "all uppercase"),
    ])
    async def test_registration_invalid_password(self, client: AsyncClient, setup_test_data, invalid_password, reason):
        """Test password validation rules"""
        data = {
            "uname": "testuser",
            "ctype": "ID Card",
            "idno": "110101199001011234",
            "bname": "Test User",
            "bpwd": invalid_password,
            "phoneNo": "13800138000",
        }

        response = await client.post("/api/v1/auth/register", json=data)

        assert response.status_code == 422

    async def test_registration_valid_passwords(self, client: AsyncClient, setup_test_data):
        """Test various valid password formats"""
        valid_passwords = [
            "Password12",
            "Test1234",
            "Secure99Pass",
            "MyP2ssw0rd",
        ]

        for idx, password in enumerate(valid_passwords):
            data = {
                "uname": f"testuser{idx}",
                "ctype": "ID Card",
                "idno": f"11010119900101{1000 + idx}",
                "bname": f"Test User {idx}",
                "bpwd": password,
                "phoneNo": f"1380013800{idx}",
            }

            response = await client.post("/api/v1/auth/register", json=data)

            assert response.status_code == 201, f"Password '{password}' should be valid"

    async def test_login_success(self, client: AsyncClient, test_user_data, setup_test_data):
        """Test successful login"""
        await client.post("/api/v1/auth/register", json=test_user_data)

        response = await client.post("/api/v1/auth/login", json={
            "username": test_user_data["uname"],
            "password": test_user_data["bpwd"]
        })

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "Login successful"
        assert "token" in data["data"]
        assert "user_info" in data["data"]
        assert data["data"]["user_info"]["uname"] == test_user_data["uname"]
        assert data["data"]["user_info"]["bname"] == test_user_data["bname"]
        assert data["data"]["user_info"]["phoneNo"] == test_user_data["phoneNo"]

    async def test_login_invalid_password(self, client: AsyncClient, test_user_data, setup_test_data):
        """Test login with incorrect password"""
        await client.post("/api/v1/auth/register", json=test_user_data)

        response = await client.post("/api/v1/auth/login", json={
            "username": test_user_data["uname"],
            "password": "WrongPassword123"
        })

        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    async def test_login_nonexistent_user(self, client: AsyncClient, setup_test_data):
        """Test login with non-existent username"""
        response = await client.post("/api/v1/auth/login", json={
            "username": "nonexistent",
            "password": "Password123"
        })

        assert response.status_code == 401

    async def test_login_case_sensitive_username(self, client: AsyncClient, test_user_data, setup_test_data):
        """Test that username is case-sensitive for login"""
        await client.post("/api/v1/auth/register", json=test_user_data)

        response = await client.post("/api/v1/auth/login", json={
            "username": test_user_data["uname"].upper(),
            "password": test_user_data["bpwd"]
        })

        assert response.status_code == 401

    async def test_token_structure(self, client: AsyncClient, test_user_data, setup_test_data):
        """Test JWT token structure and content"""
        await client.post("/api/v1/auth/register", json=test_user_data)

        response = await client.post("/api/v1/auth/login", json={
            "username": test_user_data["uname"],
            "password": test_user_data["bpwd"]
        })

        token = response.json()["data"]["token"]
        assert isinstance(token, str)
        assert token.count(".") == 2

    async def test_login_empty_credentials(self, client: AsyncClient, setup_test_data):
        """Test login with empty credentials"""
        response = await client.post("/api/v1/auth/login", json={
            "username": "",
            "password": ""
        })

        assert response.status_code == 401

    async def test_registration_idno_uniqueness(self, client: AsyncClient, setup_test_data):
        """Test that ID numbers must be unique"""
        data1 = {
            "uname": "user1",
            "ctype": "ID Card",
            "idno": "110101199001011234",
            "bname": "User 1",
            "bpwd": "Password123",
            "phoneNo": "13800138000",
        }

        await client.post("/api/v1/auth/register", json=data1)

        data2 = {
            "uname": "user2",
            "ctype": "ID Card",
            "idno": "110101199001011234",
            "bname": "User 2",
            "bpwd": "Password456",
            "phoneNo": "13800138001",
        }

        response = await client.post("/api/v1/auth/register", json=data2)

        assert response.status_code == 400

    async def test_registration_phone_uniqueness(self, client: AsyncClient, setup_test_data):
        """Test that phone numbers must be unique"""
        data1 = {
            "uname": "user1",
            "ctype": "ID Card",
            "idno": "110101199001011234",
            "bname": "User 1",
            "bpwd": "Password123",
            "phoneNo": "13800138000",
        }

        await client.post("/api/v1/auth/register", json=data1)

        data2 = {
            "uname": "user2",
            "ctype": "ID Card",
            "idno": "110101199001011235",
            "bname": "User 2",
            "bpwd": "Password456",
            "phoneNo": "13800138000",
        }

        response = await client.post("/api/v1/auth/register", json=data2)

        assert response.status_code == 400
