# GoodServices API Test Suite

Comprehensive pytest test suite for GoodServices FastAPI backend with full coverage of all API endpoints.

## Test Files

### 1. conftest.py
Shared pytest configuration and fixtures including:
- Database setup/teardown
- User authentication fixtures
- Test data generators
- Authorization headers

### 2. test_auth.py
Authentication module tests:
- User registration with validation
- Password strength verification
- User login with JWT tokens
- Credential validation
- Duplicate account prevention
- Unique constraints (username, phone, ID)

**Test count: 15 tests**

### 3. test_service_request.py
Service request CRUD operations:
- Create requests (success and failures)
- List requests with pagination
- Filter by user, service type, city, state
- Update requests (owner only)
- Delete/cancel requests (owner only)
- Authorization checks
- Optional field handling

**Test count: 21 tests**

### 4. test_service_response.py
Service response CRUD operations:
- Create responses to requests
- List responses with pagination
- Filter by user, request, state
- Update responses (creator only)
- Delete responses (creator only)
- Multiple responses per request
- State tracking

**Test count: 18 tests**

### 5. test_match.py
Service matching and acceptance workflow:
- Accept service responses
- Reject service responses
- Complete workflow: publish → respond → accept/reject
- Multiple responses per request
- Authorization checks
- State validation

**Test count: 18 tests**

### 6. test_stats.py
Monthly statistics and reporting:
- Monthly statistics queries
- Date range queries
- Filters (city, service type)
- Pagination
- Chart data structure
- Published and completed counts

**Test count: 20 tests**

## Installation

Install test dependencies:

```bash
cd /home/cutie/Agent-Helper/web_full_stack/backend
pip install -r requirements-test.txt
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_auth.py
pytest tests/test_service_request.py
```

### Run specific test class
```bash
pytest tests/test_auth.py::TestAuthentication
```

### Run specific test
```bash
pytest tests/test_auth.py::TestAuthentication::test_user_registration_success
```

### Run with verbose output
```bash
pytest -v
```

### Run with coverage report
```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

## Test Coverage

Target coverage by module:
- Authentication: 95%
- Service Requests: 90%
- Service Responses: 90%
- Service Matching: 90%
- Statistics: 85%

## Fixtures

### User Fixtures
- `test_user_data`: Basic user registration data
- `authenticated_user`: User 1 registered and logged in
- `authenticated_user_2`: User 2 registered and logged in
- `authenticated_user_3`: User 3 registered and logged in
- `auth_headers`: Authorization headers for User 1
- `auth_headers_2`: Authorization headers for User 2
- `auth_headers_3`: Authorization headers for User 3

### Data Fixtures
- `setup_test_data`: Cities and service types
- `service_request_data`: Basic service request
- `service_response_data`: Basic service response
- `created_service_request`: Creates a request
- `created_service_response`: Creates a response

## Test Categories

### Authentication Tests (15)
- Registration success and failures
- Password validation rules
- Login with various credentials
- Token generation
- Duplicate prevention

### CRUD Tests (57)
- Create operations
- Read/List operations
- Update operations
- Delete operations
- Pagination
- Filtering

### Integration Tests (18)
- Complete workflows
- Multi-user scenarios
- State transitions

## Database

Tests use SQLite in-memory database for speed:
- No external dependencies
- Automatic cleanup between tests
- Full foreign key support

## Key Features

1. **Async Testing**: Full asyncio support with httpx.AsyncClient
2. **Comprehensive Coverage**: All endpoints tested with success and failure cases
3. **Realistic Data**: Test fixtures generate realistic test data
4. **Authorization**: Tests verify JWT authentication and role-based access
5. **Pagination**: Tests validate pagination limits and page calculations
6. **Filtering**: Tests verify filter combinations
7. **State Management**: Tests track state transitions properly
8. **Error Handling**: Tests verify proper HTTP status codes and error messages

## Test Data

All tests use in-memory SQLite database with:
- 3 test cities
- 6 service types
- Test users with valid credentials
- Proper date/time handling

## Common Test Patterns

### Testing authentication
```python
async def test_login_success(self, client: AsyncClient, test_user_data, setup_test_data):
    response = await client.post("/api/v1/auth/login", json={
        "username": test_user_data["uname"],
        "password": test_user_data["bpwd"]
    })
    assert response.status_code == 200
```

### Testing authorization
```python
async def test_update_by_different_user(self, client: AsyncClient, auth_headers_2):
    response = await client.put("/api/v1/service-requests/1", json={...}, headers=auth_headers_2)
    assert response.status_code == 403
```

### Testing pagination
```python
async def test_pagination(self, client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/service-requests?page=1&size=10", headers=auth_headers)
    assert response.json()["data"]["page"] == 1
```

## Notes

- All tests are async and use pytest-asyncio
- Database is automatically created and destroyed per test
- Foreign keys are enforced in SQLite tests
- Tests are designed to be independent and can run in any order
- Uses real AsyncClient for HTTP testing (no mocking)

## Troubleshooting

### Import errors
Ensure backend is in PYTHONPATH:
```bash
cd /home/cutie/Agent-Helper/web_full_stack/backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

### Database locked errors
Ensure only one pytest session is running and clean shutdown happens

### Token expiration
Tests use fixed secret key and short expiration times are not set in tests

## CI/CD Integration

Tests are ready for CI/CD:
- No external service dependencies
- Deterministic test data
- No side effects between tests
- Clear failure messages
