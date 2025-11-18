from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, user, service_requests, service_responses, match, stats

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(user.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["Users"])
app.include_router(service_requests.router, prefix=f"{settings.API_V1_PREFIX}/service-requests", tags=["Service Requests"])
app.include_router(service_responses.router, prefix=f"{settings.API_V1_PREFIX}/service-responses", tags=["Service Responses"])
app.include_router(match.router, prefix=f"{settings.API_V1_PREFIX}/match", tags=["Service Matching"])
app.include_router(stats.router, prefix=f"{settings.API_V1_PREFIX}/stats", tags=["Statistics"])

@app.get("/")
def root():
    return {"message": "GoodServices API", "version": settings.VERSION}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
