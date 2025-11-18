# GoodServices Backend API

FastAPI backend for the GoodServices community service platform.

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and update database credentials:

```bash
cp .env.example .env
```

## Running

```bash
python run.py
```

API will be available at: http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- POST /api/v1/auth/register - Register new user
- POST /api/v1/auth/login - User login

### Users
- GET /api/v1/users/me - Get current user info
- PUT /api/v1/users/me - Update current user
- PUT /api/v1/users/password - Update password

### Service Requests
- GET /api/v1/service-requests - List service requests (paginated)
- POST /api/v1/service-requests - Create service request
- PUT /api/v1/service-requests/{id} - Update service request
- DELETE /api/v1/service-requests/{id} - Delete service request

### Service Responses
- GET /api/v1/service-responses - List service responses (paginated)
- POST /api/v1/service-responses - Create service response
- PUT /api/v1/service-responses/{id} - Update service response
- DELETE /api/v1/service-responses/{id} - Delete service response

### Service Matching
- POST /api/v1/match/accept/{response_id} - Accept service response
- POST /api/v1/match/reject/{response_id} - Reject service response

### Statistics
- GET /api/v1/stats/monthly - Get monthly statistics
