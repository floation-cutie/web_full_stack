import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta


@pytest.mark.asyncio
class TestStatistics:
    """Test statistics API endpoints"""

    async def test_monthly_statistics_basic(self, client: AsyncClient,
                                            auth_headers, setup_test_data):
        """Test basic monthly statistics query"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-03"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "chart_data" in data["data"]
        assert "items" in data["data"]
        assert "total" in data["data"]

        # Verify chart data structure
        chart_data = data["data"]["chart_data"]
        assert "months" in chart_data
        assert "published" in chart_data
        assert "completed" in chart_data
        assert len(chart_data["months"]) == len(chart_data["published"])
        assert len(chart_data["months"]) == len(chart_data["completed"])

    async def test_monthly_statistics_without_auth(self, client: AsyncClient, setup_test_data):
        """Test statistics access without authentication"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-03"
            }
        )

        assert response.status_code == 403

    async def test_monthly_statistics_with_invalid_token(self, client: AsyncClient, setup_test_data):
        """Test statistics with invalid token"""
        invalid_headers = {"Authorization": "Bearer invalid_token"}

        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-03"
            },
            headers=invalid_headers
        )

        assert response.status_code == 401

    async def test_monthly_statistics_missing_start_month(self, client: AsyncClient,
                                                          auth_headers, setup_test_data):
        """Test statistics without start month"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "end_month": "2025-03"
            },
            headers=auth_headers
        )

        assert response.status_code == 422

    async def test_monthly_statistics_missing_end_month(self, client: AsyncClient,
                                                        auth_headers, setup_test_data):
        """Test statistics without end month"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01"
            },
            headers=auth_headers
        )

        assert response.status_code == 422

    async def test_monthly_statistics_invalid_date_format(self, client: AsyncClient,
                                                          auth_headers, setup_test_data):
        """Test statistics with invalid date format"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025/01",  # Wrong format
                "end_month": "2025-03"
            },
            headers=auth_headers
        )

        # May fail during parsing
        assert response.status_code in [400, 422]

    async def test_monthly_statistics_single_month(self, client: AsyncClient,
                                                    auth_headers, setup_test_data):
        """Test statistics for single month"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-01"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["chart_data"]["months"]) == 1

    async def test_monthly_statistics_full_year(self, client: AsyncClient,
                                                auth_headers, setup_test_data):
        """Test statistics for full year"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-12"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["chart_data"]["months"]) == 12

    async def test_monthly_statistics_with_city_filter(self, client: AsyncClient,
                                                       auth_headers, setup_test_data):
        """Test statistics with city filter"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-03",
                "city_id": 1
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200

    async def test_monthly_statistics_with_service_type_filter(self, client: AsyncClient,
                                                               auth_headers, setup_test_data):
        """Test statistics with service type filter"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-03",
                "service_type_id": 1
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200

    async def test_monthly_statistics_with_both_filters(self, client: AsyncClient,
                                                        auth_headers, setup_test_data):
        """Test statistics with both city and service type filters"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-03",
                "city_id": 1,
                "service_type_id": 1
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200

    async def test_monthly_statistics_pagination(self, client: AsyncClient,
                                                 auth_headers, setup_test_data):
        """Test statistics table pagination"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-12",
                "page": 1,
                "size": 5
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["page"] == 1
        assert data["data"]["size"] == 5
        assert "items" in data["data"]

    async def test_monthly_statistics_pagination_second_page(self, client: AsyncClient,
                                                             auth_headers, setup_test_data):
        """Test pagination on second page"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-12",
                "page": 2,
                "size": 5
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["page"] == 2

    async def test_monthly_statistics_invalid_page(self, client: AsyncClient,
                                                   auth_headers, setup_test_data):
        """Test pagination with invalid page number"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-03",
                "page": 0
            },
            headers=auth_headers
        )

        assert response.status_code == 422

    async def test_monthly_statistics_invalid_size(self, client: AsyncClient,
                                                   auth_headers, setup_test_data):
        """Test pagination with invalid size"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-03",
                "size": 200
            },
            headers=auth_headers
        )

        assert response.status_code == 422

    async def test_statistics_data_structure(self, client: AsyncClient,
                                             authenticated_user, auth_headers,
                                             service_request_data, setup_test_data):
        """Test statistics response data structure"""
        # Create a request to have some data
        await client.post(
            "/api/v1/service-requests",
            json=service_request_data,
            headers=auth_headers
        )

        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-12"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "code" in data
        assert data["code"] == 200
        assert "data" in data

        stats_data = data["data"]
        assert "chart_data" in stats_data
        assert "items" in stats_data
        assert "total" in stats_data
        assert "page" in stats_data
        assert "size" in stats_data

        # Check chart data
        chart = stats_data["chart_data"]
        assert isinstance(chart["months"], list)
        assert isinstance(chart["published"], list)
        assert isinstance(chart["completed"], list)

        # Check items
        for item in stats_data["items"]:
            assert "month" in item
            assert "publishedCount" in item
            assert "completedCount" in item

    async def test_statistics_with_published_and_completed_data(self, client: AsyncClient,
                                                                 authenticated_user,
                                                                 authenticated_user_2,
                                                                 auth_headers, auth_headers_2,
                                                                 service_request_data,
                                                                 service_response_data,
                                                                 setup_test_data):
        """Test statistics includes both published and completed counts"""
        # User 1 publishes a request
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

        # User 1 accepts (completes)
        await client.post(
            f"/api/v1/match/accept/{response_id}",
            headers=auth_headers
        )

        # Get statistics
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-12"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Both published and completed should have counts
        chart = data["data"]["chart_data"]
        assert sum(chart["published"]) > 0
        assert sum(chart["completed"]) > 0

    async def test_statistics_months_in_correct_order(self, client: AsyncClient,
                                                      auth_headers, setup_test_data):
        """Test that months in statistics are in correct chronological order"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2025-01",
                "end_month": "2025-12"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        months = data["data"]["chart_data"]["months"]
        expected = [f"2025-{str(i).zfill(2)}" for i in range(1, 13)]
        assert months == expected

    async def test_statistics_across_year_boundary(self, client: AsyncClient,
                                                   auth_headers, setup_test_data):
        """Test statistics spanning multiple years"""
        response = await client.get(
            "/api/v1/stats/monthly",
            params={
                "start_month": "2024-11",
                "end_month": "2025-02"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        months = data["data"]["chart_data"]["months"]
        assert "2024-11" in months
        assert "2024-12" in months
        assert "2025-01" in months
        assert "2025-02" in months
