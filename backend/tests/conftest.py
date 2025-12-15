import pytest
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient

from app.main import app
from app.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import BUser
from app.models.service_type import ServiceType
from app.models.city_info import CityInfo


TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Dependency override for tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a clean test database for each test"""
    Base.metadata.create_all(bind=engine)

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
async def client(db_session):
    """Create AsyncClient with test database"""
    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def setup_test_data(db_session):
    """Setup basic test data (cities and service types)"""
    cities = [
        CityInfo(id=1, city_name="Beijing"),
        CityInfo(id=2, city_name="Shanghai"),
        CityInfo(id=3, city_name="Guangzhou"),
    ]

    service_types = [
        ServiceType(id=1, service_name="Plumbing"),
        ServiceType(id=2, service_name="Elderly Care"),
        ServiceType(id=3, service_name="Cleaning"),
        ServiceType(id=4, service_name="Medical"),
        ServiceType(id=5, service_name="Meals"),
        ServiceType(id=6, service_name="Transportation"),
    ]

    for city in cities:
        db_session.add(city)
    for stype in service_types:
        db_session.add(stype)

    db_session.commit()

    return {"cities": cities, "service_types": service_types}


@pytest.fixture
def test_user_data():
    """Sample user registration data"""
    return {
        "uname": "testuser",
        "ctype": "ID Card",
        "idno": "110101199001011234",
        "bname": "Test User",
        "bpwd": "Password123",
        "phoneNo": "13800138000",
        "desc": "Test user account"
    }


@pytest.fixture
def test_user_data_2():
    """Second test user for multi-user scenarios"""
    return {
        "uname": "testuser2",
        "ctype": "ID Card",
        "idno": "110101199002021234",
        "bname": "Test User 2",
        "bpwd": "Password456",
        "phoneNo": "13800138001",
        "desc": "Second test user"
    }


@pytest.fixture
def test_user_data_3():
    """Third test user for multi-user scenarios"""
    return {
        "uname": "testuser3",
        "ctype": "ID Card",
        "idno": "110101199003031234",
        "bname": "Test User 3",
        "bpwd": "Password789",
        "phoneNo": "13800138002",
        "desc": "Third test user"
    }


@pytest.fixture
async def authenticated_user(client: AsyncClient, test_user_data, setup_test_data):
    """Create user and return authentication token"""
    await client.post("/api/v1/auth/register", json=test_user_data)

    login_response = await client.post("/api/v1/auth/login", json={
        "username": test_user_data["uname"],
        "password": test_user_data["bpwd"]
    })

    data = login_response.json()
    return {
        "token": data["data"]["token"],
        "user_info": data["data"]["user_info"]
    }


@pytest.fixture
async def authenticated_user_2(client: AsyncClient, test_user_data_2, setup_test_data):
    """Create second user and return authentication token"""
    await client.post("/api/v1/auth/register", json=test_user_data_2)

    login_response = await client.post("/api/v1/auth/login", json={
        "username": test_user_data_2["uname"],
        "password": test_user_data_2["bpwd"]
    })

    data = login_response.json()
    return {
        "token": data["data"]["token"],
        "user_info": data["data"]["user_info"]
    }


@pytest.fixture
async def authenticated_user_3(client: AsyncClient, test_user_data_3, setup_test_data):
    """Create third user and return authentication token"""
    await client.post("/api/v1/auth/register", json=test_user_data_3)

    login_response = await client.post("/api/v1/auth/login", json={
        "username": test_user_data_3["uname"],
        "password": test_user_data_3["bpwd"]
    })

    data = login_response.json()
    return {
        "token": data["data"]["token"],
        "user_info": data["data"]["user_info"]
    }


@pytest.fixture
def auth_headers(authenticated_user):
    """Get authorization headers for authenticated user"""
    return {
        "Authorization": f"Bearer {authenticated_user['token']}"
    }


@pytest.fixture
def auth_headers_2(authenticated_user_2):
    """Get authorization headers for second authenticated user"""
    return {
        "Authorization": f"Bearer {authenticated_user_2['token']}"
    }


@pytest.fixture
def auth_headers_3(authenticated_user_3):
    """Get authorization headers for third authenticated user"""
    return {
        "Authorization": f"Bearer {authenticated_user_3['token']}"
    }


@pytest.fixture
def service_request_data():
    """Sample service request creation data"""
    return {
        "sr_title": "Kitchen plumbing repair",
        "ps_begindate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "desc": "Kitchen sink is leaking badly",
        "stype_id": 1,
        "cityID": 1,
        "file_list": ""
    }


@pytest.fixture
def service_request_data_2():
    """Second service request data"""
    return {
        "sr_title": "Elderly care assistance",
        "ps_begindate": (datetime.utcnow() + timedelta(days=3)).isoformat(),
        "desc": "Need daily care for elderly parent",
        "stype_id": 2,
        "cityID": 1,
        "file_list": ""
    }


@pytest.fixture
def service_response_data():
    """Sample service response creation data"""
    return {
        "response_desc": "Professional plumbing service available",
        "file_list": None
    }


@pytest.fixture
def service_response_data_2():
    """Second service response data"""
    return {
        "response_desc": "Experienced elderly care provider",
        "file_list": None
    }


@pytest.fixture
async def created_service_request(client: AsyncClient, authenticated_user,
                                  auth_headers, service_request_data, setup_test_data):
    """Create a service request for use in tests"""
    response = await client.post(
        "/api/v1/service-requests",
        json=service_request_data,
        headers=auth_headers
    )
    return response.json()["data"]["sr_id"]


@pytest.fixture
async def created_service_response(client: AsyncClient, authenticated_user_2,
                                   auth_headers_2, created_service_request,
                                   service_response_data):
    """Create a service response for use in tests"""
    response_data = {**service_response_data, "srid": created_service_request}

    response = await client.post(
        "/api/v1/service-responses",
        json=response_data,
        headers=auth_headers_2
    )
    return response.json()["data"]["id"]
