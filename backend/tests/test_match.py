import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestServiceMatching:
    """Test service matching (accept/reject) operations"""

    async def test_accept_service_response_success(self, client: AsyncClient,
                                                   authenticated_user, auth_headers,
                                                   created_service_response,
                                                   setup_test_data):
        """Test successful acceptance of service response"""
        response = await client.post(
            f"/api/v1/match/accept/{created_service_response}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "Service response accepted successfully"
        assert "accept_id" in data["data"]

    async def test_accept_without_auth(self, client: AsyncClient,
                                       created_service_response, setup_test_data):
        """Test accepting without authentication"""
        response = await client.post(
            f"/api/v1/match/accept/{created_service_response}"
        )

        assert response.status_code == 403

    async def test_accept_with_invalid_token(self, client: AsyncClient,
                                             created_service_response, setup_test_data):
        """Test accepting with invalid token"""
        invalid_headers = {"Authorization": "Bearer invalid_token"}

        response = await client.post(
            f"/api/v1/match/accept/{created_service_response}",
            headers=invalid_headers
        )

        assert response.status_code == 401

    async def test_accept_nonexistent_response(self, client: AsyncClient,
                                               auth_headers, setup_test_data):
        """Test accepting nonexistent response"""
        response = await client.post(
            "/api/v1/match/accept/99999",
            headers=auth_headers
        )

        assert response.status_code == 404

    async def test_accept_by_non_requester(self, client: AsyncClient,
                                           auth_headers_2,
                                           created_service_response, setup_test_data):
        """Test that only request creator can accept response"""
        response = await client.post(
            f"/api/v1/match/accept/{created_service_response}",
            headers=auth_headers_2
        )

        assert response.status_code == 403

    async def test_accept_already_accepted_response(self, client: AsyncClient,
                                                    auth_headers,
                                                    created_service_response,
                                                    setup_test_data):
        """Test accepting an already accepted response"""
        # First acceptance
        await client.post(
            f"/api/v1/match/accept/{created_service_response}",
            headers=auth_headers
        )

        # Second acceptance attempt
        response = await client.post(
            f"/api/v1/match/accept/{created_service_response}",
            headers=auth_headers
        )

        assert response.status_code == 400

    async def test_accept_rejected_response(self, client: AsyncClient,
                                            auth_headers,
                                            created_service_response,
                                            setup_test_data):
        """Test accepting a response that was already rejected"""
        # Reject response first
        await client.post(
            f"/api/v1/match/reject/{created_service_response}",
            headers=auth_headers
        )

        # Try to accept
        response = await client.post(
            f"/api/v1/match/accept/{created_service_response}",
            headers=auth_headers
        )

        assert response.status_code == 400

    async def test_reject_service_response_success(self, client: AsyncClient,
                                                   auth_headers,
                                                   created_service_response,
                                                   setup_test_data):
        """Test successful rejection of service response"""
        response = await client.post(
            f"/api/v1/match/reject/{created_service_response}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "Service response rejected successfully"

    async def test_reject_without_auth(self, client: AsyncClient,
                                       created_service_response, setup_test_data):
        """Test rejecting without authentication"""
        response = await client.post(
            f"/api/v1/match/reject/{created_service_response}"
        )

        assert response.status_code == 403

    async def test_reject_with_invalid_token(self, client: AsyncClient,
                                             created_service_response, setup_test_data):
        """Test rejecting with invalid token"""
        invalid_headers = {"Authorization": "Bearer invalid_token"}

        response = await client.post(
            f"/api/v1/match/reject/{created_service_response}",
            headers=invalid_headers
        )

        assert response.status_code == 401

    async def test_reject_nonexistent_response(self, client: AsyncClient,
                                               auth_headers, setup_test_data):
        """Test rejecting nonexistent response"""
        response = await client.post(
            "/api/v1/match/reject/99999",
            headers=auth_headers
        )

        assert response.status_code == 404

    async def test_reject_by_non_requester(self, client: AsyncClient,
                                           auth_headers_2,
                                           created_service_response, setup_test_data):
        """Test that only request creator can reject response"""
        response = await client.post(
            f"/api/v1/match/reject/{created_service_response}",
            headers=auth_headers_2
        )

        assert response.status_code == 403

    async def test_reject_already_rejected_response(self, client: AsyncClient,
                                                    auth_headers,
                                                    created_service_response,
                                                    setup_test_data):
        """Test rejecting an already rejected response"""
        # First rejection
        await client.post(
            f"/api/v1/match/reject/{created_service_response}",
            headers=auth_headers
        )

        # Second rejection attempt
        response = await client.post(
            f"/api/v1/match/reject/{created_service_response}",
            headers=auth_headers
        )

        assert response.status_code == 400

    async def test_complete_workflow_publish_respond_accept(self, client: AsyncClient,
                                                            authenticated_user,
                                                            authenticated_user_2,
                                                            auth_headers, auth_headers_2,
                                                            service_request_data,
                                                            service_response_data,
                                                            setup_test_data):
        """Test complete workflow: publish -> respond -> accept"""
        # User 1 publishes request
        create_req = await client.post(
            "/api/v1/service-requests",
            json=service_request_data,
            headers=auth_headers
        )
        request_id = create_req.json()["data"]["sr_id"]

        # User 2 responds
        response_data = {**service_response_data, "srid": request_id}
        create_res = await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )
        response_id = create_res.json()["data"]["id"]

        # User 1 accepts
        accept_res = await client.post(
            f"/api/v1/match/accept/{response_id}",
            headers=auth_headers
        )

        assert accept_res.status_code == 200

    async def test_complete_workflow_publish_respond_reject(self, client: AsyncClient,
                                                            authenticated_user,
                                                            authenticated_user_2,
                                                            auth_headers, auth_headers_2,
                                                            service_request_data,
                                                            service_response_data,
                                                            setup_test_data):
        """Test complete workflow: publish -> respond -> reject"""
        # User 1 publishes request
        create_req = await client.post(
            "/api/v1/service-requests",
            json=service_request_data,
            headers=auth_headers
        )
        request_id = create_req.json()["data"]["id"]

        # User 2 responds
        response_data = {**service_response_data, "srid": request_id}
        create_res = await client.post(
            "/api/v1/service-responses",
            json=response_data,
            headers=auth_headers_2
        )
        response_id = create_res.json()["data"]["id"]

        # User 1 rejects
        reject_res = await client.post(
            f"/api/v1/match/reject/{response_id}",
            headers=auth_headers
        )

        assert reject_res.status_code == 200

    async def test_accept_one_of_multiple_responses(self, client: AsyncClient,
                                                    authenticated_user,
                                                    authenticated_user_2,
                                                    authenticated_user_3,
                                                    auth_headers, auth_headers_2,
                                                    auth_headers_3,
                                                    service_request_data,
                                                    service_response_data,
                                                    setup_test_data):
        """Test accepting one response when multiple are available"""
        # User 1 publishes request
        create_req = await client.post(
            "/api/v1/service-requests",
            json=service_request_data,
            headers=auth_headers
        )
        request_id = create_req.json()["data"]["id"]

        # User 2 responds
        response_data_2 = {**service_response_data, "srid": request_id, "response_desc": "User 2 response"}
        create_res_2 = await client.post(
            "/api/v1/service-responses",
            json=response_data_2,
            headers=auth_headers_2
        )
        response_id_2 = create_res_2.json()["data"]["id"]

        # User 3 responds
        response_data_3 = {**service_response_data, "srid": request_id, "response_desc": "User 3 response"}
        create_res_3 = await client.post(
            "/api/v1/service-responses",
            json=response_data_3,
            headers=auth_headers_3
        )
        response_id_3 = create_res_3.json()["data"]["id"]

        # User 1 accepts User 2's response
        accept_res = await client.post(
            f"/api/v1/match/accept/{response_id_2}",
            headers=auth_headers
        )

        assert accept_res.status_code == 200

        # User 3's response cannot be accepted anymore
        reject_res = await client.post(
            f"/api/v1/match/accept/{response_id_3}",
            headers=auth_headers
        )

        assert reject_res.status_code == 400

    async def test_multiple_acceptances_on_different_requests(self, client: AsyncClient,
                                                              authenticated_user,
                                                              authenticated_user_2,
                                                              auth_headers, auth_headers_2,
                                                              service_request_data,
                                                              service_response_data,
                                                              setup_test_data):
        """Test user can accept responses on different requests"""
        # User 1 publishes two requests
        create_req_1 = await client.post(
            "/api/v1/service-requests",
            json=service_request_data,
            headers=auth_headers
        )
        request_id_1 = create_req_1.json()["data"]["sr_id"]

        req_data_2 = {**service_request_data, "sr_title": "Second request"}
        create_req_2 = await client.post(
            "/api/v1/service-requests",
            json=req_data_2,
            headers=auth_headers
        )
        request_id_2 = create_req_2.json()["data"]["sr_id"]

        # User 2 responds to both
        response_data_1 = {**service_response_data, "srid": request_id_1}
        create_res_1 = await client.post(
            "/api/v1/service-responses",
            json=response_data_1,
            headers=auth_headers_2
        )
        response_id_1 = create_res_1.json()["data"]["id"]

        response_data_2 = {**service_response_data, "srid": request_id_2}
        create_res_2 = await client.post(
            "/api/v1/service-responses",
            json=response_data_2,
            headers=auth_headers_2
        )
        response_id_2 = create_res_2.json()["data"]["id"]

        # User 1 accepts both
        accept_1 = await client.post(
            f"/api/v1/match/accept/{response_id_1}",
            headers=auth_headers
        )
        assert accept_1.status_code == 200

        accept_2 = await client.post(
            f"/api/v1/match/accept/{response_id_2}",
            headers=auth_headers
        )
        assert accept_2.status_code == 200
