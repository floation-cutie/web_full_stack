"""
Comprehensive API Testing Suite for GoodServices Platform

This test suite covers:
1. Authentication APIs (register, login)
2. User APIs (profile, password change)
3. Service Request APIs (CRUD operations)
4. Service Response APIs (CRUD operations)
5. Match/Accept APIs
6. Statistics APIs

Test execution: pytest tests/test_comprehensive_api.py -v
"""

import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta


# ============================================================================
# 1. AUTHENTICATION TESTS (Priority: HIGH)
# ============================================================================

@pytest.mark.asyncio
class TestAuthentication:
    """Test authentication endpoints"""

    async def test_1_1_successful_registration(self, client: AsyncClient, setup_test_data):
        """Test Case 1.1: Successful user registration"""
        payload = {
            "uname": "testuser001",
            "bname": "Test User",
            "bpwd": "Test123",
            "phoneNo": "13800138001",
            "ctype": "ID Card",
            "idno": "110101199001011234"
        }

        response = await client.post("/api/v1/auth/register", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 200
        assert "data" in data
        assert "user_id" in data["data"]
        print(f"✓ Test 1.1 PASSED: User registered with ID {data['data']['user_id']}")

    async def test_1_2_invalid_password_too_short(self, client: AsyncClient, setup_test_data):
        """Test Case 1.2: Invalid password - too short"""
        payload = {
            "uname": "testuser002",
            "bname": "Test User",
            "bpwd": "12345",  # Only 5 characters
            "phoneNo": "13800138002",
            "ctype": "ID Card",
            "idno": "110101199001011235"
        }

        response = await client.post("/api/v1/auth/register", json=payload)

        assert response.status_code == 422
        print(f"✓ Test 1.2 PASSED: Password validation rejected short password")

    async def test_1_3_invalid_password_no_digits(self, client: AsyncClient, setup_test_data):
        """Test Case 1.3: Invalid password - no digits"""
        payload = {
            "uname": "testuser003",
            "bname": "Test User",
            "bpwd": "TestTest",  # No digits
            "phoneNo": "13800138003",
            "ctype": "ID Card",
            "idno": "110101199001011236"
        }

        response = await client.post("/api/v1/auth/register", json=payload)

        assert response.status_code == 422
        print(f"✓ Test 1.3 PASSED: Password validation rejected password without digits")

    async def test_1_4_duplicate_username(self, client: AsyncClient, setup_test_data):
        """Test Case 1.4: Duplicate username registration"""
        payload = {
            "uname": "duplicate_user",
            "bname": "Test User",
            "bpwd": "Test123",
            "phoneNo": "13800138004",
            "ctype": "ID Card",
            "idno": "110101199001011237"
        }

        # First registration
        response1 = await client.post("/api/v1/auth/register", json=payload)
        assert response1.status_code == 201

        # Second registration with same username (different phone/idno)
        payload["phoneNo"] = "13800138005"
        payload["idno"] = "110101199001011238"
        response2 = await client.post("/api/v1/auth/register", json=payload)

        assert response2.status_code == 400
        print(f"✓ Test 1.4 PASSED: Duplicate username rejected")

    async def test_2_1_successful_login(self, client: AsyncClient, setup_test_data):
        """Test Case 2.1: Successful login"""
        # Register first
        register_payload = {
            "uname": "loginuser",
            "bname": "Login User",
            "bpwd": "Login123",
            "phoneNo": "13800138010",
            "ctype": "ID Card",
            "idno": "110101199001011240"
        }
        await client.post("/api/v1/auth/register", json=register_payload)

        # Now login
        login_payload = {
            "username": "loginuser",
            "password": "Login123"
        }
        response = await client.post("/api/v1/auth/login", json=login_payload)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "token" in data["data"]
        assert "user_info" in data["data"]
        assert data["data"]["user_info"]["uname"] == "loginuser"
        print(f"✓ Test 2.1 PASSED: Login successful, token received")

    async def test_2_2_login_wrong_password(self, client: AsyncClient, setup_test_data):
        """Test Case 2.2: Login with wrong password"""
        # Register first
        register_payload = {
            "uname": "wrongpwduser",
            "bname": "Wrong Pwd User",
            "bpwd": "Correct123",
            "phoneNo": "13800138011",
            "ctype": "ID Card",
            "idno": "110101199001011241"
        }
        await client.post("/api/v1/auth/register", json=register_payload)

        # Login with wrong password
        login_payload = {
            "username": "wrongpwduser",
            "password": "Wrong123"
        }
        response = await client.post("/api/v1/auth/login", json=login_payload)

        assert response.status_code == 401
        print(f"✓ Test 2.2 PASSED: Wrong password rejected")

    async def test_2_3_login_nonexistent_user(self, client: AsyncClient, setup_test_data):
        """Test Case 2.3: Login with non-existent user"""
        login_payload = {
            "username": "nonexistentuser",
            "password": "Test123"
        }
        response = await client.post("/api/v1/auth/login", json=login_payload)

        assert response.status_code == 401
        print(f"✓ Test 2.3 PASSED: Non-existent user rejected")


# ============================================================================
# 2. USER PROFILE TESTS (Priority: MEDIUM)
# ============================================================================

@pytest.mark.asyncio
class TestUserProfile:
    """Test user profile endpoints"""

    async def test_3_1_get_current_user_info(self, client: AsyncClient,
                                             authenticated_user, auth_headers):
        """Test Case 3.1: Get current user info"""
        response = await client.get("/api/v1/users/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "data" in data
        assert data["data"]["uname"] == authenticated_user["user_info"]["uname"]
        print(f"✓ Test 3.1 PASSED: User info retrieved successfully")

    async def test_3_2_unauthorized_access(self, client: AsyncClient, setup_test_data):
        """Test Case 3.2: Access without authentication"""
        response = await client.get("/api/v1/users/me")

        assert response.status_code == 403  # HTTPBearer returns 403 for missing credentials
        print(f"✓ Test 3.2 PASSED: Unauthorized access rejected")

    async def test_3_3_invalid_token(self, client: AsyncClient, setup_test_data):
        """Test Case 3.3: Access with invalid token"""
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = await client.get("/api/v1/users/me", headers=headers)

        assert response.status_code == 401
        print(f"✓ Test 3.3 PASSED: Invalid token rejected")

    async def test_4_1_update_user_profile(self, client: AsyncClient,
                                          authenticated_user, auth_headers):
        """Test Case 4.1: Update user profile"""
        update_payload = {
            "desc": "Updated user description"
        }
        response = await client.put("/api/v1/users/me",
                                    json=update_payload,
                                    headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["desc"] == "Updated user description"
        print(f"✓ Test 4.1 PASSED: Profile updated successfully")

    async def test_5_1_change_password(self, client: AsyncClient, setup_test_data):
        """Test Case 5.1: Change password successfully"""
        # Register user
        register_payload = {
            "uname": "changepwduser",
            "bname": "Change Pwd User",
            "bpwd": "OldPass123",
            "phoneNo": "13800138020",
            "ctype": "ID Card",
            "idno": "110101199001011250"
        }
        await client.post("/api/v1/auth/register", json=register_payload)

        # Login
        login_response = await client.post("/api/v1/auth/login", json={
            "username": "changepwduser",
            "password": "OldPass123"
        })
        token = login_response.json()["data"]["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Change password
        change_pwd_payload = {
            "old_password": "OldPass123",
            "new_password": "NewPass456"
        }
        response = await client.put("/api/v1/users/me/password",
                                    json=change_pwd_payload,
                                    headers=headers)

        assert response.status_code == 200

        # Verify old password doesn't work
        old_login = await client.post("/api/v1/auth/login", json={
            "username": "changepwduser",
            "password": "OldPass123"
        })
        assert old_login.status_code == 401

        # Verify new password works
        new_login = await client.post("/api/v1/auth/login", json={
            "username": "changepwduser",
            "password": "NewPass456"
        })
        assert new_login.status_code == 200
        print(f"✓ Test 5.1 PASSED: Password changed successfully")

    async def test_5_2_wrong_old_password(self, client: AsyncClient,
                                         authenticated_user, auth_headers):
        """Test Case 5.2: Change password with wrong old password"""
        change_pwd_payload = {
            "old_password": "WrongOldPass123",
            "new_password": "NewPass456"
        }
        response = await client.put("/api/v1/users/me/password",
                                    json=change_pwd_payload,
                                    headers=auth_headers)

        assert response.status_code == 400
        print(f"✓ Test 5.2 PASSED: Wrong old password rejected")


# ============================================================================
# 3. SERVICE REQUEST TESTS (Priority: HIGH)
# ============================================================================

@pytest.mark.asyncio
class TestServiceRequests:
    """Test service request CRUD operations"""

    async def test_6_1_create_service_request(self, client: AsyncClient,
                                              authenticated_user, auth_headers,
                                              setup_test_data):
        """Test Case 6.1: Create service request successfully"""
        payload = {
            "ps_title": "Need plumbing service",
            "ps_desc": "Kitchen sink is leaking",
            "ps_address": "123 Test Street, Beijing",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }

        response = await client.post("/api/v1/service-requests",
                                    json=payload,
                                    headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 200
        assert "id" in data["data"]
        print(f"✓ Test 6.1 PASSED: Service request created with ID {data['data']['id']}")

    async def test_6_2_missing_required_fields(self, client: AsyncClient,
                                               authenticated_user, auth_headers,
                                               setup_test_data):
        """Test Case 6.2: Create request with missing required fields"""
        payload = {
            "ps_title": "Incomplete request",
            # Missing stype_id, cityID, dates, etc.
        }

        response = await client.post("/api/v1/service-requests",
                                    json=payload,
                                    headers=auth_headers)

        assert response.status_code == 422
        print(f"✓ Test 6.2 PASSED: Missing required fields rejected")

    async def test_7_1_list_service_requests(self, client: AsyncClient,
                                            authenticated_user, auth_headers,
                                            setup_test_data):
        """Test Case 7.1: List all service requests with pagination"""
        # Create a few requests first
        for i in range(3):
            payload = {
                "ps_title": f"Service request {i+1}",
                "ps_desc": f"Content {i+1}",
                "ps_address": f"Address {i+1}",
                "cityID": 1,
                "stype_id": 1,
                "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
                "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
            }
            await client.post("/api/v1/service-requests", json=payload, headers=auth_headers)

        # List requests
        response = await client.get("/api/v1/service-requests?page=1&size=10",
                                   headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert len(data["data"]["items"]) >= 3
        print(f"✓ Test 7.1 PASSED: Listed {len(data['data']['items'])} service requests")

    async def test_7_2_filter_by_service_type(self, client: AsyncClient,
                                              authenticated_user, auth_headers,
                                              setup_test_data):
        """Test Case 7.2: Filter service requests by type"""
        # Create requests with different types
        for stype_id in [1, 2]:
            payload = {
                "ps_title": f"Type {stype_id} request",
                "ps_desc": "Content",
                "ps_address": "Address",
                "cityID": 1,
                "stype_id": stype_id,
                "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
                "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
            }
            await client.post("/api/v1/service-requests", json=payload, headers=auth_headers)

        # Filter by type 1
        response = await client.get("/api/v1/service-requests?stype_id=1",
                                   headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        # All items should have stype_id = 1
        for item in data["data"]["items"]:
            assert item["stype_id"] == 1
        print(f"✓ Test 7.2 PASSED: Service type filter working")

    async def test_8_1_list_my_requests(self, client: AsyncClient,
                                       authenticated_user, auth_headers,
                                       authenticated_user_2, auth_headers_2,
                                       setup_test_data):
        """Test Case 8.1: List only my service requests"""
        # User 1 creates a request
        payload1 = {
            "ps_title": "User 1 request",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        await client.post("/api/v1/service-requests", json=payload1, headers=auth_headers)

        # User 2 creates a request
        payload2 = {
            "ps_title": "User 2 request",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        await client.post("/api/v1/service-requests", json=payload2, headers=auth_headers_2)

        # User 1 gets their requests
        response = await client.get("/api/v1/service-requests/my",
                                   headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        # All items should belong to user 1
        for item in data["data"]["items"]:
            assert item["psr_userid"] == authenticated_user["user_info"]["id"]
        print(f"✓ Test 8.1 PASSED: User can see only their own requests")

    async def test_9_1_get_single_request(self, client: AsyncClient,
                                         authenticated_user, auth_headers,
                                         setup_test_data):
        """Test Case 9.1: Get single service request details"""
        # Create a request
        payload = {
            "ps_title": "Single request",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        create_response = await client.post("/api/v1/service-requests",
                                           json=payload,
                                           headers=auth_headers)
        request_id = create_response.json()["data"]["id"]

        # Get the request
        response = await client.get(f"/api/v1/service-requests/{request_id}",
                                   headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == request_id
        assert data["data"]["ps_title"] == "Single request"
        print(f"✓ Test 9.1 PASSED: Single request retrieved successfully")

    async def test_9_2_nonexistent_request(self, client: AsyncClient,
                                          authenticated_user, auth_headers):
        """Test Case 9.2: Get non-existent request"""
        response = await client.get("/api/v1/service-requests/99999",
                                   headers=auth_headers)

        assert response.status_code == 404
        print(f"✓ Test 9.2 PASSED: Non-existent request returns 404")

    async def test_10_1_update_own_request(self, client: AsyncClient,
                                          authenticated_user, auth_headers,
                                          setup_test_data):
        """Test Case 10.1: Update own service request"""
        # Create request
        payload = {
            "ps_title": "Original title",
            "ps_desc": "Original content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        create_response = await client.post("/api/v1/service-requests",
                                           json=payload,
                                           headers=auth_headers)
        request_id = create_response.json()["data"]["id"]

        # Update request
        update_payload = {
            "ps_title": "Updated title",
            "ps_desc": "Updated content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        response = await client.put(f"/api/v1/service-requests/{request_id}",
                                    json=update_payload,
                                    headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["ps_title"] == "Updated title"
        assert data["data"]["ps_desc"] == "Updated content"
        print(f"✓ Test 10.1 PASSED: Request updated successfully")

    async def test_10_2_update_others_request(self, client: AsyncClient,
                                              authenticated_user, auth_headers,
                                              authenticated_user_2, auth_headers_2,
                                              setup_test_data):
        """Test Case 10.2: Try to update another user's request"""
        # User 1 creates request
        payload = {
            "ps_title": "User 1 request",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        create_response = await client.post("/api/v1/service-requests",
                                           json=payload,
                                           headers=auth_headers)
        request_id = create_response.json()["data"]["id"]

        # User 2 tries to update it
        update_payload = {
            "ps_title": "Hacked title",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        response = await client.put(f"/api/v1/service-requests/{request_id}",
                                    json=update_payload,
                                    headers=auth_headers_2)

        assert response.status_code == 403
        print(f"✓ Test 10.2 PASSED: Cannot update other user's request")

    async def test_11_1_cancel_own_request(self, client: AsyncClient,
                                          authenticated_user, auth_headers,
                                          setup_test_data):
        """Test Case 11.1: Cancel own service request"""
        # Create request
        payload = {
            "ps_title": "To be cancelled",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        create_response = await client.post("/api/v1/service-requests",
                                           json=payload,
                                           headers=auth_headers)
        request_id = create_response.json()["data"]["id"]

        # Cancel request
        response = await client.put(f"/api/v1/service-requests/{request_id}/cancel",
                                   headers=auth_headers)

        assert response.status_code == 200

        # Verify it's cancelled
        get_response = await client.get(f"/api/v1/service-requests/{request_id}",
                                       headers=auth_headers)
        assert get_response.json()["data"]["ps_state"] == -1
        print(f"✓ Test 11.1 PASSED: Request cancelled successfully")

    async def test_12_1_delete_own_request(self, client: AsyncClient,
                                          authenticated_user, auth_headers,
                                          setup_test_data):
        """Test Case 12.1: Delete own service request"""
        # Create request
        payload = {
            "ps_title": "To be deleted",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        create_response = await client.post("/api/v1/service-requests",
                                           json=payload,
                                           headers=auth_headers)
        request_id = create_response.json()["data"]["id"]

        # Delete request
        response = await client.delete(f"/api/v1/service-requests/{request_id}",
                                      headers=auth_headers)

        assert response.status_code in [200, 204]

        # Verify it's deleted or cancelled
        get_response = await client.get(f"/api/v1/service-requests/{request_id}",
                                       headers=auth_headers)
        # Should be 404 (deleted) or ps_state = -1 (cancelled)
        assert get_response.status_code == 404 or get_response.json()["data"]["ps_state"] == -1
        print(f"✓ Test 12.1 PASSED: Request deleted successfully")


# ============================================================================
# 4. SERVICE RESPONSE TESTS (Priority: HIGH)
# ============================================================================

@pytest.mark.asyncio
class TestServiceResponses:
    """Test service response CRUD operations"""

    async def test_13_1_respond_to_request(self, client: AsyncClient,
                                          authenticated_user, auth_headers,
                                          authenticated_user_2, auth_headers_2,
                                          setup_test_data):
        """Test Case 13.1: Respond to a service request"""
        # User 1 creates a request
        request_payload = {
            "ps_title": "Need help",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        create_response = await client.post("/api/v1/service-requests",
                                           json=request_payload,
                                           headers=auth_headers)
        request_id = create_response.json()["data"]["id"]

        # User 2 responds to it
        response_payload = {
            "srid": request_id,
            "response_desc": "I can help with this",
            "file_list": None
        }
        response = await client.post("/api/v1/service-responses",
                                    json=response_payload,
                                    headers=auth_headers_2)

        assert response.status_code == 201
        data = response.json()
        assert "id" in data["data"]
        print(f"✓ Test 13.1 PASSED: Response created with ID {data['data']['id']}")

    async def test_14_1_list_my_responses(self, client: AsyncClient,
                                         authenticated_user, auth_headers,
                                         authenticated_user_2, auth_headers_2,
                                         setup_test_data):
        """Test Case 14.1: List my service responses"""
        # User 1 creates request
        request_payload = {
            "ps_title": "Need help",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        create_response = await client.post("/api/v1/service-requests",
                                           json=request_payload,
                                           headers=auth_headers)
        request_id = create_response.json()["data"]["id"]

        # User 2 responds
        response_payload = {
            "srid": request_id,
            "response_desc": "My response",
            "file_list": None
        }
        await client.post("/api/v1/service-responses",
                         json=response_payload,
                         headers=auth_headers_2)

        # User 2 gets their responses
        response = await client.get("/api/v1/service-responses/my",
                                   headers=auth_headers_2)

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) > 0
        assert data["data"]["items"][0]["response_userid"] == authenticated_user_2["user_info"]["id"]
        print(f"✓ Test 14.1 PASSED: Listed my responses")

    async def test_15_1_cancel_my_response(self, client: AsyncClient,
                                          authenticated_user, auth_headers,
                                          authenticated_user_2, auth_headers_2,
                                          setup_test_data):
        """Test Case 15.1: Cancel my service response"""
        # User 1 creates request
        request_payload = {
            "ps_title": "Need help",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        create_response = await client.post("/api/v1/service-requests",
                                           json=request_payload,
                                           headers=auth_headers)
        request_id = create_response.json()["data"]["id"]

        # User 2 responds
        response_payload = {
            "srid": request_id,
            "response_desc": "To be cancelled",
            "file_list": None
        }
        response = await client.post("/api/v1/service-responses",
                                    json=response_payload,
                                    headers=auth_headers_2)
        response_id = response.json()["data"]["id"]

        # User 2 cancels their response
        cancel_response = await client.put(f"/api/v1/service-responses/{response_id}/cancel",
                                          headers=auth_headers_2)

        assert cancel_response.status_code == 200

        # Verify it's cancelled (response_state = 3)
        get_response = await client.get(f"/api/v1/service-responses/{response_id}",
                                       headers=auth_headers_2)
        assert get_response.json()["data"]["response_state"] == 3
        print(f"✓ Test 15.1 PASSED: Response cancelled successfully")


# ============================================================================
# 5. MATCH/ACCEPT TESTS (Priority: MEDIUM)
# ============================================================================

@pytest.mark.asyncio
class TestServiceMatching:
    """Test service matching/acceptance"""

    async def test_16_1_accept_response(self, client: AsyncClient,
                                       authenticated_user, auth_headers,
                                       authenticated_user_2, auth_headers_2,
                                       setup_test_data):
        """Test Case 16.1: Accept a service response"""
        # User 1 creates request
        request_payload = {
            "ps_title": "Need help",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        create_response = await client.post("/api/v1/service-requests",
                                           json=request_payload,
                                           headers=auth_headers)
        request_id = create_response.json()["data"]["id"]

        # User 2 responds
        response_payload = {
            "srid": request_id,
            "response_desc": "I can help",
            "file_list": None
        }
        response = await client.post("/api/v1/service-responses",
                                    json=response_payload,
                                    headers=auth_headers_2)
        response_id = response.json()["data"]["id"]

        # User 1 accepts the response
        accept_response = await client.post(f"/api/v1/match/accept/{response_id}",
                                          headers=auth_headers)

        assert accept_response.status_code in [200, 201]
        print(f"✓ Test 16.1 PASSED: Response accepted successfully")

    async def test_16_2_non_owner_accept(self, client: AsyncClient,
                                        authenticated_user, auth_headers,
                                        authenticated_user_2, auth_headers_2,
                                        authenticated_user_3, auth_headers_3,
                                        setup_test_data):
        """Test Case 16.2: Non-request-owner tries to accept"""
        # User 1 creates request
        request_payload = {
            "ps_title": "Need help",
            "ps_desc": "Content",
            "ps_address": "Address",
            "cityID": 1,
            "stype_id": 1,
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "ps_enddate": (datetime.utcnow() + timedelta(days=2)).isoformat()
        }
        create_response = await client.post("/api/v1/service-requests",
                                           json=request_payload,
                                           headers=auth_headers)
        request_id = create_response.json()["data"]["id"]

        # User 2 responds
        response_payload = {
            "srid": request_id,
            "response_desc": "I can help",
            "file_list": None
        }
        response = await client.post("/api/v1/service-responses",
                                    json=response_payload,
                                    headers=auth_headers_2)
        response_id = response.json()["data"]["id"]

        # User 3 (not the request owner) tries to accept
        accept_response = await client.post(f"/api/v1/match/accept/{response_id}",
                                          headers=auth_headers_3)

        assert accept_response.status_code == 403
        print(f"✓ Test 16.2 PASSED: Non-owner cannot accept response")


# ============================================================================
# 6. STATISTICS TESTS (Priority: LOW)
# ============================================================================

@pytest.mark.asyncio
class TestStatistics:
    """Test statistics endpoints"""

    async def test_17_1_monthly_statistics(self, client: AsyncClient,
                                          authenticated_user, auth_headers,
                                          setup_test_data):
        """Test Case 17.1: Get monthly statistics"""
        response = await client.get("/api/v1/stats/monthly?start_month=2025-01&end_month=2025-03",
                                   headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "chart_data" in data["data"]
        assert "items" in data["data"]
        print(f"✓ Test 17.1 PASSED: Statistics retrieved successfully")

    async def test_17_2_statistics_with_filters(self, client: AsyncClient,
                                               authenticated_user, auth_headers,
                                               setup_test_data):
        """Test Case 17.2: Statistics with city and service type filters"""
        response = await client.get(
            "/api/v1/stats/monthly?start_month=2025-01&end_month=2025-03&city_id=1&service_type_id=1",
            headers=auth_headers
        )

        assert response.status_code == 200
        print(f"✓ Test 17.2 PASSED: Filtered statistics working")

    async def test_17_3_statistics_pagination(self, client: AsyncClient,
                                             authenticated_user, auth_headers,
                                             setup_test_data):
        """Test Case 17.3: Statistics with pagination"""
        response = await client.get(
            "/api/v1/stats/monthly?start_month=2025-01&end_month=2025-12&page=1&size=5",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["page"] == 1
        assert data["data"]["size"] == 5
        print(f"✓ Test 17.3 PASSED: Statistics pagination working")

    async def test_17_4_statistics_without_auth(self, client: AsyncClient, setup_test_data):
        """Test Case 17.4: Statistics without authentication"""
        response = await client.get(
            "/api/v1/stats/monthly?start_month=2025-01&end_month=2025-03"
        )

        assert response.status_code == 403  # HTTPBearer returns 403 for missing credentials
        print(f"✓ Test 17.4 PASSED: Unauthorized access to statistics rejected")
