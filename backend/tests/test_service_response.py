import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestServiceResponses:
    """Test service response CRUD operations"""

    async def test_create_service_response_success(self, client: AsyncClient,
                                                   authenticated_user_2, auth_headers_2,
                                                   created_service_request,
                                                   service_response_data, setup_test_data):
        """Test successful service response creation"""
        response_data = {**service_response_data, "srid": created_service_request}

        response = await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )

        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "Service response created successfully"
        assert "id" in data["data"]

    async def test_create_response_without_auth(self, client: AsyncClient,
                                                created_service_request,
                                                service_response_data, setup_test_data):
        """Test creating response without authentication"""
        response_data = {**service_response_data, "srid": created_service_request}

        response = await client.post(
            "/api/v1/service-responses",
            json=response_data
        )

        assert response.status_code == 403

    async def test_create_response_with_invalid_token(self, client: AsyncClient,
                                                      created_service_request,
                                                      service_response_data, setup_test_data):
        """Test creating response with invalid token"""
        response_data = {**service_response_data, "srid": created_service_request}
        invalid_headers = {"Authorization": "Bearer invalid_token"}

        response = await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=invalid_headers
        )

        assert response.status_code == 401

    async def test_create_response_nonexistent_request(self, client: AsyncClient,
                                                       auth_headers_2,
                                                       service_response_data, setup_test_data):
        """Test creating response for nonexistent request"""
        response_data = {**service_response_data, "srid": 99999}

        response = await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )

        assert response.status_code in [400, 422]

    async def test_create_response_missing_request_id(self, client: AsyncClient,
                                                      auth_headers_2, setup_test_data):
        """Test creating response without request ID"""
        response_data = {
            "response_desc": "Test response"
            # Missing srid
        }

        response = await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )

        assert response.status_code == 422

    async def test_create_multiple_responses_for_same_request(self, client: AsyncClient,
                                                              auth_headers_2, auth_headers_3,
                                                              created_service_request,
                                                              service_response_data,
                                                              setup_test_data):
        """Test multiple providers responding to same request"""
        response_data_2 = {**service_response_data, "srid": created_service_request}
        response_data_3 = {
            "response_desc": "Third provider response",
            "srid": created_service_request
        }

        # Second user responds
        response2 = await client.post(
            "/api/v1/service-responses",
            json=response_data_2,
            headers=auth_headers_2
        )
        assert response2.status_code == 201

        # Third user responds
        response3 = await client.post(
            "/api/v1/service-responses",
            json=response_data_3,
            headers=auth_headers_3
        )
        assert response3.status_code == 201

    async def test_get_all_service_responses(self, client: AsyncClient,
                                             auth_headers_2,
                                             created_service_request,
                                             service_response_data, setup_test_data):
        """Test retrieving all service responses"""
        response_data = {**service_response_data, "srid": created_service_request}

        await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )

        response = await client.get(
            "/api/v1/service-responses",
            headers=auth_headers_2
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "items" in data["data"]
        assert len(data["data"]["items"]) >= 1

    async def test_get_responses_pagination(self, client: AsyncClient,
                                            auth_headers, auth_headers_2,
                                            created_service_request,
                                            service_response_data, setup_test_data):
        """Test pagination of service responses"""
        # Create 5 responses
        for i in range(5):
            response_data = {
                **service_response_data,
                "response_desc": f"Response {i}",
                "srid": created_service_request
            }
            await client.post(
                "/api/v1/service-responses",
                json=response_data,
                headers=auth_headers_2
            )

        response = await client.get(
            "/api/v1/service-responses?page=1&size=2",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 2
        assert data["data"]["total"] == 5
        assert data["data"]["page"] == 1

    async def test_get_responses_by_user_filter(self, client: AsyncClient,
                                                authenticated_user, authenticated_user_2,
                                                auth_headers, auth_headers_2,
                                                created_service_request,
                                                service_response_data, setup_test_data):
        """Test filtering responses by user ID"""
        response_data = {**service_response_data, "srid": created_service_request}

        await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )

        response = await client.get(
            f"/api/v1/service-responses?user_id={authenticated_user_2['user_info']['id']}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(item["response_userid"] == authenticated_user_2["user_info"]["id"]
                   for item in data["data"]["items"])

    async def test_get_responses_by_request_filter(self, client: AsyncClient,
                                                   auth_headers, auth_headers_2,
                                                   created_service_request,
                                                   service_response_data, setup_test_data):
        """Test filtering responses by request ID"""
        response_data = {**service_response_data, "srid": created_service_request}

        await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )

        response = await client.get(
            f"/api/v1/service-responses?srid={created_service_request}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(item["srid"] == created_service_request for item in data["data"]["items"])

    async def test_get_responses_by_state_filter(self, client: AsyncClient,
                                                 auth_headers, auth_headers_2,
                                                 created_service_request,
                                                 service_response_data, setup_test_data):
        """Test filtering responses by state"""
        response_data = {**service_response_data, "srid": created_service_request}

        await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )

        # Default state is 0 (pending)
        response = await client.get(
            "/api/v1/service-responses?response_state=0",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert all(item["response_state"] == 0 for item in data["data"]["items"])

    async def test_update_service_response(self, client: AsyncClient,
                                           auth_headers_2,
                                           created_service_response,
                                           setup_test_data):
        """Test updating a service response"""
        updated_data = {
            "response_desc": "Updated response description"
        }

        response = await client.put(
            f"/api/v1/service-responses/{created_service_response}",
            json=updated_data,
            headers=auth_headers_2
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200

    async def test_update_response_by_different_user(self, client: AsyncClient,
                                                     auth_headers, auth_headers_2,
                                                     created_service_response,
                                                     setup_test_data):
        """Test that only the creator can update a response"""
        updated_data = {"response_desc": "Updated"}

        response = await client.put(
            f"/api/v1/service-responses/{created_service_response}",
            json=updated_data,
            headers=auth_headers
        )

        assert response.status_code == 403

    async def test_update_nonexistent_response(self, client: AsyncClient,
                                               auth_headers_2, setup_test_data):
        """Test updating nonexistent response"""
        response = await client.put(
            "/api/v1/service-responses/99999",
            json={"response_desc": "Updated"},
            headers=auth_headers_2
        )

        assert response.status_code == 404

    async def test_delete_service_response(self, client: AsyncClient,
                                           auth_headers_2,
                                           created_service_response, setup_test_data):
        """Test deleting a service response"""
        response = await client.delete(
            f"/api/v1/service-responses/{created_service_response}",
            headers=auth_headers_2
        )

        assert response.status_code == 200

    async def test_delete_response_by_different_user(self, client: AsyncClient,
                                                     auth_headers, auth_headers_2,
                                                     created_service_response,
                                                     setup_test_data):
        """Test that only the creator can delete a response"""
        response = await client.delete(
            f"/api/v1/service-responses/{created_service_response}",
            headers=auth_headers
        )

        assert response.status_code == 403

    async def test_delete_nonexistent_response(self, client: AsyncClient,
                                               auth_headers_2, setup_test_data):
        """Test deleting nonexistent response"""
        response = await client.delete(
            "/api/v1/service-responses/99999",
            headers=auth_headers_2
        )

        assert response.status_code == 404

    async def test_create_response_with_file_list(self, client: AsyncClient,
                                                  auth_headers_2,
                                                  created_service_request,
                                                  setup_test_data):
        """Test creating response with file attachments"""
        response_data = {
            "response_desc": "Professional service with photos",
            "file_list": "photo1.jpg,photo2.jpg",
            "srid": created_service_request
        }

        response = await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )

        assert response.status_code == 201

    async def test_create_empty_response(self, client: AsyncClient,
                                         auth_headers_2,
                                         created_service_request, setup_test_data):
        """Test creating response with minimal data"""
        response_data = {
            "srid": created_service_request
        }

        response = await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )

        assert response.status_code == 201

    async def test_pagination_invalid_page(self, client: AsyncClient,
                                           auth_headers, setup_test_data):
        """Test pagination with invalid page number"""
        response = await client.get(
            "/api/v1/service-responses?page=0",
            headers=auth_headers
        )

        assert response.status_code == 422

    async def test_pagination_invalid_size(self, client: AsyncClient,
                                           auth_headers, setup_test_data):
        """Test pagination with size exceeding maximum"""
        response = await client.get(
            "/api/v1/service-responses?size=200",
            headers=auth_headers
        )

        assert response.status_code == 422

    async def test_response_state_tracking(self, client: AsyncClient,
                                           auth_headers, auth_headers_2,
                                           created_service_request,
                                           service_response_data, setup_test_data):
        """Test that response states are properly tracked"""
        response_data = {**service_response_data, "srid": created_service_request}

        create_response = await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )

        response_id = create_response.json()["data"]["id"]

        # Get the response and verify initial state
        get_response = await client.get(
            f"/api/v1/service-responses?srid={created_service_request}",
            headers=auth_headers
        )

        responses = get_response.json()["data"]["items"]
        assert any(r["id"] == response_id and r["response_state"] == 0 for r in responses)
