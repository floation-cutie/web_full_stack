import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta


@pytest.mark.asyncio
class TestServiceRequests:
    """Test service request CRUD operations"""

    async def test_create_service_request_success(self, client: AsyncClient,
                                                  authenticated_user, auth_headers,
                                                  service_request_data, setup_test_data):
        """Test successful service request creation"""
        response = await client.post(
            "/api/v1/service-requests",
            json=service_request_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "Service request created successfully"
        assert "sr_id" in data["data"]

    async def test_create_request_without_auth(self, client: AsyncClient,
                                               service_request_data, setup_test_data):
        """Test creating request without authentication"""
        response = await client.post(
            "/api/v1/service-requests",
            json=service_request_data
        )

        assert response.status_code == 403  # No credentials

    async def test_create_request_with_invalid_token(self, client: AsyncClient,
                                                     service_request_data, setup_test_data):
        """Test creating request with invalid token"""
        invalid_headers = {"Authorization": "Bearer invalid_token"}

        response = await client.post(
            "/api/v1/service-requests",
            json=service_request_data,
            headers=invalid_headers
        )

        assert response.status_code == 401

    async def test_create_request_missing_required_fields(self, client: AsyncClient,
                                                          auth_headers, setup_test_data):
        """Test creating request with missing required fields"""
        incomplete_data = {
            "sr_title": "Test",
            # Missing ps_begindate, desc, stype_id, cityID
        }

        response = await client.post(
            "/api/v1/service-requests",
            json=incomplete_data,
            headers=auth_headers
        )

        assert response.status_code == 422

    async def test_create_request_invalid_city(self, client: AsyncClient,
                                               auth_headers, service_request_data,
                                               setup_test_data):
        """Test creating request with invalid city ID"""
        invalid_data = {**service_request_data, "cityID": 999}

        response = await client.post(
            "/api/v1/service-requests",
            json=invalid_data,
            headers=auth_headers
        )

        assert response.status_code in [400, 422]

    async def test_create_request_invalid_service_type(self, client: AsyncClient,
                                                       auth_headers, service_request_data,
                                                       setup_test_data):
        """Test creating request with invalid service type"""
        invalid_data = {**service_request_data, "stype_id": 999}

        response = await client.post(
            "/api/v1/service-requests",
            json=invalid_data,
            headers=auth_headers
        )

        assert response.status_code in [400, 422]

    async def test_get_all_service_requests(self, client: AsyncClient,
                                            authenticated_user, auth_headers,
                                            service_request_data, setup_test_data):
        """Test retrieving all service requests"""
        # Create multiple requests
        await client.post("/api/v1/service-requests", json=service_request_data, headers=auth_headers)
        await client.post("/api/v1/service-requests", json=service_request_data, headers=auth_headers)

        response = await client.get(
            "/api/v1/service-requests",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "items" in data["data"]
        assert len(data["data"]["items"]) >= 2

    async def test_get_service_requests_pagination(self, client: AsyncClient,
                                                   auth_headers, service_request_data,
                                                   setup_test_data):
        """Test pagination of service requests"""
        # Create 5 requests
        for i in range(5):
            data = {
                **service_request_data,
                "sr_title": f"Request {i}"
            }
            await client.post("/api/v1/service-requests", json=data, headers=auth_headers)

        # Test page 1, size 2
        response = await client.get(
            "/api/v1/service-requests?page=1&size=2",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 2
        assert data["data"]["total"] == 5
        assert data["data"]["page"] == 1
        assert data["data"]["size"] == 2

    async def test_get_service_requests_page_2(self, client: AsyncClient,
                                               auth_headers, service_request_data,
                                               setup_test_data):
        """Test pagination on second page"""
        # Create 5 requests
        for i in range(5):
            data = {
                **service_request_data,
                "sr_title": f"Request {i}"
            }
            await client.post("/api/v1/service-requests", json=data, headers=auth_headers)

        # Test page 2, size 2
        response = await client.get(
            "/api/v1/service-requests?page=2&size=2",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 2
        assert data["data"]["page"] == 2

    async def test_get_requests_by_user_filter(self, client: AsyncClient,
                                               authenticated_user, authenticated_user_2,
                                               auth_headers, auth_headers_2,
                                               service_request_data, setup_test_data):
        """Test filtering requests by user ID"""
        # User 1 creates a request
        await client.post("/api/v1/service-requests", json=service_request_data, headers=auth_headers)

        # User 2 creates a request
        await client.post("/api/v1/service-requests", json=service_request_data, headers=auth_headers_2)

        # Get requests for User 1
        response = await client.get(
            f"/api/v1/service-requests?user_id={authenticated_user['user_info']['id']}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["psr_userid"] == authenticated_user["user_info"]["id"]

    async def test_get_requests_by_service_type_filter(self, client: AsyncClient,
                                                       auth_headers, setup_test_data):
        """Test filtering requests by service type"""
        data1 = {
            "sr_title": "Plumbing",
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "desc": "Need plumbing",
            "stype_id": 1,
            "cityID": 1,
            "file_list": ""
        }

        data2 = {
            "sr_title": "Cleaning",
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "desc": "Need cleaning",
            "stype_id": 3,
            "cityID": 1,
            "file_list": ""
        }

        await client.post("/api/v1/service-requests", json=data1, headers=auth_headers)
        await client.post("/api/v1/service-requests", json=data2, headers=auth_headers)

        response = await client.get(
            "/api/v1/service-requests?stype_id=1",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(item["stype_id"] == 1 for item in data["data"]["items"])

    async def test_get_requests_by_city_filter(self, client: AsyncClient,
                                               auth_headers, service_request_data,
                                               setup_test_data):
        """Test filtering requests by city"""
        data1 = {**service_request_data, "cityID": 1}
        data2 = {**service_request_data, "cityID": 2}

        await client.post("/api/v1/service-requests", json=data1, headers=auth_headers)
        await client.post("/api/v1/service-requests", json=data2, headers=auth_headers)

        response = await client.get(
            "/api/v1/service-requests?city_id=1",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(item["cityID"] == 1 for item in data["data"]["items"])

    async def test_get_requests_by_state_filter(self, client: AsyncClient,
                                                auth_headers, created_service_request,
                                                setup_test_data):
        """Test filtering requests by state"""
        response = await client.get(
            "/api/v1/service-requests?ps_state=0",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(item["ps_state"] == 0 for item in data["data"]["items"])

    async def test_update_service_request(self, client: AsyncClient,
                                          auth_headers, service_request_data,
                                          created_service_request, setup_test_data):
        """Test updating a service request"""
        updated_data = {
            "sr_title": "Updated title",
            "desc": "Updated description"
        }

        response = await client.put(
            f"/api/v1/service-requests/{created_service_request}",
            json=updated_data,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "sr_id" in data["data"]

    async def test_update_request_by_different_user(self, client: AsyncClient,
                                                    auth_headers, auth_headers_2,
                                                    created_service_request,
                                                    service_request_data, setup_test_data):
        """Test that only the creator can update a request"""
        updated_data = {"sr_title": "Updated title"}

        response = await client.put(
            f"/api/v1/service-requests/{created_service_request}",
            json=updated_data,
            headers=auth_headers_2
        )

        assert response.status_code == 403

    async def test_update_nonexistent_request(self, client: AsyncClient,
                                              auth_headers, setup_test_data):
        """Test updating nonexistent request"""
        response = await client.put(
            "/api/v1/service-requests/99999",
            json={"sr_title": "Updated"},
            headers=auth_headers
        )

        assert response.status_code == 404

    async def test_delete_service_request(self, client: AsyncClient,
                                          auth_headers, created_service_request,
                                          setup_test_data):
        """Test deleting (cancelling) a service request"""
        response = await client.delete(
            f"/api/v1/service-requests/{created_service_request}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200

        # Verify it's cancelled (ps_state = -1)
        get_response = await client.get(
            f"/api/v1/service-requests?ps_state=-1",
            headers=auth_headers
        )
        assert any(item["sr_id"] == created_service_request for item in get_response.json()["data"]["items"])

    async def test_delete_request_by_different_user(self, client: AsyncClient,
                                                    auth_headers, auth_headers_2,
                                                    created_service_request, setup_test_data):
        """Test that only the creator can delete a request"""
        response = await client.delete(
            f"/api/v1/service-requests/{created_service_request}",
            headers=auth_headers_2
        )

        assert response.status_code == 403

    async def test_delete_nonexistent_request(self, client: AsyncClient,
                                              auth_headers, setup_test_data):
        """Test deleting nonexistent request"""
        response = await client.delete(
            "/api/v1/service-requests/99999",
            headers=auth_headers
        )

        assert response.status_code == 404

    async def test_create_request_with_optional_fields(self, client: AsyncClient,
                                                       auth_headers, setup_test_data):
        """Test creating request with optional description and files"""
        data = {
            "sr_title": "Test with files",
            "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "desc": "Full description here",
            "stype_id": 1,
            "cityID": 1,
            "file_list": "photo1.jpg,photo2.jpg"
        }

        response = await client.post(
            "/api/v1/service-requests",
            json=data,
            headers=auth_headers
        )

        assert response.status_code == 201

    async def test_create_request_with_past_date(self, client: AsyncClient,
                                                 auth_headers, setup_test_data):
        """Test creating request with dates in the past"""
        data = {
            "sr_title": "Past request",
            "ps_begindate": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "desc": "Test",
            "stype_id": 1,
            "cityID": 1,
            "file_list": ""
        }

        response = await client.post(
            "/api/v1/service-requests",
            json=data,
            headers=auth_headers
        )

        # Should allow past dates (validation is optional)
        assert response.status_code in [201, 422]

    async def test_pagination_invalid_page(self, client: AsyncClient,
                                           auth_headers, setup_test_data):
        """Test pagination with invalid page number"""
        response = await client.get(
            "/api/v1/service-requests?page=0",
            headers=auth_headers
        )

        assert response.status_code == 422

    async def test_pagination_invalid_size(self, client: AsyncClient,
                                           auth_headers, setup_test_data):
        """Test pagination with size exceeding maximum"""
        response = await client.get(
            "/api/v1/service-requests?size=200",
            headers=auth_headers
        )

        assert response.status_code == 422
